#!/usr/bin/env python3

import os
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def search_real_domain(company_name, industry=None):
    """Use AI to find the real domain for a company by researching it"""
    
    prompt = f"""You are a domain research expert. Find the REAL, ACTUAL domain name for this company by using your knowledge of real companies and their websites.

Company: {company_name}
Industry: {industry}

Instructions:
1. If this is a real company you know about, provide their actual domain
2. If you're not certain, indicate uncertainty
3. Consider common domain patterns (company name without spaces/punctuation + .com)
4. For large corporations, they usually use .com
5. Some companies use abbreviated domains (e.g., General Electric = ge.com)

Return ONLY a JSON object:
{{
  "company_name": "{company_name}",
  "domain": "actual-domain.com",
  "website": "https://www.actual-domain.com",
  "confidence": "high|medium|low",
  "reasoning": "Why you believe this is correct"
}}

If you cannot find the real domain with confidence, set confidence to "low" and provide your best educated guess."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            temperature=0.1,  # Very low temperature for accuracy
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.content[0].text.strip())
        return result
        
    except Exception as e:
        print(f"❌ Error researching {company_name}: {e}")
        return None

def get_real_domains_batch(companies_batch, batch_size=5):
    """Get real domains for a batch of companies"""
    
    results = []
    
    for i, company in enumerate(companies_batch):
        company_name = company.get("company_name", "")
        industry = company.get("industry", "")
        
        print(f"🔍 Researching {i+1}/{len(companies_batch)}: {company_name}")
        
        domain_info = search_real_domain(company_name, industry)
        
        if domain_info:
            # Add domain info to company
            enriched_company = company.copy()
            enriched_company.update(domain_info)
            results.append(enriched_company)
            
            confidence = domain_info.get("confidence", "unknown")
            domain = domain_info.get("domain", "unknown")
            print(f"✅ {company_name} → {domain} ({confidence} confidence)")
        else:
            # Keep company without domain info
            results.append(company)
            print(f"❌ Could not find domain for {company_name}")
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    return results

def enrich_with_real_domains(input_file, batch_size=5):
    """Enrich companies with their real domains"""
    
    print(f"🔍 Loading companies from {input_file}...")
    
    try:
        with open(input_file, 'r') as f:
            companies = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {input_file}: {e}")
        return None
    
    print(f"📊 Found {len(companies)} companies to research")
    print(f"🔍 Researching real domains in batches of {batch_size}")
    
    enriched_companies = []
    total_batches = (len(companies) + batch_size - 1) // batch_size
    
    start_time = time.time()
    
    for batch_num in range(total_batches):
        batch_start = batch_num * batch_size
        batch_end = min(batch_start + batch_size, len(companies))
        batch_companies = companies[batch_start:batch_end]
        
        print(f"\n🔄 Processing batch {batch_num + 1}/{total_batches} ({len(batch_companies)} companies)")
        
        batch_results = get_real_domains_batch(batch_companies, len(batch_companies))
        enriched_companies.extend(batch_results)
        
        # Progress tracking
        elapsed = time.time() - start_time
        processed = len(enriched_companies)
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (len(companies) - processed) / rate / 60 if rate > 0 else 0
        
        print(f"📈 Progress: {processed}/{len(companies)} ({processed/len(companies)*100:.1f}%)")
        print(f"⏱️  Rate: {rate:.1f} companies/sec, ETA: {eta:.1f} minutes")
        
        # Rate limiting
        time.sleep(1)
    
    # Generate output filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"companies_real_domains_{timestamp}.json"
    
    print(f"\n💾 Saving companies with real domains to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump(enriched_companies, f, indent=2)
    
    # Generate statistics
    companies_with_domains = [c for c in enriched_companies if 'domain' in c]
    high_confidence = [c for c in companies_with_domains if c.get('confidence') == 'high']
    medium_confidence = [c for c in companies_with_domains if c.get('confidence') == 'medium']
    low_confidence = [c for c in companies_with_domains if c.get('confidence') == 'low']
    
    stats = {
        "input_file": input_file,
        "output_file": output_file,
        "total_companies": len(enriched_companies),
        "companies_with_domains": len(companies_with_domains),
        "high_confidence": len(high_confidence),
        "medium_confidence": len(medium_confidence),
        "low_confidence": len(low_confidence),
        "success_rate": len(companies_with_domains) / len(enriched_companies) * 100,
        "processing_time_minutes": (time.time() - start_time) / 60,
        "sample_results": [
            {
                "company": c["company_name"],
                "domain": c.get("domain", "N/A"),
                "confidence": c.get("confidence", "N/A")
            } for c in enriched_companies[:10]
        ]
    }
    
    stats_file = f"real_domains_stats_{timestamp}.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n🎉 Real domain research complete!")
    print(f"📊 Total companies: {len(enriched_companies)}")
    print(f"🌐 Found domains: {len(companies_with_domains)} ({len(companies_with_domains)/len(enriched_companies)*100:.1f}%)")
    print(f"✅ High confidence: {len(high_confidence)}")
    print(f"⚠️  Medium confidence: {len(medium_confidence)}")
    print(f"❓ Low confidence: {len(low_confidence)}")
    print(f"⏱️  Total time: {(time.time() - start_time)/60:.1f} minutes")
    print(f"📄 Output: {output_file}")
    print(f"📈 Stats: {stats_file}")
    
    return output_file, stats_file

if __name__ == "__main__":
    # Look for the most recent master file
    import glob
    
    master_files = sorted(glob.glob("companies_master_*.json"), reverse=True)
    
    if master_files:
        latest_master = master_files[0]
        print(f"🎯 Using latest master file: {latest_master}")
        batch_size = int(input("Enter batch size for research (default 5): ").strip() or "5")
        enrich_with_real_domains(latest_master, batch_size)
    else:
        print("❌ No master company files found!")
        filename = input("Enter filename to research: ").strip()
        if filename and os.path.exists(filename):
            batch_size = int(input("Enter batch size (default 5): ").strip() or "5")
            enrich_with_real_domains(filename, batch_size)
        else:
            print("No file specified or file not found.")