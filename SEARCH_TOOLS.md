# CDISC Library Search Tool Documentation

## Overview

The `search_cdisc_library` MCP tool provides universal search capability across all CDISC Library content, including variables, domains, codelists, biomedical concepts, dataset specializations, and implementation guides. This tool enables discovery and exploration of CDISC standards content with a single query.

## Available Tool

### `search_cdisc_library`

Perform a universal search across all CDISC Library entities (1M+ searchable items).

**Parameters:**
- `query` (str, required): Search query string (variable name, concept, term, etc.)
- `limit` (int, optional): Maximum number of results to return (default: 100, max: 500)
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "query": "blood pressure",
  "totalHits": 450,
  "hasMore": true,
  "returnedHits": 100,
  "hits": [
    {
      "type": "Biomedical Concept",
      "name": "Diastolic Blood Pressure",
      "href": "/mdr/bc/packages/...",
      "description": "The minimum pressure..."
    },
    {
      "type": "Variable",
      "name": "DIABP",
      "href": "/mdr/sdtmig/.../variables/DIABP",
      "label": "Diastolic Blood Pressure"
    }
  ]
}
```

---

## Search Capabilities

### What You Can Search For:

1. **Variables** - SDTM, ADaM, CDASH, SEND variables
2. **Domains** - Clinical and nonclinical domain names
3. **Codelists** - Controlled terminology codelists
4. **Biomedical Concepts** - Clinical concepts and relationships
5. **Dataset Specializations** - Domain specializations
6. **Terms** - Individual codelist terms and synonyms
7. **Labels** - Variable and domain labels
8. **Definitions** - Descriptive text content

---

## Example Searches

### 1. Search for Variables

```python
# Find all variables containing "SUBJID"
result = search_cdisc_library("SUBJID", limit=50)
print(f"Found {result['totalHits']} hits")

for hit in result['hits']:
    if hit.get('type') == 'Variable':
        print(f"  {hit['name']}: {hit.get('label', 'N/A')}")
        print(f"    Standard: {hit['href']}")
```

**Output Example:**
```
Found 120 hits
  USUBJID: Unique Subject Identifier
    Standard: /mdr/sdtmig/3-4/variables/USUBJID
  SUBJID: Subject Identifier for the Study
    Standard: /mdr/sdtmig/3-4/variables/SUBJID
```

---

### 2. Search for Biomedical Concepts

```python
# Find biomedical concepts related to blood pressure
result = search_cdisc_library("blood pressure", limit=20)

bc_hits = [h for h in result['hits'] if 'biomedical' in h.get('type', '').lower()]
print(f"Found {len(bc_hits)} biomedical concepts:")

for bc in bc_hits:
    print(f"  - {bc['name']}")
    if bc.get('description'):
        print(f"    {bc['description'][:100]}...")
```

**Output Example:**
```
Found 8 biomedical concepts:
  - Diastolic Blood Pressure
    The minimum pressure...
  - Systolic Blood Pressure
    The maximum pressure...
  - Mean Arterial Blood Pressure
    The average arterial pressure...
```

---

### 3. Search for Codelists

```python
# Find codelists related to race/ethnicity
result = search_cdisc_library("RACE", limit=25)

codelist_hits = [h for h in result['hits'] if 'codelist' in h.get('type', '').lower()]
print(f"Found {len(codelist_hits)} codelists:")

for cl in codelist_hits:
    print(f"  {cl['name']}")
    print(f"    {cl['href']}")
```

**Output Example:**
```
Found 3 codelists:
  Race
    /mdr/ct/packages/sdtmct-2025-09-26/codelists/C74457
  Ethnicity
    /mdr/ct/packages/sdtmct-2025-09-26/codelists/C66790
```

---

### 4. Search Across Multiple Standards

```python
# Search for "adverse events" across all standards
result = search_cdisc_library("adverse events", limit=100)

# Group by standard
standards = {}
for hit in result['hits']:
    href = hit.get('href', '')
    if '/sdtmig/' in href:
        standards.setdefault('SDTM', []).append(hit)
    elif '/adamig/' in href:
        standards.setdefault('ADaM', []).append(hit)
    elif '/cdashig/' in href:
        standards.setdefault('CDASH', []).append(hit)
    elif '/sendig/' in href:
        standards.setdefault('SEND', []).append(hit)

for std, hits in standards.items():
    print(f"\n{std}: {len(hits)} results")
```

---

### 5. Explore Dataset Specializations

```python
# Find dataset specializations
result = search_cdisc_library("tumor", limit=30)

spec_hits = [h for h in result['hits'] if 'specialization' in h.get('type', '').lower()]
print(f"Found {len(spec_hits)} dataset specializations:")

for spec in spec_hits:
    print(f"  {spec['name']}")
