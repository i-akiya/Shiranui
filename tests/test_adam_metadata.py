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
async def test_get_adam_variable_details_trt01p(mcp_client):
    """Test fetching TRT01P variable details from ADSL"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_adam_variable_details",
            arguments={
                "adam_variable": "TRT01P",
                "adamig_version": "1-3",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" not in result_dict, f"Error occurred: {result_dict.get('error')}"
        assert "variable" in result_dict
        assert result_dict["variable"] == "TRT01P"
        assert "dataset" in result_dict
        assert result_dict["dataset"] == "ADSL"
        assert "label" in result_dict
        assert "datatype" in result_dict


@pytest.mark.asyncio
async def test_get_adam_variable_details_paramcd(mcp_client):
    """Test fetching PARAMCD variable details"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_adam_variable_details",
            arguments={
                "adam_variable": "PARAMCD",
                "adamig_version": "1-3",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" not in result_dict, f"Error occurred: {result_dict.get('error')}"
        assert "variable" in result_dict
        assert result_dict["variable"] == "PARAMCD"
        assert "label" in result_dict


@pytest.mark.asyncio
async def test_get_adam_variable_invalid(mcp_client):
    """Test handling of invalid variable"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_adam_variable_details",
            arguments={
                "adam_variable": "INVALID_VAR_XYZ",
                "adamig_version": "1-3",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" in result_dict


@pytest.mark.asyncio
async def test_get_adam_dataset_structure_adsl(mcp_client):
    """Test fetching ADSL dataset structure"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_adam_dataset_structure",
            arguments={
                "dataset": "ADSL",
                "adamig_version": "1-3",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" not in result_dict, f"Error occurred: {result_dict.get('error')}"
        assert "dataset" in result_dict
        assert result_dict["dataset"] == "ADSL"
        assert "variables" in result_dict
        assert result_dict["variable_count"] > 0
        assert len(result_dict["variables"]) > 0


@pytest.mark.asyncio
async def test_get_adam_dataset_structure_occds(mcp_client):
    """Test fetching OCCDS dataset structure"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_adam_dataset_structure",
            arguments={
                "dataset": "OCCDS",
                "adamig_version": "1-3",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "dataset" in result_dict or "error" in result_dict


@pytest.mark.asyncio
async def test_get_adam_variable_with_codelist(mcp_client):
    """Test variable that has associated codelists"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_adam_variable_details",
            arguments={
                "adam_variable": "TRT01P",
                "adamig_version": "1-3",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "variable" in result_dict
        if "codelists" in result_dict and len(result_dict["codelists"]) > 0:
            codelist = result_dict["codelists"][0]
            assert "codelist_info" in codelist
            assert "terms" in codelist
