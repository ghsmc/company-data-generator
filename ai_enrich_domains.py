#!/usr/bin/env python3

import os
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_domains_with_ai(companies_batch, batch_size=10):
    """Use AI to generate realistic domains for a batch of companies"""
    
    # Prepare company info for AI
    company_info = []
    for i, company in enumerate(companies_batch):
        company_info.append({
            "id": i,
            "name": company.get("company_name", ""),
            "industry": company.get("industry", ""),
            "stage": company.get("company_stage", ""),
            "location": company.get("location", "")
        })
    
    prompt = f"""CRITICAL: For each company, first determine if it's a REAL existing company or fictional.

Companies:
{json.dumps(company_info, indent=2)}

For REAL companies (like Marriott, Target, XPO Logistics, Lockheed Martin, Ford, etc.):
- Use their ACTUAL real domain (marriott.com, target.com, xpo.com, lockheedmartin.com, ford.com)
- Use their real website URL
- These are publicly traded or well-known companies

For FICTIONAL/Generated companies:
- Create realistic domains they would use
- Consider industry and stage
- Use appropriate TLDs (.com, .org, .net, .io, .gov, etc.)

EXAMPLES:
- Marriott International → marriott.com (REAL)
- Target Corporation → target.com (REAL) 
- Ford Motor Company → ford.com (REAL)
- "GreenTech Solutions" → greentech.io (FICTIONAL)
- "CivicTech Solutions" → civictech.gov (FICTIONAL)

Return ONLY a JSON array:
[
  {{
    "id": 0,
    "domain": "actual-real-domain.com",
    "website": "https://www.actual-real-domain.com",
    "email_domain": "actual-real-domain.com",
    "is_real_company": true
  }},
  ...
]"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.3,  # Lower temperature for consistency
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse the response
        domain_data = json.loads(response.content[0].text.strip())
        
        # Validate response
        if not isinstance(domain_data, list) or len(domain_data) != len(company_info):
            raise ValueError(f"AI returned {len(domain_data)} domains but expected {len(company_info)}")
        
        return domain_data
        
    except Exception as e:
        print(f"❌ AI domain generation failed: {e}")
        return None

def enrich_companies_with_ai(input_file, batch_size=10):
    """Enrich companies with AI-generated domains"""
    
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
    
    print(f"📊 Found {len(companies)} companies to enrich")
    print(f"🤖 Using AI to generate domains in batches of {batch_size}")
    
    enriched_companies = []
    domains_used = set()
    total_batches = (len(companies) + batch_size - 1) // batch_size
    
    start_time = time.time()
    
    for batch_num in range(total_batches):
        batch_start = batch_num * batch_size
        batch_end = min(batch_start + batch_size, len(companies))
        batch_companies = companies[batch_start:batch_end]
        
        print(f"\n🔄 Processing batch {batch_num + 1}/{total_batches} ({len(batch_companies)} companies)")
        
        # Get AI-generated domains
        domain_data = generate_domains_with_ai(batch_companies, len(batch_companies))
        
        if domain_data is None:
            print(f"❌ Skipping batch {batch_num + 1} due to AI error")
            # Add companies without domain enrichment
            enriched_companies.extend(batch_companies)
            continue
        
        # Apply domains to companies
        for i, company in enumerate(batch_companies):
            try:
                domain_info = domain_data[i]
                
                # Check for domain uniqueness
                domain = domain_info["domain"]
                if domain in domains_used:
                    # Add a number to make it unique
                    counter = 2
                    base_domain = domain.split('.')[0]
                    tld = '.' + domain.split('.', 1)[1]
                    while f"{base_domain}{counter}{tld}" in domains_used:
                        counter += 1
                    domain = f"{base_domain}{counter}{tld}"
                    domain_info["domain"] = domain
                    domain_info["email_domain"] = domain
                    # Update website URL
                    protocol = "https://" if domain_info["website"].startswith("https://") else "http://"
                    subdomain = "www." if "www." in domain_info["website"] else ""
                    domain_info["website"] = f"{protocol}{subdomain}{domain}"
                
                domains_used.add(domain)
                
                # Add domain info to company
                enriched_company = company.copy()
                enriched_company.update(domain_info)
                enriched_companies.append(enriched_company)
                
                print(f"✅ {company['company_name']} → {domain}")
                
            except Exception as e:
                print(f"❌ Error processing company {i} in batch: {e}")
                enriched_companies.append(company)
                continue
        
        # Progress tracking
        elapsed = time.time() - start_time
        processed = len(enriched_companies)
        rate = processed / elapsed if elapsed > 0 else 0
        eta = (len(companies) - processed) / rate / 60 if rate > 0 else 0
        
        print(f"📈 Progress: {processed}/{len(companies)} ({processed/len(companies)*100:.1f}%)")
        print(f"⏱️  Rate: {rate:.1f} companies/sec, ETA: {eta:.1f} minutes")
        
        # Rate limiting to avoid API limits
        time.sleep(1)
    
    # Generate output filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"companies_ai_enriched_{timestamp}.json"
    
    print(f"\n💾 Saving AI-enriched companies to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump(enriched_companies, f, indent=2)
    
    # Generate statistics
    stats = {
        "input_file": input_file,
        "output_file": output_file,
        "total_companies": len(enriched_companies),
        "unique_domains": len(domains_used),
        "enriched_at": datetime.now().isoformat(),
        "processing_time_minutes": (time.time() - start_time) / 60,
        "batch_size": batch_size,
        "ai_model": "claude-3-5-sonnet-20241022",
        "domain_stats": {
            "com_domains": len([d for d in domains_used if d.endswith('.com')]),
            "org_domains": len([d for d in domains_used if d.endswith('.org')]),
            "net_domains": len([d for d in domains_used if d.endswith('.net')]),
            "gov_domains": len([d for d in domains_used if d.endswith('.gov')]),
            "io_domains": len([d for d in domains_used if d.endswith('.io')]),
            "other_domains": len([d for d in domains_used if not any(d.endswith(tld) for tld in ['.com', '.org', '.net', '.gov', '.io'])]),
        },
        "sample_domains": sorted(list(domains_used))[:20]  # First 20 as examples
    }
    
    stats_file = f"ai_enrichment_stats_{timestamp}.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n🎉 AI enrichment complete!")
    print(f"📊 Enriched {len(enriched_companies)} companies")
    print(f"🌐 Generated {len(domains_used)} unique domains")
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
        enrich_companies_with_ai(latest_master, batch_size=10)
    else:
        print("❌ No master company files found!")
        print("Available files:")
        for f in glob.glob("companies_*.json"):
            print(f"  - {f}")
        
        # Optionally specify a file
        filename = input("\nEnter filename to enrich (or press Enter to exit): ").strip()
        if filename and os.path.exists(filename):
            batch_size = int(input("Enter batch size (default 10): ").strip() or "10")
            enrich_companies_with_ai(filename, batch_size)
        else:
            print("No file specified or file not found.")