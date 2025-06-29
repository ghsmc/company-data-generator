import re
import json
import collections

# Read the file and use regex to find company names
with open('/Users/georgemccain/Desktop/untitled folder 2/data/enriched_companies.json', 'r') as f:
    content = f.read()

# Find all company_name entries using regex
company_names = re.findall(r'"company_name":\s*"([^"]+)"', content)
print(f'Total companies found: {len(company_names)}')

# Check for duplicates
name_counts = collections.Counter(company_names)
duplicates = {name: count for name, count in name_counts.items() if count > 1}

print(f'\nDuplicate company names: {len(duplicates)}')
if duplicates:
    print('Companies with duplicates:')
    for name, count in sorted(duplicates.items()):
        print(f'  "{name}": {count} occurrences')
        
# Check for empty or missing required fields
empty_names = company_names.count('')
missing_about = len(re.findall(r'"about":\s*""', content))
missing_industry = len(re.findall(r'"industry":\s*""', content))

print(f'\nData Quality Issues:')
print(f'  Empty company names: {empty_names}')
print(f'  Empty about fields: {missing_about}')
print(f'  Empty industry fields: {missing_industry}')

# Check for malformed salary ranges
salary_ranges = re.findall(r'"salary_range":\s*\[([^\]]+)\]', content)
invalid_ranges = 0
for salary_range in salary_ranges:
    try:
        values = [int(x.strip()) for x in salary_range.split(',')]
        if len(values) != 2 or values[0] >= values[1] or values[0] < 0:
            invalid_ranges += 1
    except:
        invalid_ranges += 1

print(f'  Invalid salary ranges: {invalid_ranges}')

# Check for companies in multiple industries
industries = re.findall(r'"industry":\s*"([^"]+)"', content)
company_industry_pairs = list(zip(company_names, industries))
company_industries = collections.defaultdict(set)

for company, industry in company_industry_pairs:
    company_industries[company].add(industry)

multiple_industries = {company: industries for company, industries in company_industries.items() if len(industries) > 1}

print(f'\nCompanies in multiple industries: {len(multiple_industries)}')
for company, industries in sorted(multiple_industries.items()):
    print(f'  "{company}": {sorted(industries)}')

# Check file structure
print(f'\nFile Structure Issues:')
array_starts = content.count('[{')
array_ends = content.count('}]')
print(f'  Array starts: {array_starts}')
print(f'  Array ends: {array_ends}')
print(f'  Properly closed arrays: {array_starts == array_ends}')

# Check for broken JSON
try:
    json.loads(content)
    print('  Valid JSON: Yes')
except json.JSONDecodeError as e:
    print(f'  Valid JSON: No - {e}')