#!/usr/bin/env python3

import os
import json
import time
import glob
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from pinecone import Pinecone
import openai

load_dotenv()

# Initialize clients
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
dense_index = pc.Index("dense-milo-companies")
sparse_index = pc.Index("sparse-milo-companies")
openai.api_key = os.getenv('OPENAI_API_KEY')

# Namespaces for real domain data
DENSE_NAMESPACE = "dense-companies-real-domains-v1"
SPARSE_NAMESPACE = "sparse-companies-real-domains-v1"

def get_dense_embedding(text: str):
    """Get dense embedding using OpenAI with correct dimensions"""
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small",
        dimensions=1024  # Match Pinecone index dimension
    )
    return response.data[0].embedding

def get_sparse_embedding(text: str):
    """Create simple sparse embedding from text tokens"""
    import re
    from collections import Counter
    
    # Basic tokenization and frequency counting
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Create sparse representation with top 20 most frequent words
    top_words = word_counts.most_common(20)
    indices = [hash(word) % 10000 for word, _ in top_words]
    values = [count / len(words) for _, count in top_words]
    
    return {
        "indices": indices,
        "values": values
    }

def upsert_company_roles(company):
    """Upsert all roles for a company with real domain info"""
    import hashlib
    
    company_id = hashlib.md5(company["company_name"].encode()).hexdigest()
    
    for role in company["roles"]:
        role_id = f"{company_id}_{hashlib.md5(role['title'].encode()).hexdigest()}"
        
        # Enhanced embedding text with domain info
        embed_text = f"""
Company: {company['company_name']}
Domain: {company.get('domain', 'N/A')}
Website: {company.get('website', 'N/A')}
About: {company['about']}
Title: {role['title']}
Department: {role.get('department', '')}
Description: {role['description']}
Location: {role['location']}
Industry: {company['industry']}
Size: {company['size']}
"""
        
        # Get embeddings
        dense_embedding = get_dense_embedding(embed_text.strip())
        sparse_embedding = get_sparse_embedding(embed_text.strip())
        
        # Enhanced metadata with domain info
        metadata = {
            "company_id": company_id,
            "company": company["company_name"],
            "domain": company.get("domain", ""),
            "website": company.get("website", ""),
            "domain_confidence": company.get("confidence", "unknown"),
            "title": role["title"],
            "department": role.get("department", ""),
            "industry": company["industry"],
            "location": role["location"],
            "description": role["description"],
            "about_company": company["about"],
            "company_size": company["size"],
            "company_stage": company.get("company_stage", ""),
            "founded": company.get("founded", ""),
            "salary_min": role["salary_range"][0] if role.get("salary_range") else 0,
            "salary_max": role["salary_range"][1] if role.get("salary_range") else 0,
            "seniority_level": role.get("seniority_level", ""),
            "required_skills": ", ".join(role.get("required_skills", [])),
            "experience_years": role.get("experience_years", 0),
            "source": "real_domains",
            "fetched_at": datetime.utcnow().isoformat()
        }
        
        # Upsert to dense index
        dense_vector = {
            "id": role_id,
            "values": dense_embedding,
            "metadata": metadata
        }
        
        dense_index.upsert(vectors=[dense_vector], namespace=DENSE_NAMESPACE)
        
        # Upsert to sparse index
        sparse_vector = {
            "id": role_id,
            "sparse_values": sparse_embedding,
            "metadata": metadata
        }
        
        sparse_index.upsert(vectors=[sparse_vector], namespace=SPARSE_NAMESPACE)
        
        domain_info = f"({company.get('domain', 'no-domain')})"
        print(f"✅ Upserted {role['title']} at {company['company_name']} {domain_info}")

def wait_for_real_domains_file():
    """Wait for and find the real domains file"""
    print("🔍 Looking for real domains file...")
    
    while True:
        # Look for completed real domains file
        real_domain_files = sorted(glob.glob("companies_real_domains_*.json"), reverse=True)
        
        if real_domain_files:
            latest_file = real_domain_files[0]
            print(f"✅ Found real domains file: {latest_file}")
            return latest_file
        
        print("⏳ Waiting for real domain enrichment to complete...")
        time.sleep(30)  # Check every 30 seconds

def upsert_real_domains_to_pinecone():
    """Main function to upsert companies with real domains to Pinecone"""
    
    # Wait for real domains file if it doesn't exist yet
    real_domains_file = wait_for_real_domains_file()
    
    print(f"🚀 Starting upsert of companies with real domains to Pinecone")
    print(f"📁 Input file: {real_domains_file}")
    print(f"📍 Dense namespace: {DENSE_NAMESPACE}")
    print(f"📍 Sparse namespace: {SPARSE_NAMESPACE}")
    
    try:
        with open(real_domains_file, 'r') as f:
            companies = json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return
    
    total_roles = 0
    companies_with_domains = 0
    start_time = time.time()
    
    for i, company in enumerate(companies, 1):
        print(f"\n🏢 Processing company {i}/{len(companies)}: {company['company_name']}")
        
        # Check if company has domain info
        has_domain = 'domain' in company and company.get('domain')
        if has_domain:
            companies_with_domains += 1
            domain_info = f" → {company['domain']}"
        else:
            domain_info = " (no domain)"
        
        print(f"   Found {len(company['roles'])} roles{domain_info}")
        
        try:
            upsert_company_roles(company)
            total_roles += len(company['roles'])
        except Exception as e:
            print(f"❌ Error processing {company['company_name']}: {e}")
            continue
        
        # Progress tracking
        if i % 50 == 0:
            elapsed = time.time() - start_time
            rate = i / elapsed if elapsed > 0 else 0
            eta = (len(companies) - i) / rate / 60 if rate > 0 else 0
            
            print(f"📈 Progress: {i}/{len(companies)} ({i/len(companies)*100:.1f}%)")
            print(f"⏱️  Rate: {rate:.1f} companies/sec, ETA: {eta:.1f} minutes")
            print(f"🌐 Companies with domains: {companies_with_domains}/{i} ({companies_with_domains/i*100:.1f}%)")
    
    print(f"\n🎉 Upsert complete!")
    print(f"📊 Total companies: {len(companies)}")
    print(f"🎯 Total roles upserted: {total_roles}")
    print(f"🌐 Companies with domains: {companies_with_domains} ({companies_with_domains/len(companies)*100:.1f}%)")
    print(f"⏱️  Total time: {(time.time() - start_time)/60:.1f} minutes")
    print(f"📍 Namespaces: {DENSE_NAMESPACE}, {SPARSE_NAMESPACE}")

if __name__ == "__main__":
    upsert_real_domains_to_pinecone()