```

---

### 6. Search by Medical Condition

```python
# Find all content related to diabetes
result = search_cdisc_library("diabetes", limit=50)

print(f"Total hits for 'diabetes': {result['totalHits']}")
print(f"\nTypes of content found:")

types = {}
for hit in result['hits']:
    hit_type = hit.get('type', 'Unknown')
    types[hit_type] = types.get(hit_type, 0) + 1

for type_name, count in sorted(types.items()):
    print(f"  {type_name}: {count}")
```

---

## Pagination

Handle large result sets with pagination:

```python
# Get first batch
page1 = search_cdisc_library("USUBJID", limit=50)
print(f"Page 1: {len(page1['hits'])} results")
print(f"Total available: {page1['totalHits']}")
print(f"More results available: {page1['hasMore']}")

# Note: CDISC Library API doesn't support offset-based pagination
# The 'hasMore' flag indicates if totalHits exceeds returned results
# To get all results, increase the limit (max 500)
```

---

## Common Search Patterns

### 1. Quick Variable Lookup

```python
def find_variable(var_name):
    """Find a variable across all standards"""
    result = search_cdisc_library(var_name, limit=20)
    variables = [h for h in result['hits'] if h.get('type') == 'Variable']
    
    for var in variables:
        standard = 'Unknown'
        if 'sdtmig' in var['href']: standard = 'SDTM'
        elif 'adamig' in var['href']: standard = 'ADaM'
        elif 'cdashig' in var['href']: standard = 'CDASH'
        elif 'sendig' in var['href']: standard = 'SEND'
        
        print(f"[{standard}] {var['name']}: {var.get('label', 'N/A')}")

# Usage
find_variable("AVAL")
```

---

### 2. Explore Related Concepts

```python
def explore_concept(term):
    """Find all CDISC content related to a medical concept"""
    result = search_cdisc_library(term, limit=100)
    
    print(f"\nExploring '{term}':")
    print(f"Total hits: {result['totalHits']}\n")
    
    # Group by type
    by_type = {}
    for hit in result['hits']:
        hit_type = hit.get('type', 'Other')
        by_type.setdefault(hit_type, []).append(hit['name'])
    
    for hit_type, names in sorted(by_type.items()):
        print(f"{hit_type} ({len(names)}):")
        for name in names[:5]:  # Show first 5
            print(f"  - {name}")
        if len(names) > 5:
            print(f"  ... and {len(names) - 5} more")
        print()

# Usage
explore_concept("hemoglobin")
```

---

### 3. Find Implementation Guide Content

```python
def find_in_guide(query, guide_type='sdtmig'):
    """Search within a specific implementation guide"""
    result = search_cdisc_library(query, limit=100)
    
    guide_hits = [h for h in result['hits'] if guide_type in h.get('href', '')]
    print(f"Found {len(guide_hits)} results in {guide_type.upper()}:")
    
    for hit in guide_hits[:10]:
        print(f"  {hit.get('name')}: {hit.get('label', hit.get('description', 'N/A'))}")

# Usage
find_in_guide("laboratory", "sdtmig")
find_in_guide("parameter", "adamig")
find_in_guide("medication", "cdashig")
```

---

## Search Tips

### 1. **Use Specific Terms**
- ✅ Good: `"USUBJID"`, `"diastolic blood pressure"`
- ❌ Less useful: `"id"`, `"pressure"`

### 2. **Search by Standards**
```python
# To find SEND-specific content, search SEND terms
search_cdisc_library("MISPEC")  # Microscopic findings specimen

# To find ADaM content, search analysis terms
search_cdisc_library("PARAMCD")  # Parameter code
```

### 3. **Combine with Specific Tools**
```python
# Step 1: Search to discover
results = search_cdisc_library("vital signs", limit=20)

# Step 2: Get detailed info with specific tool
for hit in results['hits']:
    if hit['name'] == 'VS':
        vs_domain = get_sdtm_domain_structure("VS")
        print(f"VS Domain has {vs_domain['variable_count']} variables")
```

### 4. **Use Wildcards and Partial Matches**
The API supports fuzzy matching:
```python
# These all work
search_cdisc_library("AESTDT")   # Exact
search_cdisc_library("adverse")  # Partial word
search_cdisc_library("AE")       # Abbreviation
```

---

## Integration with Other Tools

### Workflow Example: Complete Variable Investigation

```python
# 1. Search for variable
search_result = search_cdisc_library("LBTEST", limit=10)
print(f"Found {search_result['totalHits']} hits")

# 2. Identify the standard
for hit in search_result['hits']:
    if hit['name'] == 'LBTEST':
        print(f"Found in: {hit['href']}")
        
        # 3. Get detailed metadata
        if 'sdtmig' in hit['href']:
            var_details = get_sdtm_variable_details("LBTEST", "LB")
            print(f"Label: {var_details['label']}")
            print(f"Core: {var_details['core']}")
            print(f"Role: {var_details['role']}")
