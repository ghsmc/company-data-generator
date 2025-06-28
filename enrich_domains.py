#!/usr/bin/env python3

import os
import json
import re
import random
from datetime import datetime
from urllib.parse import urlparse

def clean_company_name(name):
    """Clean company name for domain generation"""
    # Remove common suffixes and special characters
    name = re.sub(r'\s+(LLC|LLP|Inc\.?|Corp\.?|Corporation|Company|Co\.?|Ltd\.?|Limited|Group|Partners|Solutions|Systems|Technologies|Services|Consulting|Associates|Holdings|Enterprises|International|Global|Worldwide|USA|America)', '', name, flags=re.IGNORECASE)
    
    # Remove special characters and spaces
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)
    
    return name.lower()

def generate_domain(company_name, industry=None):
    """Generate realistic domain name for a company"""
    
    # Clean the company name
    clean_name = clean_company_name(company_name)
    
    # Common domain patterns
    patterns = [
        lambda n: n,                           # cleanname.com
        lambda n: n + "corp",                  # cleannamecorp.com
        lambda n: n + "inc",                   # cleannameinc.com
        lambda n: n + "group",                 # cleannamegroup.com
        lambda n: n + "solutions",             # cleannamesolutions.com
        lambda n: n + "tech" if "tech" not in n else n,  # cleannametech.com
        lambda n: n + "global",                # cleannameglobal.com
        lambda n: n + "usa" if random.random() < 0.1 else n,  # cleannameusa.com (rare)
    ]
    
    # Industry-specific modifications
    industry_suffixes = {
        "Technology": ["tech", "sys", "soft", "labs", "ai"],
        "Healthcare": ["health", "med", "care", "bio"],
        "Finance": ["capital", "financial", "invest", "bank"],
        "Legal": ["law", "legal", "attorneys"],
        "Consulting": ["consulting", "advisory", "partners"],
        "Manufacturing": ["mfg", "industrial", "systems"],
        "Energy": ["energy", "power", "solar", "green"],
        "Real Estate": ["realty", "properties", "homes"],
        "Media": ["media", "digital", "studios"],
        "Education": ["edu", "learning", "academy"],
        "Retail": ["retail", "store", "market"],
        "Transportation": ["logistics", "transport", "shipping"],
        "Hospitality": ["hotels", "resorts", "hospitality"]
    }
    
    # Apply pattern
    pattern = random.choice(patterns)
    domain_base = pattern(clean_name)
    
    # Add industry-specific suffix occasionally
    if industry and industry in industry_suffixes and random.random() < 0.3:
        if not any(suffix in domain_base for suffix in industry_suffixes[industry]):
            domain_base += random.choice(industry_suffixes[industry])
    
    # Ensure reasonable length
    if len(domain_base) > 25:
        domain_base = domain_base[:25]
    elif len(domain_base) < 4:
        domain_base += "corp"
    
    # Common TLDs with realistic distribution
    tlds = [".com"] * 70 + [".net"] * 10 + [".org"] * 5 + [".co"] * 8 + [".io"] * 4 + [".ai"] * 2 + [".tech"] * 1
    
    # Adjust TLD based on industry
    if industry == "Technology":
        tlds.extend([".io"] * 10 + [".ai"] * 5 + [".tech"] * 3)
    elif industry == "Non-Profit":
        tlds.extend([".org"] * 20)
    elif industry == "Government":
        tlds = [".gov"] * 50 + [".org"] * 30 + [".com"] * 20
    
    tld = random.choice(tlds)
    
    return domain_base + tld

def generate_website_url(domain):
    """Generate full website URL"""
    # Most sites use HTTPS now
    protocol = "https" if random.random() < 0.9 else "http"
    
    # Some sites have www, some don't
    subdomain = "www." if random.random() < 0.6 else ""
    
    return f"{protocol}://{subdomain}{domain}"

def enrich_company_with_domain(company):
    """Add domain and website URL to a company"""
    company_name = company.get("company_name", "")
    industry = company.get("industry", "")
    
    # Generate domain
    domain = generate_domain(company_name, industry)
    website = generate_website_url(domain)
    
    # Add to company data
    company["domain"] = domain
    company["website"] = website
    
    # Also add email domain for contact info
    company["email_domain"] = domain
    
    return company

def enrich_companies_file(input_file):
    """Enrich all companies in a file with domains and URLs"""
    
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
    
    enriched_companies = []
    domains_used = set()
    
    for i, company in enumerate(companies, 1):
        try:
            # Ensure unique domains
            max_attempts = 5
            for attempt in range(max_attempts):
                enriched_company = enrich_company_with_domain(company.copy())
                domain = enriched_company["domain"]
                
                if domain not in domains_used:
                    domains_used.add(domain)
                    enriched_companies.append(enriched_company)
                    
                    if i % 100 == 0 or i <= 10:
                        print(f"✅ {i}/{len(companies)}: {company['company_name']} → {domain}")
                    break
                elif attempt == max_attempts - 1:
                    # If we can't get unique domain, add a number
                    base_domain = domain
                    counter = 2
                    while f"{base_domain.split('.')[0]}{counter}.{base_domain.split('.', 1)[1]}" in domains_used:
                        counter += 1
                    
                    new_domain = f"{base_domain.split('.')[0]}{counter}.{base_domain.split('.', 1)[1]}"
                    enriched_company["domain"] = new_domain
                    enriched_company["website"] = generate_website_url(new_domain)
                    enriched_company["email_domain"] = new_domain
                    
                    domains_used.add(new_domain)
                    enriched_companies.append(enriched_company)
                    
                    if i % 100 == 0 or i <= 10:
                        print(f"✅ {i}/{len(companies)}: {company['company_name']} → {new_domain}")
                    
        except Exception as e:
            print(f"❌ Error enriching company {i}: {e}")
            # Add without domain if enrichment fails
            enriched_companies.append(company)
            continue
    
    # Generate output filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"companies_enriched_{timestamp}.json"
    
    print(f"\n💾 Saving enriched companies to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump(enriched_companies, f, indent=2)
    
    # Generate statistics
    stats = {
        "input_file": input_file,
        "output_file": output_file,
        "total_companies": len(enriched_companies),
        "unique_domains": len(domains_used),
        "enriched_at": datetime.now().isoformat(),
        "domain_stats": {
            "com_domains": len([d for d in domains_used if d.endswith('.com')]),
            "org_domains": len([d for d in domains_used if d.endswith('.org')]),
            "net_domains": len([d for d in domains_used if d.endswith('.net')]),
            "other_domains": len([d for d in domains_used if not any(d.endswith(tld) for tld in ['.com', '.org', '.net'])]),
        },
        "sample_domains": list(domains_used)[:20]  # First 20 as examples
    }
    
    stats_file = f"enrichment_stats_{timestamp}.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\n🎉 Enrichment complete!")
    print(f"📊 Enriched {len(enriched_companies)} companies")
    print(f"🌐 Generated {len(domains_used)} unique domains")
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
        enrich_companies_file(latest_master)
    else:
        print("❌ No master company files found!")
        print("Available files:")
        for f in glob.glob("companies_*.json"):
            print(f"  - {f}")
        
        # Optionally specify a file
        filename = input("\nEnter filename to enrich (or press Enter to exit): ").strip()
        if filename and os.path.exists(filename):
            enrich_companies_file(filename)
        else:
            print("No file specified or file not found.")