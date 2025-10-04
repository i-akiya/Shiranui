# SDTM Metadata MCP Tools Documentation

## Overview

The SDTM Metadata MCP tools provide programmatic access to SDTM Implementation Guide (SDTM-IG) dataset and variable metadata from the CDISC Library API. These tools replicate the functionality of SAS macros for SDTM metadata retrieval, enabling automated access to SDTM domain structures, variable definitions, and controlled terminology codelists.

## Available Tools

### 1. `get_sdtm_latest_version`

Get the latest SDTM-IG version available in the CDISC Library.

**Parameters:**
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "latest_version": "3-4",
  "display_version": "3.4",
  "all_versions": ["3-4", "3-3", "3-2"]
}
```

**Example Usage:**
```python
result = get_sdtm_latest_version()
print(f"Latest SDTM-IG: {result['display_version']}")
```

---

### 2. `get_sdtm_classes`

Get SDTM domain classes (Findings, Events, Interventions, etc.).

**Parameters:**
- `sdtmig_version` (str, optional): SDTM-IG version (e.g., "3-4" or "3.4"). If not provided, uses latest version
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "sdtmig_version": "3-4",
  "class_count": 9,
  "classes": [
    {
      "name": "GeneralObservations",
      "label": "General Observations",
      "type": "Class"
    },
    {
      "name": "Interventions",
      "label": "Interventions",
      "type": "Class"
    }
  ]
}
```

**Available Classes:**
- **GeneralObservations** - General observation domains
- **Interventions** - Exposure, concomitant medications, substance use
- **Events** - Adverse events, medical history, protocol deviations
- **Findings** - Laboratory tests, vital signs, ECG, questionnaires
- **FindingsAbout** - Findings about events or interventions
- **SpecialPurpose** - Demographics, comments, disposition
- **TrialDesign** - Trial arms, elements, visits, inclusion/exclusion
- **StudyReference** - Disease milestones, medical history
- **Relationship** - Relationship datasets (RELREC, RELSPEC, RELSUB)

**Example Usage:**
```python
# Get all classes for SDTM-IG 3.4
result = get_sdtm_classes("3-4")
for cls in result["classes"]:
    print(f"{cls['name']}: {cls['label']}")
```

---

### 3. `get_sdtm_domain_structure`

Get complete domain structure with all variables for an SDTM domain.

**Parameters:**
- `domain` (str, required): SDTM domain code (e.g., "DM", "AE", "VS", "LB")
- `sdtmig_version` (str, optional): SDTM-IG version. If not provided, uses latest version
- `include_codelists` (bool, optional): If True, retrieves full codelist terms for variables with codelists. Default False for faster response
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "domain": "DM",
  "label": "Demographics",
  "description": "Demographic characteristics collected...",
  "class": "SpecialPurpose",
  "sdtmig_version": "3-4",
  "variable_count": 32,
  "variables": [
    {
      "name": "STUDYID",
      "label": "Study Identifier",
      "datatype": "Char",
      "core": "Req",
      "role": "Identifier",
      "ordinal": 1,
      "length": null
    },
    {
      "name": "USUBJID",
      "label": "Unique Subject Identifier",
      "datatype": "Char",
      "core": "Req",
      "role": "Identifier",
      "ordinal": 3,
      "length": null
    }
  ]
}
```

**Common SDTM Domains:**
- **DM** - Demographics
- **AE** - Adverse Events
- **VS** - Vital Signs
- **LB** - Laboratory Test Results
- **EX** - Exposure
- **CM** - Concomitant Medications
- **MH** - Medical History
- **DS** - Disposition
- **EG** - ECG Test Results
- **PE** - Physical Examinations
- **QS** - Questionnaires

**Variable Attributes:**
- **name**: Variable name (8 characters max)
- **label**: Variable label (40 characters max)
- **datatype**: "Char" or "Num"
- **core**: "Req" (Required), "Exp" (Expected), "Perm" (Permissible)
- **role**: "Identifier", "Topic", "Timing", "Qualifier", "Rule", "Record Qualifier"
- **ordinal**: Display order in dataset
- **length**: Maximum length for character variables

**Example Usage:**
```python
# Get Demographics domain structure
dm = get_sdtm_domain_structure("DM", "3-4")
print(f"Domain: {dm['domain']} - {dm['label']}")
print(f"Variables: {dm['variable_count']}")

# List all required variables
for var in dm["variables"]:
    if var["core"] == "Req":
        print(f"  {var['name']}: {var['label']}")

