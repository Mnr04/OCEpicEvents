import pytest
from utils import validate_email, validate_phone, validate_amount, validate_dates

def test_validate_email_valide():
    assert validate_email("test@epicevents.com") is True
    assert validate_email("prenom.nom@domaine.fr") is True

def test_validate_email_invalide():
    assert validate_email("test@.com") is False
    assert validate_email("test.com") is False
    assert validate_email("test@domaine") is False
    assert validate_email("") is False

def test_validate_phone_valide():
    assert validate_phone("+33612345678") is True
    assert validate_phone("0612345678") is True
    assert validate_phone("01 23 45 67 89") is True

def test_validate_phone_invalide():
    assert validate_phone("123") is False
    assert validate_phone("abcdefghij") is False
    assert validate_phone("") is False

def test_validate_amount_valide():
    assert validate_amount(1000) is True
    assert validate_amount(1000.50) is True
    assert validate_amount("500") is True
    assert validate_amount(0) is True

def test_validate_amount_invalide():
    assert validate_amount(-50) is False
    assert validate_amount("cent euros") is False
    assert validate_amount("") is False

def test_validate_dates_valide():
    assert validate_dates("2026-05-10 14:00", "2026-05-10 18:00") is True
    assert validate_dates("2026-05-10 14:00", "2026-05-12 14:00") is True

def test_validate_dates_invalide():
    assert validate_dates("2026-05-10 18:00", "2026-05-10 14:00") is False
    assert validate_dates("10/05/2026 14:00", "10/05/2026 18:00") is False
    assert validate_dates("Texte", "Texte") is False