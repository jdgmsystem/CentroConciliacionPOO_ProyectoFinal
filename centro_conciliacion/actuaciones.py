"""Una clase abstracta con tres subtipos y dos métodos sobrescritos."""
from abc import ABC, abstractmethod
from datetime import datetime
from .entidades import Parte, requerido


class Actuacion(ABC):
    """Concepto abstracto: una actuación genérica no es ejecutable."""
    def __init__(self, codigo: str, fecha: datetime):
        self.__codigo = requerido(codigo, "Código de actuación")
        if not isinstance(fecha, datetime):
            raise TypeError("La fecha debe ser datetime.")
        self.__fecha = fecha

    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def fecha(self) -> datetime:
        return self.__fecha

    def fecha_legible(self) -> str:
        return self.fecha.strftime("%d/%m/%Y %H:%M")

    @abstractmethod
    def describir(self) -> str:
        """Descripción especializada."""

    @abstractmethod
    def ejecutar(self) -> str:
        """Resultado simulado especializado."""


class RevisionDocumental(Actuacion):
    """Es una actuación de verificación de documentación."""
    def __init__(self, codigo: str, fecha: datetime, documentos: list[str]):
        super().__init__(codigo, fecha)
        if not documentos:
            raise ValueError("La revisión requiere documentos.")
        self.__documentos = tuple(requerido(x, "Documento") for x in documentos)

    @property
    def documentos(self) -> tuple[str, ...]:
        return self.__documentos

    def describir(self) -> str:
        return f"Revisión {self.codigo}: {len(self.documentos)} documentos - {self.fecha_legible()}"

    def ejecutar(self) -> str:
        return f"Simulación de revisión: {', '.join(self.documentos)}"


class Citacion(Actuacion):
    """Es una actuación de preparación de citación; no envía comunicaciones."""
    def __init__(self, codigo: str, fecha: datetime, destinatario: Parte, medio: str):
        super().__init__(codigo, fecha)
        if not isinstance(destinatario, Parte):
            raise TypeError("Destinatario debe ser una Parte.")
        self.__destinatario = destinatario
        self.__medio = requerido(medio, "Medio de citación")

    @property
    def destinatario(self) -> Parte:
        return self.__destinatario

    @property
    def medio(self) -> str:
        return self.__medio

    def describir(self) -> str:
        return (f"Citación {self.codigo}: {self.destinatario.nombre}, "
                f"por {self.medio} - {self.fecha_legible()}")

    def ejecutar(self) -> str:
        return f"Simulación: citación preparada para {self.destinatario.nombre} por {self.medio}"


class Audiencia(Actuacion):
    """Es una actuación consistente en agendar una audiencia."""
    def __init__(self, codigo: str, fecha: datetime, sala: str):
        super().__init__(codigo, fecha)
        self.__sala = requerido(sala, "Sala")

    @property
    def sala(self) -> str:
        return self.__sala

    def describir(self) -> str:
        return f"Audiencia {self.codigo}: {self.sala} - {self.fecha_legible()}"

    def ejecutar(self) -> str:
        return f"Simulación: audiencia programada en {self.sala} para {self.fecha_legible()}"
