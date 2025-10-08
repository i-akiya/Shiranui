import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CDISC Library Retriever")

headers = {
    "api-key": os.getenv('CDISC_LIBRARY_API_KEY'),
    "accept": "application/json"
}


def api(endpoint_url: str, headers_ = None)-> requests.Response:
    try:
        if headers_ is None:
            response = requests.get(endpoint_url, headers=headers)
            response.raise_for_status()
            return response
        else:
            response = requests.get(endpoint_url, headers=headers_)
            response.raise_for_status()
            return response

    except requests.exceptions.HTTPError as error_http:
        raise error_http
    except requests.exceptions.ConnectionError as error_connection:
        raise error_connection
    except requests.exceptions.Timeout as time_out_error:
        raise time_out_error
    except requests.exceptions.RequestException as other_error:
        raise other_error


# MCP for Biomedical Concepts V2
@mcp.tool(name="get_latest_bc_list")
async def get_latest_bc_list(headers_ = None) -> dict:
    """
    Get Latest Biomedical Concept List from CDISC Library

    Usage:
        get_latest_bc_list()
    """
    url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()

@mcp.tool(name="get_latest_bc_cat")
def get_latest_bc_cat(headers_ = None) -> dict:
    """
    Get Latest Biomedical Concept Categories from CDISC Library

    Usage:
        get_latest_bc_cat()
    """
    url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/categories"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


@mcp.tool(name="get_latest_bc")
def get_latest_bc(concept_id: str, headers_ = None) -> dict:
    """
    Get latest Biomedical Concept specified by concept_id from CDISC Library

    Args:
        concept_id (str): The ID of the Biomedical Concept to retrieve.

    Usage:
        get_latest_bc_cat("C105585")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts/{concept_id}"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


@mcp.tool(name="get_bc_package_list")
def get_bc_package_list(headers_ = None) -> dict:
    """
    Get Biomedical Concept Package List from CDISC Library

    Usage:
        get_bc_package_list()
    """
    url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


@mcp.tool(name="get_bc_for_package")
def get_bc_for_package(package: str, biomedicalconcept_id: str, headers_ = None) -> dict:
    """
    Get a specific Biomedical Concept from a specific package

    Args:
        package (str): The ID of the package to retrieve biomedical concepts from.
        biomedicalconcept_id (str): The ID of the Biomedical Concept to retrieve.

    Usage:
        get_bc_for_package("PACKAGE", "BIOM EDICALCONCEPT_ID")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package}/biomedicalconcepts/{biomedicalconcept_id}"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


@mcp.tool(name="get_bc_list_for_package")
def get_bc_list_for_package(package: str, headers_ = None) -> dict:
    """
    Get Biomedical Concept list for a specific Package

    Args:
        package(str): The ID of the Package to retrieve biomedical concept list from.

    Usage:
        get_bc_package("PACKAGE")
    """
    url=f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/packages/{package}/biomedicalconcepts"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


# MCP for SDTM Dataset Specialization
@mcp.tool(name="get_latest_bc_dataset_specializations")
def get_latest_bc_dataset_specializations(biomedicalconcept: str, headers_ = None) -> dict:
    """
    Get latest Biomedical Concept Dataset Specializations List from CDISC Library

    Args:
        biomedicalconcept (str): The biomedical concept to retrieve dataset specializations for.

    Usage:
        get_latest_bc_dataset_specializations("C105585")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/datasetspecializations?biomedicalconcept={biomedicalconcept}"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


@mcp.tool(name="get_latest_sdtm_dataset_specializations_list")
def get_latest_sdtm_dataset_specializations_list(domain: str, headers_ = None) -> dict:
    """
    Get Latest SDTM Dataset Specializations List for a specific domain

    Args:
        domain (str): The domain to retrieve dataset specializations for.

    Usage:
        get_latest_sdtm_dataset_specializations("DM")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/datasetspecializations?domain={domain}"

    print(headers_)
    if headers_ is None:
        response = api(endpoint_url=url)
    else:
        response = api(endpoint_url=url, headers_ = headers)
    return response.json()


