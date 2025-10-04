import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.shiranui.server import (
    find_adam_variable_dataset,
    get_adam_variable_details,
    get_adam_dataset_structure
)


def test_find_adam_variable_dataset():
    """Test finding which dataset contains a variable"""
    dataset = find_adam_variable_dataset("TRT01P", "1-3")
    assert dataset is not None
    assert dataset == "ADSL"


def test_get_adam_variable_details_trt01p():
    """Test fetching TRT01P variable details from ADSL"""
    result = get_adam_variable_details.fn(
        adam_variable="TRT01P",
        adamig_version="1-3"
    )
    assert "variable" in result
    assert result["variable"] == "TRT01P"
    assert result["dataset"] == "ADSL"
    assert "label" in result
    assert "datatype" in result


def test_get_adam_variable_details_paramcd():
    """Test fetching PARAMCD variable details"""
    result = get_adam_variable_details.fn(
        adam_variable="PARAMCD",
        adamig_version="1-3"
    )
    assert "variable" in result
    assert result["variable"] == "PARAMCD"
    assert "label" in result


def test_get_adam_variable_invalid():
    """Test handling of invalid variable"""
    result = get_adam_variable_details.fn(
        adam_variable="INVALID_VAR_XYZ",
        adamig_version="1-3"
    )
    assert "error" in result


def test_get_adam_dataset_structure_adsl():
    """Test fetching ADSL dataset structure"""
    result = get_adam_dataset_structure.fn(
        dataset="ADSL",
        adamig_version="1-3"
    )
    assert "dataset" in result
    assert result["dataset"] == "ADSL"
    assert "variables" in result
    assert result["variable_count"] > 0
    assert len(result["variables"]) > 0


def test_get_adam_dataset_structure_occds():
    """Test fetching OCCDS dataset structure"""
    result = get_adam_dataset_structure.fn(
        dataset="OCCDS",
        adamig_version="1-3"
    )
    assert "dataset" in result or "error" in result


def test_get_adam_variable_with_codelist():
    """Test variable that has associated codelists"""
    result = get_adam_variable_details.fn(
        adam_variable="TRT01P",
        adamig_version="1-3"
    )
    assert "variable" in result
    if "codelists" in result and len(result["codelists"]) > 0:
        codelist = result["codelists"][0]
        assert "codelist_info" in codelist
        assert "terms" in codelist
