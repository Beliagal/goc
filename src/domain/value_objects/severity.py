"""Definición del Value Object Severity dentro del núcleo del dominio."""

from dataclasses import dataclass
from functools import total_ordering
from typing import Final, ClassVar, Dict
from src.domain.exceptions.base import InvalidSeverityError


@dataclass(frozen=True, slots=True)
@total_ordering
class Severity:
    """Representa la criticidad o severidad de una vulnerabilidad de software.

    Garantiza la inmutabilidad de los datos de negocio y expone operadores
    de comparación lógica para evaluar gravedades.
    """

    value: str

    # Tabla de pesos internos para resolver la ordenación matemática total
    _WEIGHTS: ClassVar[Dict[str, int]] = {
        "INFO": 1,
        "LOW": 2,
        "MEDIUM": 3,
        "HIGH": 4,
        "CRITICAL": 5,
    }

    def __init__(self, value: str) -> None:
        """Inicializa y valida la severidad de forma agnóstica a frameworks.

        Args:
            value: Cadena de caracteres con el nivel de criticidad.

        Raises:
            InvalidSeverityError: Si el valor no se encuentra en los pesos permitidos.
        """
        normalized_value: Final[str] = value.strip().upper()

        if normalized_value not in self._WEIGHTS:
            raise InvalidSeverityError(value)

        # Bypass obligatorio de dataclasses congeladas para asignación en inicializador personalizado
        object.__setattr__(self, "value", normalized_value)

    def __lt__(self, other: object) -> bool:
        """Define si una severidad es estrictamente menor que otra basada en su peso."""
        if not isinstance(other, Severity):
            return NotImplemented
        return self._WEIGHTS[self.value] < self._WEIGHTS[other.value]

    def __str__(self) -> str:
        return self.value