@mcp.tool(name="get_latest_sdtm_specialization")
def get_latest_sdtm_specialization(dataset_specialization_id: str, headers_ = None) -> dict:
    """
    Get Latest SDTM Specialization for a specific specialization ID

    Args:
        dataset_specialization_id (str): The specialization ID to retrieve details for.

    Usage:
        get_latest_sdtm_specialization("SYSBP")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/datasetspecializations/{dataset_specialization_id}"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)
    return response.json()


@mcp.tool(name="get_sdtm_dataset_specialization_domain_list")
def get_sdtm_dataset_specialization_domain_list(headers_ = None) -> dict:
    """
    Get SDTM Dataset Specialization Domain List from CDISC Library

    Usage:
        get_sdtm_dataset_specialization_domain_list()
    """
    url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/domains"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_ = headers)

    return response.json()


@mcp.tool()
def get_sdtm_dataset_specialization_for_package(package: str, datasetspecialization: str, headers_ = None) -> dict:
    """
    Get SDTM Dataset Specialization for a specific package and dataset specialization

    Args:
        package (str): The ID of the package to retrieve dataset specializations from.
        datasetspecialization (str): The ID of the dataset specialization to retrieve.

    Usage:
        get_sdtm_dataset_specialization_for_package("PACKAGE", "DATASET_SPECIFICATION")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/packages/{package}/datasetspecializations/{datasetspecialization}"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_ = headers)

    return response.json()


@mcp.tool()
def get_sdtm_dataset_specialization_package_list(headers_ = None) -> dict:
    """
    Get SDTM Dataset Specialization Package List from CDISC Library

    Usage:
        get_sdtm_dataset_specialization_package_list()
    """
    url="https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/packages"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_ = headers)

    return response.json()


