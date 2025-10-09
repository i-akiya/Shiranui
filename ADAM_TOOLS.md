# ADaM Variable Metadata Tools

## Overview

These MCP tools provide access to ADaM (Analysis Data Model) variable metadata from the CDISC Library API, enabling retrieval of variable definitions, labels, datatypes, and associated controlled terminology codelists.

## Available Tools

### 1. `get_adam_variable_details`

Retrieve complete metadata for a specific ADaM variable including its label, datatype, core status, description, and any associated codelists.

**Parameters:**
- `adam_variable` (str, required): The ADaM variable name (e.g., TRT01P, PARAMCD, AVAL)
- `adamig_version` (str): ADaMIG version (default: "1-3")

**Example - TRT01P (Treatment):**
```python
get_adam_variable_details("TRT01P")

# Returns:
{
  "variable": "TRT01P",
  "label": "Planned Treatment for Period 01",
  "datatype": "text",
  "core": "Req",
  "description": "Planned treatment for period 01...",
  "dataset": "ADSL",
  "adamig_version": "1-3",
  "codelist_links": [...],
  "codelists": [...]
}
```

**Example - PARAMCD (Parameter Code):**
```python
get_adam_variable_details("PARAMCD", "1-3")

# Returns variable details with associated codelists if available
```

**Example - AVAL (Analysis Value):**
```python
get_adam_variable_details("AVAL")

# Returns:
{
  "variable": "AVAL",
  "label": "Analysis Value",
  "datatype": "float",
  "core": "Req",
  "dataset": "OCCDS",
  "adamig_version": "1-3",
  ...
}
```

---

### 2. `get_adam_dataset_structure`

Get the complete structure of an ADaM dataset including all its variables.

**Parameters:**
- `dataset` (str, required): The ADaM dataset name (e.g., ADSL, ADAE, OCCDS)
- `adamig_version` (str): ADaMIG version (default: "1-3")

**Example - ADSL (Subject-Level Analysis Dataset):**
```python
get_adam_dataset_structure("ADSL")

# Returns:
{
  "dataset": "ADSL",
  "label": "Subject-Level Analysis Dataset",
  "description": "One record per subject...",
  "adamig_version": "1-3",
  "variable_count": 45,
  "variables": [
    {
      "name": "STUDYID",
      "label": "Study Identifier",
      "datatype": "text",
      "core": "Req"
    },
    {
      "name": "USUBJID",
      "label": "Unique Subject Identifier",
      "datatype": "text",
      "core": "Req"
    },
    {
      "name": "TRT01P",
      "label": "Planned Treatment for Period 01",
      "datatype": "text",
      "core": "Req"
    },
    ...
  ]
}
```

**Example - ADAE (Adverse Events Analysis Dataset):**
```python
get_adam_dataset_structure("ADAE", "1-3")

# Returns complete structure with all ADAE variables
```

**Example - OCCDS (Occurrence Data Structure):**
```python
get_adam_dataset_structure("OCCDS")

# Returns generic occurrence structure variables
```

---

## Common Use Cases

### Variable Lookup and Validation
Verify a variable exists and get its metadata:
```python
result = get_adam_variable_details("TRT01P")
if "error" not in result:
    print(f"Label: {result['label']}")
    print(f"Type: {result['datatype']}")
    print(f"Core: {result['core']}")
```

### Check Variable's Associated Codelists
```python
result = get_adam_variable_details("TRT01P")
if result.get("codelists"):
    for codelist in result["codelists"]:
        print(f"Codelist: {codelist['codelist_info']['name']}")
        for term in codelist["terms"]:
            print(f"  {term['term']} = {term['decoded_value']}")
```

### List All Variables in a Dataset
```python
result = get_adam_dataset_structure("ADSL")
for var in result["variables"]:
    print(f"{var['name']:15} {var['label']}")
```

### Find Core vs. Expected Variables
```python
result = get_adam_dataset_structure("ADSL")
core_vars = [v for v in result["variables"] if v["core"] == "Req"]
expected_vars = [v for v in result["variables"] if v["core"] == "Exp"]

print(f"Required variables: {len(core_vars)}")
print(f"Expected variables: {len(expected_vars)}")
```

### Build Data Mapping
Create a mapping of variable names to labels:
```python
result = get_adam_dataset_structure("ADSL")
var_mapping = {
    v["name"]: v["label"] 
    for v in result["variables"]
}
# {"STUDYID": "Study Identifier", "USUBJID": "Unique Subject Identifier", ...}
```

---

## Error Handling

All tools return structured error messages:

**Variable Not Found:**
```python
get_adam_variable_details("INVALID_VAR")
# Returns: {"error": "Variable 'INVALID_VAR' not found in any dataset structure..."}
```

**Invalid Dataset:**
```python
get_adam_dataset_structure("NOTREAL")
# Returns: {"error": "Could not fetch dataset structure for NOTREAL"}
```

**Invalid Version:**
```python
get_adam_variable_details("TRT01P", "9-9")
# Returns error if version doesn't exist
```

---

## Integration with Other Tools

These ADaM tools work seamlessly with other Shiranui tools:

**Complete Workflow Example:**
1. Use `get_adam_dataset_structure("ADSL")` to see all available variables
2. Use `get_adam_variable_details("TRT01P")` to get specific variable metadata
3. If variable has codelists, use `get_cdisc_codelist()` for more codelist details
4. Use Biomedical Concept tools to understand clinical concepts

**Combined Example:**
```python
# Get dataset structure
dataset = get_adam_dataset_structure("ADSL")

# Get details for each variable
for var in dataset["variables"][:5]:  # First 5 variables
    details = get_adam_variable_details(var["name"])
    print(f"{details['variable']}: {details['label']}")
    
    # Check for codelists
    if details.get("codelists"):
        print(f"  Has {len(details['codelists'])} codelist(s)")
```

---

## ADaMIG Version Support

Currently supports ADaMIG versions in format:
- `"1-3"` (hyphen format)
- `"1.3"` (dot format - automatically converted)

Default version is `"1-3"` if not specified.
