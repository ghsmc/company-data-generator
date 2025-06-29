import json
import re
import collections
from difflib import SequenceMatcher

def load_production_file():
    """Load and examine the production companies file"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/production_companies.json'
    
    try:
        with open(file_path, 'r') as f:
            companies = json.load(f)
        
        print("=== PRODUCTION FILE AUDIT ===")
        print(f"✓ File loaded successfully: {len(companies)} companies")
        print(f"✓ Valid JSON structure")
        
        # Quick structural check
        sample_company = companies[0] if companies else {}
        fields = list(sample_company.keys())
        print(f"✓ Company fields: {', '.join(fields)}")
        
        return companies
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"✗ Error loading production file: {e}")
        return None

def check_remaining_duplicates(companies):
    """Check for any remaining duplicates or highly similar companies"""
    print("\n=== DUPLICATE DETECTION ===")
    
    issues = []
    
    # Check exact name duplicates
    name_counts = collections.Counter(company.get('company_name', '') for company in companies)
    exact_duplicates = {name: count for name, count in name_counts.items() if count > 1}
    
    if exact_duplicates:
        for name, count in exact_duplicates.items():
            issues.append(f"EXACT DUPLICATE: '{name}' appears {count} times")
    
    print(f"Exact duplicates: {len(exact_duplicates)}")
    
    # Check for high-similarity companies that might be the same
    high_similarity_pairs = []
    
    for i, company1 in enumerate(companies):
        name1 = company1.get('company_name', '')
        
        for j, company2 in enumerate(companies[i+1:], i+1):
            name2 = company2.get('company_name', '')
            
            if name1 and name2:
                # Calculate similarity
                similarity = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
                
                # Flag potential issues
                if similarity > 0.8:
                    # Additional checks
                    same_industry = company1.get('industry', '') == company2.get('industry', '')
                    same_stage = company1.get('company_stage', '') == company2.get('company_stage', '')
                    
                    # Check if descriptions are similar
                    about1 = company1.get('about', '').lower()
                    about2 = company2.get('about', '').lower()
                    desc_similarity = SequenceMatcher(None, about1, about2).ratio()
                    
                    confidence_score = similarity
                    if same_industry:
                        confidence_score += 0.1
                    if same_stage:
                        confidence_score += 0.05
                    if desc_similarity > 0.7:
                        confidence_score += 0.15
                    
                    if confidence_score > 0.85:
                        high_similarity_pairs.append({
                            'name1': name1,
                            'name2': name2,
                            'similarity': similarity,
                            'confidence': confidence_score,
                            'same_industry': same_industry,
                            'desc_similarity': desc_similarity
                        })
                        issues.append(f"HIGH SIMILARITY: '{name1}' <-> '{name2}' (confidence: {confidence_score:.2f})")
    
    print(f"High-similarity pairs: {len(high_similarity_pairs)}")
    
    # Show the most concerning similarities
    if high_similarity_pairs:
        print("Most concerning similarities:")
        for pair in sorted(high_similarity_pairs, key=lambda x: x['confidence'], reverse=True)[:5]:
            print(f"  • '{pair['name1']}' <-> '{pair['name2']}' (conf: {pair['confidence']:.2f})")
    
    return issues

def verify_data_accuracy(companies):
    """Verify data accuracy and information quality"""
    print("\n=== DATA ACCURACY VERIFICATION ===")
    
    issues = []
    
    # Known company validation - check if well-known companies have accurate basic info
    known_companies = {
        'tesla': {'industries': ['automotive', 'electric'], 'stage': 'public'},
        'goldman sachs': {'industries': ['finance', 'banking'], 'stage': 'public'},
        'microsoft': {'industries': ['technology', 'software'], 'stage': 'public'},
        'apple': {'industries': ['technology'], 'stage': 'public'},
        'google': {'industries': ['technology'], 'stage': 'public'},
        'amazon': {'industries': ['technology', 'retail'], 'stage': 'public'},
        'mckinsey': {'industries': ['consulting'], 'stage': 'private'},
        'blackrock': {'industries': ['finance', 'investment'], 'stage': 'public'}
    }
    
    for company in companies:
        name = company.get('company_name', '').lower()
        industry = company.get('industry', '').lower()
        stage = company.get('company_stage', '').lower()
        
        # Check known companies
        for known_name, expected in known_companies.items():
            if known_name in name:
                # Check industry
                if not any(exp_ind in industry for exp_ind in expected['industries']):
                    issues.append(f"INDUSTRY MISMATCH: '{company.get('company_name')}' - Expected {expected['industries']}, got '{industry}'")
                
                # Check stage
                if expected['stage'] not in stage:
                    issues.append(f"STAGE MISMATCH: '{company.get('company_name')}' - Expected '{expected['stage']}', got '{stage}'")
    
    # Check for obviously fake or placeholder data
    for i, company in enumerate(companies):
        name = company.get('company_name', '')
        about = company.get('about', '').lower()
        
        # Check for placeholder text
        placeholder_indicators = [
            'lorem ipsum', 'placeholder', 'sample company', 'test company',
            'example corp', 'dummy', 'fake company', '[company name]'
        ]
        
        if any(indicator in about for indicator in placeholder_indicators):
            issues.append(f"PLACEHOLDER DATA: '{name}' contains placeholder text")
        
        # Check for unrealistic company descriptions
        if len(about.strip()) < 10:
            issues.append(f"INSUFFICIENT DESCRIPTION: '{name}' has very short description")
        
        # Check for duplicate descriptions (might indicate copy-paste errors)
        for j, other_company in enumerate(companies[i+1:], i+1):
            other_about = other_company.get('about', '').lower()
            if about and len(about) > 50 and about == other_about:
                issues.append(f"DUPLICATE DESCRIPTION: '{name}' and '{other_company.get('company_name')}' have identical descriptions")
    
    print(f"Data accuracy issues: {len(issues)}")
    return issues

def validate_business_logic(companies):
    """Validate business logic and consistency"""
    print("\n=== BUSINESS LOGIC VALIDATION ===")
    
    issues = []
    
    for company in companies:
        name = company.get('company_name', '')
        industry = company.get('industry', '')
        stage = company.get('company_stage', '')
        size = company.get('size', '')
        roles = company.get('roles', [])
        
        # Company stage vs size consistency
        if stage == 'Startup' and 'Enterprise' in size:
            issues.append(f"LOGIC ERROR: '{name}' - Startup with Enterprise size")
        
        if stage == 'Public' and 'Small' in size:
            issues.append(f"LOGIC WARNING: '{name}' - Public company with Small size (unusual)")
        
        # Industry vs roles consistency
        if industry == 'Technology':
            tech_roles = sum(1 for role in roles if any(tech_word in role.get('title', '').lower() 
                                                       for tech_word in ['engineer', 'developer', 'programmer', 'architect']))
            if len(roles) > 2 and tech_roles == 0:
                issues.append(f"INDUSTRY MISMATCH: '{name}' - Technology company with no tech roles")
        
        # Role count vs company size consistency
        role_count = len(roles)
        if 'Small' in size and role_count > 8:
            issues.append(f"ROLE COUNT WARNING: '{name}' - Small company with {role_count} roles (many)")
        
        if 'Enterprise' in size and role_count < 2:
            issues.append(f"ROLE COUNT WARNING: '{name}' - Enterprise company with only {role_count} roles (few)")
        
        # Salary validation
        for j, role in enumerate(roles):
            title = role.get('title', '').lower()
            salary_range = role.get('salary_range', [])
            
            if isinstance(salary_range, list) and len(salary_range) == 2:
                try:
                    min_sal, max_sal = int(salary_range[0]), int(salary_range[1])
                    
                    # Check intern salaries
                    if 'intern' in title and min_sal > 80000:
                        issues.append(f"SALARY ERROR: '{name}' - Intern with high salary: ${min_sal:,}")
                    
                    # Check executive salaries
                    if any(exec_word in title for exec_word in ['ceo', 'president', 'chief']) and max_sal < 150000:
                        issues.append(f"SALARY WARNING: '{name}' - Executive with low salary: ${max_sal:,}")
                    
                    # Check entry level vs senior discrepancies
                    if 'senior' in title and max_sal < 70000:
                        issues.append(f"SALARY WARNING: '{name}' - Senior role with low salary: ${max_sal:,}")
                    
                    if 'entry' in title and min_sal > 100000:
                        issues.append(f"SALARY WARNING: '{name}' - Entry role with high salary: ${min_sal:,}")
                
                except (ValueError, TypeError):
                    issues.append(f"SALARY ERROR: '{name}' Role {j} - Invalid salary format")
    
    print(f"Business logic issues: {len(issues)}")
    return issues

def check_data_integrity(companies):
    """Check for data corruption or formatting issues"""
    print("\n=== DATA INTEGRITY CHECK ===")
    
    issues = []
    
    for i, company in enumerate(companies):
        name = company.get('company_name', f'Company {i}')
        
        # Required fields check
        required_fields = ['company_name', 'about', 'industry', 'company_stage', 'size']
        for field in required_fields:
            if field not in company or not str(company[field]).strip():
                issues.append(f"MISSING FIELD: '{name}' missing '{field}'")
        
        # Data type validation
        if 'culture_tags' in company and not isinstance(company['culture_tags'], list):
            issues.append(f"TYPE ERROR: '{name}' culture_tags should be list")
        
        if 'tech_stack' in company and not isinstance(company['tech_stack'], list):
            issues.append(f"TYPE ERROR: '{name}' tech_stack should be list")
        
        if 'roles' in company and not isinstance(company['roles'], list):
            issues.append(f"TYPE ERROR: '{name}' roles should be list")
        
        # Role validation
        for j, role in enumerate(company.get('roles', [])):
            if not isinstance(role, dict):
                issues.append(f"TYPE ERROR: '{name}' Role {j} should be dictionary")
                continue
            
            # Required role fields
            role_required = ['title', 'description', 'required_skills', 'location', 'salary_range']
            for field in role_required:
                if field not in role:
                    issues.append(f"MISSING ROLE FIELD: '{name}' Role {j} missing '{field}'")
            
            # Validate salary range format
            salary_range = role.get('salary_range', [])
            if not isinstance(salary_range, list) or len(salary_range) != 2:
                issues.append(f"SALARY FORMAT: '{name}' Role {j} invalid salary_range format")
            
            # Validate required_skills
            skills = role.get('required_skills', [])
            if not isinstance(skills, list):
                issues.append(f"SKILLS FORMAT: '{name}' Role {j} required_skills should be list")
    
    print(f"Data integrity issues: {len(issues)}")
    return issues

def generate_final_assessment(all_issues, companies):
    """Generate comprehensive final quality assessment"""
    print("\n" + "="*60)
    print("FINAL PRODUCTION QUALITY ASSESSMENT")
    print("="*60)
    
    # Categorize issues by severity
    critical_issues = [issue for issue in all_issues if any(keyword in issue for keyword in 
                      ['EXACT DUPLICATE', 'MISSING FIELD', 'TYPE ERROR', 'SALARY ERROR'])]
    
    warning_issues = [issue for issue in all_issues if any(keyword in issue for keyword in 
                     ['WARNING', 'MISMATCH', 'HIGH SIMILARITY'])]
    
    info_issues = [issue for issue in all_issues if issue not in critical_issues and issue not in warning_issues]
    
    total_issues = len(all_issues)
    
    print(f"📊 ISSUE SUMMARY:")
    print(f"  🔴 Critical: {len(critical_issues)}")
    print(f"  🟡 Warnings: {len(warning_issues)}")
    print(f"  ℹ️  Info: {len(info_issues)}")
    print(f"  📋 Total: {total_issues}")
    
    # Show most critical issues
    if critical_issues:
        print(f"\n🔴 CRITICAL ISSUES (TOP 10):")
        for issue in critical_issues[:10]:
            print(f"  • {issue}")
        if len(critical_issues) > 10:
            print(f"  ... and {len(critical_issues) - 10} more critical issues")
    
    # Calculate quality metrics
    total_data_points = len(companies) * 10  # Approximate data points per company
    quality_score = max(0, 100 - (total_issues / total_data_points * 100))
    
    # Adjust score based on issue severity
    severity_penalty = len(critical_issues) * 2 + len(warning_issues) * 0.5
    final_score = max(0, quality_score - severity_penalty)
    
    print(f"\n📈 QUALITY METRICS:")
    print(f"  Base Quality Score: {quality_score:.1f}/100")
    print(f"  Severity Penalty: -{severity_penalty:.1f}")
    print(f"  Final Quality Score: {final_score:.1f}/100")
    
    # Production readiness assessment
    print(f"\n🎯 PRODUCTION READINESS:")
    
    if final_score >= 98 and len(critical_issues) == 0:
        print("✅ EXCELLENT - Production ready with highest quality")
        status = "PRODUCTION_READY"
    elif final_score >= 95 and len(critical_issues) <= 2:
        print("✅ VERY GOOD - Production ready with minor issues")
        status = "PRODUCTION_READY"
    elif final_score >= 90 and len(critical_issues) <= 5:
        print("⚠️  GOOD - Production ready but needs monitoring")
        status = "PRODUCTION_READY_WITH_MONITORING"
    elif final_score >= 80:
        print("⚠️  FAIR - Needs cleanup before production")
        status = "NEEDS_CLEANUP"
    else:
        print("❌ POOR - Significant issues, not production ready")
        status = "NOT_READY"
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    if len(critical_issues) > 0:
        print(f"  1. Address {len(critical_issues)} critical issues immediately")
    if len(warning_issues) > 10:
        print(f"  2. Review {len(warning_issues)} warnings for data quality")
    if final_score < 95:
        print(f"  3. Consider additional data validation and cleanup")
    
    # Data overview
    print(f"\n📊 DATA OVERVIEW:")
    print(f"  Companies: {len(companies)}")
    print(f"  Total Roles: {sum(len(c.get('roles', [])) for c in companies)}")
    print(f"  Industries: {len(set(c.get('industry', '') for c in companies))}")
    print(f"  Avg Roles/Company: {sum(len(c.get('roles', [])) for c in companies) / len(companies):.1f}")
    
    return status, final_score, len(critical_issues)

def main():
    """Run comprehensive production file audit"""
    
    # Load and examine
    companies = load_production_file()
    if not companies:
        return False
    
    print("\n" + "="*60)
    print("RUNNING COMPREHENSIVE PRODUCTION AUDIT")
    print("="*60)
    
    # Run all checks
    all_issues = []
    
    # Check 1: Duplicates
    duplicate_issues = check_remaining_duplicates(companies)
    all_issues.extend(duplicate_issues)
    
    # Check 2: Data accuracy
    accuracy_issues = verify_data_accuracy(companies)
    all_issues.extend(accuracy_issues)
    
    # Check 3: Business logic
    logic_issues = validate_business_logic(companies)
    all_issues.extend(logic_issues)
    
    # Check 4: Data integrity
    integrity_issues = check_data_integrity(companies)
    all_issues.extend(integrity_issues)
    
    # Generate final assessment
    status, score, critical_count = generate_final_assessment(all_issues, companies)
    
    return status == "PRODUCTION_READY" or status == "PRODUCTION_READY_WITH_MONITORING"

if __name__ == "__main__":
    is_ready = main()
    exit(0 if is_ready else 1)