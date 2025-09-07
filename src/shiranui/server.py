import os
import requests
from mcp.server.fastmcp import FastMCP
# from mcp.shared.exceptions import McpError
# from shiranui.api_client.biomedical_concepts import BiomedicalConcepts
# from shiranui.exceptions.api_key_error import ApiKeyError

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
async def get_latest_bc_list(headers_ = None) -> list:
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

    return [response.json().get("_links").get("biomedicalConcepts")]

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

    return response.json().get("_links").get("datasetSpecializations")


@mcp.tool(name="get_latest_sdtm_dataset_specializations")
def get_latest_sdtm_dataset_specializations(domain: str, headers_ = None) -> dict:
    """
    Get Latest SDTM Dataset Specializations List for a specific domain

    Args:
        domain (str): The domain to retrieve dataset specializations for.

    Usage:
        get_latest_sdtm_dataset_specializations("DM")
    """
    url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/specializations/sdtm/datasetspecializations?domain={domain}"
    if headers_ is None:
        response = api(url)
    else:
        response = api(url, headers_ = headers)

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
