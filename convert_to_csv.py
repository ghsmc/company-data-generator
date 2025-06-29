import json
import csv
import pandas as pd

def convert_companies_to_csv():
    """Convert the complete companies JSON dataset to CSV format"""
    
    # Load the complete dataset
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/complete_companies_dataset.json', 'r') as f:
        companies = json.load(f)
    
    print(f"📊 Loading {len(companies)} companies from JSON...")
    
    # Create two CSV files: one for companies, one for roles
    
    # 1. Companies CSV
    companies_data = []
    roles_data = []
    
    for company in companies:
        # Extract company data
        company_row = {
            'company_name': company.get('company_name', ''),
            'about': company.get('about', ''),
            'industry': company.get('industry', ''),
            'sub_industry': company.get('sub_industry', ''),
            'company_stage': company.get('company_stage', ''),
            'size': company.get('size', ''),
            'culture_tags': ', '.join(company.get('culture_tags', [])),
            'tech_stack': ', '.join(company.get('tech_stack', [])),
            'total_roles': len(company.get('roles', []))
        }
        companies_data.append(company_row)
        
        # Extract roles data
        for role in company.get('roles', []):
            role_row = {
                'company_name': company.get('company_name', ''),
                'industry': company.get('industry', ''),
                'sub_industry': company.get('sub_industry', ''),
                'company_stage': company.get('company_stage', ''),
                'company_size': company.get('size', ''),
                'role_title': role.get('title', ''),
                'role_description': role.get('description', ''),
                'required_skills': ', '.join(role.get('required_skills', [])),
                'nice_to_have_skills': ', '.join(role.get('nice_to_have_skills', [])),
                'location': role.get('location', ''),
                'salary_min': role.get('salary_range', [None, None])[0],
                'salary_max': role.get('salary_range', [None, None])[1] if len(role.get('salary_range', [])) > 1 else None,
                'visa_sponsorship': role.get('visa_sponsorship', ''),
                'min_experience_years': role.get('min_experience_years', '')
            }
            roles_data.append(role_row)
    
    # Save companies CSV
    companies_csv_path = '/Users/georgemccain/Desktop/untitled folder 2/data/companies.csv'
    companies_df = pd.DataFrame(companies_data)
    companies_df.to_csv(companies_csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Companies CSV saved: {companies_csv_path}")
    print(f"   📊 {len(companies_data)} companies")
    
    # Save roles CSV
    roles_csv_path = '/Users/georgemccain/Desktop/untitled folder 2/data/roles.csv'
    roles_df = pd.DataFrame(roles_data)
    roles_df.to_csv(roles_csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Roles CSV saved: {roles_csv_path}")
    print(f"   📊 {len(roles_data)} roles")
    
    # Create a flattened single CSV (one row per role with company info)
    flattened_csv_path = '/Users/georgemccain/Desktop/untitled folder 2/data/complete_dataset_flattened.csv'
    roles_df.to_csv(flattened_csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Flattened CSV saved: {flattened_csv_path}")
    print(f"   📊 {len(roles_data)} rows (one per role)")
    
    # Show sample data
    print(f"\n📊 SAMPLE COMPANIES DATA:")
    print(companies_df.head(3)[['company_name', 'industry', 'sub_industry', 'total_roles']])
    
    print(f"\n📊 SAMPLE ROLES DATA:")
    print(roles_df.head(3)[['company_name', 'role_title', 'salary_min', 'salary_max', 'location']])
    
    # Summary statistics
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"  📊 Total companies: {len(companies_data):,}")
    print(f"  📊 Total roles: {len(roles_data):,}")
    print(f"  📊 Industries: {companies_df['industry'].nunique()}")
    print(f"  📊 Sub-industries: {companies_df['sub_industry'].nunique()}")
    print(f"  📊 Average roles per company: {len(roles_data) / len(companies_data):.1f}")
    
    # Industry breakdown
    print(f"\n🏢 TOP 10 INDUSTRIES BY COMPANY COUNT:")
    industry_counts = companies_df['industry'].value_counts().head(10)
    for industry, count in industry_counts.items():
        print(f"  • {industry}: {count}")
    
    return companies_csv_path, roles_csv_path, flattened_csv_path

def main():
    """Convert JSON to CSV format"""
    
    print("📄 CONVERTING JSON TO CSV FORMAT")
    print("=" * 50)
    
    try:
        companies_csv, roles_csv, flattened_csv = convert_companies_to_csv()
        
        print(f"\n✅ Successfully converted to CSV format!")
        print(f"\nGenerated files:")
        print(f"  1. {companies_csv}")
        print(f"  2. {roles_csv}")
        print(f"  3. {flattened_csv}")
        
    except Exception as e:
        print(f"❌ Error converting to CSV: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()