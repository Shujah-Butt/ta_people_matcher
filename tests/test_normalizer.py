from normalizer import (
    normalize_cnic,
    normalize_email,
    normalize_phone,
    normalize_name,
)


def test_normalize_cnic():
    assert normalize_cnic("35202-1234567-8") == "3520212345678"


def test_email():
    assert normalize_email(" Ali@Gmail.COM ") == "ali@gmail.com"


def test_phone():
    assert normalize_phone("+92-300-1234567") == "923001234567"


def test_name():
    assert normalize_name(" Muhammad   Zia Khan ") == "muhammad zia khan"