import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.shiranui.server import (
    get_latest_ct_version,
    get_ct_latest_version_tool,
    get_cdisc_codelist,
    get_ct_package_codelists
)


def test_get_latest_ct_version_sdtm():
    """Test fetching latest SDTM CT version"""
    version = get_latest_ct_version("SDTM")
    assert version is not None
    assert len(version) == 10
    assert version.count("-") == 2


def test_get_latest_ct_version_adam():
    """Test fetching latest ADAM CT version"""
    version = get_latest_ct_version("ADAM")
    assert version is not None
    assert len(version) == 10


def test_get_ct_latest_version_tool():
    """Test the MCP tool for latest version"""
    result = get_ct_latest_version_tool.fn("SDTM")
    assert "latest_version" in result
    assert result["standard"] == "SDTM"


def test_get_cdisc_codelist_ageu():
    """Test fetching AGEU (Age Units) codelist"""
    result = get_cdisc_codelist.fn(
        codelist_value="AGEU",
        standard="SDTM"
    )
    assert "codelist_info" in result
    assert result["codelist_info"]["id"] == "AGEU"
    assert len(result["terms"]) > 0


def test_get_cdisc_codelist_adam_dtype():
    """Test fetching DTYPE from ADAM"""
    result = get_cdisc_codelist.fn(
        codelist_value="DTYPE",
        standard="ADAM"
    )
    assert "codelist_info" in result
    assert result["codelist_info"]["standard"] == "ADAM"


def test_get_cdisc_codelist_invalid():
    """Test handling of invalid codelist"""
    result = get_cdisc_codelist.fn(
        codelist_value="INVALID_CODE",
        standard="SDTM"
    )
    assert "warning" in result or "error" in result


def test_get_ct_package_codelists():
    """Test listing all codelists in a package"""
    result = get_ct_package_codelists.fn("SDTM")
    assert "codelists" in result
    assert result["codelist_count"] > 0
    assert len(result["codelists"]) > 0
