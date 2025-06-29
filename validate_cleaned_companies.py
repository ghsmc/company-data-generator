import json
import collections
import re
from urllib.parse import urlparse

def load_and_examine_file(file_path):
    """Load and do basic examination of the cleaned companies file"""
    try:
        with open(file_path, 'r') as f:
            companies = json.load(f)
        
        print(f"✓ File loaded successfully")
        print(f"✓ Valid JSON structure")
        print(f"✓ Total companies: {len(companies)}")
        
        # Check if it's a list of companies
        if not isinstance(companies, list):
            print("✗ Expected a list of companies")
            return None
            
        if not companies:
            print("✗ No companies found in file")
            return None
            
        # Sample first company structure
        sample = companies[0]
        print(f"✓ Sample company fields: {list(sample.keys())}")
        
        return companies
        
    except FileNotFoundError:
        print("✗ File not found")
        return None
    except json.JSONDecodeError as e:
        print(f"✗ JSON decode error: {e}")
        return None

def check_duplicates(companies):
    """Check for any remaining duplicate companies"""
    print("\n=== DUPLICATE CHECK ===")
    
    # Check by company name
    name_counts = collections.Counter(company.get('company_name', '') for company in companies)
    name_duplicates = {name: count for name, count in name_counts.items() if count > 1}
    
    print(f"Duplicate company names: {len(name_duplicates)}")
    if name_duplicates:
        for name, count in sorted(name_duplicates.items()):
            print(f"  '{name}': {count} occurrences")
    
    # Check for similar names (potential duplicates)
    company_names = [company.get('company_name', '').lower().strip() for company in companies]
    similar_names = []
    
    for i, name1 in enumerate(company_names):
        for j, name2 in enumerate(company_names[i+1:], i+1):
            if name1 and name2:
                # Check for similar names (substring, common words)
                if (name1 in name2 or name2 in name1) and name1 != name2:
                    similar_names.append((companies[i]['company_name'], companies[j]['company_name']))
    
    print(f"Similar company names (potential duplicates): {len(similar_names)}")
    for name1, name2 in similar_names[:10]:  # Show first 10
        print(f"  '{name1}' <-> '{name2}'")
    if len(similar_names) > 10:
        print(f"  ... and {len(similar_names) - 10} more")
    
    return len(name_duplicates) == 0

def validate_data_quality(companies):
    """Validate data quality and consistency"""
    print("\n=== DATA QUALITY VALIDATION ===")
    
    issues = []
    
    # Required fields check
    required_fields = ['company_name', 'about', 'industry', 'sub_industry', 'company_stage', 'size']
    
    for i, company in enumerate(companies):
        # Check required fields
        for field in required_fields:
            if field not in company or not str(company[field]).strip():
                issues.append(f"Company {i} ('{company.get('company_name', 'Unknown')}'): Missing or empty {field}")
        
        # Check company name validity
        name = company.get('company_name', '')
        if len(name.strip()) < 2:
            issues.append(f"Company {i}: Company name too short: '{name}'")
        
        # Check about field length
        about = company.get('about', '')
        if len(about.strip()) < 10:
            issues.append(f"Company {i} ('{name}'): About description too short")
        
        # Check industry/sub_industry consistency
        industry = company.get('industry', '')
        sub_industry = company.get('sub_industry', '')
        if industry == sub_industry and industry:
            issues.append(f"Company {i} ('{name}'): Industry and sub_industry are identical")
        
        # Check culture_tags
        culture_tags = company.get('culture_tags', [])
        if not isinstance(culture_tags, list):
            issues.append(f"Company {i} ('{name}'): culture_tags should be a list")
        elif len(culture_tags) == 0:
            issues.append(f"Company {i} ('{name}'): No culture tags")
        
        # Check tech_stack
        tech_stack = company.get('tech_stack', [])
        if not isinstance(tech_stack, list):
            issues.append(f"Company {i} ('{name}'): tech_stack should be a list")
        
        # Check roles
        roles = company.get('roles', [])
        if not isinstance(roles, list):
            issues.append(f"Company {i} ('{name}'): roles should be a list")
        elif len(roles) == 0:
            issues.append(f"Company {i} ('{name}'): No roles defined")
        else:
            # Validate each role
            for j, role in enumerate(roles):
                if not isinstance(role, dict):
                    issues.append(f"Company {i} ('{name}'), Role {j}: Should be a dictionary")
                    continue
                
                # Check required role fields
                role_required = ['title', 'description', 'required_skills', 'location']
                for field in role_required:
                    if field not in role or not str(role[field]).strip():
                        issues.append(f"Company {i} ('{name}'), Role {j}: Missing {field}")
                
                # Check salary range
                if 'salary_range' in role:
                    salary_range = role['salary_range']
                    if not isinstance(salary_range, list) or len(salary_range) != 2:
                        issues.append(f"Company {i} ('{name}'), Role {j}: Invalid salary_range format")
                    else:
                        try:
                            min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                            if min_sal >= max_sal:
                                issues.append(f"Company {i} ('{name}'), Role {j}: Invalid salary range: min >= max")
                            if min_sal < 0 or max_sal < 0:
                                issues.append(f"Company {i} ('{name}'), Role {j}: Negative salary values")
                            if max_sal > 1000000:  # Sanity check
                                issues.append(f"Company {i} ('{name}'), Role {j}: Salary seems too high: {max_sal}")
                        except (ValueError, TypeError):
                            issues.append(f"Company {i} ('{name}'), Role {j}: Non-numeric salary range")
                
                # Check skills
                required_skills = role.get('required_skills', [])
                if not isinstance(required_skills, list):
                    issues.append(f"Company {i} ('{name}'), Role {j}: required_skills should be a list")
                elif len(required_skills) == 0:
                    issues.append(f"Company {i} ('{name}'), Role {j}: No required skills")
    
    print(f"Total data quality issues: {len(issues)}")
    
    # Show first 20 issues
    for issue in issues[:20]:
        print(f"  - {issue}")
    
    if len(issues) > 20:
        print(f"  ... and {len(issues) - 20} more issues")
    
    return issues