```

---

## Result Structure

Each hit in the results contains:

```json
{
  "type": "Variable | Codelist | Biomedical Concept | Domain | etc.",
  "name": "Display name or code",
  "href": "/mdr/path/to/resource",
  "label": "Human-readable label (if applicable)",
  "description": "Description text (if applicable)",
  "title": "Alternative title field"
}
```

**Note:** Not all fields are present for all hit types. Always check for field existence.

---

## Performance Considerations

1. **Limit Your Results**
   - Use `limit` parameter to control response size
   - Default 100 is good for most searches
   - Max 500 for comprehensive searches

2. **Specific vs. Broad Searches**
   - Specific: Fast, targeted results (`"USUBJID"`)
   - Broad: Slower, more results (`"subject"`)

3. **Filter Client-Side**
   - Get larger result set and filter by type
   - More efficient than multiple searches

---

## Common Use Cases

### 1. **Variable Discovery**
Find variables across all standards for mapping exercises.

### 2. **Concept Exploration**  
Discover biomedical concepts and their CDISC representations.

### 3. **Terminology Lookup**
Find codelists and terms for validation rules.

### 4. **Cross-Standard Analysis**
Compare how concepts are represented across SDTM, ADaM, CDASH, SEND.

### 5. **Implementation Guide Navigation**
Explore domains and variables before detailed queries.

---

## Error Handling

```python
result = search_cdisc_library("test query")

if "error" in result:
    print(f"Search error: {result['error']}")
elif result['totalHits'] == 0:
    print("No results found")
else:
    print(f"Found {result['totalHits']} results")
```

---

## Related Documentation

- See `SDTM_TOOLS.md` for SDTM-specific queries
- See `ADAM_TOOLS.md` for ADaM-specific queries  
- See `CDASH_TOOLS.md` for CDASH-specific queries
- See `SEND_TOOLS.md` for SEND-specific queries
- See `CODELIST_TOOLS.md` for controlled terminology

---

## Complete Example: Research Workflow

```python
# Research workflow for "hemoglobin" variable mapping

# Step 1: Universal search
print("=== Step 1: Search CDISC Library ===")
results = search_cdisc_library("hemoglobin", limit=50)
print(f"Found {results['totalHits']} total hits")

# Step 2: Identify relevant hits
print("\n=== Step 2: Identify Standards ===")
for hit in results['hits']:
    if hit.get('type') == 'Variable':
        print(f"Variable: {hit['name']} - {hit.get('label')}")
        print(f"  Location: {hit['href']}")

# Step 3: Get detailed SDTM info
print("\n=== Step 3: SDTM Details ===")
sdtm_hgb = get_sdtm_variable_details("LBTEST", "LB")
print(f"SDTM LBTEST: {sdtm_hgb['label']}")
print(f"Role: {sdtm_hgb['role']}, Core: {sdtm_hgb['core']}")

# Step 4: Get associated codelist
print("\n=== Step 4: Controlled Terminology ===")
codelist = get_cdisc_codelist("C67153", standard="SDTM")
hgb_terms = [t for t in codelist['terms'] if 'HEMOGLOBIN' in t['code'].upper()]
print(f"Hemoglobin test codes:")
for term in hgb_terms:
    print(f"  {term['code']}: {term['label']}")

# Step 5: Check ADaM representation
print("\n=== Step 5: ADaM Analysis Variable ===")
adam_result = search_cdisc_library("hemoglobin PARAM", limit=20)
adam_hits = [h for h in adam_result['hits'] if 'adamig' in h.get('href', '')]
if adam_hits:
    print(f"Found in ADaM: {adam_hits[0]['name']}")
```

---

## Best Practices

1. ✅ **Start broad, then narrow** - Use search to discover, then use specific tools
2. ✅ **Filter results by type** - Group hits by type for better organization
3. ✅ **Use with other tools** - Search is a discovery tool, not a replacement
4. ✅ **Cache common searches** - Popular searches don't change frequently
5. ✅ **Validate hits** - Not all search results may be relevant to your need

---

## CDISC Library Coverage

This tool searches across **1M+ CDISC Library entities**:
- ✅ All SDTM-IG variables and domains
- ✅ All ADaM-IG variables and datasets
- ✅ All CDASH-IG fields and domains
- ✅ All SEND-IG variables and domains
- ✅ All Biomedical Concepts
- ✅ All Controlled Terminology codelists and terms
- ✅ All Dataset Specializations
- ✅ Historical versions of all standards

**This is the most powerful discovery tool in the Shiranui MCP toolkit!** 🔍
