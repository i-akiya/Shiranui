"""
Test suite for SDTM Metadata MCP tools

These tests verify the functionality of SDTM-IG dataset and variable metadata retrieval tools.
"""

import sys
sys.path.insert(0, '../src')

from shiranui.server import (
    get_sdtm_latest_version,
    get_sdtm_classes,
    get_sdtm_domain_structure,
    get_sdtm_variable_details
)


def test_get_sdtm_latest_version():
    """Test retrieving the latest SDTM-IG version"""
    print("\n=== Test: get_sdtm_latest_version ===")
    result = get_sdtm_latest_version()
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert "latest_version" in result
    assert "display_version" in result
    assert "all_versions" in result
    
    print(f"✓ Latest SDTM-IG version: {result['latest_version']} ({result['display_version']})")
    print(f"✓ Total versions available: {len(result['all_versions'])}")


def test_version_sorting():
    """Test that version sorting handles multi-digit versions correctly"""
    print("\n=== Test: Version sorting with multi-digit versions ===")
    
    from shiranui.server import get_sdtm_latest_version
    
    versions_test = ["3-2", "3-10", "3-4", "3-3", "3-11"]
    
    def version_key(version_str):
        try:
            parts = version_str.split("-")
            return tuple(int(p) for p in parts)
        except:
            return (0, 0)
    
    sorted_versions = sorted(versions_test, key=version_key)
    expected_order = ["3-2", "3-3", "3-4", "3-10", "3-11"]
    
    assert sorted_versions == expected_order, f"Expected {expected_order}, got {sorted_versions}"
    assert sorted_versions[-1] == "3-11", f"Latest should be 3-11, got {sorted_versions[-1]}"
    
    print(f"✓ Versions sorted correctly: {sorted_versions}")
    print(f"✓ Latest version identified: {sorted_versions[-1]}")


def test_get_sdtm_classes():
    """Test retrieving SDTM domain classes"""
    print("\n=== Test: get_sdtm_classes ===")
    result = get_sdtm_classes("3-4")
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert "sdtmig_version" in result
    assert "class_count" in result
    assert "classes" in result
    assert result["class_count"] > 0
    
    print(f"✓ SDTM-IG version: {result['sdtmig_version']}")
    print(f"✓ Number of classes: {result['class_count']}")
    
    if result["classes"]:
        print(f"✓ First class: {result['classes'][0]['name']}")


def test_get_sdtm_classes_auto_version():
    """Test retrieving SDTM classes with automatic version detection"""
    print("\n=== Test: get_sdtm_classes (auto version) ===")
    result = get_sdtm_classes()
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert "classes" in result
    assert len(result["classes"]) > 0
    
    print(f"✓ Auto-detected version: {result['sdtmig_version']}")
    print(f"✓ Classes retrieved: {result['class_count']}")


def test_get_sdtm_domain_structure_dm():
    """Test retrieving Demographics domain structure"""
    print("\n=== Test: get_sdtm_domain_structure (DM) ===")
    result = get_sdtm_domain_structure("DM", "3-4")
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert result["domain"] == "DM"
    assert result["label"] == "Demographics"
    assert "variable_count" in result
    assert result["variable_count"] > 0
    assert "variables" in result
    
    print(f"✓ Domain: {result['domain']} - {result['label']}")
    print(f"✓ Class: {result['class']}")
    print(f"✓ Variables: {result['variable_count']}")
    
    studyid = next((v for v in result["variables"] if v["name"] == "STUDYID"), None)
    assert studyid is not None
    assert studyid["core"] == "Req"
    assert studyid["role"] == "Identifier"
    print(f"✓ STUDYID found with core={studyid['core']}, role={studyid['role']}")


def test_get_sdtm_domain_structure_ae():
    """Test retrieving Adverse Events domain structure"""
    print("\n=== Test: get_sdtm_domain_structure (AE) ===")
    result = get_sdtm_domain_structure("AE", "3-4")
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert result["domain"] == "AE"
    assert result["label"] == "Adverse Events"
    assert result["variable_count"] > 0
    
    print(f"✓ Domain: {result['domain']} - {result['label']}")
    print(f"✓ Variables: {result['variable_count']}")
    
    aeseq = next((v for v in result["variables"] if v["name"] == "AESEQ"), None)
    assert aeseq is not None
    print(f"✓ AESEQ found: {aeseq['label']}")


def test_get_sdtm_variable_details_with_domain():
    """Test retrieving variable details with domain specified"""
    print("\n=== Test: get_sdtm_variable_details (USUBJID in DM) ===")
    result = get_sdtm_variable_details("USUBJID", "DM", "3-4", include_codelist=False)
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert result["variable"] == "USUBJID"
    assert result["label"] == "Unique Subject Identifier"
    assert result["core"] == "Req"
    assert result["role"] == "Identifier"
    assert result["datatype"] == "Char"
    assert result["domain"] == "DM"
    
    print(f"✓ Variable: {result['variable']}")
    print(f"✓ Label: {result['label']}")
    print(f"✓ Core: {result['core']}, Role: {result['role']}, Type: {result['datatype']}")


def test_get_sdtm_variable_details_auto_domain():
    """Test retrieving variable details with automatic domain detection"""
    print("\n=== Test: get_sdtm_variable_details (AESTDTC, auto-domain) ===")
    result = get_sdtm_variable_details("AESTDTC", sdtmig_version="3-4", include_codelist=False)
    
    assert "error" not in result, f"Error occurred: {result.get('error')}"
    assert result["variable"] == "AESTDTC"
    assert result["domain"] == "AE"
    
    print(f"✓ Variable: {result['variable']}")
    print(f"✓ Auto-detected domain: {result['domain']}")
    print(f"✓ Label: {result['label']}")


def test_get_sdtm_variable_details_invalid():
    """Test handling of invalid variable name"""
    print("\n=== Test: get_sdtm_variable_details (invalid variable) ===")
    result = get_sdtm_variable_details("INVALIDVAR", "DM", "3-4", include_codelist=False)
    
    assert "error" in result
    print(f"✓ Expected error received: {result['error']}")


def run_all_tests():
    """Run all SDTM metadata tests"""
    print("\n" + "="*60)
    print("Running SDTM Metadata MCP Tools Test Suite")
    print("="*60)
    
    tests = [
        test_get_sdtm_latest_version,
        test_version_sorting,
        test_get_sdtm_classes,
        test_get_sdtm_classes_auto_version,
        test_get_sdtm_domain_structure_dm,
        test_get_sdtm_domain_structure_ae,
        test_get_sdtm_variable_details_with_domain,
        test_get_sdtm_variable_details_auto_domain,
        test_get_sdtm_variable_details_invalid
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {str(e)}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