def check_data_consistency(companies):
    """Check for data consistency across companies"""
    print("\n=== DATA CONSISTENCY CHECK ===")
    
    # Analyze distributions
    industries = collections.Counter(company.get('industry', '') for company in companies)
    company_stages = collections.Counter(company.get('company_stage', '') for company in companies)
    sizes = collections.Counter(company.get('size', '') for company in companies)
    
    print(f"Industries ({len(industries)}):")
    for industry, count in industries.most_common(10):
        print(f"  {industry}: {count}")
    
    print(f"\nCompany stages ({len(company_stages)}):")
    for stage, count in company_stages.most_common():
        print(f"  {stage}: {count}")
    
    print(f"\nCompany sizes ({len(sizes)}):")
    for size, count in sizes.most_common():
        print(f"  {size}: {count}")
    
    # Check for inconsistent values
    inconsistencies = []
    
    # Check for unusual industry values
    if 'Unknown' in industries:
        inconsistencies.append(f"Found {industries['Unknown']} companies with 'Unknown' industry")
    
    # Check for unusual stage values
    valid_stages = ['Startup', 'Early', 'Growth', 'Mature', 'Public', 'Private', 'Established']
    for stage in company_stages:
        if stage not in valid_stages and stage != '':
            inconsistencies.append(f"Unusual company stage: '{stage}' ({company_stages[stage]} companies)")
    
    # Check for unusual size values
    valid_sizes = ['Small', 'Medium', 'Large', 'Startup', '1-10', '11-50', '51-200', '201-500', '501-1000', '1000+']
    for size in sizes:
        if size not in valid_sizes and size != '':
            inconsistencies.append(f"Unusual company size: '{size}' ({sizes[size]} companies)")
    
    print(f"\nData inconsistencies: {len(inconsistencies)}")
    for inconsistency in inconsistencies:
        print(f"  - {inconsistency}")

def main():
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/cleaned_companies.json'
    
    print("=== SCANNING CLEANED COMPANIES FILE ===")
    
    # Step 1: Load and examine
    companies = load_and_examine_file(file_path)
    if not companies:
        return
    
    # Step 2: Check for duplicates
    no_duplicates = check_duplicates(companies)
    
    # Step 3: Validate data quality
    issues = validate_data_quality(companies)
    
    # Step 4: Check data consistency
    check_data_consistency(companies)
    
    # Summary
    print("\n=== SUMMARY ===")
    print(f"✓ File is valid JSON with {len(companies)} companies")
    print(f"{'✓' if no_duplicates else '✗'} No duplicate company names")
    print(f"{'✓' if len(issues) == 0 else '✗'} {len(issues)} data quality issues found")
    
    if len(issues) == 0 and no_duplicates:
        print("\n🎉 File appears to be clean and ready for use!")
    else:
        print(f"\n⚠️  File needs attention: {len(issues)} issues to fix")

if __name__ == "__main__":
    main()