@mcp.tool(name="get_sdtm_dataset_specialization_list_for_package")
def get_sdtm_dataset_specialization_list_for_package(package: str, headers_ = None) -> dict:
    """
    Get SDTM Dataset Specializations List for a specific Package

    Args:
        package(str): The ID of the package to retrieve dataset specializations list from.

    Usage:
        get_sdtm_dataset_specialization_list_for_package("PACKAGE")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/packages/{package}/datasetspecializations"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_=headers_)

    return response.json()


# MCP for Controlled Terminology Codelists
VALID_STANDARDS = [
    "SDTM", "ADAM", "CDASH", "DEFINE-XML", "SEND", 
    "DDF", "GLOSSARY", "MRCT", "PROTOCOL", "QRS", "QS-FT", "TMF"
]

def get_latest_ct_version(standard: str, headers_ = None, return_all: bool = False):
    """
    Fetch the latest Controlled Terminology version for a given standard
    
    Args:
        standard: The CDISC standard (e.g., SDTM, ADAM, CDASH)
        headers_: Optional custom headers
        return_all: If True, returns tuple of (latest, all_versions), otherwise just latest
    
    Returns:
        If return_all=False: The latest version date in YYYY-MM-DD format
        If return_all=True: Tuple of (latest_version, all_versions_list)
    """
    standard_upper = standard.upper()
    
    if standard_upper not in VALID_STANDARDS:
        raise ValueError(f"Invalid standard '{standard}'. Supported values are: {', '.join(VALID_STANDARDS)}")
    
    url = "https://api.library.cdisc.org/api/mdr/ct/packages"
    response = api(url, headers_=headers_)
    data = response.json()
    
    versions = []
    if "_links" in data and "packages" in data["_links"]:
        standard_pattern = f"{standard.lower()}ct-"
        for package in data["_links"]["packages"]:
            href = package.get("href", "")
            
            if standard_pattern in href:
                parts = href.split(standard_pattern)
                if len(parts) == 2:
                    version_date = parts[1].strip()
                    if len(version_date) == 10 and version_date.count("-") == 2:
                        try:
                            year, month, day = version_date.split("-")
                            if len(year) == 4 and len(month) == 2 and len(day) == 2:
                                versions.append(version_date)
                        except (ValueError, AttributeError):
                            continue
    
    if not versions:
        available_packages = [pkg.get("href", "") for pkg in data.get("_links", {}).get("packages", [])[:5]]
        raise Exception(
            f"No versions found for standard '{standard}'. "
            f"Expected href format: '/mdr/ct/packages/{standard.lower()}ct-YYYY-MM-DD'. "
            f"Sample available packages: {', '.join(available_packages)}"
        )
    
    versions.sort(reverse=True)
    if return_all:
        return versions[0], versions
    return versions[0]


@mcp.tool(name="get_ct_latest_version")
def get_ct_latest_version_tool(standard: str = "SDTM", headers_ = None) -> dict:
    """
    Get the latest Controlled Terminology version for a CDISC standard
    
    Args:
        standard: The CDISC standard (SDTM, ADAM, CDASH, etc.). Default is SDTM.
    
    Usage:
        get_ct_latest_version_tool("SDTM")
        get_ct_latest_version_tool("ADAM")
    
    Returns:
        Dictionary with standard, latest version, display version, and all available versions
    """
    try:
        latest_version, all_versions = get_latest_ct_version(standard, headers_=headers_, return_all=True)
        return {
            "standard": standard.upper(),
            "latest_version": latest_version,
            "display_version": latest_version,
            "all_versions": all_versions,
            "message": f"Latest {standard.upper()} CT version is {latest_version}"
        }
    except Exception as e:
        return {
            "error": str(e),
            "standard": standard
        }


@mcp.tool(name="get_cdisc_codelist")
def get_cdisc_codelist(
    codelist_value: str,
    codelist_type: str = "ID",
    standard: str = "SDTM",
    version: str = None,
    headers_ = None
) -> dict:
    """
    Retrieve CDISC Controlled Terminology codelist with terms and metadata
    
    Args:
        codelist_value: The codelist name (e.g., AGEU, PARAMCD, ACN, DTYPE)
        codelist_type: Match by 'ID' or 'CodelistCode'. Default is 'ID'.
        standard: CDISC standard (SDTM, ADAM, CDASH, etc.). Default is 'SDTM'.
        version: CT version in YYYY-MM-DD format. If not provided, fetches latest.
    
    Usage:
        get_cdisc_codelist("AGEU")
        get_cdisc_codelist("ACN", standard="SDTM")
        get_cdisc_codelist("DTYPE", standard="ADAM")
        get_cdisc_codelist("AGEU", version="2024-12-20")
        get_cdisc_codelist("C66734", codelist_type="CodelistCode")
    
    Returns:
        Dictionary containing codelist metadata and all terms with their decoded values
    """
    try:
        standard_upper = standard.upper()
        
        if standard_upper not in VALID_STANDARDS:
            return {
                "error": f"Invalid standard '{standard}'. Supported values are: {', '.join(VALID_STANDARDS)}"
            }
        
        if not codelist_value:
            return {
                "error": "You must specify a codelist_value (e.g., AGEU for SDTM or DTYPE for ADaM)"
            }
        
        if codelist_type.upper() not in ["ID", "CODELISTCODE"]:
            return {
                "error": "codelist_type must be either 'ID' or 'CodelistCode'"
            }
        
        if not version:
            version = get_latest_ct_version(standard, headers_=headers_)
        
        api_standard = f"{standard.lower()}ct"
        url = f"https://api.library.cdisc.org/api/mdr/ct/packages/{api_standard}-{version}"
        
        response = api(url, headers_=headers_)
        ct_data = response.json()
        
        if "codelists" not in ct_data:
            return {
                "error": "No codelists found in the CT package",
                "standard": standard_upper,
                "version": version
            }
        
        target_codelist = None
        
        for codelist in ct_data["codelists"]:
            if codelist_type.upper() == "ID":
                if codelist.get("submissionValue", "").upper() == codelist_value.upper():
                    target_codelist = codelist
                    break
            elif codelist_type.upper() == "CODELISTCODE":
                if codelist.get("conceptId", "").upper() == codelist_value.upper():
                    target_codelist = codelist
                    break
        
        if not target_codelist:
            return {
                "warning": f"The provided Codelist Value '{codelist_value}' does not exist in the {standard_upper} Controlled Terminology version {version}",
                "standard": standard_upper,
                "version": version,
                "codelist_type": codelist_type,
                "message": "Please check if your value is correct or if it exists in the specified standard"
            }
        
        extensible_yn = "Yes" if target_codelist.get("extensible") == "Yes" else "No"
        
        terms = []
        if "terms" in target_codelist:
            for term in target_codelist["terms"]:
                terms.append({
                    "term": term.get("submissionValue", ""),
                    "term_code": term.get("conceptId", ""),
                    "decoded_value": term.get("preferredTerm", "")
                })
        
        result = {
            "codelist_info": {
                "id": target_codelist.get("submissionValue", ""),
                "codelist_code": target_codelist.get("conceptId", ""),
                "name": target_codelist.get("name", ""),
                "extensible": extensible_yn,
                "standard": standard_upper,
                "version": version
            },
            "terms": terms,
            "term_count": len(terms)
        }
        
        return result
        
    except Exception as e:
        return {
            "error": str(e),
            "codelist_value": codelist_value,
            "standard": standard,
            "version": version if version else "auto-detect"
        }


@mcp.tool(name="get_ct_package_codelists")
def get_ct_package_codelists(
    standard: str = "SDTM",
    version: str = None,
    headers_ = None
) -> dict:
    """
    Get all codelists available in a CDISC Controlled Terminology package
    
    Args:
        standard: CDISC standard (SDTM, ADAM, CDASH, etc.). Default is 'SDTM'.
        version: CT version in YYYY-MM-DD format. If not provided, fetches latest.
    
    Usage:
        get_ct_package_codelists("SDTM")
        get_ct_package_codelists("ADAM", "2024-12-20")
    
    Returns:
        Dictionary containing all codelists with their IDs and names
    """
    try:
        standard_upper = standard.upper()
        
        if standard_upper not in VALID_STANDARDS:
            return {
                "error": f"Invalid standard '{standard}'. Supported values are: {', '.join(VALID_STANDARDS)}"
            }
        
        if not version:
            version = get_latest_ct_version(standard, headers_=headers_)
        
        api_standard = f"{standard.lower()}ct"
        url = f"https://api.library.cdisc.org/api/mdr/ct/packages/{api_standard}-{version}"
        
        response = api(url, headers_=headers_)
        ct_data = response.json()
        
        codelists = []
        if "codelists" in ct_data:
            for codelist in ct_data["codelists"]:
                codelists.append({
                    "id": codelist.get("submissionValue", ""),
                    "codelist_code": codelist.get("conceptId", ""),
                    "name": codelist.get("name", ""),
                    "extensible": "Yes" if codelist.get("extensible") == "Yes" else "No"
                })
        
        return {
            "standard": standard_upper,
            "version": version,
            "codelist_count": len(codelists),
            "codelists": codelists
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "standard": standard,
            "version": version if version else "auto-detect"
        }


# MCP for ADaM Variable Metadata
def find_adam_variable_dataset(adam_variable: str, adamig_version: str, headers_ = None):
    """
    Find which dataset structure contains a given ADaM variable
    
    Args:
        adam_variable: The ADaM variable name (e.g., TRT01P, PARAMCD)
        adamig_version: ADaMIG version in hyphen format (e.g., "1-3")
        headers_: Optional custom headers
    
    Returns:
        Dataset name (e.g., ADSL, OCCDS) or None if not found
    """
    adamig_version_hyphen = adamig_version.replace(".", "-")
    
    # First, get the list of datastructures
    url = f"https://api.library.cdisc.org/api/mdr/adam/adamig-{adamig_version_hyphen}/datastructures"
    response = api(url, headers_=headers_)
    data = response.json()
    
    if not data or "_links" not in data or "dataStructures" not in data["_links"]:
        return None
    
    # Iterate through each datastructure and query its variables
    for ds_link in data["_links"]["dataStructures"]:
        href = ds_link.get("href", "")
        if not href:
            continue
        
        # Extract dataset name from href (e.g., "/mdr/adam/adamig-1-3/datastructures/ADSL" -> "ADSL")
        ds_name = href.split("/")[-1]
        if not ds_name:
            continue
        
        # Query individual dataset to get its variables
        ds_url = f"https://api.library.cdisc.org/api/mdr/adam/adamig-{adamig_version_hyphen}/datastructures/{ds_name}"
        try:
            ds_response = api(ds_url, headers_=headers_)
            ds_data = ds_response.json()
            
            # Check analysisVariables
            if "analysisVariables" in ds_data:
                for var in ds_data["analysisVariables"]:
                    if var.get("name", "").upper() == adam_variable.upper():
                        return ds_name
            
            # Check analysisVariableSets
            if "analysisVariableSets" in ds_data:
                for var_set in ds_data["analysisVariableSets"]:
                    if "analysisVariables" in var_set:
                        for var in var_set["analysisVariables"]:
                            if var.get("name", "").upper() == adam_variable.upper():
                                return ds_name
        except Exception:
            # If a specific dataset query fails, continue to next one
            continue
    
    return None


@mcp.tool(name="get_adam_variable_details")
def get_adam_variable_details(
    adam_variable: str,
    adamig_version: str = "1-3",
    headers_ = None
) -> dict:
    """
    Retrieve ADaM variable metadata including label, datatype, and associated codelists
    
    Args:
        adam_variable: The ADaM variable name (e.g., TRT01P, PARAMCD, AVAL)
        adamig_version: ADaMIG version (e.g., "1-3" or "1.3"). Default is "1-3".
        
    Usage:
        get_adam_variable_details("TRT01P")
        get_adam_variable_details("PARAMCD", "1-3")
        get_adam_variable_details("AVAL", "1-2")
    
    Returns:
        Dictionary with variable details, label, datatype, core status, and associated codelists
    """
    try:
        adamig_version_hyphen = adamig_version.replace(".", "-")
        
        dataset = find_adam_variable_dataset(adam_variable, adamig_version_hyphen, headers_)
        if not dataset:
            return {
                "error": f"Variable '{adam_variable}' not found in any dataset structure for ADaMIG {adamig_version_hyphen}",
                "variable": adam_variable,
                "adamig_version": adamig_version_hyphen
            }
        
        url = f"https://api.library.cdisc.org/api/mdr/adam/adamig-{adamig_version_hyphen}/datastructures/{dataset}/variables/{adam_variable}"
        response = api(url, headers_=headers_)
        data = response.json()
        
        if not data:
            return {
                "error": f"Could not fetch details for variable {adam_variable} in dataset {dataset}",
                "variable": adam_variable,
                "dataset": dataset
            }
        
        details = {
            "variable": data.get("name"),
            "label": data.get("label"),
            "datatype": data.get("simpleDatatype"),
            "core": data.get("core"),
            "description": data.get("description"),
            "dataset": dataset,
            "adamig_version": adamig_version_hyphen,
            "codelist_links": [],
            "codelists": []
        }
        
        codelist_info_list = []
        if "_links" in data and "codelist" in data["_links"]:
            for link in data["_links"]["codelist"]:
                href = link.get("href")
                if href:
                    details["codelist_links"].append(href)
                    try:
                        parts = href.split("/")
                        codelist_id = parts[-1]
                        
                        if "/packages/" in href:
                            package_part = href.split("/packages/")[1].split("/")[0]
                            if "-" in package_part:
                                standard_with_ct = package_part.split("-")[0]
                                if standard_with_ct in ["sdtmct", "adamct"]:
                                    codelist_info_list.append((codelist_id, standard_with_ct, href))
                    except (IndexError, ValueError):
                        continue
        
        if codelist_info_list:
            unique_codelists = {info[0]: info for info in codelist_info_list}.values()
            fetched_versions = {}
            
            for cl_id, standard, href in unique_codelists:
                if standard not in fetched_versions:
                    ct_version = get_latest_ct_version(standard.replace("ct", "").upper(), headers_=headers_)
                    if not ct_version:
                        fetched_versions[standard] = None
                        continue
                    fetched_versions[standard] = ct_version
                
                ct_version = fetched_versions[standard]
                if ct_version:
                    codelist_result = get_cdisc_codelist(
                        codelist_value=cl_id,
                        codelist_type="CodelistCode",
                        standard=standard.replace("ct", "").upper(),
                        version=ct_version,
                        headers_=headers_
                    )
                    if codelist_result and "codelist_info" in codelist_result:
                        details["codelists"].append(codelist_result)
        
        return details
        
    except Exception as e:
        return {
            "error": str(e),
            "variable": adam_variable,
            "adamig_version": adamig_version
        }


@mcp.tool(name="get_adam_dataset_structure")
def get_adam_dataset_structure(
    dataset: str,
    adamig_version: str = "1-3",
    headers_ = None
) -> dict:
    """
    Get the structure and variables for a specific ADaM dataset
    
    Args:
        dataset: The ADaM dataset name (e.g., ADSL, ADAE, OCCDS)
        adamig_version: ADaMIG version (e.g., "1-3" or "1.3"). Default is "1-3".
    
    Usage:
        get_adam_dataset_structure("ADSL")
        get_adam_dataset_structure("ADAE", "1-3")
    
    Returns:
        Dictionary with dataset structure and list of variables
    """
    try:
        adamig_version_hyphen = adamig_version.replace(".", "-")
        
        url = f"https://api.library.cdisc.org/api/mdr/adam/adamig-{adamig_version_hyphen}/datastructures/{dataset}"
        response = api(url, headers_=headers_)
        data = response.json()
        
        if not data:
            return {
                "error": f"Could not fetch dataset structure for {dataset}",
                "dataset": dataset,
                "adamig_version": adamig_version_hyphen
            }
        
        variables = []
        
        for var in data.get("analysisVariables", []):
            variables.append({
                "name": var.get("name"),
                "label": var.get("label"),
                "datatype": var.get("simpleDatatype"),
                "core": var.get("core")
            })
        
        for var_set in data.get("analysisVariableSets", []):
            for var in var_set.get("analysisVariables", []):
                variables.append({
                    "name": var.get("name"),
                    "label": var.get("label"),
                    "datatype": var.get("simpleDatatype"),
                    "core": var.get("core")
                })
        
        variables.sort(key=lambda x: x.get("name", ""))
        
        return {
            "dataset": data.get("name"),
            "label": data.get("label"),
            "description": data.get("description"),
            "adamig_version": adamig_version_hyphen,
            "variable_count": len(variables),
            "variables": variables
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "dataset": dataset,
            "adamig_version": adamig_version
        }


@mcp.tool(name="get_sdtm_latest_version")
def get_sdtm_latest_version(headers_ = None) -> dict:
    """
    Get the latest SDTM-IG version from CDISC Library.
    
    Returns:
        dict: Contains the latest SDTM-IG version or error information.
        
    Example:
        get_sdtm_latest_version()
        Returns: {"latest_version": "3-4", "display_version": "3.4"}
    """
    try:
        url = "https://library.cdisc.org/api/mdr/sdtmig"
        
        if headers_ is None:
            response = api(url)
        else:
            response = api(url, headers_=headers_)
        
        data = response.json()
        
        if "_links" in data and "sdtmigVersions" in data["_links"]:
            versions = [link["href"].split("/")[-1] for link in data["_links"]["sdtmigVersions"]]
        else:
            versions = ["3-4", "3-3", "3-2"]
        
        if not versions:
            return {"error": "No SDTM-IG versions found"}
        
        def version_key(version_str):
            """Convert version string to tuple for proper sorting"""
            try:
                parts = version_str.split("-")
                return tuple(int(p) for p in parts)
            except:
                return (0, 0)
        
        sorted_versions = sorted(versions, key=version_key)
        latest_version_hyphen = sorted_versions[-1]
        latest_version_dot = latest_version_hyphen.replace("-", ".")
        
        return {
            "latest_version": latest_version_hyphen,
            "display_version": latest_version_dot,
            "all_versions": sorted_versions
        }
        
    except Exception as e:
        latest_default = "3-4"
        return {
            "latest_version": latest_default,
            "display_version": latest_default.replace("-", "."),
            "all_versions": [latest_default],
            "note": "Using default version due to API error"
        }


@mcp.tool(name="get_sdtm_classes")
def get_sdtm_classes(sdtmig_version: str = None, headers_ = None) -> dict:
    """
    Get SDTM domain classes (Findings, Events, Interventions, etc.) from CDISC Library.
    
    Args:
        sdtmig_version (str, optional): SDTM-IG version (e.g., "3-4" or "3.4"). 
                                        If not provided, uses latest version.
        headers_ (dict, optional): Custom headers for API request.
        
    Returns:
        dict: Contains SDTM classes with their domains or error information.
        
    Example:
        get_sdtm_classes("3-4")
        Returns list of classes: FINDINGS, EVENTS, INTERVENTIONS, SPECIAL PURPOSE, etc.
    """
    try:
        if sdtmig_version is None:
            version_info = get_sdtm_latest_version(headers_=headers_)
            if "error" in version_info:
                return version_info
            sdtmig_version = version_info["latest_version"]
        else:
            sdtmig_version = sdtmig_version.replace(".", "-")
        
        url = f"https://library.cdisc.org/api/mdr/sdtmig/{sdtmig_version}/classes"
        
        if headers_ is None:
            response = api(url)
        else:
            response = api(url, headers_=headers_)
        
        data = response.json()
        
        classes = []
        for cls in data.get("_links", {}).get("classes", []):
            class_name = cls.get("href", "").split("/")[-1]
            classes.append({
                "name": class_name,
                "label": cls.get("title"),
                "type": cls.get("type")
            })
        
        return {
            "sdtmig_version": sdtmig_version,
            "class_count": len(classes),
            "classes": classes
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "sdtmig_version": sdtmig_version
        }


@mcp.tool(name="get_sdtm_domain_structure")
def get_sdtm_domain_structure(domain: str, sdtmig_version: str = None, include_codelists: bool = False, headers_ = None) -> dict:
    """
    Get complete domain structure with all variables for an SDTM domain.
    
    Args:
        domain (str): SDTM domain code (e.g., "DM", "AE", "VS", "LB").
        sdtmig_version (str, optional): SDTM-IG version (e.g., "3-4" or "3.4"). 
                                        If not provided, uses latest version.
        include_codelists (bool, optional): If True, retrieves full codelist terms for variables. 
                                           Default False for faster response.
        headers_ (dict, optional): Custom headers for API request.
        
    Returns:
        dict: Contains domain metadata and complete list of variables with their attributes.
        
    Example:
        get_sdtm_domain_structure("DM", "3-4")
        Returns demographics domain with all required/expected/permissible variables
    """
    try:
        domain = domain.upper()
        
        if sdtmig_version is None:
            version_info = get_sdtm_latest_version(headers_=headers_)
            if "error" in version_info:
                return version_info
            sdtmig_version = version_info["latest_version"]
        else:
            sdtmig_version = sdtmig_version.replace(".", "-")
        
        url = f"https://library.cdisc.org/api/mdr/sdtmig/{sdtmig_version}/datasets/{domain}"
        
        if headers_ is None:
            response = api(url)
        else:
            response = api(url, headers_=headers_)
        
        data = response.json()
        
        variables = []
        
        for var_link in data.get("datasetVariables", []):
            var_data = {
                "name": var_link.get("name"),
                "label": var_link.get("label"),
                "datatype": var_link.get("simpleDatatype"),
                "core": var_link.get("core"),
                "role": var_link.get("role"),
                "ordinal": var_link.get("ordinal"),
                "length": var_link.get("maxLength")
            }
            
            if include_codelists and "_links" in var_link and "codelist" in var_link["_links"]:
                codelist_href = var_link["_links"]["codelist"]["href"]
                try:
                    parts = codelist_href.split("/")
                    codelist_id = parts[-1]
                    
                    if "/packages/" in codelist_href:
                        package_part = codelist_href.split("/packages/")[1].split("/")[0]
                        if "-" in package_part:
                            standard_with_ct = package_part.split("-")[0]
                            if standard_with_ct.endswith("ct"):
                                standard = standard_with_ct[:-2].upper()
                                
                                ct_version_info = get_latest_ct_version(standard, headers_=headers_)
                                if "error" not in ct_version_info:
                                    ct_version = ct_version_info["latest_version"]
                                    codelist_data = get_cdisc_codelist(
                                        codelist_id, 
                                        standard=standard, 
                                        version=ct_version,
                                        headers_=headers_
                                    )
                                    if "error" not in codelist_data:
                                        var_data["codelist"] = codelist_data
                except:
                    pass
            
            variables.append(var_data)
        
        variables.sort(key=lambda x: x.get("ordinal", 999))
        
        return {
            "domain": domain,
            "label": data.get("label"),
            "description": data.get("description"),
            "class": data.get("datasetClass", {}).get("name"),
            "sdtmig_version": sdtmig_version,
            "variable_count": len(variables),
            "variables": variables
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "domain": domain,
            "sdtmig_version": sdtmig_version
        }


def find_sdtm_variable_domain(variable: str, sdtmig_version: str, headers_ = None):
    """
    Helper function to find which SDTM domain contains a specific variable.
    Searches common domains first for efficiency.
    """
    common_domains = ["DM", "AE", "VS", "LB", "EX", "CM", "MH", "DS", "EG", "PE", "QS"]
    
    variable_upper = variable.upper()
    
    for domain in common_domains:
        try:
            url = f"https://library.cdisc.org/api/mdr/sdtmig/{sdtmig_version}/datasets/{domain}"
            
            if headers_ is None:
                response = api(url)
            else:
                response = api(url, headers_=headers_)
            
            data = response.json()
            
            for var_link in data.get("datasetVariables", []):
                if var_link.get("name", "").upper() == variable_upper:
                    return domain
                    
        except:
            continue
    
    return None


@mcp.tool(name="get_sdtm_variable_details")
def get_sdtm_variable_details(variable: str, domain: str = None, sdtmig_version: str = None, include_codelist: bool = True, headers_ = None) -> dict:
    """
    Get detailed metadata for a specific SDTM variable.
    
    Args:
        variable (str): Variable name (e.g., "USUBJID", "AESTDTC", "LBORRES").
        domain (str, optional): SDTM domain code (e.g., "DM", "AE", "VS"). 
                               If not provided, will search common domains.
        sdtmig_version (str, optional): SDTM-IG version (e.g., "3-4" or "3.4"). 
                                        If not provided, uses latest version.
        include_codelist (bool, optional): If True, retrieves full codelist terms. Default True.
        headers_ (dict, optional): Custom headers for API request.
        
    Returns:
        dict: Contains variable metadata including name, label, datatype, core, role, 
              and optionally associated codelist terms.
        
    Example:
        get_sdtm_variable_details("AESTDTC", "AE", "3-4")
        Returns metadata for AE Start Date/Time variable
    """
    try:
        variable = variable.upper()
        
        if sdtmig_version is None:
            version_info = get_sdtm_latest_version(headers_=headers_)
            if "error" in version_info:
                return version_info
            sdtmig_version = version_info["latest_version"]
        else:
            sdtmig_version = sdtmig_version.replace(".", "-")
        
        if domain is None:
            domain = find_sdtm_variable_domain(variable, sdtmig_version, headers_=headers_)
            if domain is None:
                return {
                    "error": f"Variable '{variable}' not found in common SDTM domains",
                    "variable": variable
                }
        else:
            domain = domain.upper()
        
        url = f"https://library.cdisc.org/api/mdr/sdtmig/{sdtmig_version}/datasets/{domain}"
        
        if headers_ is None:
            response = api(url)
        else:
            response = api(url, headers_=headers_)
        
        data = response.json()
        
        variable_data = None
        for var_link in data.get("datasetVariables", []):
            if var_link.get("name", "").upper() == variable:
                variable_data = var_link
                break
        
        if variable_data is None:
            return {
                "error": f"Variable '{variable}' not found in domain '{domain}'",
                "variable": variable,
                "domain": domain
            }
        
        details = {
            "variable": variable_data.get("name"),
            "label": variable_data.get("label"),
            "datatype": variable_data.get("simpleDatatype"),
            "core": variable_data.get("core"),
            "role": variable_data.get("role"),
            "ordinal": variable_data.get("ordinal"),
            "length": variable_data.get("maxLength"),
            "domain": domain,
            "sdtmig_version": sdtmig_version,
            "codelist": None
        }
        
        if include_codelist and "_links" in variable_data and "codelist" in variable_data["_links"]:
            codelist_href = variable_data["_links"]["codelist"]["href"]
            try:
                parts = codelist_href.split("/")
                codelist_id = parts[-1]
                
                if "/packages/" in codelist_href:
                    package_part = codelist_href.split("/packages/")[1].split("/")[0]
                    if "-" in package_part:
                        standard_with_ct = package_part.split("-")[0]
                        if standard_with_ct.endswith("ct"):
                            standard = standard_with_ct[:-2].upper()
                            
                            ct_version_info = get_latest_ct_version(standard, headers_=headers_)
                            if "error" not in ct_version_info:
                                ct_version = ct_version_info["latest_version"]
                                codelist_data = get_cdisc_codelist(
                                    codelist_id, 
                                    standard=standard, 
                                    version=ct_version,
                                    headers_=headers_
                                )
                                if "error" not in codelist_data:
                                    details["codelist"] = codelist_data
            except:
                pass
        
        return details
        
    except Exception as e:
        return {
            "error": str(e),
            "variable": variable,
            "domain": domain,
            "sdtmig_version": sdtmig_version
        }
