import json

def create_missing_consulting_firms():
    """Create data for missing major consulting firms"""
    
    consulting_firms = [
        {
            "company_name": "Boston Consulting Group (BCG)",
            "about": "Boston Consulting Group is a global management consulting firm and the world's second-largest consulting firm, partnering with leaders in business and society to tackle their most important challenges.",
            "industry": "Strategy & Management Consulting",
            "sub_industry": "Management Consulting",
            "company_stage": "Private",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Strategic", "Analytical", "Global", "Impact-Driven"],
            "tech_stack": ["PowerBI", "Tableau", "Python", "R", "SQL"],
            "roles": [
                {
                    "title": "Management Consultant",
                    "description": "Work with senior executives to solve complex business problems across various industries.",
                    "required_skills": ["Strategy", "Problem Solving", "Business Analysis"],
                    "nice_to_have_skills": ["MBA", "Quantitative Analysis"],
                    "location": "Boston, MA",
                    "salary_range": [165000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Principal",
                    "description": "Lead client engagements and drive strategic initiatives for major corporations.",
                    "required_skills": ["Leadership", "Strategy", "Client Management"],
                    "nice_to_have_skills": ["Industry Expertise", "Business Development"],
                    "location": "Boston, MA",
                    "salary_range": [300000, 500000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        },
        {
            "company_name": "Bain & Company",
            "about": "Bain & Company is a global management consulting firm that helps companies create sustainable, superior value for their customers, shareholders, and communities.",
            "industry": "Strategy & Management Consulting",
            "sub_industry": "Management Consulting",
            "company_stage": "Private",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Results-Oriented", "Collaborative", "Entrepreneurial", "Data-Driven"],
            "tech_stack": ["Excel", "PowerPoint", "Python", "R", "Tableau"],
            "roles": [
                {
                    "title": "Associate Consultant",
                    "description": "Support senior consultants in developing strategic solutions for Fortune 500 clients.",
                    "required_skills": ["Strategy", "Analytics", "Problem Solving"],
                    "nice_to_have_skills": ["MBA", "Business Analysis"],
                    "location": "Boston, MA",
                    "salary_range": [170000, 290000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Manager",
                    "description": "Lead project teams and client relationships while developing strategic recommendations.",
                    "required_skills": ["Leadership", "Client Management", "Strategy"],
                    "nice_to_have_skills": ["Industry Experience", "Business Development"],
                    "location": "Boston, MA",
                    "salary_range": [250000, 400000],
                    "visa_sponsorship": True,
                    "min_experience_years": 5
                }
            ]
        },
        {
            "company_name": "PwC (PricewaterhouseCoopers)",
            "about": "PwC is a multinational professional services network and one of the Big Four accounting firms, providing audit, tax, and consulting services to clients worldwide.",
            "industry": "Strategy & Management Consulting",
            "sub_industry": "Professional Services",
            "company_stage": "Private",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Professional", "Global", "Diverse", "Client-Focused"],
            "tech_stack": ["SAP", "Oracle", "Salesforce", "Power BI", "Python"],
            "roles": [
                {
                    "title": "Management Consultant",
                    "description": "Provide strategic advice and implementation support to clients across various industries.",
                    "required_skills": ["Consulting", "Business Analysis", "Project Management"],
                    "nice_to_have_skills": ["Industry Expertise", "Change Management"],
                    "location": "New York, NY",
                    "salary_range": [95000, 165000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Senior Manager",
                    "description": "Lead client engagements and manage complex consulting projects.",
                    "required_skills": ["Leadership", "Client Management", "Strategy"],
                    "nice_to_have_skills": ["Business Development", "Industry Expertise"],
                    "location": "New York, NY",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 6
                }
            ]
        },
        {
            "company_name": "EY (Ernst & Young)",
            "about": "EY is a multinational professional services partnership and one of the Big Four accounting firms, providing assurance, tax, transaction, and advisory services.",
            "industry": "Strategy & Management Consulting",
            "sub_industry": "Professional Services",
            "company_stage": "Private",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovative", "Inclusive", "Global", "Purpose-Driven"],
            "tech_stack": ["Microsoft Suite", "Tableau", "Alteryx", "Python", "Power BI"],
            "roles": [
                {
                    "title": "Business Consultant",
                    "description": "Support clients in transformation initiatives and strategic planning across multiple industries.",
                    "required_skills": ["Consulting", "Business Analysis", "Strategy"],
                    "nice_to_have_skills": ["Digital Transformation", "Change Management"],
                    "location": "New York, NY",
                    "salary_range": [90000, 155000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Senior Consultant",
                    "description": "Lead workstreams on client engagements and drive business transformation initiatives.",
                    "required_skills": ["Leadership", "Strategy", "Client Management"],
                    "nice_to_have_skills": ["Industry Expertise", "Digital Solutions"],
                    "location": "New York, NY",
                    "salary_range": [130000, 220000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        },
        {
            "company_name": "KPMG",
            "about": "KPMG is a multinational professional services network and one of the Big Four accounting firms, providing audit, tax, and advisory services to clients worldwide.",
            "industry": "Strategy & Management Consulting",
            "sub_industry": "Professional Services",
            "company_stage": "Private",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Professional", "Collaborative", "Global", "Values-Driven"],
            "tech_stack": ["Microsoft Suite", "SAP", "Oracle", "Tableau", "R"],
            "roles": [
                {
                    "title": "Advisory Consultant",
                    "description": "Provide strategic advisory services to help clients navigate complex business challenges.",
                    "required_skills": ["Consulting", "Business Analysis", "Problem Solving"],
                    "nice_to_have_skills": ["Risk Management", "Regulatory Compliance"],
                    "location": "New York, NY",
                    "salary_range": [88000, 150000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Director",
                    "description": "Lead large-scale client engagements and drive business development initiatives.",
                    "required_skills": ["Leadership", "Client Management", "Strategy"],
                    "nice_to_have_skills": ["Business Development", "Industry Expertise"],
                    "location": "New York, NY",
                    "salary_range": [180000, 320000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        }
    ]
    
    return consulting_firms

def create_missing_investment_banks():
    """Create data for missing major investment banks"""
    
    investment_banks = [
        {
            "company_name": "UBS",
            "about": "UBS is a Swiss multinational investment bank and financial services company, providing wealth management, asset management, and investment banking services to private, corporate, and institutional clients worldwide.",
            "industry": "Banking and Finance",
            "sub_industry": "Investment Banking",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Swiss Excellence", "Global", "Client-Focused", "Innovative"],
            "tech_stack": ["Bloomberg Terminal", "Reuters", "Python", "SQL", "Excel"],
            "roles": [
                {
                    "title": "Investment Banking Analyst",
                    "description": "Support execution of M&A transactions, IPOs, and other corporate finance activities.",
                    "required_skills": ["Financial Modeling", "Valuation", "Excel"],
                    "nice_to_have_skills": ["Bloomberg", "Capital Markets"],
                    "location": "New York, NY",
                    "salary_range": [155000, 210000],
                    "visa_sponsorship": True,
                    "min_experience_years": 0
                },
                {
                    "title": "Vice President - Investment Banking",
                    "description": "Lead client relationships and manage complex M&A and capital markets transactions.",
                    "required_skills": ["Client Management", "Transaction Execution", "Leadership"],
                    "nice_to_have_skills": ["Industry Expertise", "Business Development"],
                    "location": "New York, NY",
                    "salary_range": [300000, 500000],
                    "visa_sponsorship": True,
                    "min_experience_years": 7
                }
            ]
        },
        {
            "company_name": "Deutsche Bank",
            "about": "Deutsche Bank is a German multinational investment bank and financial services company, providing investment banking, retail banking, transaction banking, and asset management services.",
            "industry": "Banking and Finance",
            "sub_industry": "Investment Banking",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["European Leader", "Global", "Innovation-Driven", "Performance-Oriented"],
            "tech_stack": ["Bloomberg Terminal", "Reuters", "Python", "R", "SQL"],
            "roles": [
                {
                    "title": "Investment Banking Associate",
                    "description": "Execute M&A transactions and capital markets deals while managing client relationships.",
                    "required_skills": ["Financial Analysis", "M&A", "Capital Markets"],
                    "nice_to_have_skills": ["German Language", "European Markets"],
                    "location": "New York, NY",
                    "salary_range": [175000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Managing Director",
                    "description": "Lead major client relationships and oversee significant M&A and capital markets transactions.",
                    "required_skills": ["Leadership", "Client Management", "Business Development"],
                    "nice_to_have_skills": ["Industry Expertise", "International Markets"],
                    "location": "New York, NY",
                    "salary_range": [500000, 1000000],
                    "visa_sponsorship": True,
                    "min_experience_years": 12
                }
            ]
        },
        {
            "company_name": "BNP Paribas",
            "about": "BNP Paribas is a French international banking group and a major global bank, providing investment banking, asset management, and financial services worldwide.",
            "industry": "Banking and Finance",
            "sub_industry": "Investment Banking",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["European Heritage", "Global Presence", "Sustainable Finance", "Innovation"],
            "tech_stack": ["Bloomberg Terminal", "Thomson Reuters", "Python", "MATLAB", "SQL"],
            "roles": [
                {
                    "title": "Corporate Finance Analyst",
                    "description": "Support M&A transactions, equity and debt capital markets, and corporate advisory services.",
                    "required_skills": ["Financial Modeling", "Valuation", "Capital Markets"],
                    "nice_to_have_skills": ["French Language", "European Markets"],
                    "location": "New York, NY",
                    "salary_range": [145000, 200000],
                    "visa_sponsorship": True,
                    "min_experience_years": 0
                },
                {
                    "title": "Director - Investment Banking",
                    "description": "Manage client relationships and lead execution of complex investment banking transactions.",
                    "required_skills": ["Client Management", "M&A", "Leadership"],
                    "nice_to_have_skills": ["Cross-Border Transactions", "Industry Expertise"],
                    "location": "New York, NY",
                    "salary_range": [350000, 600000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        },
        {
            "company_name": "Société Générale",
            "about": "Société Générale is a French multinational investment bank and financial services company, providing corporate and investment banking, asset management, and securities services.",
            "industry": "Banking and Finance",
            "sub_industry": "Investment Banking",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["French Excellence", "Innovation", "Global Network", "Entrepreneurial"],
            "tech_stack": ["Bloomberg Terminal", "Reuters", "Python", "VBA", "SQL"],
            "roles": [
                {
                    "title": "Investment Banking Analyst",
                    "description": "Support equity and debt capital markets transactions and M&A advisory services.",
                    "required_skills": ["Financial Analysis", "Capital Markets", "Excel"],
                    "nice_to_have_skills": ["French Language", "Derivatives"],
                    "location": "New York, NY",
                    "salary_range": [140000, 195000],
                    "visa_sponsorship": True,
                    "min_experience_years": 0
                },
                {
                    "title": "Vice President",
                    "description": "Lead transaction execution and client coverage in corporate finance and capital markets.",
                    "required_skills": ["Transaction Execution", "Client Management", "Leadership"],
                    "nice_to_have_skills": ["Structured Products", "European Markets"],
                    "location": "New York, NY",
                    "salary_range": [280000, 450000],
                    "visa_sponsorship": True,
                    "min_experience_years": 6
                }
            ]
        },
        {
            "company_name": "Nomura Holdings",
            "about": "Nomura Holdings is a Japanese financial holding company and a major global investment bank, providing investment banking, asset management, and brokerage services worldwide.",
            "industry": "Banking and Finance",
            "sub_industry": "Investment Banking",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Japanese Heritage", "Asian Markets", "Global Ambition", "Client-Centric"],
            "tech_stack": ["Bloomberg Terminal", "Thomson Reuters", "Python", "R", "SQL"],
            "roles": [
                {
                    "title": "Investment Banking Associate",
                    "description": "Execute M&A transactions and capital markets deals with focus on Asia-Pacific markets.",
                    "required_skills": ["Financial Modeling", "M&A", "Asian Markets"],
                    "nice_to_have_skills": ["Japanese Language", "Cross-Border Transactions"],
                    "location": "New York, NY",
                    "salary_range": [165000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Executive Director",
                    "description": "Lead client coverage and major transaction execution across Asia-Pacific and global markets.",
                    "required_skills": ["Client Management", "Leadership", "Cross-Border M&A"],
                    "nice_to_have_skills": ["Asian Market Expertise", "Business Development"],
                    "location": "New York, NY",
                    "salary_range": [400000, 700000],
                    "visa_sponsorship": True,
                    "min_experience_years": 10
                }
            ]
        }
    ]
    
    return investment_banks

def add_missing_firms_to_production():
    """Add missing consulting and investment banking firms to enhanced production file"""
    
    # Load current enhanced production file
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/enhanced_production_companies.json', 'r') as f:
        current_companies = json.load(f)
    
    print(f"📊 Current companies: {len(current_companies)}")
    
    # Create new firms data
    print("Creating missing consulting firms...")
    consulting_firms = create_missing_consulting_firms()
    
    print("Creating missing investment banks...")
    investment_banks = create_missing_investment_banks()
    
    # Combine all new firms
    new_firms = consulting_firms + investment_banks
    
    print(f"📊 Adding {len(new_firms)} new firms:")
    print(f"  • {len(consulting_firms)} consulting firms")
    print(f"  • {len(investment_banks)} investment banks")
    
    # Add to existing companies
    updated_companies = current_companies + new_firms
    
    print(f"📊 Total companies after addition: {len(updated_companies)}")
    
    # Save updated file
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/final_enhanced_companies.json'
    
    with open(output_file, 'w') as f:
        json.dump(updated_companies, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved final enhanced file: {output_file}")
    
    # Show what was added
    print("\n🏢 CONSULTING FIRMS ADDED:")
    for firm in consulting_firms:
        name = firm['company_name']
        roles = len(firm['roles'])
        print(f"  • {name} - {roles} roles")
    
    print("\n🏦 INVESTMENT BANKS ADDED:")
    for bank in investment_banks:
        name = bank['company_name']
        roles = len(bank['roles'])
        print(f"  • {name} - {roles} roles")
    
    # Calculate final stats
    total_roles = sum(len(company.get('roles', [])) for company in updated_companies)
    data_points = len(updated_companies) * 10 + total_roles * 8
    
    print(f"\n📊 FINAL STATISTICS:")
    print(f"  Companies: {len(updated_companies):,}")
    print(f"  Total roles: {total_roles:,}")
    print(f"  Data points: ~{data_points:,}")
    
    return updated_companies

def main():
    """Add missing major consulting firms and investment banks"""
    
    print("🏢 ADDING MISSING CONSULTING FIRMS & INVESTMENT BANKS")
    print("=" * 60)
    
    updated_companies = add_missing_firms_to_production()
    
    print(f"\n✅ Successfully added missing firms to production dataset!")
    
    return updated_companies

if __name__ == "__main__":
    main()