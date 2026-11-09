"""Servicio coordinador de casos y agenda de conciliadores."""
from .actuaciones import Audiencia
from .entidades import CasoConciliacion, requerido
from .excepciones import CasoDuplicadoError, HorarioNoDisponibleError


class CentroConciliacion:
    """Registra casos y evita conflictos de agenda por conciliador y fecha."""
    def __init__(self, nombre: str):
        self.__nombre = requerido(nombre, "Centro")
        self.__casos: dict[str, CasoConciliacion] = {}
        self.__agenda: dict[tuple, str] = {}

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def casos(self) -> tuple[CasoConciliacion, ...]:
        return tuple(self.__casos.values())

    def registrar_caso(self, caso: CasoConciliacion) -> None:
        if not isinstance(caso, CasoConciliacion):
            raise TypeError("Debe registrarse un CasoConciliacion.")
        if caso.radicado in self.__casos:
            raise CasoDuplicadoError(f"Ya existe el radicado {caso.radicado}.")
        self.__casos[caso.radicado] = caso

    def consultar_caso(self, radicado: str) -> CasoConciliacion:
        return self.__casos[radicado]

    def programar_audiencia(self, radicado: str, audiencia: Audiencia) -> None:
        if not isinstance(audiencia, Audiencia):
            raise TypeError("Debe programarse una Audiencia.")
        caso = self.consultar_caso(radicado)
        clave = (caso.conciliador.identificacion, audiencia.fecha)
        if clave in self.__agenda:
            raise HorarioNoDisponibleError(
                f"{caso.conciliador.nombre} tiene audiencia a las "
                f"{audiencia.fecha_legible()} en el caso {self.__agenda[clave]}.")
        # Sólo ocupa el horario si el registro interno finaliza correctamente.
        caso.registrar_actuacion(audiencia)
        self.__agenda[clave] = radicado

    def resumen(self) -> str:
        return f"{self.nombre}: {len(self.__casos)} casos, {len(self.__agenda)} audiencias"
