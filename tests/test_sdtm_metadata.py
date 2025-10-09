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
async def test_get_sdtm_latest_version(mcp_client):
    """Test retrieving the latest SDTM-IG version"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_latest_version",
            arguments={"headers_": headers}
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
async def test_get_sdtm_classes(mcp_client):
    """Test retrieving SDTM domain classes"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_classes",
            arguments={"sdtmig_version": "3-4", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "sdtmig_version" in result_dict
        assert "class_count" in result_dict
        assert "classes" in result_dict
        assert result_dict["class_count"] > 0
        assert len(result_dict["classes"]) > 0


@pytest.mark.asyncio
async def test_get_sdtm_classes_auto_version(mcp_client):
    """Test retrieving SDTM classes with automatic version detection"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_classes",
            arguments={"headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "classes" in result_dict
        assert len(result_dict["classes"]) > 0


@pytest.mark.asyncio
async def test_get_sdtm_domain_structure_dm(mcp_client):
    """Test retrieving Demographics domain structure"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_domain_structure",
            arguments={"domain": "DM", "sdtmig_version": "3-4", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "DM"
        assert result_dict["label"] == "Demographics"
        assert "variable_count" in result_dict
        assert result_dict["variable_count"] > 0
        assert "variables" in result_dict
        
        # Verify STUDYID exists
        studyid = next((v for v in result_dict["variables"] if v["name"] == "STUDYID"), None)
        assert studyid is not None
        assert studyid["core"] == "Req"
        assert studyid["role"] == "Identifier"


@pytest.mark.asyncio
async def test_get_sdtm_domain_structure_ae(mcp_client):
    """Test retrieving Adverse Events domain structure"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_domain_structure",
            arguments={"domain": "AE", "sdtmig_version": "3-4", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["domain"] == "AE"
        assert result_dict["label"] == "Adverse Events"
        assert result_dict["variable_count"] > 0
        
        # Verify AESEQ exists
        aeseq = next((v for v in result_dict["variables"] if v["name"] == "AESEQ"), None)
        assert aeseq is not None


@pytest.mark.asyncio
async def test_get_sdtm_variable_details_with_domain(mcp_client):
    """Test retrieving variable details with domain specified"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_variable_details",
            arguments={
                "variable": "USUBJID",
                "domain": "DM",
                "sdtmig_version": "3-4",
                "include_codelist": False,
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["variable"] == "USUBJID"
        assert result_dict["label"] == "Unique Subject Identifier"
        assert result_dict["core"] == "Req"
        assert result_dict["role"] == "Identifier"
        assert result_dict["datatype"] == "Char"
        assert result_dict["domain"] == "DM"


@pytest.mark.asyncio
async def test_get_sdtm_variable_details_auto_domain(mcp_client):
    """Test retrieving variable details with automatic domain detection"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_variable_details",
            arguments={
                "variable": "AESTDTC",
                "sdtmig_version": "3-4",
                "include_codelist": False,
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["variable"] == "AESTDTC"
        assert result_dict["domain"] == "AE"


@pytest.mark.asyncio
async def test_get_sdtm_variable_details_invalid(mcp_client):
    """Test handling of invalid variable name"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_variable_details",
            arguments={
                "variable": "INVALIDVAR",
                "domain": "DM",
                "sdtmig_version": "3-4",
                "include_codelist": False,
                "headers_": headers
            }
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "error" in result_dict
