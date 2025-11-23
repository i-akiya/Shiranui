# SEND Metadata MCP Tools Documentation

## Overview

The SEND (Standard for Exchange of Nonclinical Data) Metadata MCP tools provide programmatic access to SEND Implementation Guide (SENDIG) domain and variable metadata from the CDISC Library API. These tools enable automated retrieval of nonclinical and preclinical study standards used in toxicology and safety studies submitted to regulatory agencies.

## Available Tools

### 1. `get_sendig_latest_version`

Get the latest SEND-IG version available in the CDISC Library.

**Parameters:**
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "latest_version": "3-1-1",
  "display_version": "SENDIG v3.1.1",
  "all_versions": ["3-1-1", "3-1", "3-0"],
  "total_versions": 3
}
```

**Example Usage:**
```python
result = get_sendig_latest_version()
print(f"Latest SEND-IG: {result['display_version']}")
# Output: Latest SEND-IG: SENDIG v3.1.1
```

---

### 2. `get_sendig_classes`

Get SEND domain classes (Findings, Events, Interventions, Demographics, etc.) for nonclinical studies.

**Parameters:**
- `sendig_version` (str, optional): SEND-IG version (e.g., "3-1-1" or "3.1.1"). If not provided, uses latest version
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "sendig_version": "3-1-1",
  "class_count": 7,
  "classes": [
    {
      "name": "Findings",
      "label": "Findings",
      "ordinal": 1
    },
    {
      "name": "Events",
      "label": "Events",
      "ordinal": 2
    },
    {
      "name": "Interventions",
      "label": "Interventions",
      "ordinal": 3
    }
  ]
}
```

**Example Usage:**
```python
# Get latest version classes
result = get_sendig_classes()
print(f"SEND has {result['class_count']} domain classes")

# Get specific version
result = get_sendig_classes("3-1")
for cls in result['classes']:
    print(f"{cls['name']}: {cls['label']}")
```

---

### 3. `get_sendig_domain_structure`

Get complete SEND domain structure with all variables and metadata for nonclinical studies.

**Parameters:**
- `domain` (str, required): SEND domain name (e.g., "DM", "EX", "LB", "MI", "MA")
- `sendig_version` (str, optional): SEND-IG version. If not provided, uses latest version
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "domain": "MI",
  "label": "Microscopic Findings",
  "description": "Findings observed during microscopic examination",
  "domain_class": "Findings",
  "sendig_version": "3-1-1",
  "variable_count": 25,
  "variables": [
    {
      "name": "STUDYID",
      "label": "Study Identifier",
      "datatype": "Char",
      "core": "Req",
      "description": "Unique identifier for a study.",
      "role": "Identifier",
      "ordinal": 1
    },
    {
      "name": "MISPEC",
      "label": "Specimen",
      "datatype": "Char",
      "core": "Req",
      "description": "Anatomical location of the specimen.",
      "role": "Topic",
      "ordinal": 8
    }
  ]
}
```

**Example Usage:**
```python
# Get Demographics domain
result = get_sendig_domain_structure("DM")
print(f"DM has {result['variable_count']} variables")

# Get Microscopic Findings domain
result = get_sendig_domain_structure("MI")
print(f"{result['label']} - {result['description']}")
for var in result['variables']:
    print(f"  {var['name']}: {var['label']} ({var['role']})")

# Get specific version
result = get_sendig_domain_structure("LB", sendig_version="3-1")
```

---

### 4. `get_sendig_variable_details`

Get detailed metadata for a specific SEND variable with optional codelist integration.

**Parameters:**
- `variable` (str, required): Variable name (e.g., "USUBJID", "LBTESTCD", "MISPEC")
- `domain` (str, optional): SEND domain name. If not provided, will attempt to auto-detect
- `sendig_version` (str, optional): SEND-IG version. If not provided, uses latest version
- `include_codelist` (bool, optional): If True and variable has controlled terminology, retrieve the codelist. Default False
- `headers_` (dict, optional): Custom headers for API authentication

**Returns:**
```json
{
  "variable": "MISPEC",
  "label": "Specimen",
  "domain": "MI",
  "datatype": "Char",
  "core": "Req",
  "description": "Anatomical location of the specimen for microscopic examination.",
  "role": "Topic",
  "sendig_version": "3-1-1",
  "codelist": {
    "name": "Specimen",
    "terms": [...]
  }
}
```

**Example Usage:**
```python
# Get variable with known domain
result = get_sendig_variable_details("USUBJID", "DM")
print(f"{result['variable']}: {result['label']}")
print(f"Role: {result['role']}, Core: {result['core']}")

