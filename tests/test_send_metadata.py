import json
import os

import pytest
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
async def test_get_sendig_latest_version(mcp_client):
    """Test SENDIG latest version detection"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_latest_version",
            arguments={"headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "latest_version" in result_dict
        assert "display_version" in result_dict
        assert "all_versions" in result_dict
        assert isinstance(result_dict["all_versions"], list)
        assert result_dict["total_versions"] > 0


@pytest.mark.asyncio
async def test_get_sendig_classes(mcp_client):
    """Test SEND domain classes retrieval"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_classes",
            arguments={"headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "sendig_version" in result_dict
        assert "class_count" in result_dict
        assert result_dict["class_count"] > 0
        assert "classes" in result_dict
        assert isinstance(result_dict["classes"], list)


@pytest.mark.asyncio
async def test_get_sendig_domain_structure_dm(mcp_client):
    """Test SEND Demographics domain structure"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_domain_structure",
            arguments={"domain": "DM", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "DM"
        assert "label" in result_dict
        assert result_dict["variable_count"] > 0
        assert "variables" in result_dict

        # Check for USUBJID variable
        assert any(v["name"] == "USUBJID" for v in result_dict["variables"])


@pytest.mark.asyncio
async def test_get_sendig_domain_structure_lb(mcp_client):
    """Test SEND Laboratory Findings domain structure"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_domain_structure",
            arguments={"domain": "LB", "sendig_version": "3-1-1", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "LB"
        assert result_dict["variable_count"] > 0

        # Check for LBTESTCD variable
        assert any(v["name"] == "LBTESTCD" for v in result_dict["variables"])


@pytest.mark.asyncio
async def test_get_sendig_variable_details(mcp_client):
    """Test SEND variable details retrieval"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_variable_details",
            arguments={"variable": "USUBJID", "domain": "DM", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["variable"] == "USUBJID"
        assert result_dict["domain"] == "DM"
        assert "label" in result_dict
        assert "datatype" in result_dict


@pytest.mark.asyncio
async def test_get_sendig_variable_auto_detect(mcp_client):
    """Test SEND variable auto-detection"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_variable_details",
            arguments={"variable": "LBTESTCD", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["variable"] == "LBTESTCD"
        assert "domain" in result_dict
        assert result_dict["domain"] is not None


@pytest.mark.asyncio
async def test_sendig_version_normalization(mcp_client):
    """Test version format normalization (3.1.1 -> 3-1-1)"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_domain_structure",
            arguments={"domain": "DM", "sendig_version": "3.1.1", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["sendig_version"] == "3-1-1"


@pytest.mark.asyncio
async def test_get_sendig_domain_mi(mcp_client):
    """Test SEND Microscopic Findings domain"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_domain_structure",
            arguments={"domain": "MI", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "MI"
        assert result_dict["variable_count"] > 0

        # Check for SEND-specific variables
        variable_names = [v["name"] for v in result_dict["variables"]]
        send_vars = ["MISPEC", "MIMETHOD", "MITSTDTL"]
        assert any(var in variable_names for var in send_vars)


@pytest.mark.asyncio
async def test_sendig_invalid_domain(mcp_client):
    """Test SEND error handling for invalid domain"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sendig_domain_structure",
            arguments={"domain": "INVALID_DOMAIN", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" in result_dict or "warning" in result_dict
