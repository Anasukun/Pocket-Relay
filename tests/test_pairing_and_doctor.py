from unittest import mock
from pocketrelay.cli.doctor import format_doctor_report, run_doctor_checks
from pocketrelay.security.pairing import PairingManager


def test_pairing_manager():
    pm = PairingManager()
    code = pm.generate_code()
    
    assert len(code) == 6
    assert code.isdigit()
    
    # Test incorrect code
    assert not pm.verify_code("000000")
    
    # Test valid code
    assert pm.verify_code(code)
    
    # Test single-use (already used code)
    assert not pm.verify_code(code)

def test_pairing_brute_force_lockout():
    pm = PairingManager()
    code = pm.generate_code()
    
    for _ in range(5):
        assert not pm.verify_code("000000")
        
    # Lockout should prevent the correct code from working
    assert not pm.verify_code(code)

def test_pairing_uses_secrets():
    with mock.patch("pocketrelay.security.pairing.secrets.randbelow") as mock_rand:
        mock_rand.return_value = 123456
        pm = PairingManager()
        pm.generate_code()
        mock_rand.assert_called_once_with(900000)

def test_doctor_report():
    checks = run_doctor_checks()
    assert "Python Version" in checks
    assert "Git CLI" in checks
    
    report = format_doctor_report()
    assert "PocketRelay System Doctor" in report