# Get Adverse Events domain with codelists
ae = get_sdtm_domain_structure("AE", "3-4", include_codelists=True)
```

---

### 4. `get_sdtm_variable_details`

Get detailed metadata for a specific SDTM variable.

**Parameters:**
- `variable` (str, required): Variable name (e.g., "USUBJID", "AESTDTC", "LBORRES")
- `domain` (str, optional): SDTM domain code. If not provided, will search common domains
- `sdtmig_version` (str, optional): SDTM-IG version. If not provided, uses latest version
- `include_codelist` (bool, optional): If True, retrieves full codelist terms. Default True
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "variable": "USUBJID",
  "label": "Unique Subject Identifier",
  "datatype": "Char",
  "core": "Req",
  "role": "Identifier",
  "ordinal": 3,
  "length": null,
  "domain": "DM",
  "sdtmig_version": "3-4",
  "codelist": null
}
```

**Example Usage:**
```python
# Get variable details with domain specified
usubjid = get_sdtm_variable_details("USUBJID", "DM", "3-4")
print(f"{usubjid['variable']}: {usubjid['label']}")
print(f"Core: {usubjid['core']}, Role: {usubjid['role']}")

# Automatic domain detection
aestdtc = get_sdtm_variable_details("AESTDTC")
print(f"Variable found in domain: {aestdtc['domain']}")

# Get variable with codelist
aesev = get_sdtm_variable_details("AESEV", "AE", include_codelist=True)
if aesev["codelist"]:
    print("Valid severity values:")
    for term in aesev["codelist"]["terms"]:
        print(f"  {term['term']}: {term['decoded_value']}")
```

---

## Integration with CT Codelist Tools

The SDTM tools seamlessly integrate with the existing CT Codelist tools to provide complete variable metadata including controlled terminology codelists.

**Example - Complete Variable Metadata:**
```python
# Get variable with codelist
var_details = get_sdtm_variable_details("SEX", "DM", include_codelist=True)

print(f"Variable: {var_details['variable']}")
print(f"Label: {var_details['label']}")

if var_details["codelist"]:
    codelist = var_details["codelist"]
    print(f"Codelist: {codelist['name']} ({codelist['submission_value']})")
    print("Valid values:")
    for term in codelist["terms"]:
        print(f"  {term['term']}: {term['decoded_value']}")
```

---

## Use Cases

### 1. Generate SDTM Domain Specifications

```python
# Generate specification for all variables in VS domain
vs = get_sdtm_domain_structure("VS", "3-4")

print(f"Domain: {vs['domain']} - {vs['label']}")
print(f"\nVariables ({vs['variable_count']}):")
print("-" * 80)
print(f"{'Variable':<12} {'Label':<40} {'Type':<8} {'Core':<6} {'Role'}")
print("-" * 80)

for var in vs["variables"]:
    print(f"{var['name']:<12} {var['label']:<40} {var['datatype']:<8} {var['core']:<6} {var['role']}")
```

### 2. Validate Dataset Structure

```python
# Check if dataset contains all required variables
domain = "LB"
lb_spec = get_sdtm_domain_structure(domain, "3-4")

required_vars = [v["name"] for v in lb_spec["variables"] if v["core"] == "Req"]
print(f"Required variables for {domain}:")
for var in required_vars:
    print(f"  - {var}")
```

### 3. Build Data Dictionaries

```python
# Create data dictionary with codelists
domains = ["DM", "AE", "VS", "LB"]

for domain_code in domains:
    domain = get_sdtm_domain_structure(domain_code, "3-4", include_codelists=True)
    print(f"\n{domain['domain']}: {domain['label']}")
    print("="*60)
    
    for var in domain["variables"]:
        print(f"\n{var['name']} - {var['label']}")
        print(f"  Type: {var['datatype']}, Core: {var['core']}, Role: {var['role']}")
        
        if "codelist" in var and var["codelist"]:
            cl = var["codelist"]
            print(f"  Codelist: {cl['name']} - {len(cl['terms'])} terms")
```

### 4. Create Empty SDTM Datasets (SAS-like)

