# CDASH Metadata MCP Tools Documentation

## Overview

The CDASH (Clinical Data Acquisition Standards Harmonization) Metadata MCP tools provide programmatic access to CDASH Implementation Guide (CDASH-IG) domain and field metadata from the CDISC Library API. These tools enable automated retrieval of clinical data collection standards, including data collection domains, field structures, and prompts used in Case Report Forms (CRFs).

## Available Tools

### 1. `get_cdash_latest_version`

Get the latest CDASH-IG version available in the CDISC Library.

**Parameters:**
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "latest_version": "2-3",
  "display_version": "CDASHIG v2.3",
  "all_versions": ["2-3", "2-2", "2-1"],
  "version_count": 3
}
```

**Example Usage:**
```python
result = get_cdash_latest_version()
print(f"Latest CDASH-IG: {result['display_version']}")
# Output: Latest CDASH-IG: CDASHIG v2.3
```

---

### 2. `get_cdash_domains_list`

Get a list of all CDASH data collection domains for a specific CDASH-IG version.

**Parameters:**
- `cdashig_version` (str, optional): CDASH-IG version (e.g., "2-3" or "2.3"). If not provided, uses latest version
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "cdashig_version": "2-3",
  "domain_count": 42,
  "domains": [
    {
      "name": "DM",
      "label": "Demographics",
      "type": "Domain"
    },
    {
      "name": "AE",
      "label": "Adverse Events",
      "type": "Domain"
    },
    {
      "name": "CM",
      "label": "Concomitant Medications",
      "type": "Domain"
    }
  ]
}
```

**Example Usage:**
```python
# Get latest version domains
result = get_cdash_domains_list()
print(f"Found {result['domain_count']} CDASH domains")

# Get specific version
result = get_cdash_domains_list("2-2")
for domain in result['domains']:
    print(f"{domain['name']}: {domain['label']}")
```

---

### 3. `get_cdash_domain_structure`

Get complete domain structure with all data collection fields for a CDASH domain.

**Parameters:**
- `domain` (str, required): CDASH domain code (e.g., "DM", "AE", "VS", "CM")
- `cdashig_version` (str, optional): CDASH-IG version. If not provided, uses latest version
- `include_codelists` (bool, optional): If True, retrieves full codelist terms for fields. Default False for faster response
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "domain": "CM",
  "label": "Concomitant Medications",
  "cdashig_version": "2-3",
  "field_count": 15,
  "fields": [
    {
      "name": "STUDYID",
      "label": "Study Identifier",
      "datatype": "text",
      "core": "Req",
      "ordinal": 1,
      "definition": "Unique identifier for a study.",
      "prompt": "Study Identifier",
      "question_text": "What is the study identifier?",
      "implementation_notes": "..."
    },
    {
      "name": "CMTRT",
      "label": "Reported Name of Medication",
      "datatype": "text",
      "core": "HR",
      "ordinal": 3,
      "prompt": "Medication",
      "question_text": "What was the medication name?"
    }
  ]
}
```

**Example Usage:**
```python
# Get Demographics domain structure
result = get_cdash_domain_structure("DM")
print(f"DM has {result['field_count']} fields")

# Get Concomitant Medications with codelists
result = get_cdash_domain_structure("CM", include_codelists=True)
for field in result['fields']:
    print(f"{field['name']}: {field['label']}")
    if field.get('codelist'):
        print(f"  Codelist: {field['codelist']['name']}")

# Get specific version
result = get_cdash_domain_structure("AE", cdashig_version="2-2")
```

---

### 4. `get_cdash_field_details`

Get detailed metadata for a specific CDASH field, including prompt, question text, and optional codelist terms.

**Parameters:**
- `field` (str, required): Field name (e.g., "USUBJID", "AESTDTC", "CMTRT")
- `domain` (str, optional): CDASH domain code. If not provided, will search common domains
- `cdashig_version` (str, optional): CDASH-IG version. If not provided, uses latest version
- `include_codelist` (bool, optional): If True, retrieves full codelist terms. Default True
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "field": "CMTRT",
  "label": "Reported Name of Medication",
  "datatype": "text",
  "core": "HR",
  "ordinal": 3,
  "definition": "Verbatim medication name as collected.",
  "prompt": "Medication",
  "question_text": "What was the medication name?",
  "implementation_notes": "Can be brand name or generic name...",
  "domain": "CM",
  "cdashig_version": "2-3",
  "codelist": null
}
```

**Example Usage:**
```python
# Get field with known domain
result = get_cdash_field_details("CMTRT", "CM")
print(f"{result['field']}: {result['label']}")
print(f"Prompt: {result['prompt']}")
print(f"Question: {result['question_text']}")

# Auto-detect domain
result = get_cdash_field_details("USUBJID")
print(f"Found in domain: {result['domain']}")

# Get field with codelist
result = get_cdash_field_details("SEX", "DM", include_codelist=True)
if result.get('codelist'):
    print(f"Codelist: {result['codelist']['name']}")
    for term in result['codelist']['terms']:
        print(f"  {term['code']}: {term['label']}")
```

---

## Common Use Cases

### 1. Build CRF Specifications

