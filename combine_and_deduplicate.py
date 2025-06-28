#!/usr/bin/env python3
"""
Combine all batch files and deduplicate companies based on company name.
"""

import json
import glob
from datetime import datetime
from collections import defaultdict

def load_batch_files():
    """Load all batch files and combine them into one list."""
    all_companies = []
    batch_files = sorted(glob.glob("companies_batch_*.json"))
    
    print(f"Found {len(batch_files)} batch files")
    
    for file_path in batch_files:
        print(f"Loading {file_path}...")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                companies = json.load(f)
                all_companies.extend(companies)
                print(f"  Added {len(companies)} companies")
        except Exception as e:
            print(f"  Error loading {file_path}: {e}")
    
    print(f"Total companies loaded: {len(all_companies)}")
    return all_companies

def deduplicate_companies(companies):
    """Deduplicate companies based on company name, keeping the first occurrence."""
    seen_names = set()
    unique_companies = []
    duplicates = []
    
    for company in companies:
        company_name = company.get('company_name', '').strip()
        
        if company_name and company_name not in seen_names:
            seen_names.add(company_name)
            unique_companies.append(company)
        else:
            duplicates.append(company_name)
    
    print(f"Original companies: {len(companies)}")
    print(f"Unique companies: {len(unique_companies)}")
    print(f"Duplicates removed: {len(duplicates)}")
    
    # Show some duplicate examples
    if duplicates:
        duplicate_counts = defaultdict(int)
        for dup in duplicates:
            duplicate_counts[dup] += 1
        
        print(f"Top duplicates:")
        for name, count in sorted(duplicate_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {name}: {count + 1} occurrences")
    
    return unique_companies

def save_combined_file(companies, filename):
    """Save the combined and deduplicated companies to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(companies, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(companies)} companies to {filename}")
        
        # Calculate statistics
        total_roles = sum(len(company.get('roles', [])) for company in companies)
        industries = set(company.get('industry', '') for company in companies if company.get('industry'))
        
        print(f"Statistics:")
        print(f"  Total companies: {len(companies)}")
        print(f"  Total roles: {total_roles}")
        print(f"  Unique industries: {len(industries)}")
        
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def main():
    print("Starting batch file combination and deduplication...")
    
    # Load all batch files
    all_companies = load_batch_files()
    
    if not all_companies:
        print("No companies found in batch files!")
        return
    
    # Deduplicate
    unique_companies = deduplicate_companies(all_companies)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"companies_combined_deduplicated_{timestamp}.json"
    
    # Save combined file
    if save_combined_file(unique_companies, filename):
        print(f"Successfully created {filename}")
    else:
        print("Failed to create combined file")

if __name__ == "__main__":
    main()