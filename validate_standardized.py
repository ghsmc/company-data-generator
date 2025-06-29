import json
import collections

def validate_standardized_companies():
    """Validate the standardized companies file"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    try:
        with open(file_path, 'r') as f:
            companies = json.load(f)
        
        print("=== STANDARDIZED COMPANIES VALIDATION ===")
        print(f"✓ File loaded successfully")
        print(f"✓ Valid JSON structure")
        print(f"✓ Total companies: {len(companies)}")
        
        # Check company stages
        stages = collections.Counter(company.get('company_stage', '') for company in companies)
        print(f"\\nCompany stages ({len(stages)}):")
        for stage, count in stages.most_common():
            print(f"  {stage}: {count}")
        
        # Check company sizes
        sizes = collections.Counter(company.get('size', '') for company in companies)
        print(f"\\nCompany sizes ({len(sizes)}):")
        for size, count in sizes.most_common():
            print(f"  {size}: {count}")
        
        # Check locations from roles
        all_locations = []
        for company in companies:
            for role in company.get('roles', []):
                location = role.get('location', '')
                if location:
                    all_locations.append(location)
        
        location_counts = collections.Counter(all_locations)
        print(f"\\nTop 15 role locations:")
        for location, count in location_counts.most_common(15):
            print(f"  {location}: {count}")
        
        # Check for issues
        issues = []
        
        # Validate standardized values
        valid_stages = ['Public', 'Private', 'Startup', 'Non-Profit', 'Government', 'Established', 'Growth']
        valid_sizes = ['Small (1-49)', 'Medium (50-199)', 'Large (200-999)', 'Very Large (1,000-4,999)', 'Enterprise (5,000+)', 'Unknown']
        
        for i, company in enumerate(companies):
            name = company.get('company_name', f'Company {i}')
            
            # Check stage
            stage = company.get('company_stage', '')
            if stage not in valid_stages:
                issues.append(f"'{name}': Invalid company stage '{stage}'")
            
            # Check size
            size = company.get('size', '')
            if size not in valid_sizes:
                issues.append(f"'{name}': Invalid company size '{size}'")
            
            # Check roles
            for j, role in enumerate(company.get('roles', [])):
                # Check salary range
                salary_range = role.get('salary_range', [])
                if isinstance(salary_range, list) and len(salary_range) == 2:
                    try:
                        min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                        if min_sal >= max_sal:
                            issues.append(f"'{name}', Role {j}: Invalid salary range: {salary_range}")
                        if max_sal > 500000:
                            issues.append(f"'{name}', Role {j}: Salary too high: {max_sal}")
                    except (ValueError, TypeError):
                        issues.append(f"'{name}', Role {j}: Non-numeric salary range")
                
                # Check required data
                if not role.get('description', '').strip():
                    issues.append(f"'{name}', Role {j}: Missing description")
                if not role.get('location', '').strip():
                    issues.append(f"'{name}', Role {j}: Missing location")
                if not role.get('required_skills') or len(role.get('required_skills', [])) == 0:
                    issues.append(f"'{name}', Role {j}: No required skills")
        
        print(f"\\n=== VALIDATION RESULTS ===")
        print(f"Data quality issues found: {len(issues)}")
        
        if issues:
            print(f"\\nFirst 10 issues:")
            for issue in issues[:10]:
                print(f"  - {issue}")
            if len(issues) > 10:
                print(f"  ... and {len(issues) - 10} more")
        
        # Summary
        standardized_stages = all(stage in valid_stages for stage in stages.keys())
        standardized_sizes = all(size in valid_sizes for size in sizes.keys())
        
        print(f"\\n=== SUMMARY ===")
        print(f"✓ File is valid JSON with {len(companies)} companies")
        print(f"{'✓' if standardized_stages else '✗'} Company stages standardized")
        print(f"{'✓' if standardized_sizes else '✗'} Company sizes standardized")
        print(f"{'✓' if len(issues) == 0 else '✗'} {len(issues)} data quality issues remaining")
        
        if len(issues) == 0 and standardized_stages and standardized_sizes:
            print("\\n🎉 File is fully standardized and ready for production!")
        else:
            print(f"\\n⚠️  File needs minor cleanup: {len(issues)} issues to address")
        
        return len(issues) == 0
        
    except FileNotFoundError:
        print("✗ Standardized file not found")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ JSON decode error: {e}")
        return False

if __name__ == "__main__":
    validate_standardized_companies()