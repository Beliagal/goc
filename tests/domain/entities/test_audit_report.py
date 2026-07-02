"""Suite de pruebas unitarias para la entidad AuditReport bajo TDD estricto."""

import pytest
from uuid import UUID
from datetime import datetime
from src.domain.entities.audit_report import AuditReport
from src.domain.entities.finding import Finding
from src.domain.value_objects.vulnerability import VulnerabilityType


@pytest.fixture
def sample_finding():
    """Fixture que proporciona un hallazgo válido para las pruebas."""
    return Finding(
        vulnerability_type=VulnerabilityType("SQL_INJECTION"),
        file_path="src/auth.py",
        line_number=15,
        code_snippet="query = f'SELECT * FROM users WHERE name = {name}'",
        description="SQL Injection detectado."
    )


def test_should_create_valid_empty_report():
    """Debe instanciar un reporte válido sin hallazgos iniciales."""
    report = AuditReport(repository_url="https://github.com/Beliagal/goc")

    assert isinstance(report.id, UUID)
    assert report.repository_url == "https://github.com/Beliagal/goc"
    assert len(report.findings) == 0
    assert isinstance(report.created_at, datetime)


def test_should_allow_adding_findings():
    """Debe permitir añadir nuevos hallazgos al reporte de forma controlada."""
    report = AuditReport(repository_url="https://github.com/Beliagal/goc")
    finding = Finding(
        vulnerability_type=VulnerabilityType("XSS"),
        file_path="src/templates.py",
        line_number=10,
        code_snippet="<div>{user_input}</div>",
        description="XSS potencial."
    )

    report.add_finding(finding)
    assert len(report.findings) == 1
    assert report.findings[0] == finding


def test_findings_list_should_be_immutable_externally():
    """La lista de hallazgos expuesta no debe permitir modificaciones directas de tipo append."""
    report = AuditReport(repository_url="https://github.com/Beliagal/goc")
    
    # Debe lanzar un error o no alterar el estado interno si se intenta modificar la propiedad expuesta
    with pytest.raises(AttributeError):
        report.findings = []  # type: ignore


def test_should_calculate_correct_severity_summary(sample_finding):
    """Debe computar el resumen de severidades de forma exacta."""
    report = AuditReport(repository_url="https://github.com/Beliagal/goc")
    
    # Añadimos un hallazgo HIGH (SQL_INJECTION por defecto)
    report.add_finding(sample_finding)
    
    # Añadimos un hallazgo CRITICAL explícito
    critical_finding = Finding(
        vulnerability_type=VulnerabilityType("INSECURE_DESERIALIZATION"),
        file_path="src/pickle_loader.py",
        line_number=8,
        code_snippet="pickle.loads(data)",
        description="Deserialización insegura."
    )
    report.add_finding(critical_finding)

    summary = report.get_severity_summary()
    assert summary["CRITICAL"] == 1
    assert summary["HIGH"] == 1
    assert summary["MEDIUM"] == 0
    assert summary["LOW"] == 0
    assert summary["INFO"] == 0
    assert report.total_findings == 2