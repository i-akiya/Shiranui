import pytest
import os
import json
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from mcp.types import TextContent


@pytest.fixture
def mcp_client():
    transport = StdioTransport(
        command="python",
        args=[".venv/bin/shiranui"],
        keep_alive=False
    )
    client = Client(transport)

    headers = {
        "api-key": os.getenv('CDISC_LIBRARY_API_KEY'),
        "accept": "application/json"
    }

    return {"client": client, "headers": headers}


@pytest.mark.asyncio
async def test_get_ct_latest_version(mcp_client):
    """Test retrieving the latest CT version for a standard"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_ct_latest_version",
            arguments={"standard": "sdtm", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "latest_version" in result_dict
        assert "display_version" in result_dict
        assert "all_versions" in result_dict
        assert isinstance(result_dict["all_versions"], list)
        assert len(result_dict["all_versions"]) > 0


@pytest.mark.asyncio
async def test_get_cdisc_codelist_by_id(mcp_client):
    """Test retrieving a codelist by ID (AGEU - Age Units)"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdisc_codelist",
            arguments={
                "standard": "sdtm",
                "codelist_value": "AGEU",
                "codelist_type": "ID",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "codelist_info" in result_dict
        assert result_dict["codelist_info"]["id"] == "AGEU"
        assert "terms" in result_dict
        assert len(result_dict["terms"]) > 0
        
        # Check for expected terms
        term_codes = [term["term"] for term in result_dict["terms"]]
        assert "YEARS" in term_codes
        assert "MONTHS" in term_codes


@pytest.mark.asyncio
async def test_get_cdisc_codelist_adam(mcp_client):
    """Test retrieving an ADaM codelist (DTYPE)"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdisc_codelist",
            arguments={
                "standard": "adam",
                "codelist_value": "DTYPE",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "codelist_info" in result_dict
        assert result_dict["codelist_info"]["standard"] == "ADAM"


@pytest.mark.asyncio
async def test_get_cdisc_codelist_invalid(mcp_client):
    """Test handling of invalid codelist"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdisc_codelist",
            arguments={
                "standard": "sdtm",
                "codelist_value": "INVALID_CODE",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "warning" in result_dict or "error" in result_dict


@pytest.mark.asyncio
async def test_get_ct_package_codelists(mcp_client):
    """Test retrieving all codelists for a CT package"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_ct_package_codelists",
            arguments={
                "standard": "sdtm",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "standard" in result_dict
        assert result_dict["standard"] == "SDTM"
        assert "version" in result_dict
        assert "codelist_count" in result_dict
        assert "codelists" in result_dict
        assert len(result_dict["codelists"]) > 50
        
        # Check that AGEU exists in the list
        codelist_ids = [cl["id"] for cl in result_dict["codelists"]]
        assert "AGEU" in codelist_ids


@pytest.mark.asyncio
async def test_get_ct_package_codelists_adam(mcp_client):
    """Test retrieving ADaM codelists"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_ct_package_codelists",
            arguments={
                "standard": "adam",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["standard"] == "ADAM"
        assert "codelists" in result_dict
        assert len(result_dict["codelists"]) > 0