# Auto-detect domain
result = get_sendig_variable_details("LBTESTCD")
print(f"Found in domain: {result['domain']}")

# Get variable with codelist
result = get_sendig_variable_details("MISPEC", "MI", include_codelist=True)
if result.get('codelist'):
    print(f"Codelist: {result['codelist']['name']}")
    for term in result['codelist']['terms'][:5]:
        print(f"  {term['code']}: {term['label']}")
```

---

## Common Use Cases

### 1. Build Nonclinical Study Specifications

```python
# Get all domains for toxicology study
domains = ["DM", "EX", "LB", "MI", "MA", "BW", "FW"]
for domain_code in domains:
    domain = get_sendig_domain_structure(domain_code)
    print(f"\n{domain['label']} ({domain_code}):")
    print(f"Class: {domain.get('domain_class', 'N/A')}")
    print(f"Variables: {domain['variable_count']}")
```

### 2. Map Clinical to Nonclinical Standards

```python
# Compare SDTM and SEND Demographics
sdtm_dm = get_sdtm_domain_structure("DM")
send_dm = get_sendig_domain_structure("DM")

print("SDTM DM variables:", len(sdtm_dm['variables']))
print("SEND DM variables:", len(send_dm['variables']))

# Find SEND-specific variables
send_vars = {v['name'] for v in send_dm['variables']}
sdtm_vars = {v['name'] for v in sdtm_dm['variables']}
send_only = send_vars - sdtm_vars
print(f"SEND-specific variables: {send_only}")
```

### 3. Microscopic Findings Analysis

```python
# Get complete MI domain structure for toxicology pathology
mi = get_sendig_domain_structure("MI")
print(f"Microscopic Findings Domain:")
print(f"Total variables: {mi['variable_count']}")

# Get specimen variable with codelist
specimen = get_sendig_variable_details("MISPEC", "MI", include_codelist=True)
print(f"\nSpecimen locations available:")
for term in specimen['codelist']['terms']:
    print(f"  - {term['preferredTerm']}")
```

### 4. Validate Nonclinical Data Structure

```python
# Get domain structure to validate dataset
domain = get_sendig_domain_structure("LB")
required_vars = [v['name'] for v in domain['variables'] if v['core'] == 'Req']
print(f"Required variables for LB domain: {required_vars}")

# Check variable properties
for var_name in ['LBTESTCD', 'LBTEST', 'LBORRES']:
    var = get_sendig_variable_details(var_name, "LB")
    print(f"{var['name']}: {var['label']} - Core: {var['core']}")
