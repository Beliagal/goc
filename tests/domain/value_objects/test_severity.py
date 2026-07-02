"""Suite de pruebas unitarias para el Value Object Severity bajo TDD estricto."""

import pytest
from dataclasses import FrozenInstanceError
from src.domain.value_objects.severity import Severity
from src.domain.exceptions.base import InvalidSeverityError


def test_should_create_valid_severity():
    """Debe permitir la instanciación de severidades válidas en mayúsculas."""
    severity = Severity("CRITICAL")
    assert severity.value == "CRITICAL"


def test_should_normalize_lowercase_input():
    """Debe normalizar automáticamente las entradas en minúsculas a mayúsculas."""
    severity = Severity("high")
    assert severity.value == "HIGH"


def test_should_raise_error_for_invalid_severity():
    """Debe lanzar InvalidSeverityError si el valor proporcionado no está tipificado."""
    with pytest.raises(InvalidSeverityError) as exc_info:
        Severity("UNKNOWN_SEVERITY")

    assert "UNKNOWN_SEVERITY" in exc_info.value.message


def test_severity_equality_by_value():
    """Dos instancias con el mismo valor deben ser estructuralmente iguales."""
    sev1 = Severity("MEDIUM")
    sev2 = Severity("medium")
    assert sev1 == sev2


def test_severity_immutability():
    """Debe garantizar la inmutabilidad y lanzar un error si se intenta modificar."""
    severity = Severity("LOW")
    with pytest.raises(FrozenInstanceError):
        severity.value = "HIGH"  # type: ignore


def test_severity_logical_comparisons():
    """Debe validar la ordenación lógica basada en la gravedad del hallazgo."""
    critical = Severity("CRITICAL")
    high = Severity("HIGH")
    medium = Severity("MEDIUM")
    low = Severity("LOW")
    info = Severity("INFO")

    assert critical > high
    assert high >= medium
    assert low < medium
    assert info <= low
    assert critical != info