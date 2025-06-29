import json
import pandas as pd

def export_companies_to_csv():
    """Export companies data to CSV excluding roles but including all other company details"""
    
    # Load the complete dataset
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/complete_companies_dataset.json', 'r') as f:
        companies = json.load(f)
    
    print(f"📊 Loading {len(companies)} companies from JSON...")
    
    # Extract company data only (excluding roles)
    companies_data = []
    
    for company in companies:
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
    
    # Create DataFrame and save to CSV
    companies_df = pd.DataFrame(companies_data)
    csv_path = '/Users/georgemccain/Desktop/untitled folder 2/data/companies_only.csv'
    
    companies_df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Companies CSV exported: {csv_path}")
    print(f"   📊 {len(companies_data)} companies")
    print(f"   📊 {len(companies_df.columns)} columns")
    
    # Show sample data
    print(f"\n📊 SAMPLE DATA:")
    print(companies_df.head(5))
    
    # Show all column names
    print(f"\n📋 COLUMNS:")
    for i, col in enumerate(companies_df.columns, 1):
        print(f"  {i}. {col}")
    
    # Summary statistics
    print(f"\n📈 SUMMARY:")
    print(f"  📊 Total companies: {len(companies_data):,}")
    print(f"  📊 Industries: {companies_df['industry'].nunique()}")
    print(f"  📊 Sub-industries: {companies_df['sub_industry'].nunique()}")
    
    # Industry breakdown
    print(f"\n🏢 TOP 10 INDUSTRIES:")
    industry_counts = companies_df['industry'].value_counts().head(10)
    for industry, count in industry_counts.items():
        print(f"  • {industry}: {count}")
    
    return csv_path

if __name__ == "__main__":
    export_companies_to_csv()