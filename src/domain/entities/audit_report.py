"""Definición de la entidad AuditReport dentro del núcleo del dominio."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Tuple, Dict
from src.domain.entities.finding import Finding


@dataclass
class AuditReport:
    """Representa el reporte consolidado de una auditoría de seguridad de un repositorio.

    Actúa como raíz del agregado para controlar la colección de hallazgos detectados
    y exponer métricas operacionales computadas en caliente.
    """

    repository_url: str
    id: UUID = field(default_factory=uuid4, init=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc), init=False)
    _findings: List[Finding] = field(default_factory=list, init=False)

    @property
    def findings(self) -> Tuple[Finding, ...]:
        """Expone los hallazgos actuales de forma inmutable para evitar efectos secundarios externos."""
        return tuple(self._findings)

    @property
    def total_findings(self) -> int:
        """Devuelve el volumen total de vulnerabilidades registradas."""
        return len(self._findings)

    def add_finding(self, finding: Finding) -> None:
        """Añade un hallazgo validado al reporte de auditoría.

        Args:
            finding: Instancia estructurada de la entidad Finding.
        """
        self._findings.append(finding)

    def get_severity_summary(self) -> Dict[str, int]:
        """Calcula al vuelo la distribución cuantitativa de los hallazgos por severidad.

        Returns:
            Diccionario estructurado con el conteo por cada nivel de Severity.
        """
        summary = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
            "INFO": 0
        }
        for finding in self._findings:
            summary[finding.severity.value] += 1
        return summary

    def __eq__(self, other: object) -> bool:
        """Compara la igualdad basándose de forma única en la identidad del reporte."""
        if not isinstance(other, AuditReport):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)