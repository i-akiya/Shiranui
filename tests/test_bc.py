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
async def test_get_bc_list(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool("get_latest_bc_list", arguments={"headers_": headers})
        result = response[0]
        result_dict = json.loads(result.text)
        bc_list = result_dict.get("_links").get("biomedicalConcepts")
        assert isinstance(result, TextContent)
        assert len(bc_list) > 1000
        assert any(item.get("title") == "Mean Heart Rate by Electrocardiogram" for item in bc_list) == True
        assert any(
            item.get("title") == "Segmented Neutrophil to Leukocyte Ratio Measurement" for item in bc_list
        ) == True

        href_ = None
        for item in bc_list:
            if item.get("title") == "Trial Screen Failure":
                href_ = item.get("href")
                break

        assert href_ == "/mdr/bc/biomedicalconcepts/C49628"


@pytest.mark.asyncio
async def test_get_latest_bc_cat(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool("get_latest_bc_cat", arguments={"headers_": headers})
        result = response[0]
        result_dict = json.loads(result.text)
        bc_cat = result_dict.get("_links").get("categories")

        assert isinstance(result, TextContent)
        assert len(bc_cat) > 300
        assert any(item.get("name") == "Subject Characteristics" for item in bc_cat) == True

        retrieved_dict = None
        serology_test_dict = {
            "href": "/mdr/bc/biomedicalconcepts?category=Serology%20Tests",
            "title": "Biomedical Concepts Category (Serology Tests)",
            "type": "Biomedical Concepts Category"
        }
        for item in bc_cat:
            if item.get("name") == "Serology Tests":
                retrieved_dict = item.get("_links").get("self")
                break

        assert retrieved_dict == serology_test_dict


@pytest.mark.asyncio
async def test_get_latest_bc(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        concept_id = "C105585"  # Example concept ID for testing
        response = await client.call_tool(
            "get_latest_bc", arguments={"concept_id": concept_id, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)

        parentBiomedicalConcept = {
            "href": "/mdr/bc/biomedicalconcepts/C49237",
            "title": "Chemistry Test",
            "type": "Biomedical Concept"
        }
        assert result_dict.get("_links").get("parentBiomedicalConcept") == parentBiomedicalConcept

        self_= {
            "href": "/mdr/bc/biomedicalconcepts/C105585",
            "title": "Glucose Measurement",
            "type": "Biomedical Concept"
        }
        assert result_dict.get("_links").get("self") == self_

        assert result_dict.get("conceptId") == "C105585"
        assert result_dict.get("shortName") == "Glucose Measurement"


@pytest.mark.asyncio
async def test_get_bc_package_list(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_bc_package_list", arguments={"headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)
        bc_packages = result_dict.get("_links").get("packages")

        assert isinstance(result, TextContent)
        assert len(bc_packages) > 10
        assert any(
            item.get("title") == "Biomedical Concept Package Effective 2025-07-01" for item in bc_packages
        ) == True

        href_ = None
        for item in bc_packages:
            if item.get("title") == "Biomedical Concept Package Effective 2024-12-17":
                href_ = item.get("href")
                break

        assert href_ == "/mdr/bc/packages/2024-12-17/biomedicalconcepts"


@pytest.mark.asyncio
async def test_get_bc_for_package(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        package = "2024-12-17"
        biomedicalconcept_id = "C111280"  # Example concept ID for testing
        response = await client.call_tool(
            "get_bc_for_package",
            arguments={"package": package, "biomedicalconcept_id": biomedicalconcept_id, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict.get("conceptId") == biomedicalconcept_id
        assert result_dict.get("shortName") == "Myocardial Infarction ECG Assessment"

        parentBiomedicalConcept = {
            "href": "/mdr/bc/packages/2023-07-06/biomedicalconcepts/C83146",
            "title": "Electrocardiogram Test",
            "type": "Biomedical Concept"
        }
        assert result_dict.get("_links").get("parentBiomedicalConcept") == parentBiomedicalConcept

        self_link = {
            "href": "/mdr/bc/packages/2024-12-17/biomedicalconcepts/C111280",
            "title": "Myocardial Infarction ECG Assessment",
            "type": "Biomedical Concept"
        }
        assert result_dict.get("_links").get("self") == self_link


@pytest.mark.asyncio
async def test_get_bc_list_for_package(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        package = "2025-07-01"  # Example package for testing
        response = await client.call_tool(
            "get_bc_list_for_package",
            arguments={"package": package, "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)
        bc_list = result_dict.get("_links").get("biomedicalConcepts")

        assert isinstance(result, TextContent)
        assert len(bc_list) > 100
        assert any(item.get("title") == "CDISC ADAS-Cog - Naming Objects and Fingers: 10" for item in bc_list) == True

        href_ = None
        for item in bc_list:
            if item.get("title") == "CDISC ADAS-Cog - Delayed Word Recall: Word 4":
                href_ = item.get("href")
                break

        assert href_ == "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100219"

# @pytest.mark.asyncio
# async def test_get_sdtm_dataset_specializations(mcp_client):
#     client = mcp_client.get("client")
#     headers = mcp_client.get("headers")

#     # Execute operations
#     async with client:
#         domain = "DM"
#         response = await client.call_tool(
#             "get_latest_sdtm_dataset_specializations",
#             arguments={"domain": domain, "headers_": headers}
#         )
#         result = response[0]
#         result_dict = json.loads(result.text)
#         specializations = result_dict.get("_links").get("specializations")

#         assert isinstance(result, TextContent)
#         assert len(specializations) > 1
#         assert any(item.get("domain") == domain for item in specializations) == True

#         href_ = None
#         for item in specializations:
#             if item.get("name") == "US DM Specialization":
#                 href_ = item.get("href")
#                 break

#         assert href_ is not None
