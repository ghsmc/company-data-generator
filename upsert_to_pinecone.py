#!/usr/bin/env python3

import os
import json
import uuid
import hashlib
import requests
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from pinecone import Pinecone

load_dotenv()

# Initialize clients
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
dense_index = pc.Index("dense-milo-companies")
sparse_index = pc.Index("sparse-milo-companies")

# Namespaces
DENSE_NAMESPACE = "dense-companies-claude-v9-simple"
SPARSE_NAMESPACE = "sparse-companies-claude-v9-simple"

def get_dense_embedding(text: str):
    """Get dense embedding using OpenAI with dimension reduction"""
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    response = openai.embeddings.create(
        input=text,
        model="text-embedding-3-small",
        dimensions=1024  # Match Pinecone index dimension
    )
    return response.data[0].embedding

def get_sparse_embedding(text: str):
    """Create simple sparse embedding from text tokens"""
    # Simple sparse embedding: use word frequency as sparse values
    import re
    from collections import Counter
    
    # Basic tokenization and frequency counting
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Create simple sparse representation with top 20 most frequent words
    top_words = word_counts.most_common(20)
    indices = [hash(word) % 10000 for word, _ in top_words]  # Simple hash to indices
    values = [count / len(words) for _, count in top_words]  # Normalize frequencies
    
    return {
        "indices": indices,
        "values": values
    }

def upsert_company_roles(company):
    """Upsert all roles for a company to both dense and sparse indexes"""
    company_id = hashlib.md5(company["company_name"].encode()).hexdigest()
    
    for role in company["roles"]:
        role_id = f"{company_id}_{hashlib.md5(role['title'].encode()).hexdigest()}"
        
        # Create embedding text
        embed_text = f"""
Company: {company['company_name']}
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
        
        # Shared metadata
        metadata = {
            "company_id": company_id,
            "company": company["company_name"],
            "title": role["title"],
            "department": role.get("department", ""),
            "industry": company["industry"],
            "location": role["location"],
            "description": role["description"],
            "about_company": company["about"],
            "company_size": company["size"],
            "salary_min": role["salary_range"][0] if role.get("salary_range") else 0,
            "salary_max": role["salary_range"][1] if role.get("salary_range") else 0,
            "source": "simple_generate",
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
        
        print(f"✅ Upserted {role['title']} at {company['company_name']}")

def main():
    """Load companies and upsert all roles to Pinecone"""
    with open("companies_20250624_132852.json", "r") as f:
        companies = json.load(f)
    
    print(f"🚀 Starting upsert of {len(companies)} companies to Pinecone")
    print(f"📍 Dense namespace: {DENSE_NAMESPACE}")
    print(f"📍 Sparse namespace: {SPARSE_NAMESPACE}")
    
    total_roles = 0
    for i, company in enumerate(companies, 1):
        print(f"\n🏢 Processing company {i}/{len(companies)}: {company['company_name']}")
        print(f"   Found {len(company['roles'])} roles")
        
        try:
            upsert_company_roles(company)
            total_roles += len(company['roles'])
        except Exception as e:
            print(f"❌ Error processing {company['company_name']}: {e}")
            continue
    
    print(f"\n🎉 Completed! Upserted {total_roles} roles from {len(companies)} companies")

if __name__ == "__main__":
    main()