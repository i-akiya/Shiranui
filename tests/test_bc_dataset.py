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
async def test_get_latest_bc_dataset_specializations(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool("get_latest_bc_dataset_specializations",
            arguments={"biomedicalconcept": "WSTCIR", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict.get("name") == "Dataset Specializations (latest version)"
        assert result_dict.get("_links").get("datasetSpecializations") == {"sdtm": []}


# @pytest.mark.asyncio
# async def test_get_latest_sdtm_dataset_specializations_list(mcp_client):
#     client = mcp_client.get("client")
#     headers = mcp_client.get("headers")

#     async with client:
#         response = await client.call_tool(
#             name="get_latest_sdtm_dataset_specializations_list",
#             arguments={"domain": "EG", "headers_": headers}
#         )
#         result = response[0]
#


@pytest.mark.asyncio
async def test_get_latest_sdtm_specialization(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_latest_sdtm_specialization",
            arguments={"dataset_specialization_id": "AXISVOLT", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        assert result_dict.get("datasetSpecializationId") == "AXISVOLT"
        assert result_dict.get("shortName") == "Axis and Voltage ECG Assessment"

        parent_biomedical_concept_dict = {
            "href": "/mdr/bc/biomedicalconcepts/C111132",
            "title": "Axis and Voltage ECG Assessment",
            "type": "Biomedical Concept"
        }
        assert result_dict.get("_links").get("parentBiomedicalConcept") == parent_biomedical_concept_dict


# @pytest.mark.asyncio
# async def test_get_sdtm_dataset_specialization_domain_list(mcp_client):
#     client = mcp_client.get("client")
#     headers = mcp_client.get("headers")

#     async with client:
#         response = await client.call_tool(
#             "get_sdtm_dataset_specialization_domain_list",
#             arguments={"headers_": headers}
#         )
#         result = response[0]


# @pytest.mark.asyncio
# async def test_get_sdtm_dataset_specialization_for_package(mcp_client):
#     client = mcp_client.get("client")
#     headers = mcp_client.get("headers")

#     async with client:
#         response = await client.call_tool(
#             "get_sdtm_dataset_specialization_for_package",
#             arguments={"package": "2024-06-27", "datasetspecialization": "DTHEXIND", "headers_": headers}
#         )
#         result = response[0]


# @pytest.mark.asyncio
# async def test_get_sdtm_dataset_specialization_package_list(mcp_client):
#     client = mcp_client.get("client")
#     headers = mcp_client.get("headers")

#     async with client:
#         response = await client.call_tool(
#             "get_sdtm_dataset_specialization_package_list",
#             arguments={"headers_": headers}
#         )
#         result = response[0]


@pytest.mark.asyncio
async def test_get_sdtm_dataset_specialization_list_for_package(mcp_client):
    client = mcp_client.get("client")
    headers = mcp_client.get("headers")

    async with client:
        response = await client.call_tool(
            "get_sdtm_dataset_specialization_list_for_package",
            arguments={"package": "2024-04-02", "headers_": headers}
        )
        result = response[0]
        result_dict = json.loads(result.text)

        assert isinstance(result, TextContent)
        dataset_specialition_list =  result_dict.get("_links").get("datasetSpecializations")
        assert len(dataset_specialition_list) > 60
        assert any(item.get("title") == "Lab Findings of New or Worsening Heart Failure" for item in dataset_specialition_list) == True
        assert any(
            item.get("title") == "Stroke Type" for item in dataset_specialition_list
        ) == True

        href_ = None
        for item in dataset_specialition_list:
            if item.get("title") == "Transcription Genetic Indicator":
                href_ = item.get("href")
                break

        assert href_ == "/mdr/specializations/sdtm/packages/2024-04-02/datasetspecializations/TRNSCPTNGENTRNIND"
