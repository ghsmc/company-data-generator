import json

def check_missing_major_companies():
    """Check which major companies are missing from our production file"""
    
    # Load current production file
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/production_companies.json', 'r') as f:
        companies = json.load(f)
    
    # Get list of current company names (lowercase for comparison)
    current_companies = [company.get('company_name', '').lower() for company in companies]
    
    print("=== CHECKING FOR MISSING MAJOR COMPANIES ===")
    
    # Major companies we should have
    major_companies = {
        # Big Tech (FAANG+)
        'Apple Inc.': 'apple',
        'Google (Alphabet)': 'google',
        'Meta (Facebook)': 'meta',
        'Amazon': 'amazon', 
        'Netflix': 'netflix',
        'Microsoft Corporation': 'microsoft',
        
        # Other Major Tech
        'Palantir Technologies': 'palantir',
        'OpenAI': 'openai',
        'Anthropic': 'anthropic',
        'SpaceX': 'spacex',
        'Uber Technologies': 'uber',
        'Lyft': 'lyft',
        'Airbnb': 'airbnb',
        'Spotify': 'spotify',
        'Twitter (X)': 'twitter',
        'TikTok (ByteDance)': 'tiktok',
        'Zoom Video Communications': 'zoom',
        'Slack Technologies': 'slack',
        'Salesforce': 'salesforce',
        'Adobe': 'adobe',
        'Oracle Corporation': 'oracle',
        'IBM': 'ibm',
        'Intel Corporation': 'intel',
        'NVIDIA Corporation': 'nvidia',
        'AMD': 'amd',
        
        # Major Finance
        'JPMorgan Chase': 'jpmorgan',
        'Bank of America': 'bank of america',
        'Wells Fargo': 'wells fargo',
        'Goldman Sachs': 'goldman sachs',
        'Morgan Stanley': 'morgan stanley',
        'Citigroup': 'citigroup',
        'BlackRock': 'blackrock',
        'Vanguard': 'vanguard',
        
        # Major Consulting
        'McKinsey & Company': 'mckinsey',
        'Boston Consulting Group': 'boston consulting',
        'Bain & Company': 'bain',
        'Deloitte': 'deloitte',
        'PwC': 'pwc',
        'EY (Ernst & Young)': 'ernst',
        'KPMG': 'kpmg',
        'Accenture': 'accenture',
        
        # Major Healthcare/Pharma
        'Johnson & Johnson': 'johnson',
        'Pfizer': 'pfizer',
        'Moderna': 'moderna',
        'Merck & Co.': 'merck',
        'AbbVie': 'abbvie',
        
        # Major Retail/Consumer
        'Walmart': 'walmart',
        'Target Corporation': 'target',
        'Costco': 'costco',
        'Home Depot': 'home depot',
        'Starbucks': 'starbucks',
        'Nike': 'nike',
        'Coca-Cola': 'coca-cola',
        'PepsiCo': 'pepsi',
        
        # Major Industrial
        'General Electric': 'general electric',
        'Boeing': 'boeing',
        'Lockheed Martin': 'lockheed',
        'Caterpillar': 'caterpillar',
        '3M': '3m',
        
        # Major Energy
        'ExxonMobil': 'exxonmobil',
        'Chevron': 'chevron',
        'ConocoPhillips': 'conocophillips'
    }
    
    # Check which are missing
    missing_companies = []
    present_companies = []
    
    for company_name, search_term in major_companies.items():
        found = False
        for current_name in current_companies:
            if search_term in current_name or any(word in current_name for word in search_term.split()):
                found = True
                present_companies.append(company_name)
                break
        
        if not found:
            missing_companies.append(company_name)
    
    print(f"✅ Major companies present: {len(present_companies)}")
    print(f"❌ Major companies missing: {len(missing_companies)}")
    
    if missing_companies:
        print(f"\\n🚨 MISSING MAJOR COMPANIES:")
        for company in sorted(missing_companies):
            print(f"  • {company}")
    
    if present_companies:
        print(f"\\n✅ MAJOR COMPANIES PRESENT:")
        for company in sorted(present_companies)[:10]:  # Show first 10
            print(f"  • {company}")
        if len(present_companies) > 10:
            print(f"  ... and {len(present_companies) - 10} more")
    
    return missing_companies, present_companies

if __name__ == "__main__":
    missing, present = check_missing_major_companies()
    print(f"\\n📊 SUMMARY: {len(missing)} missing, {len(present)} present")