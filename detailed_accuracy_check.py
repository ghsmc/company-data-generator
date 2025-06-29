import json
import re

def detailed_accuracy_check():
    """Get detailed breakdown of accuracy issues"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    with open(file_path, 'r') as f:
        companies = json.load(f)
    
    print("=== DETAILED ACCURACY ISSUES BREAKDOWN ===")
    
    accuracy_issues = []
    
    for i, company in enumerate(companies):
        name = company.get('company_name', f'Company {i}')
        
        # Check for placeholder or generic text
        about = company.get('about', '')
        if any(placeholder in about.lower() for placeholder in [
            'lorem ipsum', 'placeholder', 'todo', 'tbd', 'company description',
            'add description', 'insert description'
        ]):
            accuracy_issues.append(f"PLACEHOLDER TEXT: '{name}' has placeholder text in description")
        
        # Check industry validity
        industry = company.get('industry', '')
        
        # List of all industries that should be recognized
        known_industries = {
            'agriculture', 'automotive', 'banking', 'finance', 'technology', 'healthcare',
            'energy', 'manufacturing', 'media', 'entertainment', 'real estate',
            'policy', 'international affairs', 'legal', 'retail', 'transportation',
            'biotechnology', 'pharmaceuticals', 'consulting', 'strategy', 'investment'
        }
        
        industry_words = set(industry.lower().split())
        if industry and not any(known_word in industry_words for known_word in known_industries):
            accuracy_issues.append(f"UNKNOWN INDUSTRY: '{name}' - '{industry}'")
        
        # Check roles
        roles = company.get('roles', [])
        if not roles:
            accuracy_issues.append(f"NO ROLES: '{name}' has no job roles defined")
        
        for j, role in enumerate(roles):
            role_title = role.get('title', '')
            
            # Check for placeholder role titles
            if any(placeholder in role_title.lower() for placeholder in [
                'todo', 'tbd', 'placeholder', 'role title', 'job title'
            ]):
                accuracy_issues.append(f"PLACEHOLDER ROLE: '{name}' Role {j} has placeholder title")
            
            # Check salary ranges for reasonableness
            salary_range = role.get('salary_range', [])
            if isinstance(salary_range, list) and len(salary_range) == 2:
                try:
                    min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                    
                    # Check for unrealistic salaries
                    if min_sal < 15000:
                        accuracy_issues.append(f"LOW SALARY: '{name}' Role {j} - ${min_sal:,}")
                    
                    if max_sal > 1000000:
                        accuracy_issues.append(f"HIGH SALARY: '{name}' Role {j} - ${max_sal:,}")
                    
                    # Check salary vs role title consistency
                    title_lower = role_title.lower()
                    if 'intern' in title_lower and min_sal > 100000:
                        accuracy_issues.append(f"SALARY MISMATCH: '{name}' Intern role - ${min_sal:,}")
                    
                    if any(senior_word in title_lower for senior_word in ['ceo', 'cto', 'cfo', 'president', 'director']) and max_sal < 100000:
                        accuracy_issues.append(f"SALARY MISMATCH: '{name}' Senior role - ${max_sal:,}")
                
                except (ValueError, TypeError):
                    accuracy_issues.append(f"INVALID SALARY: '{name}' Role {j} has non-numeric salary range")
            
            # Check location format
            location = role.get('location', '')
            if location and location not in ['Remote', 'Remote/Not Specified', 'Multiple Locations']:
                # Check for malformed locations
                if ',' not in location and len(location.split()) > 3:
                    accuracy_issues.append(f"INVALID LOCATION: '{name}' Role {j} - '{location}'")
    
    # Print detailed breakdown
    categories = {
        'PLACEHOLDER': [],
        'UNKNOWN INDUSTRY': [],
        'NO ROLES': [],
        'SALARY': [],
        'LOCATION': [],
        'OTHER': []
    }
    
    for issue in accuracy_issues:
        categorized = False
        for category in categories:
            if category in issue:
                categories[category].append(issue)
                categorized = True
                break
        if not categorized:
            categories['OTHER'].append(issue)
    
    print(f"Total accuracy issues: {len(accuracy_issues)}")
    print()
    
    for category, issues in categories.items():
        if issues:
            print(f"{category} ISSUES ({len(issues)}):")
            for issue in issues[:5]:
                print(f"  • {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
            print()
    
    # Check specific company examples
    print("=== SAMPLE COMPANY DATA VERIFICATION ===")
    
    # Check a few well-known companies for accuracy
    sample_companies = ['Goldman Sachs', 'Tesla, Inc.', 'Microsoft Corporation', 'Apple Inc.']
    
    for target_name in sample_companies:
        found_company = None
        for company in companies:
            if target_name.lower() in company.get('company_name', '').lower():
                found_company = company
                break
        
        if found_company:
            name = found_company['company_name']
            industry = found_company.get('industry', '')
            stage = found_company.get('company_stage', '')
            size = found_company.get('size', '')
            
            print(f"✓ {name}:")
            print(f"  Industry: {industry}")
            print(f"  Stage: {stage}")
            print(f"  Size: {size}")
            print(f"  Roles: {len(found_company.get('roles', []))}")
        else:
            print(f"✗ {target_name} not found in dataset")
    
    return accuracy_issues

if __name__ == "__main__":
    detailed_accuracy_check()