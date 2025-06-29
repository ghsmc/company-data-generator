import json
from difflib import SequenceMatcher

def analyze_potential_duplicates():
    """Analyze the most concerning potential duplicate companies"""
    file_path = '/Users/georgemccain/Desktop/untitled folder 2/data/standardized_companies.json'
    
    with open(file_path, 'r') as f:
        companies = json.load(f)
    
    print("=== POTENTIAL DUPLICATE COMPANIES ANALYSIS ===")
    
    # Find high-confidence potential duplicates
    high_confidence_duplicates = []
    company_names = [(i, company.get('company_name', '')) for i, company in enumerate(companies)]
    
    for i, (idx1, name1) in enumerate(company_names):
        for idx2, name2 in company_names[i+1:]:
            if name1 and name2:
                similarity = SequenceMatcher(None, name1.lower(), name2.lower()).ratio()
                
                # High confidence duplicate criteria
                if similarity > 0.8 or (similarity > 0.6 and abs(len(name1) - len(name2)) <= 10):
                    company1 = companies[idx1]
                    company2 = companies[idx2]
                    
                    # Additional checks for same company
                    same_industry = company1.get('industry') == company2.get('industry')
                    same_about = SequenceMatcher(None, 
                                               company1.get('about', '').lower(),
                                               company2.get('about', '').lower()).ratio() > 0.7
                    
                    high_confidence_duplicates.append({
                        'name1': name1,
                        'name2': name2,
                        'similarity': similarity,
                        'same_industry': same_industry,
                        'same_about': same_about,
                        'company1': company1,
                        'company2': company2
                    })
    
    print(f"High-confidence potential duplicates: {len(high_confidence_duplicates)}")
    print()
    
    # Analyze each potential duplicate
    for dup in high_confidence_duplicates:
        print(f"🔍 POTENTIAL DUPLICATE:")
        print(f"  '{dup['name1']}' <-> '{dup['name2']}'")
        print(f"  Name similarity: {dup['similarity']:.2f}")
        print(f"  Same industry: {dup['same_industry']}")
        print(f"  Similar description: {dup['same_about']}")
        
        # Compare key details
        c1, c2 = dup['company1'], dup['company2']
        print(f"  Company 1: {c1.get('industry', 'N/A')} | {c1.get('company_stage', 'N/A')} | {len(c1.get('roles', []))} roles")
        print(f"  Company 2: {c2.get('industry', 'N/A')} | {c2.get('company_stage', 'N/A')} | {len(c2.get('roles', []))} roles")
        
        # Recommendation
        if dup['similarity'] > 0.9 and dup['same_industry']:
            print(f"  🚨 LIKELY DUPLICATE - Strong recommendation to merge")
        elif dup['similarity'] > 0.8 and (dup['same_industry'] or dup['same_about']):
            print(f"  ⚠️  POSSIBLE DUPLICATE - Manual review recommended")
        else:
            print(f"  ℹ️  SIMILAR NAMES - Likely different companies")
        
        print()
    
    # Special check for obvious company variations
    print("=== OBVIOUS COMPANY NAME VARIATIONS ===")
    variations_found = []
    
    for company in companies:
        name = company.get('company_name', '')
        
        # Check for common variations
        if name.endswith(' Corporation') or name.endswith(' Corp.') or name.endswith(' Inc.'):
            base_name = name.replace(' Corporation', '').replace(' Corp.', '').replace(' Inc.', '')
            
            # Look for base name in other companies
            for other_company in companies:
                other_name = other_company.get('company_name', '')
                if other_name != name and base_name.lower() in other_name.lower():
                    variations_found.append((name, other_name))
    
    # Remove duplicates from variations_found
    unique_variations = []
    for var in variations_found:
        reverse_var = (var[1], var[0])
        if reverse_var not in unique_variations:
            unique_variations.append(var)
    
    if unique_variations:
        print(f"Found {len(unique_variations)} potential name variations:")
        for name1, name2 in unique_variations[:10]:
            print(f"  • '{name1}' <-> '{name2}'")
        if len(unique_variations) > 10:
            print(f"  ... and {len(unique_variations) - 10} more")
    else:
        print("No obvious name variations found")
    
    return high_confidence_duplicates

if __name__ == "__main__":
    analyze_potential_duplicates()