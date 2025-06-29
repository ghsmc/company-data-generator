import json
import csv
import pandas as pd

def convert_to_single_companies_csv():
    """Convert the complete companies JSON dataset to a single CSV with roles as columns"""
    
    # Load the complete dataset
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/complete_companies_dataset.json', 'r') as f:
        companies = json.load(f)
    
    print(f"📊 Loading {len(companies)} companies from JSON...")
    
    # Create single CSV with companies and roles as columns
    companies_data = []
    
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
        
        # Add roles as a structured column
        roles_list = []
        for role in company.get('roles', []):
            role_info = {
                'title': role.get('title', ''),
                'description': role.get('description', ''),
                'required_skills': role.get('required_skills', []),
                'nice_to_have_skills': role.get('nice_to_have_skills', []),
                'location': role.get('location', ''),
                'salary_range': role.get('salary_range', []),
                'visa_sponsorship': role.get('visa_sponsorship', ''),
                'min_experience_years': role.get('min_experience_years', '')
            }
            roles_list.append(role_info)
        
        # Convert roles to a formatted string for CSV
        roles_formatted = []
        for i, role in enumerate(roles_list, 1):
            salary_range = role['salary_range']
            salary_str = f"${salary_range[0]:,}-${salary_range[1]:,}" if len(salary_range) == 2 else "Not specified"
            
            role_str = f"""Role {i}: {role['title']}
  Description: {role['description']}
  Location: {role['location']}
  Salary: {salary_str}
  Required Skills: {', '.join(role['required_skills'])}
  Nice-to-Have: {', '.join(role['nice_to_have_skills'])}
  Experience: {role['min_experience_years']} years
  Visa Sponsorship: {role['visa_sponsorship']}"""
            
            roles_formatted.append(role_str)
        
        company_row['roles'] = '\n\n'.join(roles_formatted)
        
        # Also add individual role columns for easier filtering
        for i, role in enumerate(roles_list, 1):
            if i <= 5:  # Limit to first 5 roles to keep CSV manageable
                company_row[f'role_{i}_title'] = role['title']
                company_row[f'role_{i}_location'] = role['location']
                salary_range = role['salary_range']
                company_row[f'role_{i}_salary_min'] = salary_range[0] if len(salary_range) >= 1 else ''
                company_row[f'role_{i}_salary_max'] = salary_range[1] if len(salary_range) >= 2 else ''
                company_row[f'role_{i}_required_skills'] = ', '.join(role['required_skills'])
                company_row[f'role_{i}_visa_sponsorship'] = role['visa_sponsorship']
                company_row[f'role_{i}_min_experience'] = role['min_experience_years']
        
        companies_data.append(company_row)
    
    # Save single companies CSV
    csv_path = '/Users/georgemccain/Desktop/untitled folder 2/data/companies_with_roles.csv'
    companies_df = pd.DataFrame(companies_data)
    
    # Fill NaN values with empty strings for cleaner CSV
    companies_df = companies_df.fillna('')
    
    companies_df.to_csv(csv_path, index=False, encoding='utf-8')
    
    print(f"✅ Companies CSV saved: {csv_path}")
    print(f"   📊 {len(companies_data)} companies")
    print(f"   📊 {companies_df.shape[1]} columns")
    
    # Show sample data
    print(f"\n📊 SAMPLE DATA:")
    sample_cols = ['company_name', 'industry', 'total_roles', 'role_1_title', 'role_1_salary_min', 'role_1_location']
    available_cols = [col for col in sample_cols if col in companies_df.columns]
    print(companies_df.head(3)[available_cols])
    
    # Show column names
    print(f"\n📋 COLUMN NAMES:")
    for i, col in enumerate(companies_df.columns, 1):
        print(f"  {i:2d}. {col}")
        if i >= 20:  # Show first 20 columns
            print(f"      ... and {len(companies_df.columns) - 20} more columns")
            break
    
    # Summary statistics
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"  📊 Total companies: {len(companies_data):,}")
    print(f"  📊 Total columns: {companies_df.shape[1]}")
    print(f"  📊 Industries: {companies_df['industry'].nunique()}")
    print(f"  📊 Average roles per company: {companies_df['total_roles'].mean():.1f}")
    print(f"  📊 Max roles in single company: {companies_df['total_roles'].max()}")
    
    # Industry breakdown
    print(f"\n🏢 TOP 10 INDUSTRIES BY COMPANY COUNT:")
    industry_counts = companies_df['industry'].value_counts().head(10)
    for industry, count in industry_counts.items():
        print(f"  • {industry}: {count}")
    
    return csv_path

def main():
    """Convert JSON to single companies CSV with roles as columns"""
    
    print("📄 CONVERTING JSON TO SINGLE COMPANIES CSV")
    print("=" * 50)
    
    try:
        csv_path = convert_to_single_companies_csv()
        
        print(f"\n✅ Successfully converted to single companies CSV!")
        print(f"\nGenerated file: {csv_path}")
        print(f"\nThe CSV contains:")
        print(f"  • One row per company")
        print(f"  • All company details as columns")
        print(f"  • All roles formatted in a 'roles' column")
        print(f"  • Individual role details as separate columns (role_1_title, role_1_salary_min, etc.)")
        
    except Exception as e:
        print(f"❌ Error converting to CSV: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()