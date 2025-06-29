import json
import re
from collections import defaultdict

def parse_malformed_json(file_path):
    """Parse the malformed JSON file and extract company records"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    companies = []
    
    # Split content by array boundaries and parse each array
    array_pattern = r'\[({[^}]*}(?:,\s*{[^}]*})*)\]'
    arrays = re.findall(array_pattern, content, re.DOTALL)
    
    for array_content in arrays:
        try:
            # Wrap in array brackets and parse
            json_string = '[' + array_content + ']'
            parsed_companies = json.loads(json_string)
            companies.extend(parsed_companies)
        except json.JSONDecodeError:
            # Try parsing individual objects
            object_pattern = r'{[^{}]*(?:{[^{}]*}[^{}]*)*}'
            objects = re.findall(object_pattern, array_content, re.DOTALL)
            
            for obj_str in objects:
                try:
                    company = json.loads(obj_str)
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
    
    for name, group in company_groups.items():
        if len(group) == 1:
            deduplicated.append(group[0])
        else:
            # Find the most complete record (most fields, longest descriptions)
            best_company = max(group, key=lambda c: (
                len([k for k, v in c.items() if v]),  # Number of non-empty fields
                len(str(c.get('about', ''))),         # Length of description
                len(c.get('roles', [])),              # Number of roles
                len(c.get('tech_stack', []))          # Number of tech stack items
            ))
            deduplicated.append(best_company)
            print(f"Deduplicated '{name}': kept 1 of {len(group)} records")
    
    print(f"After deduplication: {len(deduplicated)} companies")
    return deduplicated

def fix_data_quality(companies):
    """Fix data quality issues"""
    fixed_companies = []
    issues_fixed = 0
    
    for company in companies:
        fixed_company = company.copy()
        
        # Fix salary ranges
        if 'roles' in fixed_company:
            for role in fixed_company['roles']:
                if 'salary_range' in role:
                    salary_range = role['salary_range']
                    if isinstance(salary_range, list) and len(salary_range) == 2:
                        try:
                            min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                            if min_sal >= max_sal or min_sal < 0:
                                # Fix invalid range
                                if min_sal >= max_sal:
                                    role['salary_range'] = [min_sal, min_sal + 30000]
                                else:
                                    role['salary_range'] = [abs(min_sal), abs(max_sal)]
                                issues_fixed += 1
                        except (ValueError, TypeError):
                            # Set default range if unparseable
                            role['salary_range'] = [50000, 80000]
                            issues_fixed += 1
        
        # Ensure required fields exist
        required_fields = {
            'company_name': '',
            'about': '',
            'industry': '',
            'sub_industry': '',
            'company_stage': '',
            'size': '',
            'culture_tags': [],
            'tech_stack': [],
            'roles': []
        }
        
        for field, default in required_fields.items():
            if field not in fixed_company or not fixed_company[field]:
                if field not in fixed_company:
                    fixed_company[field] = default
                    issues_fixed += 1
        
        # Clean up string fields
        string_fields = ['company_name', 'about', 'industry', 'sub_industry', 'company_stage', 'size']
        for field in string_fields:
            if isinstance(fixed_company[field], str):
                fixed_company[field] = fixed_company[field].strip()
        
        fixed_companies.append(fixed_company)
    
    print(f"Fixed {issues_fixed} data quality issues")
    return fixed_companies

def main():
    input_file = '/Users/georgemccain/Desktop/untitled folder 2/data/enriched_companies.json'
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/cleaned_companies.json'
    
    print("Step 1: Parsing malformed JSON...")
    companies = parse_malformed_json(input_file)
    
    print("\nStep 2: Removing duplicates...")
    deduplicated = deduplicate_companies(companies)
    
    print("\nStep 3: Fixing data quality issues...")
    cleaned = fix_data_quality(deduplicated)
    
    print("\nStep 4: Writing cleaned data...")
    with open(output_file, 'w') as f:
        json.dump(cleaned, f, indent=2, ensure_ascii=False)
    
    print(f"\nCleaning complete!")
    print(f"Original: {len(companies)} companies")
    print(f"Cleaned: {len(cleaned)} companies") 
    print(f"Removed: {len(companies) - len(cleaned)} duplicates")
    print(f"Output saved to: {output_file}")
    
    # Validate the output
    try:
        with open(output_file, 'r') as f:
            json.load(f)
        print("✓ Output file is valid JSON")
    except json.JSONDecodeError as e:
        print(f"✗ Output file has JSON errors: {e}")

if __name__ == "__main__":
    main()