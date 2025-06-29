import json
import re
from collections import defaultdict
from difflib import SequenceMatcher

def load_companies(file_path):
    """Load companies from JSON file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def standardize_company_stage(stage):
    """Standardize company stage to consistent values"""
    if not stage or stage.strip() == '':
        return 'Unknown'
    
    stage_lower = stage.lower().strip()
    
    # Public companies (any mention of public, NYSE, NASDAQ, etc.)
    if any(keyword in stage_lower for keyword in ['public', 'nyse', 'nasdaq', 'listed', 'traded']):
        return 'Public'
    
    # Private companies
    if any(keyword in stage_lower for keyword in ['private', 'subsidiary', 'division', 'owned']):
        return 'Private'
    
    # Startups and early stage
    if any(keyword in stage_lower for keyword in ['startup', 'early', 'seed', 'series']):
        return 'Startup'
    
    # Non-profit organizations
    if any(keyword in stage_lower for keyword in ['non-profit', 'nonprofit', 'foundation', 'ngo']):
        return 'Non-Profit'
    
    # Government and agencies
    if any(keyword in stage_lower for keyword in ['government', 'agency', 'state-owned', 'crown']):
        return 'Government'
    
    # Established/Mature companies
    if any(keyword in stage_lower for keyword in ['established', 'mature']):
        return 'Established'
    
    # Growth stage
    if any(keyword in stage_lower for keyword in ['growth', 'growing']):
        return 'Growth'
    
    # Default based on common values
    common_mappings = {
        'public': 'Public',
        'private': 'Private',
        'startup': 'Startup',
        'mature': 'Established',
        'established': 'Established',
        'growth': 'Growth',
        'growing': 'Growth'
    }
    
    return common_mappings.get(stage_lower, 'Private')

def standardize_company_size(size):
    """Standardize company size to consistent ranges"""
    if not size or size.strip() == '':
        return 'Unknown'
    
    size_str = size.lower().strip()
    
    # Extract numbers from size string
    numbers = re.findall(r'[\d,]+', size_str)
    if numbers:
        # Convert to integers, handling commas
        nums = [int(n.replace(',', '')) for n in numbers]
        max_size = max(nums)
        
        # Categorize by size
        if max_size < 50:
            return 'Small (1-49)'
        elif max_size < 200:
            return 'Medium (50-199)'
        elif max_size < 1000:
            return 'Large (200-999)'
        elif max_size < 5000:
            return 'Very Large (1,000-4,999)'
        else:
            return 'Enterprise (5,000+)'
    
    # Handle text-based sizes
    if any(keyword in size_str for keyword in ['small', 'startup']):
        return 'Small (1-49)'
    elif any(keyword in size_str for keyword in ['medium']):
        return 'Medium (50-199)'
    elif any(keyword in size_str for keyword in ['large']) and 'very' not in size_str:
        return 'Large (200-999)'
    elif any(keyword in size_str for keyword in ['very large', 'enterprise']):
        return 'Enterprise (5,000+)'
    
    return 'Unknown'

def standardize_location(location):
    """Standardize location to consistent format"""
    if not location or location.strip() == '':
        return 'Remote/Not Specified'
    
    location = location.strip()
    
    # Handle common variations
    location_mappings = {
        'various locations': 'Multiple Locations',
        'various global locations': 'Multiple Locations',
        'multiple locations': 'Multiple Locations',
        'multiple global locations': 'Multiple Locations',
        'global': 'Multiple Locations',
        'worldwide': 'Multiple Locations',
        'remote': 'Remote',
        'work from home': 'Remote',
        'telecommute': 'Remote'
    }
    
    location_lower = location.lower()
    if location_lower in location_mappings:
        return location_mappings[location_lower]
    
    # Standardize US state abbreviations
    us_states = {
        'ca': 'CA', 'california': 'CA',
        'ny': 'NY', 'new york': 'NY',
        'tx': 'TX', 'texas': 'TX',
        'fl': 'FL', 'florida': 'FL',
        'wa': 'WA', 'washington': 'WA',
        'il': 'IL', 'illinois': 'IL',
        'ma': 'MA', 'massachusetts': 'MA',
        'pa': 'PA', 'pennsylvania': 'PA',
        'oh': 'OH', 'ohio': 'OH',
        'ga': 'GA', 'georgia': 'GA',
        'nc': 'NC', 'north carolina': 'NC',
        'va': 'VA', 'virginia': 'VA',
        'co': 'CO', 'colorado': 'CO',
        'az': 'AZ', 'arizona': 'AZ',
        'or': 'OR', 'oregon': 'OR',
        'ct': 'CT', 'connecticut': 'CT',
        'nj': 'NJ', 'new jersey': 'NJ',
        'md': 'MD', 'maryland': 'MD',
        'mn': 'MN', 'minnesota': 'MN',
        'wi': 'WI', 'wisconsin': 'WI',
        'mo': 'MO', 'missouri': 'MO',
        'tn': 'TN', 'tennessee': 'TN',
        'in': 'IN', 'indiana': 'IN',
        'mi': 'MI', 'michigan': 'MI',
        'al': 'AL', 'alabama': 'AL',
        'ar': 'AR', 'arkansas': 'AR'
    }
    
    # Format: City, State or City, Country
    parts = [part.strip() for part in location.split(',')]
    if len(parts) >= 2:
        city = parts[0].title()
        state_or_country = parts[1].strip().lower()
        
        # Check if it's a US state
        if state_or_country in us_states:
            return f"{city}, {us_states[state_or_country]}"
        elif len(state_or_country) == 2 and state_or_country.upper() in us_states.values():
            return f"{city}, {state_or_country.upper()}"
        else:
            # Capitalize country name
            country = state_or_country.title()
            # Handle common country variations
            country_mappings = {
                'Usa': 'USA',
                'United States': 'USA', 
                'Us': 'USA',
                'Uk': 'UK',
                'United Kingdom': 'UK'
            }
            country = country_mappings.get(country, country)
            return f"{city}, {country}"
    
    # Single location (country or city)
    return location.title()

def fix_salary_range(salary_range):
    """Fix and validate salary ranges"""
    if not salary_range or not isinstance(salary_range, list) or len(salary_range) != 2:
        return [50000, 80000]  # Default range
    
    try:
        min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
        
        # Fix invalid ranges
        if min_sal >= max_sal:
            max_sal = min_sal + 30000
        
        # Cap unrealistic salaries
        if max_sal > 500000:
            max_sal = 500000
            min_sal = max(min_sal, 300000)
        
        # Set minimum threshold
        if min_sal < 20000:
            min_sal = 30000
            if max_sal < min_sal:
                max_sal = min_sal + 30000
        
        return [min_sal, max_sal]
    
    except (ValueError, TypeError):
        return [50000, 80000]

def fix_missing_role_data(role, company_name, industry):
    """Fix missing role data with reasonable defaults"""
    # Fix missing description
    if not role.get('description', '').strip():
        title = role.get('title', 'Professional')
        role['description'] = f"Work as a {title} at {company_name}, contributing to {industry} industry operations and growth."
    
    # Fix missing location
    if not role.get('location', '').strip():
        role['location'] = 'Not Specified'
    
    # Fix missing required skills
    if not role.get('required_skills') or len(role.get('required_skills', [])) == 0:
        # Generate skills based on title and industry
        title_lower = role.get('title', '').lower()
        generic_skills = ['Communication', 'Problem Solving', 'Teamwork']
        
        if 'engineer' in title_lower:
            role['required_skills'] = ['Engineering', 'Technical Analysis', 'Project Management'] + generic_skills
        elif 'analyst' in title_lower:
            role['required_skills'] = ['Data Analysis', 'Research', 'Excel'] + generic_skills
        elif 'manager' in title_lower:
            role['required_skills'] = ['Leadership', 'Management', 'Strategic Planning'] + generic_skills
        elif 'developer' in title_lower:
            role['required_skills'] = ['Programming', 'Software Development', 'Debugging'] + generic_skills
        elif 'sales' in title_lower:
            role['required_skills'] = ['Sales', 'Customer Relations', 'Negotiation'] + generic_skills
        else:
            role['required_skills'] = ['Industry Knowledge'] + generic_skills
    
    # Ensure nice_to_have_skills exists
    if 'nice_to_have_skills' not in role:
        role['nice_to_have_skills'] = []
    
    # Ensure other required fields
    if 'visa_sponsorship' not in role:
        role['visa_sponsorship'] = True
    
    if 'min_experience_years' not in role:
        role['min_experience_years'] = 2
    
    return role

def resolve_potential_duplicates(companies):
    """Resolve potential duplicate companies"""
    resolved = []
    name_groups = defaultdict(list)
    
    # Group similar companies
    for company in companies:
        name = company['company_name'].lower().strip()
        # Find base name (remove common suffixes)
        base_name = re.sub(r'\s+(inc\.?|corp\.?|corporation|company|llc|ltd\.?|co\.?)$', '', name)
        name_groups[base_name].append(company)
    
    for base_name, group in name_groups.items():
        if len(group) == 1:
            resolved.append(group[0])
        else:
            # Check if they're actually the same company
            truly_same = []
            for company in group:
                # Check similarity
                is_duplicate = False
                for existing in truly_same:
                    similarity = SequenceMatcher(None, 
                                               company['company_name'].lower(), 
                                               existing['company_name'].lower()).ratio()
                    if similarity > 0.8:  # 80% similar
                        # Keep the one with more complete data
                        if len(str(company.get('about', ''))) > len(str(existing.get('about', ''))):
                            truly_same.remove(existing)
                            truly_same.append(company)
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    truly_same.append(company)
            
            resolved.extend(truly_same)
    
    return resolved

def standardize_companies(companies):
    """Apply all standardizations to companies"""
    standardized = []
    fixes_applied = {
        'stages_fixed': 0,
        'sizes_fixed': 0,
        'locations_fixed': 0,
        'salary_ranges_fixed': 0,
        'missing_data_fixed': 0,
        'culture_tags_added': 0
    }
    
    for company in companies:
        std_company = company.copy()
        
        # Standardize company stage
        original_stage = std_company.get('company_stage', '')
        std_company['company_stage'] = standardize_company_stage(original_stage)
        if original_stage != std_company['company_stage']:
            fixes_applied['stages_fixed'] += 1
        
        # Standardize company size
        original_size = std_company.get('size', '')
        std_company['size'] = standardize_company_size(original_size)
        if original_size != std_company['size']:
            fixes_applied['sizes_fixed'] += 1
        
        # Add culture tags if missing
        if not std_company.get('culture_tags') or len(std_company.get('culture_tags', [])) == 0:
            # Generate basic culture tags based on industry and size
            industry = std_company.get('industry', '').lower()
            stage = std_company.get('company_stage', '').lower()
            
            culture_tags = ['Professional']
            
            if 'technology' in industry:
                culture_tags.extend(['Innovative', 'Tech-Driven'])
            elif 'finance' in industry:
                culture_tags.extend(['Analytical', 'Results-Oriented'])
            elif 'healthcare' in industry:
                culture_tags.extend(['Caring', 'Impact-Driven'])
            else:
                culture_tags.extend(['Collaborative', 'Growth-Oriented'])
            
            if 'startup' in stage:
                culture_tags.append('Fast-Paced')
            elif 'public' in stage:
                culture_tags.append('Established')
            
            std_company['culture_tags'] = culture_tags
            fixes_applied['culture_tags_added'] += 1
        
        # Fix roles
        if 'roles' in std_company and isinstance(std_company['roles'], list):
            for role in std_company['roles']:
                # Standardize location
                original_location = role.get('location', '')
                role['location'] = standardize_location(original_location)
                if original_location != role['location']:
                    fixes_applied['locations_fixed'] += 1
                
                # Fix salary range
                original_salary = role.get('salary_range', [])
                role['salary_range'] = fix_salary_range(original_salary)
                if original_salary != role['salary_range']:
                    fixes_applied['salary_ranges_fixed'] += 1
                
                # Fix missing role data
                role_before = len([k for k, v in role.items() if v and v != []])
                role = fix_missing_role_data(role, std_company['company_name'], std_company.get('industry', ''))
                role_after = len([k for k, v in role.items() if v and v != []])
                if role_after > role_before:
                    fixes_applied['missing_data_fixed'] += 1
        
        standardized.append(std_company)
    
    return standardized, fixes_applied

def main():
    input_file = '/Users/georgemccain/Desktop/untitled folder 2/data/cleaned_companies.json'
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    print("=== COMPREHENSIVE DATA STANDARDIZATION ===")
    
    # Load companies
    print("Loading companies...")
    companies = load_companies(input_file)
    print(f"Loaded {len(companies)} companies")
    
    # Resolve potential duplicates
    print("\\nResolving potential duplicates...")
    companies = resolve_potential_duplicates(companies)
    print(f"After duplicate resolution: {len(companies)} companies")
    
    # Apply standardizations
    print("\\nApplying standardizations...")
    standardized, fixes = standardize_companies(companies)
    
    # Save results
    print("\\nSaving standardized data...")
    with open(output_file, 'w') as f:
        json.dump(standardized, f, indent=2, ensure_ascii=False)
    
    # Report results
    print("\\n=== STANDARDIZATION COMPLETE ===")
    print(f"Input companies: {len(companies)}")
    print(f"Output companies: {len(standardized)}")
    print(f"\\nFixes applied:")
    for fix_type, count in fixes.items():
        print(f"  {fix_type.replace('_', ' ').title()}: {count}")
    
    print(f"\\nOutput saved to: {output_file}")
    
    # Validate output
    try:
        with open(output_file, 'r') as f:
            json.load(f)
        print("✓ Output file is valid JSON")
    except json.JSONDecodeError as e:
        print(f"✗ Output file has JSON errors: {e}")
    
    # Show sample of standardized values
    print("\\n=== SAMPLE STANDARDIZED VALUES ===")
    stages = set(c['company_stage'] for c in standardized)
    sizes = set(c['size'] for c in standardized)
    print(f"Company stages: {sorted(stages)}")
    print(f"Company sizes: {sorted(sizes)}")
    
    # Sample locations from roles
    locations = set()
    for company in standardized[:20]:  # Sample from first 20 companies
        for role in company.get('roles', []):
            locations.add(role.get('location', ''))
    print(f"Sample locations: {sorted(list(locations))[:10]}")

if __name__ == "__main__":
    main()