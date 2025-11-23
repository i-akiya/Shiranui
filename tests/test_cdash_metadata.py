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
async def test_get_cdashig_latest_version(mcp_client):
    """Test CDASHIG latest version detection"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_latest_version",
            arguments={"headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "latest_version" in result_dict
        assert "display_version" in result_dict
        assert "all_versions" in result_dict
        assert isinstance(result_dict["all_versions"], list)
        assert result_dict["version_count"] > 0


@pytest.mark.asyncio
async def test_get_cdashig_domains(mcp_client):
    """Test CDASHIG domains list retrieval"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_domains",
            arguments={"headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "cdashig_version" in result_dict
        assert "domains" in result_dict
        assert result_dict["domain_count"] > 0
        assert isinstance(result_dict["domains"], list)
        
        # Check for DM domain
        assert any(d["name"] == "DM" for d in result_dict["domains"])


@pytest.mark.asyncio
async def test_get_cdashig_domains_specific_version(mcp_client):
    """Test CDASHIG domains list with specific version (v2.1)"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_domains",
            arguments={"cdashig_version": "2-1", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["cdashig_version"] == "2-1"
        assert result_dict["domain_count"] > 0


@pytest.mark.asyncio
async def test_get_cdashig_domain_structure_cm(mcp_client):
    """Test CDASHIG domain structure for Concomitant Medications"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_domain_structure",
            arguments={"domain": "CM", "cdashig_version": "2-1", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "CM"
        assert "label" in result_dict
        assert result_dict["field_count"] > 0
        assert "fields" in result_dict
        
        # Check for CMTRT field
        assert any(f["name"] == "CMTRT" for f in result_dict["fields"])


@pytest.mark.asyncio
async def test_get_cdashig_domain_structure_dm(mcp_client):
    """Test CDASHIG domain structure for Demographics"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_domain_structure",
            arguments={"domain": "DM", "cdashig_version": "2-1", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "DM"
        assert result_dict["field_count"] > 0
        
        # Check for birth date field (can be BRTHDAT, BRTHDT, or BRTHDTC)
        field_names = [f["name"] for f in result_dict["fields"]]
        assert any(name in ["BRTHDAT", "BRTHDT", "BRTHDTC"] for name in field_names)


@pytest.mark.asyncio
async def test_get_cdashig_field_details(mcp_client):
    """Test CDASHIG field details retrieval"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_field_details",
            arguments={
                "field_name": "CMTRT",
                "domain": "CM",
                "cdashig_version": "2-1",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["field"] == "CMTRT"
        assert result_dict["domain"] == "CM"
        assert "label" in result_dict
        assert "datatype" in result_dict


@pytest.mark.asyncio
async def test_get_cdashig_field_auto_detect(mcp_client):
    """Test CDASHIG field details with automatic domain detection"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_field_details",
            arguments={
                "field_name": "STUDYID",
                "cdashig_version": "2-1",
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["field"] == "STUDYID"
        assert "domain" in result_dict
        assert result_dict["domain"] is not None


@pytest.mark.asyncio
async def test_cdashig_version_normalization(mcp_client):
    """Test CDASHIG version format normalization (2.1 -> 2-1)"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_domains",
            arguments={"cdashig_version": "2.1", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["cdashig_version"] == "2-1"


@pytest.mark.asyncio
async def test_cdashig_invalid_domain(mcp_client):
    """Test CDASHIG error handling for invalid domain"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_cdashig_domain_structure",
            arguments={"domain": "INVALID_DOMAIN", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" in result_dict or "warning" in result_dict
