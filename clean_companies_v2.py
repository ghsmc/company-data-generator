import json
import re
from collections import defaultdict

def parse_malformed_json(file_path):
    """Parse the malformed JSON file and extract company records"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    companies = []
    
    # Use regex to find all complete company objects
    company_pattern = r'\{"company_name":\s*"[^"]*"[^}]*\}'
    matches = re.finditer(company_pattern, content, re.DOTALL)
    
    for match in matches:
        company_str = match.group()
        
        # Find the complete object by counting braces
        start_pos = match.start()
        brace_count = 0
        end_pos = start_pos
        
        for i, char in enumerate(content[start_pos:], start_pos):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = i + 1
                    break
        
        try:
            company_json = content[start_pos:end_pos]
            company = json.loads(company_json)
            companies.append(company)
        except json.JSONDecodeError:
            continue
    
    print(f"Extracted {len(companies)} company records")
    return companies

def deduplicate_companies(companies):
    """Remove duplicates, keeping the most complete record"""
    company_groups = defaultdict(list)
    
    # Group companies by name
    for company in companies:
        name = company.get('company_name', '').strip()
        if name:
            company_groups[name].append(company)
    
    deduplicated = []
    duplicates_removed = 0
    
    for name, group in company_groups.items():
        if len(group) == 1:
            deduplicated.append(group[0])
        else:
            # Find the most complete record
            best_company = max(group, key=lambda c: (
                len([k for k, v in c.items() if v and v != [] and v != ""]),  # Non-empty fields
                len(str(c.get('about', ''))),                                # Description length
                len(c.get('roles', [])),                                     # Number of roles
                len(c.get('tech_stack', []))                                 # Tech stack size
            ))
            deduplicated.append(best_company)
            duplicates_removed += len(group) - 1
            print(f"Deduplicated '{name}': kept 1 of {len(group)} records")
    
    print(f"After deduplication: {len(deduplicated)} companies")
    print(f"Duplicates removed: {duplicates_removed}")
    return deduplicated

def fix_data_quality(companies):
    """Fix data quality issues"""
    fixed_companies = []
    issues_fixed = 0
    
    for company in companies:
        fixed_company = company.copy()
        
        # Fix salary ranges
        if 'roles' in fixed_company and isinstance(fixed_company['roles'], list):
            for role in fixed_company['roles']:
                if isinstance(role, dict) and 'salary_range' in role:
                    salary_range = role['salary_range']
                    if isinstance(salary_range, list) and len(salary_range) == 2:
                        try:
                            min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                            if min_sal >= max_sal:
                                role['salary_range'] = [min_sal, min_sal + 30000]
                                issues_fixed += 1
                            elif min_sal < 0:
                                role['salary_range'] = [abs(min_sal), abs(max_sal)]
                                issues_fixed += 1
                        except (ValueError, TypeError):
                            role['salary_range'] = [50000, 80000]
                            issues_fixed += 1
        
        # Ensure required fields exist with proper defaults
        if 'company_name' not in fixed_company:
            fixed_company['company_name'] = "Unknown Company"
            issues_fixed += 1
        if 'about' not in fixed_company:
            fixed_company['about'] = ""
            issues_fixed += 1
        if 'industry' not in fixed_company:
            fixed_company['industry'] = "Unknown"
            issues_fixed += 1
        if 'sub_industry' not in fixed_company:
            fixed_company['sub_industry'] = ""
            issues_fixed += 1
        if 'company_stage' not in fixed_company:
            fixed_company['company_stage'] = "Unknown"
            issues_fixed += 1
        if 'size' not in fixed_company:
            fixed_company['size'] = "Unknown"
            issues_fixed += 1
        if 'culture_tags' not in fixed_company:
            fixed_company['culture_tags'] = []
            issues_fixed += 1
        if 'tech_stack' not in fixed_company:
            fixed_company['tech_stack'] = []
            issues_fixed += 1
        if 'roles' not in fixed_company:
            fixed_company['roles'] = []
            issues_fixed += 1
        
        # Clean up string fields
        string_fields = ['company_name', 'about', 'industry', 'sub_industry', 'company_stage', 'size']
        for field in string_fields:
            if field in fixed_company and isinstance(fixed_company[field], str):
                fixed_company[field] = fixed_company[field].strip()
        
        fixed_companies.append(fixed_company)
    
    print(f"Fixed {issues_fixed} data quality issues")
    return fixed_companies

def validate_companies(companies):
    """Validate the cleaned data"""
    issues = []
    
    for i, company in enumerate(companies):
        # Check required fields
        if not company.get('company_name', '').strip():
            issues.append(f"Company {i}: Missing company name")
        
        # Check salary ranges
        if 'roles' in company:
            for j, role in enumerate(company['roles']):
                if 'salary_range' in role:
                    salary_range = role['salary_range']
                    if not (isinstance(salary_range, list) and len(salary_range) == 2):
                        issues.append(f"Company {i}, Role {j}: Invalid salary range format")
                    else:
                        try:
                            min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                            if min_sal >= max_sal or min_sal < 0:
                                issues.append(f"Company {i}, Role {j}: Invalid salary range values")
                        except (ValueError, TypeError):
                            issues.append(f"Company {i}, Role {j}: Non-numeric salary range")
    
    return issues

def main():
    input_file = '/Users/georgemccain/Desktop/untitled folder 2/data/enriched_companies.json'
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/cleaned_companies.json'
    
    print("Step 1: Parsing malformed JSON...")
    companies = parse_malformed_json(input_file)
    
    if not companies:
        print("No companies found! Trying alternative parsing...")
        # Alternative: use regex to extract company data
        with open(input_file, 'r') as f:
            content = f.read()
        
        company_names = re.findall(r'"company_name":\s*"([^"]+)"', content)
        print(f"Found {len(company_names)} company name references")
        return
    
    print("\nStep 2: Removing duplicates...")
    deduplicated = deduplicate_companies(companies)
    
    print("\nStep 3: Fixing data quality issues...")
    cleaned = fix_data_quality(deduplicated)
    
    print("\nStep 4: Validating cleaned data...")
    validation_issues = validate_companies(cleaned)
    if validation_issues:
        print(f"Found {len(validation_issues)} validation issues:")
        for issue in validation_issues[:5]:  # Show first 5
            print(f"  - {issue}")
        if len(validation_issues) > 5:
            print(f"  ... and {len(validation_issues) - 5} more")
    else:
        print("No validation issues found")
    
    print("\nStep 5: Writing cleaned data...")
    with open(output_file, 'w') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    
    print(f"\nCleaning complete!")
    print(f"Original: {len(companies)} companies")
    print(f"Cleaned: {len(cleaned)} companies") 
    print(f"Removed: {len(companies) - len(cleaned)} duplicates")
    print(f"Output saved to: {output_file}")
    
    # Validate the output JSON
    try:
        with open(output_file, 'r') as f:
            json.load(f)
        print("✓ Output file is valid JSON")
    except json.JSONDecodeError as e:
        print(f"✗ Output file has JSON errors: {e}")

if __name__ == "__main__":
    main()