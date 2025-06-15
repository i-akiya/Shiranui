import os
import requests
import pandas as pd
from requests.exceptions import RequestException
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS

mcp = FastMCP("CDISC Library Retriever", )
api_key = os.getenv('CDISC_LIBRARY_API_KEY')


@mcp.tool()
def get_bc_list() -> list:
    """
    Get Biomedical Concepts List

    Usage:
        get_bc_list()
    """
    try:
        url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts"

        headers = {
            "api-key": api_key,
            "aaccept": "application/json"
        }

        response = requests.get(url, headers=headers)

        return [response.json().get("_links").get("biomedicalConcepts")]
    except McpError as e:
        raise e


@mcp.tool()
def get_latest_bc_cat() -> list:
    """
    Get Latest Biomedical Concept Categories List from CDISC Library

    Usage:
        get_latest_bc_cat()
    """

    try:
        url = "https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/categories"

        headers = {
            "api-key": api_key,
            "aaccept": "application/json"
        }

        response = requests.get(url, headers=headers)
        # dict_response = response.json()

        return [response.json().get("_links").get("categories")]
    except McpError as e:
        raise e


@mcp.tool()
def get_latest_bc(concept_id: str) -> str:
    """
    Get latest Biomedical Concept specified by concept_id from CDISC Library

    Args:
        concept_id (str): The ID of the Biomedical Concept to retrieve.

    Usage:
        get_latest_bc_cat("C105585")
    """

    try:
        url = f"https://api.library.cdisc.org/api/cosmos/v2/mdr/bc/biomedicalconcepts/{concept_id}"

        headers = {
            "api-key": api_key,
            "aaccept": "application/json"
        }

        response = requests.get(url, headers=headers)

        return response.content.decode("utf-8")
    except McpError as e:
        raise e

