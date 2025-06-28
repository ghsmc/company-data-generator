#!/usr/bin/env python3

import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def generate_companies(count=50):
    """Generate diverse companies across industries"""
    
    industries = [
        "Technology", "Healthcare", "Finance", "Retail", "Manufacturing", 
        "Education", "Energy", "Transportation", "Real Estate", "Media",
        "Hospitality", "Consulting", "Legal", "Non-Profit", "Government"
    ]
    
    all_companies = []
    
    for i in range(count):
        industry = random.choice(industries)
        
        # Add randomization to prompts
        seed = random.randint(1000, 9999)
        temperature_words = ["innovative", "established", "growing", "dynamic", "leading"]
        temp_word = random.choice(temperature_words)
        
        prompt = f"""Generate 1 {temp_word} company in {industry} (seed: {seed}).

Create a realistic company with 3-5 job roles. Use actual job titles from this industry.

JSON format:
{{
  "company_name": "Realistic company name",
  "about": "What this company does",
  "industry": "{industry}",
  "size": "Employee count range",
  "roles": [
    {{
      "title": "Real job title",
      "department": "Department",
      "description": "Job description",
      "location": "City, State",
      "salary_range": [min, max]
    }}
  ]
}}

Return ONLY valid JSON."""

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            company_data = json.loads(response.content[0].text.strip())
            all_companies.append(company_data)
            print(f"✅ Generated: {company_data['company_name']} ({industry})")
            
        except Exception as e:
            print(f"❌ Error generating company {i+1}: {e}")
            continue
    
    # Save results
    output_file = f"companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(all_companies, f, indent=2)
    
    print(f"\n📊 Generated {len(all_companies)} companies")
    print(f"💾 Saved to: {output_file}")
    return all_companies

if __name__ == "__main__":
    generate_companies(1000)