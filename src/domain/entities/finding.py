"""Definición de la entidad Finding en el núcleo del dominio."""

from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Optional
from src.domain.value_objects.vulnerability import VulnerabilityType
from src.domain.value_objects.severity import Severity
from src.domain.exceptions.base import InvalidFindingError


@dataclass
class Finding:
    """Representa un hallazgo de vulnerabilidad o defecto de diseño detectado.

    Es una entidad con identidad propia (id) basada en UUID4 y maneja sus propias
    reglas de validación estructural invariants.
    """

    vulnerability_type: VulnerabilityType
    file_path: str
    line_number: int
    code_snippet: str
    description: str
    severity: Severity = field(init=False)
    id: UUID = field(default_factory=uuid4, init=False)

    def __post_init__(self) -> None:
        """Valida las invariantes del hallazgo tras la instanciación de la factoría."""
        self._validate_invariants()
        
        # Si no se ha inyectado una severidad específica durante el ciclo de vida (vía bypass),
        # se asume la severidad recomendada por defecto de la vulnerabilidad detectada.
        if not hasattr(self, "severity"):
            self.severity = self.vulnerability_type.default_severity

    def __init__(
        self,
        vulnerability_type: VulnerabilityType,
        file_path: str,
        line_number: int,
        code_snippet: str,
        description: str,
        severity: Optional[Severity] = None,
    ) -> None:
        """Constructor personalizado para permitir inicialización flexible y limpia."""
        self.vulnerability_type = vulnerability_type
        self.file_path = file_path
        self.line_number = line_number
        self.code_snippet = code_snippet
        self.description = description
        self.id = uuid4()
        
        if severity is not None:
            self.severity = severity
            
        self.__post_init__()

    def _validate_invariants(self) -> None:
        """Verifica de forma estricta las reglas de integridad de la entidad."""
        if not self.file_path or not self.file_path.strip():
            raise InvalidFindingError("La ruta del archivo no puede estar vacía o contener solo espacios.")
            
        if self.line_number <= 0:
            raise InvalidFindingError(f"La línea de código debe ser un entero positivo. Recibido: {self.line_number}")

    def update_severity(self, new_severity: Severity) -> None:
        """Modifica la criticidad del hallazgo mediante lógica explícita de negocio.

        Args:
            new_severity: Instancia del objeto Severity con la nueva ponderación.
        """
        self.severity = new_severity

    def __eq__(self, other: object) -> bool:
        """Compara la igualdad basándose estrictamente en la identidad de la entidad."""
        if not isinstance(other, Finding):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)