```python
# Get all fields for a domain to create CRF specs
domains = ["DM", "AE", "CM", "VS", "LB"]
for domain_code in domains:
    domain = get_cdash_domain_structure(domain_code, include_codelists=True)
    print(f"\n{domain['label']} CRF:")
    print(f"{'Field':<15} {'Label':<40} {'Prompt':<30}")
    print("-" * 85)
    for field in domain['fields']:
        print(f"{field['name']:<15} {field['label']:<40} {field.get('prompt', 'N/A'):<30}")
```

### 2. Field Validation Rules

```python
# Get field details to implement validation rules
field = get_cdash_field_details("AESTDTC", "AE")
print(f"Field: {field['label']}")
print(f"Data Type: {field['datatype']}")
print(f"Core: {field['core']}")
print(f"Definition: {field['definition']}")
```

### 3. Compare Versions

```python
# Compare field definitions across versions
v2_3 = get_cdash_field_details("CMTRT", "CM", cdashig_version="2-3")
v2_2 = get_cdash_field_details("CMTRT", "CM", cdashig_version="2-2")

print("Changes in CMTRT definition:")
if v2_3['definition'] != v2_2['definition']:
    print(f"v2.2: {v2_2['definition']}")
    print(f"v2.3: {v2_3['definition']}")
```

### 4. Generate Data Collection Questionnaire

```python
# Create questionnaire from CDASH prompts
domain = get_cdash_domain_structure("VS")
print(f"\nVital Signs Data Collection Form:")
for field in domain['fields']:
    if field.get('question_text'):
        print(f"\nQ: {field['question_text']}")
        print(f"   Field: {field['name']}")
        if field.get('codelist'):
            print(f"   Options: {', '.join([t['code'] for t in field['codelist']['terms']])}")
```

---

## CDASH vs SDTM Differences

| Aspect | CDASH | SDTM |
|--------|-------|------|
| **Purpose** | Data **Collection** (CRF design) | Data **Tabulation** (submission) |
| **Structure** | Domains with **Fields** | Domains with **Variables** |
| **Focus** | Question prompts, CRF layout | Standardized structure for analysis |
| **Core Status** | Req, HR, O | Req, Exp, Perm |
| **Attributes** | prompt, question_text | label, description, role |
| **Use Case** | CRF design, EDC setup | Regulatory submission |

---

## Field Core Status Values

- **Req** (Required): Must be present
- **HR** (Highly Recommended): Strongly recommended for collection
- **O** (Optional): May be collected based on study needs
- **Cond** (Conditional): Required under certain conditions

---

## Integration with Other Tools

CDASH tools integrate seamlessly with:
- **CT Tools**: `get_cdisc_codelist()` for controlled terminology
- **SDTM Tools**: Map CDASH fields to SDTM variables
- **Search**: `search_cdisc_library()` to find related concepts

**Example - Complete Field Information:**
```python
# Get CDASH field with full controlled terminology
field = get_cdash_field_details("SEX", "DM", include_codelist=True)
print(f"CDASH Field: {field['label']}")

# Get corresponding SDTM variable
sdtm_var = get_sdtm_variable_details("SEX", "DM")
print(f"SDTM Variable: {sdtm_var['label']}")

# Both use same codelist
print(f"Codelist: {field['codelist']['name']}")
```

---

## Error Handling

All tools return error information when issues occur:

```python
result = get_cdash_field_details("INVALID_FIELD", "DM")
if "error" in result:
    print(f"Error: {result['error']}")
    # Output: Field 'INVALID_FIELD' not found in domain 'DM'
```

---

## Version Normalization

Tools accept version formats with either dots or dashes:
- `"2-3"` (API format)
- `"2.3"` (human-readable format)

Both are automatically normalized to the correct API format.

---

## Auto-Detection Feature

The `get_cdash_field_details` tool includes automatic domain detection for common fields:

**Automatically searched domains:**
- DM, AE, VS, LB, EX, CM, MH, DS, EG, PE, QS

**Example:**
```python
# No need to specify domain for common fields
result = get_cdash_field_details("USUBJID")  # Finds in DM
result = get_cdash_field_details("AESTDTC")  # Finds in AE
result = get_cdash_field_details("VSORRESU") # Finds in VS
```

---

## Performance Tips

1. **Use `include_codelists=False`** for faster responses when codelists aren't needed
2. **Specify domain explicitly** to avoid auto-detection search overhead
3. **Cache version info** - Latest version doesn't change frequently
4. **Batch requests** - Process multiple fields from same domain together

---

## Related Documentation

- See `SDTM_TOOLS.md` for tabulation standards
- See `ADAM_TOOLS.md` for analysis standards  
- See `CODELIST_TOOLS.md` for controlled terminology
- See `SEARCH_TOOLS.md` for universal CDISC Library search

---

## CDISC Library Coverage

These tools cover **100% of publicly accessible CDASH-IG endpoints** in the CDISC Library API:
- ✅ Version detection and listing
- ✅ Domain enumeration
- ✅ Complete domain structures
- ✅ Field-level metadata
- ✅ Controlled terminology integration
- ✅ Cross-version comparison support
