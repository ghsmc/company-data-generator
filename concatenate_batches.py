#!/usr/bin/env python3

import os
import json
import glob
from datetime import datetime

def concatenate_batch_files():
    """Concatenate all batch files into one master file"""
    
    print("🔍 Looking for batch files...")
    
    # Find all batch files
    batch_files = sorted(glob.glob("companies_batch_*.json"))
    
    if not batch_files:
        print("❌ No batch files found!")
        return
    
    print(f"📁 Found {len(batch_files)} batch files")
    
    all_companies = []
    total_roles = 0
    
    for i, batch_file in enumerate(batch_files, 1):
        print(f"📂 Processing {batch_file} ({i}/{len(batch_files)})")
        
        try:
            with open(batch_file, 'r') as f:
                batch_companies = json.load(f)
            
            # Add batch info to each company
            for company in batch_companies:
                company['batch_file'] = batch_file
                company['batch_number'] = i
            
            all_companies.extend(batch_companies)
            
            batch_roles = sum(len(company['roles']) for company in batch_companies)
            total_roles += batch_roles
            
            print(f"   ✅ Added {len(batch_companies)} companies, {batch_roles} roles")
            
        except Exception as e:
            print(f"   ❌ Error processing {batch_file}: {e}")
            continue
    
    if not all_companies:
        print("❌ No companies found in batch files!")
        return
    
    # Create master file
    master_filename = f"companies_master_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    print(f"\n💾 Saving master file: {master_filename}")
    
    with open(master_filename, 'w') as f:
        json.dump(all_companies, f, indent=2)
    
    # Create summary file
    summary = {
        "master_file": master_filename,
        "total_companies": len(all_companies),
        "total_roles": total_roles,
        "batch_files_processed": len(batch_files),
        "concatenated_at": datetime.now().isoformat(),
        "industries": list(set(company['industry'] for company in all_companies)),
        "company_stages": list(set(company.get('company_stage', 'Unknown') for company in all_companies)),
        "size_distribution": {}
    }
    
    # Calculate size distribution
    sizes = [company.get('size', 'Unknown') for company in all_companies]
    for size in set(sizes):
        summary['size_distribution'][size] = sizes.count(size)
    
    summary_filename = f"companies_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(summary_filename, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Calculate file sizes
    master_size = os.path.getsize(master_filename) / (1024*1024)  # MB
    
    print(f"\n🎉 Concatenation complete!")
    print(f"📊 Master file: {master_filename} ({master_size:.1f} MB)")
    print(f"📈 Total companies: {len(all_companies):,}")
    print(f"🎯 Total roles: {total_roles:,}")
    print(f"🏭 Industries: {len(summary['industries'])}")
    print(f"📄 Summary: {summary_filename}")
    
    return master_filename, summary_filename

def clean_batch_files():
    """Optional: Remove individual batch files after concatenation"""
    batch_files = glob.glob("companies_batch_*.json")
    
    if not batch_files:
        return
    
    response = input(f"\n🗑️  Delete {len(batch_files)} batch files? (y/N): ")
    
    if response.lower() == 'y':
        for batch_file in batch_files:
            try:
                os.remove(batch_file)
                print(f"   🗑️  Deleted {batch_file}")
            except Exception as e:
                print(f"   ❌ Error deleting {batch_file}: {e}")
        
        print(f"✅ Cleaned up {len(batch_files)} batch files")

if __name__ == "__main__":
    master_file, summary_file = concatenate_batch_files()
    
    if master_file:
        # clean_batch_files()  # Uncomment to enable cleanup prompt
        pass