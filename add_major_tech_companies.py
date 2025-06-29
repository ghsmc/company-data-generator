import json

def create_enterprise_software_companies():
    """Create data for major enterprise software companies"""
    
    companies = [
        {
            "company_name": "Salesforce",
            "about": "Salesforce is an American cloud-based software company that provides customer relationship management (CRM) software and applications focused on sales, customer service, marketing automation, analytics, and application development.",
            "industry": "Technology",
            "sub_industry": "Enterprise Software",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Customer Success", "Innovation", "Equality", "Trailblazer"],
            "tech_stack": ["Salesforce Platform", "Apex", "Lightning", "Java", "JavaScript"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and maintain Salesforce's cloud-based CRM platform and enterprise applications.",
                    "required_skills": ["Software Engineering", "Java", "JavaScript"],
                    "nice_to_have_skills": ["Salesforce Platform", "Cloud Computing"],
                    "location": "San Francisco, CA",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Product Manager",
                    "description": "Drive product strategy and development for Salesforce's enterprise software solutions.",
                    "required_skills": ["Product Management", "Strategy", "Enterprise Software"],
                    "nice_to_have_skills": ["CRM", "B2B SaaS"],
                    "location": "San Francisco, CA",
                    "salary_range": [170000, 300000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                },
                {
                    "title": "Solutions Architect",
                    "description": "Design and implement Salesforce solutions for enterprise customers.",
                    "required_skills": ["Solution Architecture", "Salesforce Platform", "Enterprise Integration"],
                    "nice_to_have_skills": ["CRM", "Cloud Architecture"],
                    "location": "San Francisco, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 5
                }
            ]
        },
        {
            "company_name": "Oracle Corporation",
            "about": "Oracle Corporation is an American multinational computer technology corporation that offers database software and technology, cloud engineered systems, and enterprise software products.",
            "industry": "Technology",
            "sub_industry": "Enterprise Software",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Performance", "Global", "Enterprise-Focused"],
            "tech_stack": ["Oracle Database", "Java", "SQL", "PL/SQL", "Oracle Cloud"],
            "roles": [
                {
                    "title": "Software Developer",
                    "description": "Develop and maintain Oracle's database and enterprise software products.",
                    "required_skills": ["Software Development", "Java", "Database Systems"],
                    "nice_to_have_skills": ["Oracle Database", "Cloud Computing"],
                    "location": "Redwood City, CA",
                    "salary_range": [140000, 230000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Principal Software Engineer",
                    "description": "Lead technical architecture and development of Oracle's enterprise software solutions.",
                    "required_skills": ["Software Architecture", "Java", "Distributed Systems"],
                    "nice_to_have_skills": ["Oracle Technologies", "Cloud Platforms"],
                    "location": "Redwood City, CA",
                    "salary_range": [180000, 320000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        },
        {
            "company_name": "SAP",
            "about": "SAP SE is a German multinational software corporation that makes enterprise software to manage business operations and customer relations, headquartered in Walldorf, Germany.",
            "industry": "Technology",
            "sub_industry": "Enterprise Software",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Purpose-Driven", "Global", "Collaborative"],
            "tech_stack": ["SAP HANA", "ABAP", "Java", "JavaScript", "SAP Cloud Platform"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop enterprise software solutions for SAP's global customer base.",
                    "required_skills": ["Software Engineering", "Java", "Enterprise Applications"],
                    "nice_to_have_skills": ["SAP Technologies", "ABAP"],
                    "location": "Palo Alto, CA",
                    "salary_range": [135000, 220000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Cloud Architect",
                    "description": "Design and implement cloud-based enterprise solutions using SAP technologies.",
                    "required_skills": ["Cloud Architecture", "SAP Cloud Platform", "Enterprise Integration"],
                    "nice_to_have_skills": ["SAP HANA", "Microservices"],
                    "location": "Palo Alto, CA",
                    "salary_range": [170000, 290000],
                    "visa_sponsorship": True,
                    "min_experience_years": 6
                }
            ]
        },
        {
            "company_name": "ServiceNow",
            "about": "ServiceNow Inc. is an American software company that provides digital workflows that create great experiences and unlock productivity for employees and the enterprise.",
            "industry": "Technology",
            "sub_industry": "Enterprise Software",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Inclusive", "High-Performance", "Customer-Focused"],
            "tech_stack": ["ServiceNow Platform", "JavaScript", "AngularJS", "Java", "REST APIs"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and enhance ServiceNow's digital workflow platform and enterprise applications.",
                    "required_skills": ["Software Engineering", "JavaScript", "Web Development"],
                    "nice_to_have_skills": ["ServiceNow Platform", "AngularJS"],
                    "location": "Santa Clara, CA",
                    "salary_range": [145000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Staff Software Engineer",
                    "description": "Lead technical design and implementation of complex ServiceNow platform features.",
                    "required_skills": ["Software Architecture", "JavaScript", "System Design"],
                    "nice_to_have_skills": ["ServiceNow Development", "Enterprise Platforms"],
                    "location": "Santa Clara, CA",
                    "salary_range": [200000, 350000],
                    "visa_sponsorship": True,
                    "min_experience_years": 7
                }
            ]
        },
        {
            "company_name": "Workday",
            "about": "Workday Inc. is an American on-demand financial management and human capital management software vendor, providing software-as-a-service (SaaS) applications for enterprise customers.",
            "industry": "Technology",
            "sub_industry": "Enterprise Software",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Fun", "Customer Service", "Employee Satisfaction"],
            "tech_stack": ["Java", "Scala", "React", "Spring", "Workday Platform"],
            "roles": [
                {
                    "title": "Software Application Engineer",
                    "description": "Develop and maintain Workday's enterprise SaaS applications for HR and finance.",
                    "required_skills": ["Software Engineering", "Java", "Enterprise Applications"],
                    "nice_to_have_skills": ["SaaS", "HR Technology"],
                    "location": "Pleasanton, CA",
                    "salary_range": [140000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Principal Software Engineer",
                    "description": "Lead architecture and development of Workday's core platform and applications.",
                    "required_skills": ["Software Architecture", "Java", "Distributed Systems"],
                    "nice_to_have_skills": ["Workday Platform", "SaaS Architecture"],
                    "location": "Pleasanton, CA",
                    "salary_range": [190000, 330000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        }
    ]
    
    return companies

def create_hardware_semiconductor_companies():
    """Create data for major hardware and semiconductor companies"""
    
    companies = [
        {
            "company_name": "Qualcomm",
            "about": "Qualcomm Incorporated is an American multinational semiconductor and telecommunications equipment company that designs and markets wireless telecommunications products and services.",
            "industry": "Technology",
            "sub_industry": "Semiconductors",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Wireless Technology", "Global", "Engineering Excellence"],
            "tech_stack": ["C/C++", "Verilog", "SystemVerilog", "Python", "MATLAB"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop software for Qualcomm's wireless communication and semiconductor products.",
                    "required_skills": ["Software Engineering", "C/C++", "Embedded Systems"],
                    "nice_to_have_skills": ["Wireless Technologies", "DSP"],
                    "location": "San Diego, CA",
                    "salary_range": [130000, 220000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Hardware Engineer",
                    "description": "Design and develop semiconductor products and wireless communication systems.",
                    "required_skills": ["Hardware Design", "Digital Design", "Verilog"],
                    "nice_to_have_skills": ["RF Design", "ASIC Design"],
                    "location": "San Diego, CA",
                    "salary_range": [135000, 230000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "Broadcom Inc.",
            "about": "Broadcom Inc. is an American designer, developer, manufacturer and global supplier of semiconductor and infrastructure software products, serving the data center, networking, software, broadband, wireless, and storage markets.",
            "industry": "Technology",
            "sub_industry": "Semiconductors",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Excellence", "Global", "Technology Leadership"],
            "tech_stack": ["C/C++", "Verilog", "SystemVerilog", "Python", "Perl"],
            "roles": [
                {
                    "title": "ASIC Design Engineer",
                    "description": "Design and develop application-specific integrated circuits for networking and storage products.",
                    "required_skills": ["ASIC Design", "Verilog", "Digital Design"],
                    "nice_to_have_skills": ["SystemVerilog", "Synthesis"],
                    "location": "San Jose, CA",
                    "salary_range": [140000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                },
                {
                    "title": "Software Engineer",
                    "description": "Develop software for Broadcom's semiconductor and infrastructure products.",
                    "required_skills": ["Software Engineering", "C/C++", "Embedded Systems"],
                    "nice_to_have_skills": ["Networking", "Storage Systems"],
                    "location": "San Jose, CA",
                    "salary_range": [135000, 230000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                }
            ]
        },
        {
            "company_name": "Micron Technology",
            "about": "Micron Technology Inc. is an American producer of computer memory and computer data storage including dynamic random-access memory, flash memory, and USB flash drives.",
            "industry": "Technology",
            "sub_industry": "Semiconductors",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Quality", "Global", "Technology Excellence"],
            "tech_stack": ["C/C++", "Python", "MATLAB", "Verilog", "Assembly"],
            "roles": [
                {
                    "title": "Memory Design Engineer",
                    "description": "Design and develop memory products including DRAM, NAND flash, and emerging memory technologies.",
                    "required_skills": ["Memory Design", "Digital Design", "Circuit Design"],
                    "nice_to_have_skills": ["DRAM", "NAND Flash"],
                    "location": "Boise, ID",
                    "salary_range": [125000, 210000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                },
                {
                    "title": "Software Engineer",
                    "description": "Develop software for memory testing, validation, and product development.",
                    "required_skills": ["Software Engineering", "C/C++", "Embedded Systems"],
                    "nice_to_have_skills": ["Memory Technologies", "Test Engineering"],
                    "location": "Boise, ID",
                    "salary_range": [120000, 200000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                }
            ]
        }
    ]
    
    return companies

def create_cybersecurity_companies():
    """Create data for major cybersecurity companies"""
    
    companies = [
        {
            "company_name": "Okta",
            "about": "Okta Inc. is an American identity and access management company that provides cloud software that helps companies manage and secure user authentication into applications.",
            "industry": "Technology",
            "sub_industry": "Cybersecurity",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Customer First", "Innovation", "Integrity", "Transparency"],
            "tech_stack": ["Java", "JavaScript", "React", "AWS", "Kubernetes"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and maintain Okta's identity and access management platform.",
                    "required_skills": ["Software Engineering", "Java", "JavaScript"],
                    "nice_to_have_skills": ["Identity Management", "Security"],
                    "location": "San Francisco, CA",
                    "salary_range": [155000, 270000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Security Engineer",
                    "description": "Design and implement security features for Okta's identity platform.",
                    "required_skills": ["Security Engineering", "Identity Management", "Cloud Security"],
                    "nice_to_have_skills": ["OAuth", "SAML"],
                    "location": "San Francisco, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "Zscaler",
            "about": "Zscaler Inc. is an American cloud-based information security company that provides internet security, web security, firewalls, sandboxing, SSL inspection, antivirus, vulnerability management and granular control of user activity in cloud computing, mobile and IoT environments.",
            "industry": "Technology",
            "sub_industry": "Cybersecurity",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Customer-Centric", "High Performance", "Agile"],
            "tech_stack": ["Java", "Python", "Go", "JavaScript", "AWS"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop cloud security solutions and network security products.",
                    "required_skills": ["Software Engineering", "Java", "Network Security"],
                    "nice_to_have_skills": ["Cloud Security", "Cybersecurity"],
                    "location": "San Jose, CA",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Principal Engineer",
                    "description": "Lead technical architecture for Zscaler's cloud security platform.",
                    "required_skills": ["Software Architecture", "Security Engineering", "Distributed Systems"],
                    "nice_to_have_skills": ["Cloud Platforms", "Network Security"],
                    "location": "San Jose, CA",
                    "salary_range": [200000, 350000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        },
        {
            "company_name": "Fortinet",
            "about": "Fortinet Inc. is an American multinational corporation that develops and markets cybersecurity software, appliances and services, such as firewalls, anti-virus, intrusion prevention and endpoint security.",
            "industry": "Technology",
            "sub_industry": "Cybersecurity",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Security-First", "Innovation", "Global", "Performance"],
            "tech_stack": ["C/C++", "Python", "Linux", "Networking", "Security Protocols"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop cybersecurity products including firewalls, intrusion prevention, and endpoint security.",
                    "required_skills": ["Software Engineering", "C/C++", "Network Security"],
                    "nice_to_have_skills": ["Cybersecurity", "Linux"],
                    "location": "Sunnyvale, CA",
                    "salary_range": [140000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Security Research Engineer",
                    "description": "Research and develop advanced threat detection and prevention technologies.",
                    "required_skills": ["Security Research", "Malware Analysis", "Threat Intelligence"],
                    "nice_to_have_skills": ["Reverse Engineering", "Machine Learning"],
                    "location": "Sunnyvale, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        }
    ]
    
    return companies

def create_social_media_companies():
    """Create data for major social media and internet platform companies"""
    
    companies = [
        {
            "company_name": "X (formerly Twitter)",
            "about": "X Corp. (formerly Twitter) is an American social media and social networking service where users post and interact with messages known as 'tweets', operating as a global platform for real-time information sharing.",
            "industry": "Technology",
            "sub_industry": "Social Media",
            "company_stage": "Private",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Fast-Paced", "Innovation", "Real-Time", "Global Impact"],
            "tech_stack": ["Scala", "Java", "JavaScript", "React", "MySQL"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and scale systems that power real-time global conversations on X platform.",
                    "required_skills": ["Software Engineering", "Distributed Systems", "Scala"],
                    "nice_to_have_skills": ["Real-time Systems", "Social Media"],
                    "location": "San Francisco, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "ML Engineer",
                    "description": "Develop machine learning systems for content recommendation, moderation, and user experience.",
                    "required_skills": ["Machine Learning", "Python", "Distributed Systems"],
                    "nice_to_have_skills": ["NLP", "Recommendation Systems"],
                    "location": "San Francisco, CA",
                    "salary_range": [170000, 300000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "LinkedIn",
            "about": "LinkedIn Corporation is an American business and employment-focused social media platform that is used for professional networking and career development, owned by Microsoft.",
            "industry": "Technology",
            "sub_industry": "Social Media",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Professional", "Growth Mindset", "Inclusive", "Member-First"],
            "tech_stack": ["Java", "Scala", "JavaScript", "React", "Kafka"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build professional networking and career development features for LinkedIn's global platform.",
                    "required_skills": ["Software Engineering", "Java", "Distributed Systems"],
                    "nice_to_have_skills": ["Social Networks", "Recommendation Systems"],
                    "location": "Sunnyvale, CA",
                    "salary_range": [155000, 270000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Data Scientist",
                    "description": "Use data to improve member experience and professional networking features.",
                    "required_skills": ["Data Science", "Statistics", "Python"],
                    "nice_to_have_skills": ["A/B Testing", "Social Networks"],
                    "location": "Sunnyvale, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "Snapchat (Snap Inc.)",
            "about": "Snap Inc. is an American multimedia instant messaging app and service developed by Snap Inc., known for its disappearing messages and innovative AR camera features.",
            "industry": "Technology",
            "sub_industry": "Social Media",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Creative", "Innovative", "Fast-Moving", "Fun"],
            "tech_stack": ["Python", "Java", "JavaScript", "React", "C++"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop features for Snapchat's multimedia messaging and AR camera platform.",
                    "required_skills": ["Software Engineering", "Python", "Mobile Development"],
                    "nice_to_have_skills": ["Computer Vision", "AR/VR"],
                    "location": "Santa Monica, CA",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "AR Engineer",
                    "description": "Build augmented reality experiences and camera features for Snapchat.",
                    "required_skills": ["AR/VR Development", "Computer Vision", "C++"],
                    "nice_to_have_skills": ["Computer Graphics", "Mobile AR"],
                    "location": "Santa Monica, CA",
                    "salary_range": [165000, 290000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        }
    ]
    
    return companies

def create_developer_tools_companies():
    """Create data for major developer tools and platform companies"""
    
    companies = [
        {
            "company_name": "GitHub",
            "about": "GitHub Inc. is a platform and cloud-based service for software development and version control using Git, providing distributed version control and source code management functionality, owned by Microsoft.",
            "industry": "Technology",
            "sub_industry": "Developer Tools",
            "company_stage": "Public",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Open Source", "Developer-First", "Collaborative", "Innovation"],
            "tech_stack": ["Ruby", "Go", "JavaScript", "React", "MySQL"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and maintain GitHub's platform for software development and collaboration.",
                    "required_skills": ["Software Engineering", "Ruby", "Git"],
                    "nice_to_have_skills": ["Open Source", "Developer Tools"],
                    "location": "San Francisco, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Principal Engineer",
                    "description": "Lead technical architecture for GitHub's developer platform and services.",
                    "required_skills": ["Software Architecture", "Distributed Systems", "Platform Engineering"],
                    "nice_to_have_skills": ["Git", "Developer Experience"],
                    "location": "San Francisco, CA",
                    "salary_range": [200000, 350000],
                    "visa_sponsorship": True,
                    "min_experience_years": 8
                }
            ]
        },
        {
            "company_name": "GitLab",
            "about": "GitLab Inc. is an open-core company that provides GitLab, a DevOps software package that can develop, secure, and operate software in a single application.",
            "industry": "Technology",
            "sub_industry": "Developer Tools",
            "company_stage": "Public",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Remote-First", "Transparency", "Collaboration", "Results-Focused"],
            "tech_stack": ["Ruby", "Go", "JavaScript", "Vue.js", "PostgreSQL"],
            "roles": [
                {
                    "title": "Backend Engineer",
                    "description": "Develop GitLab's DevOps platform backend systems and APIs.",
                    "required_skills": ["Backend Development", "Ruby", "API Design"],
                    "nice_to_have_skills": ["DevOps", "Git"],
                    "location": "Remote",
                    "salary_range": [140000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Senior Frontend Engineer",
                    "description": "Build user interfaces and experiences for GitLab's DevOps platform.",
                    "required_skills": ["Frontend Development", "JavaScript", "Vue.js"],
                    "nice_to_have_skills": ["DevOps", "User Experience"],
                    "location": "Remote",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        },
        {
            "company_name": "Docker",
            "about": "Docker Inc. is an American technology company that develops productivity tools for software developers, including Docker Desktop and Docker Hub for containerization and application development.",
            "industry": "Technology",
            "sub_industry": "Developer Tools",
            "company_stage": "Private",
            "size": "Medium (50-199)",
            "culture_tags": ["Innovation", "Open Source", "Developer-Centric", "Containerization"],
            "tech_stack": ["Go", "Python", "JavaScript", "React", "Kubernetes"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Develop Docker's containerization platform and developer productivity tools.",
                    "required_skills": ["Software Engineering", "Go", "Containerization"],
                    "nice_to_have_skills": ["Docker", "Kubernetes"],
                    "location": "Palo Alto, CA",
                    "salary_range": [145000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "DevOps Engineer",
                    "description": "Build and maintain infrastructure for Docker's platform and services.",
                    "required_skills": ["DevOps", "Kubernetes", "Cloud Platforms"],
                    "nice_to_have_skills": ["Docker", "CI/CD"],
                    "location": "Palo Alto, CA",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        }
    ]
    
    return companies

def create_gaming_ecommerce_companies():
    """Create data for major gaming and e-commerce companies"""
    
    companies = [
        {
            "company_name": "Epic Games",
            "about": "Epic Games Inc. is an American video game and software developer and publisher known for the Unreal Engine, Fortnite, and the Epic Games Store digital distribution platform.",
            "industry": "Technology",
            "sub_industry": "Gaming",
            "company_stage": "Private",
            "size": "Very Large (1,000-4,999)",
            "culture_tags": ["Creative", "Innovation", "Gaming-First", "Cutting-Edge"],
            "tech_stack": ["C++", "Unreal Engine", "Python", "C#", "JavaScript"],
            "roles": [
                {
                    "title": "Game Developer",
                    "description": "Develop games and interactive experiences using Unreal Engine and cutting-edge technology.",
                    "required_skills": ["Game Development", "C++", "Unreal Engine"],
                    "nice_to_have_skills": ["3D Graphics", "Game Design"],
                    "location": "Cary, NC",
                    "salary_range": [120000, 200000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Engine Programmer",
                    "description": "Develop and maintain Unreal Engine for game developers worldwide.",
                    "required_skills": ["Engine Development", "C++", "3D Graphics"],
                    "nice_to_have_skills": ["Rendering", "Game Engines"],
                    "location": "Cary, NC",
                    "salary_range": [140000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 4
                }
            ]
        },
        {
            "company_name": "eBay",
            "about": "eBay Inc. is an American multinational e-commerce company that facilitates consumer-to-consumer and business-to-consumer sales through its website, operating as an online marketplace and auction platform.",
            "industry": "Technology",
            "sub_industry": "E-commerce",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Global", "Diverse", "Customer-Focused"],
            "tech_stack": ["Java", "JavaScript", "React", "Node.js", "Scala"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build and maintain eBay's e-commerce marketplace platform and services.",
                    "required_skills": ["Software Engineering", "Java", "Distributed Systems"],
                    "nice_to_have_skills": ["E-commerce", "Microservices"],
                    "location": "San Jose, CA",
                    "salary_range": [145000, 250000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Data Scientist",
                    "description": "Use data to improve buyer and seller experiences on eBay's marketplace.",
                    "required_skills": ["Data Science", "Machine Learning", "Python"],
                    "nice_to_have_skills": ["E-commerce", "Recommendation Systems"],
                    "location": "San Jose, CA",
                    "salary_range": [150000, 260000],
                    "visa_sponsorship": True,
                    "min_experience_years": 3
                }
            ]
        },
        {
            "company_name": "PayPal",
            "about": "PayPal Holdings Inc. is an American multinational financial technology company operating an online payments system in the majority of countries that support online money transfers.",
            "industry": "Technology",
            "sub_industry": "Fintech",
            "company_stage": "Public",
            "size": "Enterprise (5,000+)",
            "culture_tags": ["Innovation", "Financial Inclusion", "Security-First", "Global"],
            "tech_stack": ["Java", "JavaScript", "React", "Node.js", "Python"],
            "roles": [
                {
                    "title": "Software Engineer",
                    "description": "Build secure and scalable payment systems for PayPal's global platform.",
                    "required_skills": ["Software Engineering", "Java", "Financial Systems"],
                    "nice_to_have_skills": ["Payments", "Security"],
                    "location": "San Jose, CA",
                    "salary_range": [140000, 240000],
                    "visa_sponsorship": True,
                    "min_experience_years": 2
                },
                {
                    "title": "Senior Software Engineer",
                    "description": "Lead development of PayPal's payment processing and financial services platform.",
                    "required_skills": ["Software Engineering", "System Design", "Java"],
                    "nice_to_have_skills": ["Fintech", "Distributed Systems"],
                    "location": "San Jose, CA",
                    "salary_range": [160000, 280000],
                    "visa_sponsorship": True,
                    "min_experience_years": 5
                }
            ]
        }
    ]
    
    return companies

def add_all_tech_companies():
    """Add all missing major tech companies to the final enhanced file"""
    
    # Load current final enhanced file
    with open('/Users/georgemccain/Desktop/untitled folder 2/data/final_enhanced_companies.json', 'r') as f:
        current_companies = json.load(f)
    
    print(f"📊 Current companies: {len(current_companies)}")
    
    # Create all new tech companies
    print("Creating enterprise software companies...")
    enterprise_software = create_enterprise_software_companies()
    
    print("Creating hardware/semiconductor companies...")
    hardware_companies = create_hardware_semiconductor_companies()
    
    print("Creating cybersecurity companies...")
    cybersecurity_companies = create_cybersecurity_companies()
    
    print("Creating social media companies...")
    social_media_companies = create_social_media_companies()
    
    print("Creating developer tools companies...")
    developer_tools_companies = create_developer_tools_companies()
    
    print("Creating gaming/e-commerce companies...")
    gaming_ecommerce_companies = create_gaming_ecommerce_companies()
    
    # Combine all new companies
    all_new_companies = (enterprise_software + hardware_companies + cybersecurity_companies + 
                        social_media_companies + developer_tools_companies + gaming_ecommerce_companies)
    
    print(f"📊 Adding {len(all_new_companies)} new tech companies:")
    print(f"  • {len(enterprise_software)} enterprise software companies")
    print(f"  • {len(hardware_companies)} hardware/semiconductor companies")
    print(f"  • {len(cybersecurity_companies)} cybersecurity companies")
    print(f"  • {len(social_media_companies)} social media companies")
    print(f"  • {len(developer_tools_companies)} developer tools companies")
    print(f"  • {len(gaming_ecommerce_companies)} gaming/e-commerce companies")
    
    # Add to existing companies
    updated_companies = current_companies + all_new_companies
    
    print(f"📊 Total companies after addition: {len(updated_companies)}")
    
    # Save updated file
    output_file = '/Users/georgemccain/Desktop/untitled folder 2/data/complete_companies_dataset.json'
    
    with open(output_file, 'w') as f:
        json.dump(updated_companies, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Saved complete dataset: {output_file}")
    
    # Show summary of what was added
    print("\n🏢 TECH COMPANIES ADDED BY CATEGORY:")
    
    categories = [
        ("Enterprise Software", enterprise_software),
        ("Hardware/Semiconductors", hardware_companies),
        ("Cybersecurity", cybersecurity_companies),
        ("Social Media", social_media_companies),
        ("Developer Tools", developer_tools_companies),
        ("Gaming/E-commerce", gaming_ecommerce_companies)
    ]
    
    for category_name, companies in categories:
        print(f"\n{category_name}:")
        for company in companies:
            name = company['company_name']
            roles = len(company['roles'])
            print(f"  • {name} - {roles} roles")
    
    # Calculate final stats
    total_roles = sum(len(company.get('roles', [])) for company in updated_companies)
    data_points = len(updated_companies) * 10 + total_roles * 8
    
    print(f"\n📊 FINAL COMPLETE DATASET STATISTICS:")
    print(f"  Companies: {len(updated_companies):,}")
    print(f"  Total roles: {total_roles:,}")
    print(f"  Data points: ~{data_points:,}")
    
    return updated_companies

def main():
    """Add all missing major tech companies"""
    
    print("🚀 ADDING MAJOR TECH COMPANIES TO DATASET")
    print("=" * 60)
    
    updated_companies = add_all_tech_companies()
    
    print(f"\n✅ Successfully created complete companies dataset with comprehensive tech coverage!")
    
    return updated_companies

if __name__ == "__main__":
    main()