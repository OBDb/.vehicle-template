import pytest
import os
import json
from pathlib import Path
from typing import Dict, Any

# These will be imported from the schemas repository
from schemas.python.signals_testing import obd_testrunner
from schemas.python.can_frame import CANIDFormat

REPO_ROOT = Path(__file__).parent.parent.absolute()

TEST_CASES = [
    # Example response test
    # 2021 model year
    # {
    #     "model_year": "2021",
    #     "signalset": "default.json",
    #     "tests": [
    #         # Target vehicle speed - -61.2 km/h
    #         ("76C0562A224FF56", {"F150_CC_TGT_VSS": -61.2}),
    #     ]
    # },
]

def load_signalset(filename: str) -> str:
    """Load a signalset JSON file from the standard location."""
    signalset_path = REPO_ROOT / "signalsets" / "v3" / filename
    with open(signalset_path) as f:
        return f.read()

@pytest.mark.parametrize("test_group", TEST_CASES)
def test_responses(test_group: Dict[str, Any]):
    """Test signal decoding against known responses."""
    signalset_json = load_signalset(test_group["signalset"])

    # Run each test case in the group
    for response_hex, expected_values in test_group["tests"]:
        try:
            obd_testrunner(
                signalset_json,
                response_hex,
                expected_values,
                can_id_format=CANIDFormat.ELEVEN_BIT
            )
        except Exception as e:
            pytest.fail(
                f"Failed on response {response_hex} "
                f"(Model Year: {test_group['model_year']}, "
                f"Signalset: {test_group['signalset']}): {e}"
            )

if __name__ == '__main__':
    pytest.main([__file__])
