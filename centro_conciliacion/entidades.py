"""Entidades del dominio, encapsulamiento y composición."""
from __future__ import annotations

from .excepciones import EstadoCasoInvalidoError


def requerido(valor: str, nombre: str) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"{nombre} no puede estar vacío.")
    return valor.strip()


class Parte:
    """Participante de un proceso de conciliación."""
    def __init__(self, identificacion: str, nombre: str, correo: str):
        self.__identificacion = requerido(identificacion, "Identificación")
        self.__nombre = requerido(nombre, "Nombre")
        self.__correo = ""
        self.actualizar_correo(correo)

    @property
    def identificacion(self) -> str:
        return self.__identificacion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def correo(self) -> str:
        return self.__correo

    def actualizar_correo(self, correo: str) -> None:
        nuevo = requerido(correo, "Correo")
        if nuevo.count("@") != 1 or nuevo.startswith("@") or nuevo.endswith("@"):
            raise ValueError("El correo no tiene un formato básico válido.")
        self.__correo = nuevo

    def descripcion(self) -> str:
        return f"{self.nombre} ({self.identificacion})"


class Conciliador:
    """Responsable de actuaciones y audiencias."""
    def __init__(self, identificacion: str, nombre: str, especialidad: str):
        self.__identificacion = requerido(identificacion, "Identificación")
        self.__nombre = requerido(nombre, "Nombre")
        self.__especialidad = requerido(especialidad, "Especialidad")

    @property
    def identificacion(self) -> str:
        return self.__identificacion

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def especialidad(self) -> str:
        return self.__especialidad

    def descripcion(self) -> str:
        return f"{self.nombre} ({self.especialidad})"


class ExpedienteDigital:
    """Parte constitutiva de un caso: administra referencias de documentos."""
    def __init__(self, radicado: str):
        self.__radicado = requerido(radicado, "Radicado")
        self.__documentos: list[str] = []

    @property
    def radicado(self) -> str:
        return self.__radicado

    @property
    def documentos(self) -> tuple[str, ...]:
        return tuple(self.__documentos)

    def anexar_documento(self, nombre: str) -> None:
        nuevo = requerido(nombre, "Documento")
        if nuevo in self.__documentos:
            raise ValueError("El documento ya está referenciado.")
        self.__documentos.append(nuevo)

    def contar_documentos(self) -> int:
        return len(self.__documentos)


class CasoConciliacion:
    """Agregado raíz: relaciones con partes, conciliador y actuaciones."""
    RADICADO = "RADICADO"
    EN_TRAMITE = "EN_TRAMITE"
    CERRADO = "CERRADO"

    def __init__(self, radicado: str, asunto: str, solicitante: Parte,
                 convocado: Parte, conciliador: Conciliador):
        if not isinstance(solicitante, Parte) or not isinstance(convocado, Parte):
            raise TypeError("Solicitante y convocado deben ser objetos Parte.")
        if solicitante.identificacion == convocado.identificacion:
            raise ValueError("Solicitante y convocado deben ser distintos.")
        if not isinstance(conciliador, Conciliador):
            raise TypeError("El responsable debe ser un objeto Conciliador.")
        self.__radicado = requerido(radicado, "Radicado")
        self.__asunto = requerido(asunto, "Asunto")
        self.__solicitante = solicitante
        self.__convocado = convocado
        self.__conciliador = conciliador
        self.__estado = self.RADICADO
        self.__expediente = ExpedienteDigital(self.__radicado)  # COMPOSICIÓN
        self.__actuaciones: list[object] = []

    @property
    def radicado(self) -> str:
        return self.__radicado

    @property
    def asunto(self) -> str:
        return self.__asunto

    @property
    def solicitante(self) -> Parte:
        return self.__solicitante

    @property
    def convocado(self) -> Parte:
        return self.__convocado

    @property
    def conciliador(self) -> Conciliador:
        return self.__conciliador

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def expediente(self) -> ExpedienteDigital:
        return self.__expediente

    @property
    def actuaciones(self) -> tuple[object, ...]:
        return tuple(self.__actuaciones)

    def actualizar_asunto(self, asunto: str) -> None:
        if self.estado == self.CERRADO:
            raise EstadoCasoInvalidoError("No puede modificarse un caso cerrado.")
        self.__asunto = requerido(asunto, "Asunto")

    def registrar_actuacion(self, actuacion: object) -> None:
        from .actuaciones import Actuacion
        if self.estado == self.CERRADO:
            raise EstadoCasoInvalidoError("No se admiten actuaciones en un caso cerrado.")
        if not isinstance(actuacion, Actuacion):
            raise TypeError("Debe recibirse una actuación válida.")
        if any(a.codigo == actuacion.codigo for a in self.__actuaciones):
            raise ValueError("Ya existe una actuación con ese código en el caso.")
        self.__actuaciones.append(actuacion)
        self.__estado = self.EN_TRAMITE

    def cerrar(self, observacion: str) -> None:
        if self.estado != self.EN_TRAMITE:
            raise EstadoCasoInvalidoError(
                f"El caso {self.radicado} está en {self.estado}; no puede cerrarse.")
        documento = f"Cierre: {requerido(observacion, 'Observación')}"
        self.__expediente.anexar_documento(documento)
        self.__estado = self.CERRADO

    def resumen(self) -> str:
        return (f"{self.radicado} | {self.asunto} | {self.estado} | "
                f"Solicitante: {self.solicitante.nombre} | "
                f"Convocado: {self.convocado.nombre} | "
                f"Conciliador: {self.conciliador.nombre} | "
                f"Actuaciones: {len(self.__actuaciones)} | "
                f"Documentos: {self.expediente.contar_documentos()}")
