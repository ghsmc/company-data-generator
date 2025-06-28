import os
import sqlite3
import json
import time
import uuid
import hashlib
import requests
from datetime import datetime
from dotenv import load_dotenv
from anthropic import Anthropic
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# === CONFIG ===
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY") or "pc-...")
dense_index = pc.Index("dense-milo-companies")
sparse_index = pc.Index("sparse-milo-companies")
# Use batch number in namespace for parallel processing
batch_num = os.getenv("BATCH_NUM", "1")
DENSE_NAMESPACE = f"dense-companies-claude-v8-batch{batch_num}"
SPARSE_NAMESPACE = f"sparse-companies-claude-v8-batch{batch_num}"

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
# Use batch-specific file names for parallel processing  
batch_num = os.getenv("BATCH_NUM", "1")
DB_PATH = os.path.join(DATA_DIR, f"companies_batch{batch_num}.db")
JSON_PATH = os.path.join(DATA_DIR, f"enriched_companies_batch{batch_num}.json")
PROGRESS_PATH = os.path.join(DATA_DIR, f"progress_batch{batch_num}.json")

# === DB SETUP ===
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
  id TEXT PRIMARY KEY,
  company_name TEXT,
  about TEXT,
  industry TEXT,
  sub_industry TEXT,
  company_stage TEXT,
  size TEXT,
  culture_tags TEXT,
  tech_stack TEXT,
  source TEXT,
  fetched_at TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS roles (
  id TEXT PRIMARY KEY,
  company_id TEXT,
  company_name TEXT,
  title TEXT,
  department TEXT,
  seniority_level TEXT,
  industry TEXT,
  sub_industry TEXT,
  location TEXT,
  description TEXT,
  required_skills TEXT,
  nice_to_have_skills TEXT,
  salary_min INTEGER,
  salary_max INTEGER,
  visa_sponsorship BOOLEAN,
  min_experience_years INTEGER,
  source TEXT,
  fetched_at TEXT,
  FOREIGN KEY (company_id) REFERENCES companies (id)
)
""")
conn.commit()

# === HELPERS ===
def gpt(prompt, model="claude-3-5-sonnet-20241022", retries=3):
    for attempt in range(retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=4000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise e

import requests

def get_dense_embedding(text: str):
    # Use a simple embedding service or local model
    # For now, create a mock embedding vector of 1024 dimensions
    # In production, you'd use sentence-transformers or another embedding service
    import hashlib
    
    # Create a deterministic hash-based embedding for demo
    hash_obj = hashlib.sha256(text.encode())
    hash_bytes = hash_obj.digest()
    
    # Convert to 1024 floats
    embedding = []
    for i in range(1024):
        byte_val = hash_bytes[i % len(hash_bytes)]
        # Normalize to [-1, 1]
        embedding.append((byte_val - 128) / 128.0)
    
    return embedding

def get_sparse_embedding(text: str):
    # For now, use the dense embedding and convert to sparse format
    dense_emb = get_dense_embedding(text)
    # Convert to sparse format: only non-zero values with their indices
    threshold = 0.1
    sparse_dict = {}
    for i, val in enumerate(dense_emb):
        if abs(val) > threshold:
            sparse_dict[i] = float(val)
    
    # Return in Pinecone sparse format
    return {
        "indices": list(sparse_dict.keys()),
        "values": list(sparse_dict.values())
    }

def cached_gpt(prompt, cache_prefix="gpt", model="claude-3-5-sonnet-20241022"):
    cache_key = hashlib.sha256(prompt.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{cache_prefix}-{cache_key}.json")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    result = gpt(prompt, model=model)
    try:
        # Extract JSON from markdown code blocks if present
        if "```json" in result:
            start = result.find("```json") + 7
            end = result.find("```", start)
            result = result[start:end].strip()
        elif "```" in result:
            start = result.find("```") + 3
            end = result.find("```", start)
            result = result[start:end].strip()
        
        # Find the JSON object (starts with { or [)
        json_start = -1
        for i, char in enumerate(result):
            if char in ['{', '[']:
                json_start = i
                break
        
        if json_start >= 0:
            # Find the matching closing bracket
            bracket_count = 0
            json_end = -1
            start_char = result[json_start]
            end_char = '}' if start_char == '{' else ']'
            
            for i in range(json_start, len(result)):
                if result[i] == start_char:
                    bracket_count += 1
                elif result[i] == end_char:
                    bracket_count -= 1
                    if bracket_count == 0:
                        json_end = i + 1
                        break
            
            if json_end > 0:
                result = result[json_start:json_end].strip()
        
        parsed = json.loads(result)
        with open(cache_file, "w") as f:
            json.dump(parsed, f, indent=2)
        return parsed
    except json.JSONDecodeError as e:
        print(f"Invalid JSON from Claude:\n{result[:500]}...")
        print(f"JSON Error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        print(f"Result type: {type(result)}")
        print(f"Result preview: {str(result)[:200]}...")
        raise

def save_json(companies):
    with open(JSON_PATH, "a") as f:
        json.dump(companies, f)
        f.write(",\n")

def save_to_sqlite(company, role, company_id, role_id):
    # Save company
    cursor.execute("""
    INSERT OR IGNORE INTO companies (
        id, company_name, about, industry, sub_industry, company_stage, size,
        culture_tags, tech_stack, source, fetched_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        company_id,
        company["company_name"],
        company["about"],
        company["industry"],
        company["sub_industry"],
        company.get("company_stage", ""),
        company.get("size", ""),
        json.dumps(company.get("culture_tags", [])),
        json.dumps(company.get("tech_stack", [])),
        "gpt",
        datetime.utcnow().isoformat()
    ))
    
    # Save role
    cursor.execute("""
    INSERT OR IGNORE INTO roles (
        id, company_id, company_name, title, department, seniority_level, industry, sub_industry, 
        location, description, required_skills, nice_to_have_skills,
        salary_min, salary_max, visa_sponsorship, min_experience_years, source, fetched_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        role_id,
        company_id,
        company["company_name"],
        role["title"],
        role.get("department", ""),
        role.get("seniority_level", ""),
        company["industry"],
        company["sub_industry"],
        role["location"],
        role["description"],
        json.dumps(role["required_skills"]),
        json.dumps(role["nice_to_have_skills"]),
        role["salary_range"][0] if role["salary_range"] else 0,
        role["salary_range"][1] if role["salary_range"] else 0,
        role["visa_sponsorship"],
        role["min_experience_years"],
        "gpt",
        datetime.utcnow().isoformat()
    ))
    conn.commit()

def upsert_to_pinecone(company, role, company_id, role_id):
    embed_text = f"""
Company: {company['company_name']}
About: {company['about']}
Title: {role['title']}
Department: {role.get('department', '')}
Seniority: {role.get('seniority_level', '')}
Description: {role['description']}
Skills: {', '.join(role['required_skills'] + role['nice_to_have_skills'])}
Culture: {', '.join(company.get('culture_tags', []))}
Tech Stack: {', '.join(company.get('tech_stack', []))}
"""

    # Get both dense and sparse embeddings
    dense_embedding = get_dense_embedding(embed_text.strip())
    sparse_embedding = get_sparse_embedding(embed_text.strip())

    # Shared metadata
    metadata = {
        "company_id": company_id,
        "company": company["company_name"],
        "title": role["title"],
        "department": role.get("department", ""),
        "seniority_level": role.get("seniority_level", ""),
        "industry": company["industry"],
        "sub_industry": company["sub_industry"],
        "location": role["location"],
        "description": role["description"],
        "required_skills": ", ".join(role["required_skills"]),
        "nice_to_have_skills": ", ".join(role["nice_to_have_skills"]),
        "skills": ", ".join(role["required_skills"] + role["nice_to_have_skills"]),
        "tech_stack": ", ".join(company.get("tech_stack", [])),
        "culture_tags": ", ".join(company.get("culture_tags", [])),
        "about_company": company["about"],
        "company_stage": company.get("company_stage", ""),
        "company_size": company.get("size", ""),
        "salary_min": role["salary_range"][0] if role["salary_range"] else 0,
        "salary_max": role["salary_range"][1] if role["salary_range"] else 0,
        "visa_sponsorship": role["visa_sponsorship"],
        "min_experience_years": role["min_experience_years"],
        "source": "gpt",
        "fetched_at": datetime.utcnow().isoformat()
    }

    # Dense vector
    dense_vector = {
        "id": role_id,
        "values": dense_embedding,
        "metadata": metadata
    }

    # Sparse vector  
    sparse_vector = {
        "id": role_id,
        "sparse_values": sparse_embedding,
        "metadata": metadata
    }

    # Upsert to both indexes
    dense_index.upsert([dense_vector], namespace=DENSE_NAMESPACE)
    sparse_index.upsert([sparse_vector], namespace=SPARSE_NAMESPACE)

    print(f"✅ Upserted {metadata['title']} ({metadata['department']}) at {metadata['company']} to both dense and sparse indexes")

def get_industry_tree():
    prompt = """Return ONLY a valid JSON object of major industries and their sub-industries. Include these additional sectors:

{
  "Finance": ["Private Equity", "Venture Capital", "Investment Banking", "Commercial Banking", "Insurance", "Asset Management", "Hedge Funds", "Financial Planning", "Credit Services", "Payment Processing", "Cryptocurrency", "Microfinance"],
  "Technology": ["Software Development", "Cloud Computing", "Artificial Intelligence", "Cybersecurity", "Data Analytics", "Telecommunications", "Hardware Manufacturing", "Semiconductors", "Internet Services", "IT Consulting", "Mobile Applications", "Gaming"],
  "Healthcare": ["Pharmaceuticals", "Medical Devices", "Biotechnology", "Healthcare Providers", "Health Insurance", "Digital Health", "Medical Research", "Hospital Management", "Mental Health Services", "Elder Care", "Veterinary Services", "Telemedicine"],
  "Government & Public Sector": ["Federal Government", "State Government", "Local Government", "Military & Defense", "Law Enforcement", "Public Safety", "Public Education", "Social Services", "Urban Planning", "Public Health", "Transportation Authority", "Regulatory Agencies"],
  "Legal Services": ["Corporate Law", "Litigation", "Family Law", "Criminal Defense", "Intellectual Property", "Real Estate Law", "Employment Law", "Immigration Law", "Tax Law", "Environmental Law", "Legal Technology", "Court Administration"],
  "Non-Profit & NGO": ["Healthcare Non-Profits", "Educational Non-Profits", "Environmental Organizations", "Human Rights Organizations", "Religious Organizations", "Arts & Culture Non-Profits", "Community Development", "International Aid", "Animal Welfare", "Advocacy Organizations", "Foundations", "Think Tanks"],
  "Arts & Culture": ["Museums", "Performing Arts", "Visual Arts", "Music Industry", "Film & Television", "Theater", "Dance Companies", "Art Galleries", "Cultural Centers", "Arts Education", "Creative Agencies", "Arts Administration"],
  "Manufacturing": ["Automotive", "Aerospace", "Electronics", "Industrial Equipment", "Consumer Goods", "Chemical Production", "Food Processing", "Textiles", "Metal Fabrication", "Plastics", "Furniture", "Medical Equipment"],
  "Energy": ["Oil & Gas", "Renewable Energy", "Nuclear Power", "Coal Mining", "Utilities", "Energy Distribution", "Solar Power", "Wind Power", "Hydroelectric Power", "Energy Storage", "Energy Trading", "Geothermal"],
  "Real Estate": ["Residential Development", "Commercial Properties", "Property Management", "Real Estate Investment", "Construction", "Architecture", "Interior Design", "Facilities Management", "Urban Planning", "Real Estate Brokerage"],
  "Retail": ["E-commerce", "Department Stores", "Grocery", "Fashion", "Electronics Retail", "Home Improvement", "Specialty Retail", "Direct Marketing", "Wholesale", "Luxury Goods", "Automotive Retail", "Sporting Goods"],
  "Education": ["K-12 Education", "Higher Education", "Online Learning", "Professional Training", "Educational Technology", "Special Education", "Language Learning", "Test Preparation", "Early Childhood Education", "Vocational Training"],
  "Transportation": ["Airlines", "Shipping", "Railways", "Logistics", "Automotive Transport", "Public Transit", "Freight Services", "Marine Transport", "Aviation Services", "Transportation Infrastructure"],
  "Strategy & Management Consulting": ["Top-Tier Strategy Consulting", "Management Consulting", "Technology Consulting", "Digital Transformation", "Operations Consulting", "Organization Design", "Change Management", "Business Development", "Market Research", "Due Diligence", "Post-Merger Integration", "Innovation Consulting"],
  "Investment & Private Markets": ["Private Equity", "Venture Capital", "Growth Equity", "Hedge Funds", "Investment Banking", "Asset Management", "Real Estate Investment", "Infrastructure Investment", "Sovereign Wealth Funds", "Family Offices", "Pension Funds", "Endowment Management"],
  "Professional Services": ["Top Law Firms", "Big Four Accounting", "Executive Search", "Corporate Advisory", "Tax Advisory", "Audit & Assurance", "Risk Advisory", "Forensic Accounting", "Valuation Services", "Restructuring", "Compliance", "ESG Advisory"],
  "Policy & International Affairs": ["Think Tanks", "Policy Research", "International Organizations", "Diplomatic Services", "Development Organizations", "NGOs & Foundations", "Political Consulting", "Government Relations", "Trade Organizations", "Multilateral Institutions", "Embassy Services", "Foreign Policy"],
  "Media & Publishing": ["Elite Media Organizations", "Financial Media", "Policy Publications", "Book Publishing", "Digital Media Platforms", "Journalism", "Editorial", "Broadcasting", "Documentary Production", "Content Strategy", "Communications", "Public Relations"],
  "Technology & Innovation": ["Big Tech", "AI & Machine Learning", "Fintech", "Healthtech", "Edtech", "Enterprise Software", "Cybersecurity", "Data Analytics", "Cloud Computing", "Blockchain", "Robotics", "Quantum Computing"],
  "Research & Academia": ["Research Institutions", "University Administration", "Academic Research", "Policy Research", "Economic Research", "Social Research", "Scientific Research", "R&D Labs", "Innovation Centers", "Academic Publishing", "Educational Leadership", "Research Funding"],
  "High-End Retail & Luxury": ["Luxury Brands", "High-End Retail", "Premium Consumer Goods", "Luxury Hospitality", "Private Banking", "Wealth Services", "Art & Auction Houses", "Fine Dining", "Premium Travel", "Luxury Real Estate", "Private Aviation", "Yacht Industry"],
  "Emerging Industries": ["Clean Energy", "Climate Tech", "Space Technology", "Autonomous Vehicles", "Biotechnology", "Precision Medicine", "Virtual Reality", "Augmented Reality", "Drone Technology", "3D Printing", "Nanotechnology", "Smart Cities"]
}

Return ONLY this JSON object, no other text."""
    return cached_gpt(prompt, cache_prefix="industry-tree-elite-yale-focused", model="claude-3-5-sonnet-20241022")

def web_search_companies(industry, subindustry):
    """Search for real companies and job data in the specified industry"""
    try:
        # Search for companies in this industry
        search_query = f"top companies {subindustry} {industry} careers jobs"
        
        # Make a web search request (you'll need to implement this with your preferred search API)
        # For now, using a simple requests approach
        search_results = f"Web search results for: {search_query}"
        
        return search_results
    except Exception as e:
        print(f"Web search failed: {e}")
        return ""

def get_enriched_companies(industry, subindustry):
    # First, search for real company data
    web_data = web_search_companies(industry, subindustry)
    
    prompt = f"""You are a recruitment expert with access to web search data. Generate 15 real companies in "{subindustry}" ({industry}).

Web search context: {web_data}

For EACH company, create EXACTLY 5-8 job roles that actually exist at that specific type of company based on real job postings and company structures.

IMPORTANT: Generate 5-8 roles per company to keep responses manageable. Include entry-level, mid-level, senior, and executive positions.

Research and use REAL job titles from actual companies in this industry. DO NOT use generic templates.

Examples of industry-appropriate roles:
- Investment Banks: Investment Banking Analyst, Equity Research Associate, Trader, Managing Director, Vice President M&A
- Manufacturing: Production Manager, Quality Engineer, Plant Supervisor, Supply Chain Analyst, Manufacturing Engineer
- Healthcare: Registered Nurse, Physician, Medical Technician, Clinical Research Coordinator, Healthcare Administrator
- Retail: Store Manager, Buyer, Visual Merchandiser, Inventory Planner, District Manager

Use realistic:
- Job titles that exist at these companies
- Department structures
- Salary ranges for the industry/location
- Required skills specific to the role
- Company stages and sizes

JSON format:
[
  {{
    "company_name": "Real Company Name",
    "about": "What this company actually does",
    "industry": "{industry}",
    "sub_industry": "{subindustry}",
    "company_stage": "Public/Private/Startup",
    "size": "Actual employee count range",
    "culture_tags": ["Based on real company culture"],
    "tech_stack": ["Tools actually used in this industry"],
    "roles": [
      {{
        "title": "Real job title from job postings",
        "department": "Actual department name", 
        "description": "Real job responsibilities",
        "required_skills": ["Skills from real job postings"],
        "nice_to_have_skills": ["Additional relevant skills"],
        "location": "Real office locations",
        "salary_range": [market_rate_min, market_rate_max],
        "visa_sponsorship": true/false,
        "min_experience_years": 0-15,
        "seniority_level": "Entry/Mid/Senior/Director/VP/C-Suite"
      }}
    ]
  }}
]

Return ONLY valid JSON with realistic data."""
    # Add batch number to cache key for multiple runs
    batch_num = os.getenv("BATCH_NUM", "1")
    return cached_gpt(prompt, cache_prefix=f"{industry}-{subindustry}-v8-15companies-batch{batch_num}")

def load_progress():
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_PATH, "w") as f:
        json.dump(progress, f)

# === BATCH PROCESSING ===
def run_batch(target_industries=None, start_from=None):
    """Run processing for specific industries or continue from a checkpoint"""
    industry_tree = get_industry_tree()
    progress = load_progress()
    
    # Filter industries if specified
    if target_industries:
        industry_tree = {k: v for k, v in industry_tree.items() if k in target_industries}
    
    started = start_from is None
    total_processed = 0
    
    for industry, subindustries in industry_tree.items():
        for subindustry in subindustries:
            key = f"{industry}::{subindustry}"
            
            # Skip until we reach start_from
            if not started:
                if key == start_from:
                    started = True
                else:
                    continue
            
            if progress.get(key) == "done":
                continue
                
            print(f"\n🔍 {industry} > {subindustry}")
            try:
                result = get_enriched_companies(industry, subindustry)
                
                # Handle case where Claude wraps in {"companies": [...]}
                if isinstance(result, dict) and "companies" in result:
                    companies = result["companies"]
                elif isinstance(result, list):
                    companies = result
                elif isinstance(result, dict):
                    # Check if it's a single company wrapped in a dict
                    if "company_name" in result:
                        companies = [result]
                    elif "status" in result:
                        print(f"Claude returned status message instead of companies. Skipping...")
                        continue
                    else:
                        print(f"Dict without 'companies' key. Keys: {list(result.keys())}")
                        print(f"Sample data: {str(result)[:200]}...")
                        continue
                else:
                    print(f"Expected list or dict with 'companies' key, got {type(result)}")
                    continue
                
                print(f"Got {len(companies)} companies")
                    
                save_json(companies)
                for i, company in enumerate(companies):
                    if not isinstance(company, dict):
                        print(f"Expected dict, got {type(company)}: {company}")
                        continue
                        
                    print(f"Processing company {i+1}/{len(companies)}: {company.get('company_name', 'Unknown')}")
                    # Clean company name for ASCII-only IDs
                    clean_name = company['company_name'].lower()
                    # Remove non-ASCII characters
                    clean_name = ''.join(c for c in clean_name if ord(c) < 128)
                    # Replace spaces and special chars with dashes
                    clean_name = ''.join(c if c.isalnum() else '-' for c in clean_name)
                    # Remove multiple consecutive dashes
                    clean_name = '-'.join(filter(None, clean_name.split('-')))
                    company_id = f"{clean_name}-{uuid.uuid4().hex[:6]}"
                    roles = company.get("roles", [])
                    print(f"  Found {len(roles)} roles")
                    
                    for j, role in enumerate(roles):
                        # Ensure all required fields exist with defaults
                        role.setdefault("title", "Unknown Title")
                        role.setdefault("department", "")
                        role.setdefault("description", "")
                        role.setdefault("required_skills", [])
                        role.setdefault("nice_to_have_skills", [])
                        role.setdefault("location", "")
                        # Fix salary_range to ensure it's always a valid list with 2 elements
                        salary_range = role.get("salary_range", [0, 0])
                        if not isinstance(salary_range, list) or len(salary_range) != 2:
                            salary_range = [0, 0]
                        role["salary_range"] = salary_range
                        role.setdefault("visa_sponsorship", False)
                        role.setdefault("min_experience_years", 0)
                        role.setdefault("seniority_level", "")
                        
                        print(f"  Processing role {j+1}/{len(roles)}: {role['title']}")
                        # Clean role title for ASCII-only IDs
                        clean_title = role['title'].lower()
                        clean_title = ''.join(c for c in clean_title if ord(c) < 128)
                        clean_title = ''.join(c if c.isalnum() else '-' for c in clean_title)
                        clean_title = '-'.join(filter(None, clean_title.split('-')))
                        role_id = f"{company_id}-{clean_title}-{uuid.uuid4().hex[:6]}"
                        save_to_sqlite(company, role, company_id, role_id)
                        upsert_to_pinecone(company, role, company_id, role_id)
                        time.sleep(0.05)  # Minimal sleep for massive scale
                        
                progress[key] = "done"
                save_progress(progress)
                total_processed += len(companies)
                print(f"📊 Total companies processed so far: {total_processed}")
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error in {industry} > {subindustry}: {e}")
                time.sleep(3)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            # Run specific industries: python main.py batch "Government & Public Sector,Legal Services"
            if len(sys.argv) > 2:
                industries = sys.argv[2].split(",")
                run_batch(target_industries=industries)
            else:
                print("Available industries:")
                tree = get_industry_tree()
                for industry in tree.keys():
                    print(f"  - {industry}")
        elif sys.argv[1] == "continue":
            # Continue from checkpoint: python main.py continue "Industry::Sub-Industry"
            start_point = sys.argv[2] if len(sys.argv) > 2 else None
            run_batch(start_from=start_point)
        else:
            print("Usage:")
            print("  python main.py                                    # Run all industries")
            print("  python main.py batch 'Legal Services'            # Run specific industry")
            print("  python main.py continue 'Finance::Private Equity' # Continue from checkpoint")
    else:
        # Run all industries
        run_batch()