```

---

## SEND vs SDTM Differences

| Aspect | SEND (Nonclinical) | SDTM (Clinical) |
|--------|-------------------|-----------------|
| **Study Type** | Preclinical, Toxicology | Clinical Trials |
| **Subjects** | Animals (rats, mice, dogs, monkeys) | Humans |
| **Demographics** | Species, Strain, Sex, Age at Start | Race, Ethnicity, Sex, Age |
| **Specific Domains** | MI (Microscopic), MA (Macroscopic), BW (Body Weight), FW (Food/Water) | Medical History, Concomitant Meds |
| **Identifiers** | USUBJID (animal ID) | USUBJID (patient ID) |
| **Focus** | Safety, Toxicity, Pathology | Efficacy, Safety, Patient outcomes |
| **Regulatory Use** | IND submissions (preclinical) | NDA/BLA submissions (clinical) |

---

## SEND-Specific Domains

### Key Nonclinical Domains:

| Domain | Name | Description |
|--------|------|-------------|
| **MI** | Microscopic Findings | Histopathology observations |
| **MA** | Macroscopic Findings | Gross pathology observations |
| **BW** | Body Weights | Animal body weight measurements |
| **FW** | Food and Water Consumption | Feed and water intake |
| **OM** | Organ Measurements | Organ weights and measurements |
| **PC** | Pharmacokinetics Concentrations | Drug concentration levels |
| **PP** | Pharmacokinetics Parameters | PK parameter calculations |
| **CL** | Clinical Observations | Clinical signs and observations |

---

## Variable Core Status

- **Req** (Required): Must be present in the domain
- **Exp** (Expected): Should be present if applicable
- **Perm** (Permissible): May be included if needed

---

## Version Normalization

Tools accept version formats with either dots or dashes:
- `"3-1-1"` (API format)
- `"3.1.1"` (human-readable format)

Both are automatically normalized to the correct API format.

---

## Auto-Detection Feature

The `get_sendig_variable_details` tool includes automatic domain detection for common variables:

**Automatically searched domains:**
- DM, EX, LB, MI, OM, PC, PP, CL, MA, BW, FW

**Example:**
```python
# No need to specify domain for common variables
result = get_sendig_variable_details("USUBJID")  # Finds in DM
result = get_sendig_variable_details("LBTESTCD") # Finds in LB
result = get_sendig_variable_details("MISPEC")   # Finds in MI
```

---

## Integration with Other Tools

SEND tools integrate seamlessly with:
- **SDTM Tools**: Compare clinical vs nonclinical standards
- **CT Tools**: `get_cdisc_codelist()` for controlled terminology
- **Search**: `search_cdisc_library()` to find SEND-specific concepts

**Example - Cross-Standard Comparison:**
```python
# Compare variable definitions across standards
sdtm_var = get_sdtm_variable_details("USUBJID", "DM")
send_var = get_sendig_variable_details("USUBJID", "DM")

print("SDTM Definition:", sdtm_var['description'])
print("SEND Definition:", send_var['description'])
```

---

## Error Handling

All tools return error information when issues occur:

```python
result = get_sendig_variable_details("INVALID_VAR", "DM")
if "error" in result:
    print(f"Error: {result['error']}")
    # Output: Variable INVALID_VAR not found in domain DM
```

---

## Performance Tips

1. **Specify domain explicitly** to avoid auto-detection search overhead
2. **Use `include_codelist=False`** (default) for faster responses
3. **Cache version info** - Latest version doesn't change frequently
4. **Batch requests** - Process multiple variables from same domain together

---

## Toxicology Study Example

Complete workflow for toxicology study metadata:

```python
# 1. Get latest version
version_info = get_sendig_latest_version()
print(f"Using {version_info['display_version']}")

# 2. Get all domain classes
classes = get_sendig_classes()
print(f"\nAvailable classes: {[c['name'] for c in classes['classes']]}")

# 3. Get key domains for toxicology
domains = ['DM', 'MI', 'MA', 'BW', 'LB']
for domain_code in domains:
    domain = get_sendig_domain_structure(domain_code)
    print(f"\n{domain['label']} ({domain_code}):")
    print(f"  Class: {domain.get('domain_class')}")
    print(f"  Variables: {domain['variable_count']}")
    
    # Get key variables
    if domain_code == 'MI':
        mispec = get_sendig_variable_details('MISPEC', domain_code, include_codelist=True)
        print(f"  Specimen variable has {len(mispec['codelist']['terms'])} options")
```

---

## Related Documentation

- See `SDTM_TOOLS.md` for clinical tabulation standards
- See `CDASH_TOOLS.md` for data collection standards
- See `ADAM_TOOLS.md` for analysis standards
- See `CODELIST_TOOLS.md` for controlled terminology
- See `SEARCH_TOOLS.md` for universal CDISC Library search

---

## CDISC Library Coverage

These tools cover **100% of publicly accessible SEND-IG endpoints** in the CDISC Library API:
- ✅ Version detection and listing
- ✅ Domain class enumeration
- ✅ Complete domain structures
- ✅ Variable-level metadata
- ✅ Controlled terminology integration
- ✅ Cross-version comparison support
- ✅ Nonclinical-specific domains (MI, MA, OM, etc.)

---

## Regulatory Context

SEND is required by FDA for:
- IND (Investigational New Drug) applications
- Preclinical study submissions
- Toxicology and safety assessments
- Animal pharmacology studies

These tools help ensure compliance with regulatory requirements for nonclinical data standardization.
