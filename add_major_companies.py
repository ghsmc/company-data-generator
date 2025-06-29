import json

def create_major_companies_data():
    """Create properly formatted data for missing major companies"""
    
    major_companies = [
        {
            "company_name": "Apple Inc.",
            "about": "Apple Inc. is an American multinational technology company that designs, develops, and sells consumer electronics, computer software, and online services. Known for innovative products like iPhone, iPad, Mac, and services.",
            "industry": "Technology",
            "sub_industry": "Consumer Electronics",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovative", "Design-Focused", "Premium Quality", "Collaborative"],
            "tech_stack": ["Swift", "Objective-C", "iOS", "macOS"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop and maintain software for Apple's ecosystem of products and services.",
                    "required_skills": ["Swift", "iOS Development", "Software Engineering"],
                    "nice_to_have_skills": ["Machine Learning", "UI/UX Design"],
                    "location": "Cupertino, CA",
                    "salary_range": [150000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                },
                {
                    "title": "Product Manager",
                    "description": "Lead product strategy and development for Apple's innovative products.",
                    "required_skills": ["Product Management", "Strategy", "Cross-functional Leadership"],
                    "nice_to_have_skills": ["Technical Background", "Design Thinking"],
                    "location": "Cupertino, CA",
                    "salary_range": [180000, 300000],
                    "visa_sponsorship": True,
                    "min_experience_years": 5
                },
                {
                    "title": "Hardware Engineer",
                    "description": "Design and develop cutting-edge hardware for Apple's product lineup.",
                    "required_skills": ["Hardware Design", "Electrical Engineering", "Circuit Design"],
                    "nice_to_have_skills": ["RF Engineering", "Semiconductor Design"],
                    "location": "Cupertino, CA",
                    "salary_range": [140000, 220000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        },
        {
            "company_name": "Google (Alphabet)",
            "about": "Google LLC is an American multinational technology company that specializes in Internet-related services and products, including search, cloud computing, advertising technologies, and artificial intelligence.",
            "industry": "Technology", 
            "sub_industry": "Internet Services",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovative", "Data-Driven", "Collaborative", "Global"],
            "tech_stack": ["Python", "Java", "Go", "TensorFlow", "Kubernetes"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and maintain Google's products and infrastructure at massive scale.",
                    "required_skills": ["Software Engineering", "Algorithms", "System Design"],
                    "nice_to_have_skills": ["Machine Learning", "Distributed Systems"],
                    "location": "Mountain View, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Research Scientist",
                    "description": "Conduct cutting-edge research in AI, machine learning, and computer science.",
                    "required_skills": ["Research", "Machine Learning", "PhD in relevant field"],
                    "nice_to_have_skills": ["Publications", "Deep Learning"],
                    "location": "Mountain View, CA",
                    "salary_range": [200000, 350000],
                    "visa_sponsorship": True,
                    "min_experience_years": 0
                },
                {
                    "title": "Product Manager",
                    "description": "Drive product strategy and execution for Google's suite of products.",
                    "required_skills": ["Product Management", "Analytics", "Strategy"],
                    "nice_to_have_skills": ["Technical Background", "A/B Testing"],
                    "location": "Mountain View, CA",
                    "salary_range": [170000, 300000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        },
        {
            "company_name": "Meta (Facebook)",
            "about": "Meta Platforms Inc. is an American multinational technology conglomerate focused on social media, virtual reality, and metaverse technologies, operating platforms like Facebook, Instagram, and WhatsApp.",
            "industry": "Technology",
            "sub_industry": "Social Media",
            "company_stage": "Public", 
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Move Fast", "Bold", "Innovative", "Connected"],
            "tech_stack": ["React", "Python", "PHP", "JavaScript", "PyTorch"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build products that connect billions of people around the world.",
                    "required_skills": ["Software Engineering", "Web Development", "Mobile Development"],
                    "nice_to_have_skills": ["React", "Machine Learning"],
                    "location": "Menlo Park, CA",
                    "salary_range": [155000, 270000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Data Scientist",
                    "description": "Use data to drive product decisions and improve user experiences across Meta's platforms.",
                    "required_skills": ["Data Science", "Statistics", "Python"],
                    "nice_to_have_skills": ["A/B Testing", "Machine Learning"],
                    "location": "Menlo Park, CA",
                    "salary_range": [150000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                },
                {
                    "title": "VR/AR Engineer",
                    "description": "Develop virtual and augmented reality experiences for the metaverse.",
                    "required_skills": ["VR/AR Development", "3D Programming", "Unity/Unreal"],
                    "nice_to_have_skills": ["Computer Vision", "Graphics Programming"],
                    "location": "Menlo Park, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "Amazon",
            "about": "Amazon.com Inc. is an American multinational technology company focusing on e-commerce, cloud computing, digital streaming, and artificial intelligence, operating Amazon Web Services and retail platforms.",
            "industry": "Technology",
            "sub_industry": "E-commerce",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Customer Obsessed", "Ownership", "Innovative", "High Standards"],
            "tech_stack": ["Java", "Python", "AWS", "Scala", "TypeScript"],
            "roles": [
                {
                    "title": "Software Development Engineer",
                    "description": "Build and scale Amazon's vast technology infrastructure and customer-facing products.",
                    "required_skills": ["Software Engineering", "System Design", "Algorithms"],
                    "nice_to_have_skills": ["AWS", "Distributed Systems"],
                    "location": "Seattle, WA",
                    "salary_range": [145000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Product Manager",
                    "description": "Drive product strategy and development for Amazon's customer experiences.",
                    "required_skills": ["Product Management", "Data Analysis", "Strategy"],
                    "nice_to_have_skills": ["Technical Background", "A/B Testing"],
                    "location": "Seattle, WA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                },
                {
                    "title": "Solutions Architect",
                    "description": "Help customers design and implement solutions using AWS cloud services.",
                    "required_skills": ["Cloud Architecture", "AWS", "Solution Design"],
                    "nice_to_have_skills": ["DevOps", "Machine Learning"],
                    "location": "Seattle, WA",
                    "salary_range": [140000, 220000],
                    "visa_sponsorship": True,
                    "min_experience_years": 5
                }
            ]
        },
        {
            "company_name": "Microsoft Corporation",
            "about": "Microsoft Corporation is an American multinational technology corporation that develops, manufactures, licenses, supports, and sells computer software, consumer electronics, and personal computers.",
            "industry": "Technology",
            "sub_industry": "Software",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Inclusive", "Innovative", "Growth Mindset", "Collaborative"],
            "tech_stack": [".NET", "C#", "Azure", "TypeScript", "Python"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop software solutions that empower every person and organization on the planet.",
                    "required_skills": ["Software Engineering", "C#", ".NET"],
                    "nice_to_have_skills": ["Azure", "Cloud Development"],
                    "location": "Redmond, WA",
                    "salary_range": [140000, 230000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Cloud Solution Architect",
                    "description": "Help customers design and implement cloud solutions using Microsoft Azure.",
                    "required_skills": ["Cloud Architecture", "Azure", "Enterprise Solutions"],
                    "nice_to_have_skills": ["DevOps", "Kubernetes"],
                    "location": "Redmond, WA",
                    "salary_range": [150000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 5
                },
                {
                    "title": "Product Manager",
                    "description": "Drive product strategy and development for Microsoft's productivity and cloud solutions.",
                    "required_skills": ["Product Management", "Strategy", "Technical Understanding"],
                    "nice_to_have_skills": ["Enterprise Software", "B2B Experience"],
                    "location": "Redmond, WA",
                    "salary_range": [155000, 270000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        },
        {
            "company_name": "Palantir Technologies",
            "about": "Palantir Technologies Inc. is an American software company that specializes in big data analytics, serving government and commercial clients with data integration and analysis platforms.",
            "industry": "Technology",
            "sub_industry": "Data Analytics",
            "company_stage": "Public",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Mission-Driven", "Analytical", "Innovative", "Impact-Focused"],
            "tech_stack": ["Java", "Python", "TypeScript", "React", "Big Data"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build software that helps solve the world's most important problems through data analysis.",
                    "required_skills": ["Software Engineering", "Data Structures", "Algorithms"],
                    "nice_to_have_skills": ["Big Data", "Machine Learning"],
                    "location": "Palo Alto, CA",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Forward Deployed Engineer",
                    "description": "Work directly with customers to implement and customize Palantir's software solutions.",
                    "required_skills": ["Software Engineering", "Customer Interaction", "Problem Solving"],
                    "nice_to_have_skills": ["Consulting", "Domain Expertise"],
                    "location": "Multiple Locations",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "OpenAI",
            "about": "OpenAI is an American artificial intelligence research laboratory consisting of the for-profit corporation OpenAI LP and non-profit parent company OpenAI Inc, focused on developing artificial general intelligence.",
            "industry": "Technology",
            "sub_industry": "Artificial Intelligence",
            "company_stage": "Private",
            "size": "Medium (50-199)",
            "culture_tags": ["Research-Focused", "Innovative", "Mission-Driven", "Collaborative"],
            "tech_stack": ["Python", "PyTorch", "TensorFlow", "Kubernetes", "Machine Learning"],
            "roles": [
                {
                    "title": "Research Scientist",
                    "description": "Conduct cutting-edge research in artificial intelligence and machine learning.",
                    "required_skills": ["Machine Learning", "Research", "Python"],
                    "nice_to_have_skills": ["Deep Learning", "Publications", "PhD"],
                    "location": "San Francisco, CA",
                    "salary_range": [200000, 400000],
                    "visa_sponsorship": True,
                    "min_experience_years": 0
                },
                {
                    "title": "Machine Learning Engineer",
                    "description": "Build and deploy AI systems that advance the state of artificial intelligence.",
                    "required_skills": ["Machine Learning", "Software Engineering", "PyTorch"],
                    "nice_to_have_skills": ["Large Language Models", "Distributed Systems"],
                    "location": "San Francisco, CA",
                    "salary_range": [180000, 350000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "Anthropic",
            "about": "Anthropic is an AI safety company focused on developing safe, beneficial artificial intelligence systems through research in AI alignment and safety techniques.",
            "industry": "Technology",
            "sub_industry": "Artificial Intelligence",
            "company_stage": "Private",
            "size": "Small (1-49)",
            "culture_tags": ["Safety-Focused", "Research-Driven", "Ethical", "Innovative"],
            "tech_stack": ["Python", "PyTorch", "Machine Learning", "NLP"],
            "roles": [
                {
                    "title": "AI Safety Researcher",
                    "description": "Research methods to make AI systems safe, beneficial, and aligned with human values.",
                    "required_skills": ["Machine Learning", "Research", "AI Safety"],
                    "nice_to_have_skills": ["Publications", "PhD", "Ethics"],
                    "location": "San Francisco, CA",
                    "salary_range": [190000, 380000],
                    "visa_sponsorship": True,
                    "min_experience_years": 0
                },
                {
                    "title": "Research Engineer",
                    "description": "Build infrastructure and tools to support AI safety research.",
                    "required_skills": ["Software Engineering", "Machine Learning", "Python"],
                    "nice_to_have_skills": ["Research", "AI Safety"],
                    "location": "San Francisco, CA",
                    "salary_range": [170000, 320000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                }
            ]
        },
        {
            "company_name": "SpaceX",
            "about": "SpaceX is an American aerospace manufacturer and space transportation company founded by Elon Musk, focused on reducing space transportation costs and enabling Mars colonization.",
            "industry": "Aerospace",
            "sub_industry": "Space Technology",
            "company_stage": "Private",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Mission-Driven", "Fast-Paced", "Innovative", "High-Performance"],
            "tech_stack": ["C++", "Python", "Linux", "Real-time Systems"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop flight software and ground systems for rockets and spacecraft.",
                    "required_skills": ["Software Engineering", "C++", "Real-time Systems"],
                    "nice_to_have_skills": ["Aerospace", "Embedded Systems"],
                    "location": "Hawthorne, CA",
                    "salary_range": [130000, 220000],
                    "visa_sponsorship": False,
                    "min_experience_years": 2
                },
                {
                    "title": "Aerospace Engineer",
                    "description": "Design and develop rockets, spacecraft, and related systems.",
                    "required_skills": ["Aerospace Engineering", "CAD", "Systems Engineering"],
                    "nice_to_have_skills": ["Propulsion", "Structures"],
                    "location": "Hawthorne, CA",
                    "salary_range": [120000, 200000],
                    "visa_sponsorship": False,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "Netflix",
            "about": "Netflix Inc. is an American subscription streaming service and production company that offers a wide variety of TV series, documentaries, and feature films across a wide variety of genres and languages.",
            "industry": "Media & Entertainment",
            "sub_industry": "Streaming",
            "company_stage": "Public",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Freedom & Responsibility", "High Performance", "Innovative", "Data-Driven"],
            "tech_stack": ["Java", "Python", "JavaScript", "React", "AWS"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and scale the technology that powers Netflix's global streaming platform.",
                    "required_skills": ["Software Engineering", "Distributed Systems", "Java"],
                    "nice_to_have_skills": ["Microservices", "Cloud Computing"],
                    "location": "Los Gatos, CA",
                    "salary_range": [170000, 300000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                },
                {
                    "title": "Data Scientist",
                    "description": "Use data to improve content recommendations and user experience.",
                    "required_skills": ["Data Science", "Machine Learning", "Statistics"],
                    "nice_to_have_skills": ["Recommendation Systems", "A/B Testing"],
                    "location": "Los Gatos, CA",
                    "salary_range": [180000, 320000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        }
    ]
    
    return major_companies

def add_companies_to_production(new_companies):
    """Add new companies to the production file"""
    
    # Load current production file
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/production_companies.json', 'r') as f:
        current_companies = json.load(f)
    
    print(f"Current companies: {len(current_companies)}")
    
    # Add new companies
    updated_companies = current_companies + new_companies
    
    print(f"After adding: {len(updated_companies)} companies")
    print(f"Added: {len(new_companies)} new companies")
    
    # Save updated file
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/enhanced_production_companies.json'
    
    with open(output_file, 'w') as f:
        json.dump(updated_companies, f, indent=2, ensure_ascii=False)
    
    print(f"Saved enhanced file: {output_file}")
    
    # Show what was added
    print("\\nAdded companies:")
    for company in new_companies:
        name = company['company_name']
        industry = company['industry'] 
        roles = len(company['roles'])
        print(f"  • {name} ({industry}) - {roles} roles")
    
    return updated_companies

def main():
    """Add major missing companies to production file"""
    
    print("🏢 ADDING MAJOR COMPANIES TO PRODUCTION FILE")
    print("=" * 50)
    
    # Create company data
    print("Creating company data...")
    new_companies = create_major_companies_data()
    
    # Add to production file
    print("Adding to production file...")
    updated_companies = add_companies_to_production(new_companies)
    
    # Calculate new stats
    total_roles = sum(len(company.get('roles', [])) for company in updated_companies)
    data_points = len(updated_companies) * 10 + total_roles * 8
    
    print(f"\\n📊 FINAL STATISTICS:")
    print(f"  Companies: {len(updated_companies):,}")
    print(f"  Total roles: {total_roles:,}")
    print(f"  Data points: ~{data_points:,}")
    
    print(f"\\n✅ Successfully enhanced production file with major companies!")

if __name__ == "__main__":
    main()