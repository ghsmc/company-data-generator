#!/usr/bin/env python3

import os
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Expanded industry list for better diversity
INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Retail", "Manufacturing", 
    "Education", "Energy", "Transportation", "Real Estate", "Media",
    "Hospitality", "Consulting", "Legal", "Non-Profit", "Government",
    "Agriculture", "Aerospace", "Automotive", "Biotechnology", "Construction",
    "Entertainment", "Fashion", "Food & Beverage", "Insurance", "Mining",
    "Pharmaceuticals", "Telecommunications", "Utilities", "Logistics", "Sports"
]

def generate_batch(batch_size=100, batch_num=1):
    """Generate a batch of companies with detailed progress tracking"""
    companies = []
    
    for i in range(batch_size):
        industry = random.choice(INDUSTRIES)
        
        # Enhanced randomization
        seed = random.randint(10000, 99999)
        company_types = ["startup", "mid-size", "enterprise", "Fortune 500", "family-owned", "public", "private equity backed"]
        company_type = random.choice(company_types)
        
        role_count = random.choice([3, 4, 5, 6])  # Vary role count
        
        prompt = f"""Generate 1 {company_type} company in {industry} (batch {batch_num}, seed: {seed}).

Create exactly {role_count} diverse job roles covering entry to executive levels.

Key requirements:
- Use REAL company names that could exist
- Include mix of seniority levels (entry, mid, senior, director, VP)
- Realistic salaries for {industry} industry
- Diverse job functions within the company
- Accurate location data (real cities)

JSON format:
{{
  "company_name": "Realistic company name",
  "about": "Detailed company description",
  "industry": "{industry}",
  "company_stage": "Startup/Growth/Mature/Public",
  "size": "Employee count range",
  "location": "City, State/Country",
  "founded": "Year founded",
  "roles": [
    {{
      "title": "Specific job title",
      "department": "Department name",
      "description": "Detailed job description",
      "location": "City, State",
      "salary_range": [min_salary, max_salary],
      "seniority_level": "Entry/Mid/Senior/Director/VP/C-Suite",
      "required_skills": ["skill1", "skill2", "skill3"],
      "experience_years": 0-15
    }}
  ]
}}

Return ONLY valid JSON."""

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=3000,
                temperature=0.8,  # Higher temp for more diversity
                messages=[{"role": "user", "content": prompt}]
            )
            
            company_data = json.loads(response.content[0].text.strip())
            companies.append(company_data)
            
            print(f"✅ Batch {batch_num}: {i+1}/{batch_size} - {company_data['company_name']} ({industry})")
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
            
        except Exception as e:
            print(f"❌ Batch {batch_num}: Error {i+1}/{batch_size}: {e}")
            continue
    
    return companies

def save_batch(companies, batch_num):
    """Save batch to separate file"""
    filename = f"companies_batch_{batch_num:03d}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(companies, f, indent=2)
    return filename

def generate_10k_companies():
    """Generate 10,000 companies in batches of 100"""
    print("🚀 Starting generation of 10,000 companies...")
    print("📊 Processing in batches of 100 for better memory management")
    
    all_files = []
    total_companies = 0
    total_roles = 0
    
    start_time = time.time()
    
    for batch_num in range(1, 101):  # 100 batches of 100 companies each
        print(f"\n🔄 Starting batch {batch_num}/100...")
        
        batch_companies = generate_batch(100, batch_num)
        
        if batch_companies:
            filename = save_batch(batch_companies, batch_num)
            all_files.append(filename)
            
            batch_roles = sum(len(company['roles']) for company in batch_companies)
            total_companies += len(batch_companies)
            total_roles += batch_roles
            
            elapsed = time.time() - start_time
            rate = total_companies / elapsed if elapsed > 0 else 0
            eta = (10000 - total_companies) / rate / 60 if rate > 0 else 0
            
            print(f"📊 Batch {batch_num} complete: {len(batch_companies)} companies, {batch_roles} roles")
            print(f"📈 Total progress: {total_companies}/10,000 companies ({total_companies/100:.1f}%)")
            print(f"⏱️  Rate: {rate:.1f} companies/sec, ETA: {eta:.1f} minutes")
            print(f"💾 Saved to: {filename}")
        
        # Longer pause between batches
        time.sleep(1)
    
    # Create master index file
    master_index = {
        "total_companies": total_companies,
        "total_roles": total_roles,
        "batch_files": all_files,
        "generated_at": datetime.now().isoformat(),
        "generation_time_seconds": time.time() - start_time
    }
    
    with open("companies_10k_index.json", "w") as f:
        json.dump(master_index, f, indent=2)
    
    print(f"\n🎉 Generation complete!")
    print(f"📊 Generated {total_companies} companies with {total_roles} total roles")
    print(f"⏱️  Total time: {(time.time() - start_time)/60:.1f} minutes")
    print(f"📁 Files: {len(all_files)} batch files + 1 index file")

if __name__ == "__main__":
    generate_10k_companies()