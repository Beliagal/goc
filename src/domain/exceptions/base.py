"""Módulo de excepciones base para el dominio de Guardian of the Code.

Garantiza un control de errores semántico y fuertemente tipado, evitando
el uso de excepciones genéricas de Python en las capas internas.
"""


class DomainException(Exception):
    """Excepción base para todos los errores de lógica de negocio del dominio."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class InvalidSeverityError(DomainException):
    """Se lanza cuando se intenta instanciar una severidad que no es válida."""

    def __init__(self, invalid_value: str) -> None:
        message = (
            f"El valor '{invalid_value}' no es una severidad válida. "
            "Valores permitidos: CRITICAL, HIGH, MEDIUM, LOW, INFO."
        )
        super().__init__(message)
        self.invalid_value = invalid_value


class UnsupportedVulnerabilityTypeError(DomainException):
    """Se lanza cuando se invoca una categoría de vulnerabilidad no soportada."""

    def __init__(self, invalid_name: str) -> None:
        message = (
            f"El tipo de vulnerabilidad '{invalid_name}' no está catalogado en el sistema "
            "o infringe las directrices de taxonomía OWASP/CWE integradas."
        )
        super().__init__(message)
        self.invalid_name = invalid_name


class InvalidFindingError(DomainException):
    """Se lanza cuando un hallazgo viola las reglas de validación estructural del dominio."""
    pass