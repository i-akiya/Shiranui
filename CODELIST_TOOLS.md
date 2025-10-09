# CDISC Controlled Terminology Codelist Tools

## Overview

These MCP tools provide programmatic access to CDISC Controlled Terminology codelists, enabling AI assistants and applications to retrieve standardized clinical trial terminology.

## Available Tools

### 1. `get_ct_latest_version`

Get the latest Controlled Terminology version for any CDISC standard.

**Parameters:**
- `standard` (str): CDISC standard name (default: "SDTM")

**Supported Standards:**
SDTM, ADAM, CDASH, DEFINE-XML, SEND, DDF, GLOSSARY, MRCT, PROTOCOL, QRS, QS-FT, TMF

**Example:**
```python
get_ct_latest_version("SDTM")
# Returns: {"standard": "SDTM", "latest_version": "2024-12-20", "message": "..."}

get_ct_latest_version("ADAM")
# Returns: {"standard": "ADAM", "latest_version": "2024-09-27", "message": "..."}
```

---

### 2. `get_cdisc_codelist`

Retrieve a complete CDISC Controlled Terminology codelist with all terms and metadata.

**Parameters:**
- `codelist_value` (str, required): The codelist ID or CodelistCode
- `codelist_type` (str): Match by "ID" or "CodelistCode" (default: "ID")
- `standard` (str): CDISC standard (default: "SDTM")
- `version` (str): CT version in YYYY-MM-DD format (auto-detects latest if not provided)

**Example - SDTM Age Units:**
```python
get_cdisc_codelist("AGEU", standard="SDTM")

# Returns:
{
  "codelist_info": {
    "id": "AGEU",
    "codelist_code": "C66734",
    "name": "Age Unit",
    "extensible": "No",
    "standard": "SDTM",
    "version": "2024-12-20"
  },
  "terms": [
    {"term": "DAYS", "term_code": "C25301", "decoded_value": "Days"},
    {"term": "WEEKS", "term_code": "C29844", "decoded_value": "Weeks"},
    {"term": "MONTHS", "term_code": "C29846", "decoded_value": "Months"},
    {"term": "YEARS", "term_code": "C29848", "decoded_value": "Years"}
  ],
  "term_count": 4
}
```

**Example - ADAM Derivation Type:**
```python
get_cdisc_codelist("DTYPE", standard="ADAM")

# Returns DTYPE codelist with terms like "MAXIMUM", "MINIMUM", "AVERAGE", etc.
```

**Example - By CodelistCode:**
```python
get_cdisc_codelist("C66734", codelist_type="CodelistCode", standard="SDTM")

# Returns same AGEU codelist matched by its NCI code
```

**Example - Specific Version:**
```python
get_cdisc_codelist("ACN", standard="SDTM", version="2024-09-27")

# Returns ACN (Action Taken) codelist from specific CT version
```

---

### 3. `get_ct_package_codelists`

List all codelists available in a CDISC Controlled Terminology package.

**Parameters:**
- `standard` (str): CDISC standard (default: "SDTM")
- `version` (str): CT version in YYYY-MM-DD format (auto-detects latest if not provided)

**Example:**
```python
get_ct_package_codelists("SDTM")

# Returns:
{
  "standard": "SDTM",
  "version": "2024-12-20",
  "codelist_count": 183,
  "codelists": [
    {
      "id": "ACN",
      "codelist_code": "C66767",
      "name": "Action Taken",
      "extensible": "No"
    },
    {
      "id": "AGEU",
      "codelist_code": "C66734",
      "name": "Age Unit",
      "extensible": "No"
    },
    ...
  ]
}
```

**Example - ADAM Codelists:**
```python
get_ct_package_codelists("ADAM")

# Returns all ADAM CT codelists
```

---

## Common Use Cases

### Validate Study Values
Check if a value exists in a specific codelist:
```python
codelist = get_cdisc_codelist("AGEU")
valid_values = [term["term"] for term in codelist["terms"]]
# ["DAYS", "WEEKS", "MONTHS", "YEARS"]
```

### Build Decode Mappings
Create term-to-decode mapping for data processing:
```python
codelist = get_cdisc_codelist("ACN")
decode_map = {
    term["term"]: term["decoded_value"] 
    for term in codelist["terms"]
}
# {"DOSE INCREASED": "Dose Increased", "DOSE NOT CHANGED": "Dose Not Changed", ...}
```

### Discover Available Codelists
Find all codelists in a standard:
```python
all_codelists = get_ct_package_codelists("SDTM")
codelist_names = [cl["id"] for cl in all_codelists["codelists"]]
# ["ACN", "AGEU", "ARETTYPE", ...]
```

### Check Extensibility
Determine if custom terms are allowed:
```python
codelist = get_cdisc_codelist("RACE")
is_extensible = codelist["codelist_info"]["extensible"]
# "Yes" or "No"
```

---

## Error Handling

All tools return structured error messages:

**Invalid Standard:**
```python
get_cdisc_codelist("AGEU", standard="INVALID")
# Returns: {"error": "Invalid standard 'INVALID'. Supported values are: SDTM, ADAM, ..."}
```

**Codelist Not Found:**
```python
get_cdisc_codelist("NOTREAL")
# Returns: {"warning": "The provided Codelist Value 'NOTREAL' does not exist...", ...}
```

---

## Integration with Existing Shiranui Tools

These codelist tools complement Shiranui's existing capabilities:

- **Biomedical Concepts** → Understand clinical concepts
- **Dataset Specializations** → Define dataset structures  
- **Codelists** → Validate and decode terminology

Together, they provide comprehensive access to CDISC standards!
