import pytest

from voxcausal.security import StorageAccess, is_compliant, violations

OK = dict(region="uksouth", sas_minutes=15, tls_version="1.3", https_only=True, user_delegation=True)


def test_incident_fix_is_compliant():
    assert is_compliant(StorageAccess(**OK))


@pytest.mark.parametrize("change,expected", [
    ({"region": "eastus"}, "UK South"),
    ({"sas_minutes": 60}, "15 min"),
    ({"sas_minutes": 0}, "15 min"),
    ({"tls_version": "1.0"}, "TLS menor"),
    ({"tls_version": "x"}, "inválida"),
    ({"https_only": False}, "HTTP"),
    ({"user_delegation": False}, "delegación"),
])
def test_each_violation_detected(change, expected):
    errs = violations(StorageAccess(**{**OK, **change}))
    assert len(errs) == 1 and expected in errs[0]
