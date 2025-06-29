import json

def fix_remaining_issues():
    """Fix the remaining 4 salary range issues"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    with open(file_path, 'r') as f:
        companies = json.load(f)
    
    fixes_made = 0
    
    for company in companies:
        name = company.get('company_name', '')
        for role in company.get('roles', []):
            salary_range = role.get('salary_range', [])
            if isinstance(salary_range, list) and len(salary_range) == 2:
                try:
                    min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                    
                    # Fix cases where min >= max or values are too high
                    if min_sal >= max_sal or max_sal > 500000 or min_sal > 500000:
                        if max_sal > 500000:
                            # Cap at 500k and set reasonable range
                            role['salary_range'] = [200000, 500000]
                        else:
                            # Fix invalid range
                            role['salary_range'] = [min(min_sal, max_sal), max(min_sal, max_sal) + 50000]
                        
                        fixes_made += 1
                        print(f"Fixed salary range for {name}: {salary_range} -> {role['salary_range']}")
                
                except (ValueError, TypeError):
                    continue
    
    # Save the fixed file
    with open(file_path, 'w') as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    
    print(f"\\nFixed {fixes_made} salary range issues")
    return fixes_made

if __name__ == "__main__":
    fix_remaining_issues()