```python
# Replicate SAS %make_empty_dataset functionality
def create_empty_dataset_spec(domain, version="3-4"):
    """Generate dataset specification for creating empty SDTM dataset"""
    
    spec = get_sdtm_domain_structure(domain, version)
    
    dataset_spec = {
        "name": spec["domain"],
        "label": spec["label"],
        "variables": []
    }
    
    for var in spec["variables"]:
        var_spec = {
            "name": var["name"],
            "type": "character" if var["datatype"] == "Char" else "numeric",
            "length": var["length"] if var["datatype"] == "Char" else 8,
            "label": var["label"]
        }
        dataset_spec["variables"].append(var_spec)
    
    return dataset_spec

# Usage
dm_spec = create_empty_dataset_spec("DM")
print(f"Dataset: {dm_spec['name']}")
print(f"Variables: {len(dm_spec['variables'])}")
```

### 5. Map Variables Across Domains

```python
# Find all domains that contain a specific variable
def find_variable_in_domains(variable_name, domains=None):
    """Find which domains contain a specific variable"""
    
    if domains is None:
        domains = ["DM", "AE", "VS", "LB", "EX", "CM", "MH", "DS", "EG", "PE", "QS"]
    
    found_in = []
    
    for domain in domains:
        try:
            var = get_sdtm_variable_details(variable_name, domain, include_codelist=False)
            if "error" not in var:
                found_in.append({
                    "domain": domain,
                    "label": var["label"],
                    "core": var["core"]
                })
        except:
            continue
    
    return found_in

# Usage
results = find_variable_in_domains("USUBJID")
print("USUBJID found in:")
for r in results:
    print(f"  {r['domain']}: {r['label']} (Core: {r['core']})")
```

---

## Version Support

The tools support all SDTM-IG versions available in the CDISC Library:
- **SDTM-IG v3.4** (latest, based on SDTM v2.0)
- **SDTM-IG v3.3** (based on SDTM v1.7)
- **SDTM-IG v3.2** (based on SDTM v1.4)
- Earlier versions (3.1.2, 3.1.1, etc.)

Version format accepts both:
- Hyphenated: `"3-4"`, `"3-3"`, `"3-2"`
- Dot notation: `"3.4"`, `"3.3"`, `"3.2"` (automatically converted)

---

## Error Handling

All tools return structured error responses:

```json
{
  "error": "Variable 'INVALIDVAR' not found in domain 'DM'",
  "variable": "INVALIDVAR",
  "domain": "DM"
}
```

**Common Errors:**
- Invalid domain code
- Variable not found in specified domain
- Invalid SDTM-IG version
- API connection errors

---

## Technical Notes

### API Endpoints Used

- **SDTM-IG Version:** `GET /api/mdr/sdtmig`
- **Classes:** `GET /api/mdr/sdtmig/{version}/classes`
- **Domain Metadata:** `GET /api/mdr/sdtmig/{version}/datasets/{domain}`
- **CT Codelists:** `GET /api/mdr/ct/packages/{standard}ct-{version}/codelists/{id}`

### Performance Considerations

- **Variable Metadata:** Fast (<500ms per request)
- **Domain Structure:** Moderate (<1s per domain)
- **Domain Structure with Codelists:** Slower (2-5s per domain, depending on number of variables with codelists)
- **Auto Domain Detection:** Searches up to 11 common domains, may take 2-3s

**Optimization Tips:**
- Specify domain when possible to avoid auto-detection
- Set `include_codelists=False` for faster responses when codelists not needed
- Cache results for frequently accessed domains/variables

---

## Comparison with SAS Macros

| SAS Macro | MCP Tool Equivalent |
|-----------|---------------------|
| `%make_empty_dataset(dataset=DM)` | `get_sdtm_domain_structure("DM")` |
| `&DMKEEPSTRING` | Extract `variable.name` from results |
| `&DMSORTSTRING` | Sort by `variable.ordinal` |
| Finding variable metadata | `get_sdtm_variable_details()` |
| Manual spec lookup | Automated with `include_codelists=True` |

---

## Related Tools

These SDTM tools work seamlessly with:
- **CT Codelist Tools** - For controlled terminology codelists
- **ADaM Metadata Tools** - For analysis dataset metadata
- **Biomedical Concepts Tools** - For therapeutic area concepts
- **Dataset Specialization Tools** - For domain-specific BC mappings

---

## Support

For issues or questions:
- CDISC Library API: https://api.developer.library.cdisc.org
- CDISC Standards: https://www.cdisc.org/standards/foundational/sdtmig
- GitHub: https://github.com/i-akiya/Shiranui

---

**Last Updated:** October 3, 2025  
**SDTM-IG Version:** 3.4  
**Tools Version:** 1.0
