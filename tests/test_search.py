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
async def test_search_variable(mcp_client):
    """Test searching for a common variable (USUBJID)"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "USUBJID", "limit": 10, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "query" in result_dict
        assert result_dict["query"] == "USUBJID"
        assert "totalHits" in result_dict
        assert result_dict["totalHits"] > 0
        assert "hits" in result_dict
        assert isinstance(result_dict["hits"], list)


@pytest.mark.asyncio
async def test_search_biomedical_concept(mcp_client):
    """Test searching for biomedical concepts"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "blood pressure", "limit": 20, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["query"] == "blood pressure"
        assert result_dict["totalHits"] > 0
        assert "returnedHits" in result_dict
        
        # Check for biomedical concept results
        bc_results = [h for h in result_dict.get('hits', []) if 'biomedical' in h.get('type', '').lower()]
        assert len(bc_results) > 0


@pytest.mark.asyncio
async def test_search_domain(mcp_client):
    """Test searching for a domain"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "demographics", "limit": 15, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["query"] == "demographics"
        assert result_dict["totalHits"] > 0
        assert len(result_dict["hits"]) <= 15


@pytest.mark.asyncio
async def test_search_codelist(mcp_client):
    """Test searching for controlled terminology"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "RACE", "limit": 25, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["query"] == "RACE"
        assert result_dict["totalHits"] > 0
        
        # Check for codelist results
        codelist_results = [h for h in result_dict.get('hits', []) if 'codelist' in h.get('type', '').lower()]
        assert len(codelist_results) > 0


@pytest.mark.asyncio
async def test_search_limit(mcp_client):
    """Test search result limiting"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "test", "limit": 5, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["returnedHits"] <= 5
        assert "hasMore" in result_dict


@pytest.mark.asyncio
async def test_search_pagination(mcp_client):
    """Test search pagination with hasMore flag"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "USUBJID", "limit": 1, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict["returnedHits"] == 1
        assert "hasMore" in result_dict
        # For USUBJID, there should be more results
        assert result_dict["hasMore"] == True


@pytest.mark.asyncio
async def test_search_empty_query(mcp_client):
    """Test search with empty or very short query"""
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "search_cdisc_library",
            arguments={"query": "X", "limit": 10, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert "query" in result_dict
        assert "hits" in result_dict
