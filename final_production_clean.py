import json
import re
from difflib import SequenceMatcher

def load_companies():
    """Load the standardized companies file"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    with open(file_path, 'r') as f:
        companies = json.load(f)
    
    print(f"Loaded {len(companies)} companies for final cleaning")
    return companies

def merge_duplicate_companies(companies):
    """Merge confirmed duplicate companies"""
    print("\n=== MERGING DUPLICATE COMPANIES ===")
    
    duplicates_to_merge = [
        # (keep_index, remove_index, reason)
        ("Archer Daniels Midland (ADM)", "Archer Daniels Midland Company", "Same company - ADM has more roles"),
        ("AutoNation", "AutoNation, Inc.", "Same company - AutoNation has more roles"),
    ]
    
    companies_to_remove = []
    merges_completed = 0
    
    # Find and merge duplicates
    for keep_name, remove_name, reason in duplicates_to_merge:
        keep_company = None
        remove_company = None
        remove_index = None
        
        for i, company in enumerate(companies):
            name = company.get('company_name', '')
            if name == keep_name:
                keep_company = company
            elif name == remove_name:
                remove_company = company
                remove_index = i
        
        if keep_company and remove_company:
            print(f"Merging: '{remove_name}' -> '{keep_name}' ({reason})")
            
            # Merge roles if remove_company has unique ones
            existing_role_titles = {role.get('title', '').lower() for role in keep_company.get('roles', [])}
            
            for role in remove_company.get('roles', []):
                role_title = role.get('title', '').lower()
                if role_title not in existing_role_titles:
                    keep_company['roles'].append(role)
                    existing_role_titles.add(role_title)
            
            # Merge tech_stack
            existing_tech = set(keep_company.get('tech_stack', []))
            for tech in remove_company.get('tech_stack', []):
                if tech not in existing_tech:
                    keep_company['tech_stack'].append(tech)
                    existing_tech.add(tech)
            
            # Mark for removal
            companies_to_remove.append(remove_index)
            merges_completed += 1
        else:
            print(f"Could not find companies to merge: '{keep_name}' / '{remove_name}'")
    
    # Remove duplicates (in reverse order to maintain indices)
    for index in sorted(companies_to_remove, reverse=True):
        companies.pop(index)
    
    print(f"Completed {merges_completed} merges, removed {len(companies_to_remove)} duplicates")
    return companies

def expand_industry_classifications(companies):
    """Fix industry classification issues"""
    print("\n=== EXPANDING INDUSTRY CLASSIFICATIONS ===")
    
    industry_fixes = 0
    
    # Add missing valid industries
    valid_industries = {
        'agriculture', 'automotive', 'banking', 'finance', 'technology', 'healthcare',
        'energy', 'manufacturing', 'media', 'entertainment', 'real estate',
        'policy', 'international affairs', 'legal', 'retail', 'transportation',
        'biotechnology', 'pharmaceuticals', 'consulting', 'strategy', 'investment'
    }
    
    for company in companies:
        industry = company.get('industry', '').lower()
        
        # Fix specific misclassified industries
        if 'real estate' in industry.lower():
            if company.get('industry') != 'Real Estate':
                company['industry'] = 'Real Estate'
                industry_fixes += 1
        
        elif 'biotechnology' in industry.lower():
            if company.get('industry') != 'Biotechnology':
                company['industry'] = 'Biotechnology'
                industry_fixes += 1
    
    print(f"Fixed {industry_fixes} industry classifications")
    return companies

def fix_location_formatting(companies):
    """Fix malformed location entries"""
    print("\n=== FIXING LOCATION FORMATTING ===")
    
    location_fixes = 0
    
    # Common location fixes
    location_mappings = {
        'various locations in the usa': 'Multiple US Locations',
        'various locations in the us': 'Multiple US Locations', 
        'various locations in the us and uk': 'Multiple Locations (US & UK)',
        'various locations across the usa': 'Multiple US Locations',
        'multiple us locations': 'Multiple US Locations',
        'regional offices': 'Multiple Locations',
        'global': 'Multiple Locations',
        'worldwide': 'Multiple Locations'
    }
    
    for company in companies:
        for role in company.get('roles', []):
            location = role.get('location', '').strip()
            location_lower = location.lower()
            
            if location_lower in location_mappings:
                role['location'] = location_mappings[location_lower]
                location_fixes += 1
            
            # Fix capitalization issues
            elif location and ',' in location:
                parts = [part.strip().title() for part in location.split(',')]
                # Handle state abbreviations
                if len(parts) == 2 and len(parts[1]) == 2:
                    parts[1] = parts[1].upper()
                
                standardized = ', '.join(parts)
                if standardized != location:
                    role['location'] = standardized
                    location_fixes += 1
    
    print(f"Fixed {location_fixes} location formatting issues")
    return companies

def adjust_salary_ranges(companies):
    """Adjust unrealistic salary ranges"""
    print("\n=== ADJUSTING SALARY RANGES ===")
    
    salary_fixes = 0
    
    for company in companies:
        company_name = company.get('company_name', '')
        
        for role in company.get('roles', []):
            salary_range = role.get('salary_range', [])
            role_title = role.get('title', '').lower()
            
            if isinstance(salary_range, list) and len(salary_range) == 2:
                try:
                    min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                    original_range = [min_sal, max_sal]
                    fixed = False
                    
                    # Fix executive salaries that are too low
                    if any(keyword in role_title for keyword in ['director', 'vp', 'vice president', 'senior director']):
                        if max_sal < 100000:
                            min_sal = max(min_sal, 90000)
                            max_sal = max(max_sal, 150000)
                            fixed = True
                    
                    # Cap extremely high salaries (except for top executives)
                    if max_sal > 800000 and not any(keyword in role_title for keyword in ['ceo', 'cfo', 'cto', 'president']):
                        max_sal = min(max_sal, 500000)
                        min_sal = min(min_sal, 350000)
                        fixed = True
                    
                    # Ensure min < max
                    if min_sal >= max_sal:
                        max_sal = min_sal + 30000
                        fixed = True
                    
                    if fixed:
                        role['salary_range'] = [min_sal, max_sal]
                        salary_fixes += 1
                        print(f"  Fixed {company_name} - {role_title}: {original_range} -> {[min_sal, max_sal]}")
                
                except (ValueError, TypeError):
                    continue
    
    print(f"Adjusted {salary_fixes} salary ranges")
    return companies

def remove_obvious_similar_companies(companies):
    """Remove any remaining obvious duplicates we might have missed"""
    print("\n=== FINAL DUPLICATE CHECK ===")
    
    # Check for very high similarity companies
    companies_to_remove = []
    
    for i, company1 in enumerate(companies):
        if i in companies_to_remove:
            continue
            
        name1 = company1.get('company_name', '')
        
        for j, company2 in enumerate(companies[i+1:], i+1):
            if j in companies_to_remove:
                continue
                
            name2 = company2.get('company_name', '')
            
            # Very strict criteria for automatic removal
            similarity = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
            same_industry = company1.get('industry') == company2.get('industry')
            
            # Only remove if extremely similar and same industry
            if similarity > 0.95 and same_industry:
                # Keep the one with more roles
                roles1 = len(company1.get('roles', []))
                roles2 = len(company2.get('roles', []))
                
                if roles1 >= roles2:
                    companies_to_remove.append(j)
                    print(f"Removing very similar: '{name2}' (keeping '{name1}' - more complete)")
                else:
                    companies_to_remove.append(i)
                    print(f"Removing very similar: '{name1}' (keeping '{name2}' - more complete)")
                    break
    
    # Remove in reverse order
    for index in sorted(set(companies_to_remove), reverse=True):
        companies.pop(index)
    
    print(f"Removed {len(set(companies_to_remove))} additional similar companies")
    return companies

def validate_final_quality(companies):
    """Run final quality validation"""
    print("\n=== FINAL QUALITY VALIDATION ===")
    
    issues = []
    
    # Check for remaining duplicates
    names = [company.get('company_name', '') for company in companies]
    duplicate_names = [name for name in set(names) if names.count(name) > 1]
    
    if duplicate_names:
        issues.extend([f"Duplicate name: {name}" for name in duplicate_names])
    
    # Check critical data completeness
    for i, company in enumerate(companies):
        name = company.get('company_name', f'Company {i}')
        
        # Must have these fields
        if not company.get('company_name', '').strip():
            issues.append(f"Missing company name: Company {i}")
        
        if not company.get('industry', '').strip():
            issues.append(f"Missing industry: {name}")
        
        if not company.get('roles', []):
            issues.append(f"No roles: {name}")
        
        # Check roles
        for j, role in enumerate(company.get('roles', [])):
            if not role.get('title', '').strip():
                issues.append(f"Missing role title: {name} Role {j}")
            
            if not role.get('location', '').strip():
                issues.append(f"Missing location: {name} Role {j}")
    
    print(f"Final validation issues: {len(issues)}")
    if issues:
        print("Remaining issues:")
        for issue in issues[:10]:
            print(f"  - {issue}")
        if len(issues) > 10:
            print(f"  ... and {len(issues) - 10} more")
    
    # Calculate final quality score
    total_possible_issues = len(companies) * 3  # 3 critical checks per company
    quality_score = max(0, 100 - (len(issues) / total_possible_issues * 100))
    
    print(f"\nFINAL QUALITY SCORE: {quality_score:.1f}/100")
    
    return len(issues) == 0, quality_score

def main():
    """Run the complete final cleaning process"""
    print("🧹 FINAL PRODUCTION CLEANING PROCESS")
    print("=" * 50)
    
    # Load data
    companies = load_companies()
    original_count = len(companies)
    
    # Apply all fixes
    companies = merge_duplicate_companies(companies)
    companies = expand_industry_classifications(companies)
    companies = fix_location_formatting(companies)
    companies = adjust_salary_ranges(companies)
    companies = remove_obvious_similar_companies(companies)
    
    # Final validation
    is_clean, quality_score = validate_final_quality(companies)
    
    # Save final version
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/production_companies.json'
    
    with open(output_file, 'w') as f:
        json.dump(companies, f, indent=2, ensure_ascii=False)
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎉 FINAL CLEANING COMPLETE!")
    print("=" * 50)
    print(f"📊 Original companies: {original_count}")
    print(f"📊 Final companies: {len(companies)}")
    print(f"📊 Companies removed: {original_count - len(companies)}")
    print(f"📊 Quality score: {quality_score:.1f}/100")
    
    if quality_score >= 95:
        print("✅ PRODUCTION READY - Excellent quality!")
    elif quality_score >= 90:
        print("✅ PRODUCTION READY - Good quality")
    else:
        print("⚠️  Needs additional review")
    
    print(f"📁 Final file: {output_file}")
    
    # Validate JSON
    try:
        with open(output_file, 'r') as f:
            json.load(f)
        print("✅ Valid JSON structure")
    except json.JSONDecodeError as e:
        print(f"❌ JSON validation failed: {e}")
    
    return len(companies), quality_score

if __name__ == "__main__":
    main()