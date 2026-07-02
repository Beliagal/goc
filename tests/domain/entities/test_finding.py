"""Suite de pruebas unitarias para la entidad Finding bajo TDD estricto."""

import pytest
from uuid import UUID
from src.domain.entities.finding import Finding
from src.domain.value_objects.vulnerability import VulnerabilityType
from src.domain.value_objects.severity import Severity
from src.domain.exceptions.base import InvalidFindingError


def test_should_create_valid_finding_with_defaults():
    """Debe instanciar un hallazgo válido y asignar un UUID automático y la severidad por defecto."""
    vuln_type = VulnerabilityType("SQL_INJECTION")
    finding = Finding(
        vulnerability_type=vuln_type,
        file_path="src/infrastructure/db.py",
        line_number=42,
        code_snippet="cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')",
        description="Inyección SQL directa detectada por concatenación de strings."
    )

    assert isinstance(finding.id, UUID)
    assert finding.vulnerability_type == vuln_type
    assert finding.severity == vuln_type.default_severity
    assert finding.file_path == "src/infrastructure/db.py"
    assert finding.line_number == 42


def test_should_allow_explicit_severity_override():
    """Debe permitir instanciar un hallazgo forzando una severidad distinta a la de por defecto."""
    vuln_type = VulnerabilityType("XSS")  # Default is MEDIUM
    custom_severity = Severity("CRITICAL")

    finding = Finding(
        vulnerability_type=vuln_type,
        file_path="src/views.py",
        line_number=12,
        code_snippet="return HTML(user_input)",
        description="XSS reflejado crítico en punto de entrada de administración.",
        severity=custom_severity
    )

    assert finding.severity == custom_severity


def test_should_raise_error_for_invalid_line_number():
    """Debe lanzar InvalidFindingError si la línea de código es menor o igual a cero."""
    vuln_type = VulnerabilityType("USE_OF_WEAK_HASH")
    
    with pytest.raises(InvalidFindingError, match="La línea de código debe ser un entero positivo"):
        Finding(
            vulnerability_type=vuln_type,
            file_path="src/utils.py",
            line_number=0,
            code_snippet="md5(pass)",
            description="Uso de hash débil."
        )


@pytest.mark.parametrize("empty_value", ["", "   ", "\t"])
def test_should_raise_error_for_empty_file_path(empty_value: str):
    """Debe impedir rutas de archivo vacías o con puros espacios."""
    vuln_type = VulnerabilityType("HARDCODED_CREDENTIALS")
    
    with pytest.raises(InvalidFindingError, match="La ruta del archivo no puede estar vacía"):
        Finding(
            vulnerability_type=vuln_type,
            file_path=empty_value,
            line_number=10,
            code_snippet="secret = '123'",
            description="Clave a fuego."
        )


def test_identity_equality_based_only_on_id():
    """Dos entidades Finding con el mismo ID son iguales, independientemente de sus datos."""
    vuln_type = VulnerabilityType("XSS")
    finding1 = Finding(
        vulnerability_type=vuln_type,
        file_path="a.py",
        line_number=1,
        code_snippet="...",
        description="Desc"
    )
    
    # Clonamos la instancia modificando campos pero manteniendo el mismo ID exacto
    finding2 = Finding(
        vulnerability_type=vuln_type,
        file_path="b.py",
        line_number=99,
        code_snippet="different_code()",
        description="Diferente descripción",
        severity=Severity("CRITICAL")
    )
    object.__setattr__(finding2, "id", finding1.id)

    assert finding1 == finding2


def test_should_allow_business_mutation_methods():
    """Debe permitir actualizar la severidad mediante métodos semánticos explícitos."""
    vuln_type = VulnerabilityType("SQL_INJECTION")
    finding = Finding(
        vulnerability_type=vuln_type,
        file_path="src/db.py",
        line_number=5,
        code_snippet="...",
        description="..."
    )
    
    new_severity = Severity("LOW")
    finding.update_severity(new_severity)
    assert finding.severity == new_severity