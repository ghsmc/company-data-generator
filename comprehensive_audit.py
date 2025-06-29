import json
import re
import collections
from difflib import SequenceMatcher

def load_and_examine_file():
    """Load and examine the standardized companies file"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    try:
        with open(file_path, 'r') as f:
            companies = json.load(f)
        
        print("=== COMPREHENSIVE DATA AUDIT ===")
        print(f"✓ File loaded successfully: {len(companies)} companies")
        print(f"✓ Valid JSON structure")
        
        return companies
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"✗ Error loading file: {e}")
        return None

def check_duplicates_and_similar(companies):
    """Check for exact duplicates and potentially similar companies"""
    print("\n=== DUPLICATE AND SIMILARITY CHECK ===")
    
    issues = []
    
    # Check exact name duplicates
    name_counts = collections.Counter(company.get('company_name', '') for company in companies)
    exact_duplicates = {name: count for name, count in name_counts.items() if count > 1}
    
    print(f"Exact duplicate names: {len(exact_duplicates)}")
    if exact_duplicates:
        for name, count in exact_duplicates.items():
            issues.append(f"DUPLICATE: '{name}' appears {count} times")
            print(f"  ⚠️  '{name}': {count} occurrences")
    
    # Check for similar company names (potential duplicates)
    similar_pairs = []
    company_names = [(i, company.get('company_name', '')) for i, company in enumerate(companies)]
    
    for i, (idx1, name1) in enumerate(company_names):
        for idx2, name2 in company_names[i+1:]:
            if name1 and name2:
                # Calculate similarity
                similarity = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
                
                # Check for substring relationships or high similarity
                name1_clean = re.sub(r'\s+(inc\.?|corp\.?|corporation|company|llc|ltd\.?|co\.?)$', '', name1.lower().strip())
                name2_clean = re.sub(r'\s+(inc\.?|corp\.?|corporation|company|llc|ltd\.?|co\.?)$', '', name2.lower().strip())
                
                if (similarity > 0.85 or 
                    name1_clean in name2_clean or 
                    name2_clean in name1_clean or
                    abs(len(name1_clean) - len(name2_clean)) <= 3 and similarity > 0.75):
                    
                    similar_pairs.append((name1, name2, similarity))
                    issues.append(f"SIMILAR: '{name1}' <-> '{name2}' (similarity: {similarity:.2f})")
    
    print(f"Similar company names: {len(similar_pairs)}")
    for name1, name2, sim in similar_pairs[:10]:  # Show first 10
        print(f"  ⚠️  '{name1}' <-> '{name2}' ({sim:.2f})")
    
    if len(similar_pairs) > 10:
        print(f"  ... and {len(similar_pairs) - 10} more similar pairs")
    
    return issues

def verify_data_accuracy(companies):
    """Verify accuracy of company information, roles, and salaries"""
    print("\n=== DATA ACCURACY VERIFICATION ===")
    
    issues = []
    
    # Check company information accuracy
    for i, company in enumerate(companies):
        name = company.get('company_name', f'Company {i}')
        
        # Check company name validity
        if not name or len(name.strip()) < 2:
            issues.append(f"INVALID NAME: Company {i} has invalid name: '{name}'")
        
        # Check for placeholder or generic text
        about = company.get('about', '')
        if any(placeholder in about.lower() for placeholder in [
            'lorem ipsum', 'placeholder', 'todo', 'tbd', 'company description',
            'add description', 'insert description'
        ]):
            issues.append(f"PLACEHOLDER TEXT: '{name}' has placeholder text in description")
        
        # Check industry consistency
        industry = company.get('industry', '')
        sub_industry = company.get('sub_industry', '')
        
        # Validate industry classifications
        known_industries = {
            'agriculture', 'automotive', 'banking', 'finance', 'technology', 'healthcare',
            'energy', 'manufacturing', 'media', 'entertainment', 'real estate',
            'policy', 'international affairs', 'legal', 'retail', 'transportation'
        }
        
        industry_words = set(industry.lower().split())
        if industry and not any(known_word in industry_words for known_word in known_industries):
            issues.append(f"UNKNOWN INDUSTRY: '{name}' has unusual industry: '{industry}'")
        
        # Check roles accuracy
        roles = company.get('roles', [])
        if not roles:
            issues.append(f"NO ROLES: '{name}' has no job roles defined")
        
        for j, role in enumerate(roles):
            role_title = role.get('title', '')
            
            # Check for placeholder role titles
            if any(placeholder in role_title.lower() for placeholder in [
                'todo', 'tbd', 'placeholder', 'role title', 'job title'
            ]):
                issues.append(f"PLACEHOLDER ROLE: '{name}' Role {j} has placeholder title")
            
            # Check salary ranges for reasonableness
            salary_range = role.get('salary_range', [])
            if isinstance(salary_range, list) and len(salary_range) == 2:
                try:
                    min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                    
                    # Check for unrealistic salaries
                    if min_sal < 15000:
                        issues.append(f"LOW SALARY: '{name}' Role {j} has very low salary: ${min_sal:,}")
                    
                    if max_sal > 1000000:
                        issues.append(f"HIGH SALARY: '{name}' Role {j} has very high salary: ${max_sal:,}")
                    
                    # Check salary vs role title consistency
                    title_lower = role_title.lower()
                    if 'intern' in title_lower and min_sal > 100000:
                        issues.append(f"SALARY MISMATCH: '{name}' Intern role has high salary: ${min_sal:,}")
                    
                    if any(senior_word in title_lower for senior_word in ['ceo', 'cto', 'cfo', 'president', 'director']) and max_sal < 100000:
                        issues.append(f"SALARY MISMATCH: '{name}' Senior role has low salary: ${max_sal:,}")
                
                except (ValueError, TypeError):
                    issues.append(f"INVALID SALARY: '{name}' Role {j} has non-numeric salary range")
            
            # Check location reasonableness
            location = role.get('location', '')
            if location and location not in ['Remote', 'Remote/Not Specified', 'Multiple Locations']:
                # Basic location format check
                if ',' not in location and len(location.split()) > 3:
                    issues.append(f"INVALID LOCATION: '{name}' Role {j} has malformed location: '{location}'")
    
    print(f"Data accuracy issues found: {len(issues)}")
    return issues

def validate_industry_consistency(companies):
    """Validate industry classifications and check for consistency"""
    print("\n=== INDUSTRY CONSISTENCY VALIDATION ===")
    
    issues = []
    
    # Analyze industry distributions
    industries = collections.Counter(company.get('industry', '') for company in companies)
    sub_industries = collections.Counter(company.get('sub_industry', '') for company in companies)
    
    print(f"Industries found: {len(industries)}")
    print(f"Sub-industries found: {len(sub_industries)}")
    
    # Check for industry/sub-industry mismatches
    industry_mapping = collections.defaultdict(set)
    
    for company in companies:
        industry = company.get('industry', '')
        sub_industry = company.get('sub_industry', '')
        if industry and sub_industry:
            industry_mapping[industry].add(sub_industry)
    
    # Look for potential inconsistencies
    for company in companies:
        name = company.get('company_name', '')
        industry = company.get('industry', '')
        sub_industry = company.get('sub_industry', '')
        
        # Check if sub-industry makes sense for the industry
        if industry == 'Technology' and sub_industry == 'Farming':
            issues.append(f"INDUSTRY MISMATCH: '{name}' - Technology company with Farming sub-industry")
        
        if industry == 'Healthcare' and sub_industry == 'Software Development':
            issues.append(f"INDUSTRY MISMATCH: '{name}' - Healthcare company with Software Development sub-industry")
        
        # Check company stage vs industry consistency
        stage = company.get('company_stage', '')
        if stage == 'Non-Profit' and industry in ['Finance', 'Banking']:
            issues.append(f"STAGE MISMATCH: '{name}' - Non-profit in Finance/Banking industry")
    
    print(f"Industry consistency issues: {len(issues)}")
    return issues

def check_logical_inconsistencies(companies):
    """Check for logical inconsistencies in company data"""
    print("\n=== LOGICAL CONSISTENCY CHECK ===")
    
    issues = []
    
    for company in companies:
        name = company.get('company_name', '')
        stage = company.get('company_stage', '')
        size = company.get('size', '')
        roles = company.get('roles', [])
        
        # Check stage vs size consistency
        if stage == 'Startup' and 'Enterprise' in size:
            issues.append(f"SIZE MISMATCH: '{name}' - Startup with Enterprise size")
        
        if stage == 'Public' and 'Small' in size:
            issues.append(f"SIZE MISMATCH: '{name}' - Public company with Small size")
        
        # Check tech stack reasonableness
        tech_stack = company.get('tech_stack', [])
        industry = company.get('industry', '')
        
        if industry == 'Agriculture' and 'React' in tech_stack and len(tech_stack) > 5:
            issues.append(f"TECH MISMATCH: '{name}' - Agriculture company with extensive web tech stack")
        
        # Check role count vs company size
        role_count = len(roles)
        if 'Small' in size and role_count > 10:
            issues.append(f"ROLE COUNT MISMATCH: '{name}' - Small company with {role_count} roles")
        
        if 'Enterprise' in size and role_count < 2:
            issues.append(f"ROLE COUNT MISMATCH: '{name}' - Enterprise company with only {role_count} roles")
        
        # Check culture tags for generic/repeated content
        culture_tags = company.get('culture_tags', [])
        if len(culture_tags) > len(set(culture_tags)):
            issues.append(f"DUPLICATE TAGS: '{name}' has duplicate culture tags")
        
        if len(culture_tags) > 8:
            issues.append(f"TOO MANY TAGS: '{name}' has excessive culture tags ({len(culture_tags)})")
    
    print(f"Logical inconsistency issues: {len(issues)}")
    return issues

def generate_summary_report(all_issues):
    """Generate a comprehensive summary report"""
    print("\n" + "="*60)
    print("COMPREHENSIVE DATA AUDIT SUMMARY")
    print("="*60)
    
    if not all_issues:
        print("🎉 EXCELLENT! No issues found in the dataset.")
        print("✅ Data is accurate, consistent, and production-ready")
        return True
    
    # Categorize issues
    issue_categories = {
        'DUPLICATE': [],
        'SIMILAR': [],
        'PLACEHOLDER': [],
        'INVALID': [],
        'MISMATCH': [],
        'OTHER': []
    }
    
    for issue in all_issues:
        categorized = False
        for category in issue_categories:
            if issue.startswith(category):
                issue_categories[category].append(issue)
                categorized = True
                break
        if not categorized:
            issue_categories['OTHER'].append(issue)
    
    # Report by category
    total_issues = len(all_issues)
    print(f"📊 TOTAL ISSUES FOUND: {total_issues}")
    
    for category, issues in issue_categories.items():
        if issues:
            print(f"\n🔍 {category} ISSUES ({len(issues)}):")
            for issue in issues[:5]:  # Show first 5 of each type
                print(f"  • {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more {category.lower()} issues")
    
    # Priority recommendations
    print(f"\n🎯 PRIORITY RECOMMENDATIONS:")
    
    high_priority = len(issue_categories['DUPLICATE']) + len(issue_categories['INVALID'])
    medium_priority = len(issue_categories['SIMILAR']) + len(issue_categories['MISMATCH'])
    low_priority = len(issue_categories['PLACEHOLDER']) + len(issue_categories['OTHER'])
    
    if high_priority > 0:
        print(f"  🔴 HIGH: Fix {high_priority} critical issues (duplicates, invalid data)")
    if medium_priority > 0:
        print(f"  🟡 MEDIUM: Review {medium_priority} consistency issues")
    if low_priority > 0:
        print(f"  🟢 LOW: Clean up {low_priority} minor issues")
    
    # Overall assessment  
    data_quality_score = max(0, 100 - (total_issues / 323 * 100))  # Use known company count
    print(f"\n📈 DATA QUALITY SCORE: {data_quality_score:.1f}/100")
    
    if data_quality_score >= 95:
        print("✅ EXCELLENT - Dataset is production-ready")
    elif data_quality_score >= 85:
        print("✅ GOOD - Minor cleanup recommended")
    elif data_quality_score >= 70:
        print("⚠️  FAIR - Moderate cleanup needed")
    else:
        print("❌ POOR - Significant cleanup required")
    
    return data_quality_score >= 85

def main():
    # Load and examine
    companies = load_and_examine_file()
    if not companies:
        return
    
    # Run all checks
    all_issues = []
    
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE AUDIT...")
    print("="*60)
    
    # Check 1: Duplicates and similar names
    duplicate_issues = check_duplicates_and_similar(companies)
    all_issues.extend(duplicate_issues)
    
    # Check 2: Data accuracy
    accuracy_issues = verify_data_accuracy(companies)
    all_issues.extend(accuracy_issues)
    
    # Check 3: Industry consistency
    industry_issues = validate_industry_consistency(companies)
    all_issues.extend(industry_issues)
    
    # Check 4: Logical consistency
    logic_issues = check_logical_inconsistencies(companies)
    all_issues.extend(logic_issues)
    
    # Generate final report
    is_production_ready = generate_summary_report(all_issues)
    
    return is_production_ready

if __name__ == "__main__":
    main()