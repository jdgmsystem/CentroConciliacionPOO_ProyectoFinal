"""Excepciones propias del centro de conciliación."""

class ErrorConciliacion(Exception):
    """Error base del dominio."""

class CasoDuplicadoError(ErrorConciliacion):
    """El radicado ya está registrado."""

class HorarioNoDisponibleError(ErrorConciliacion):
    """El conciliador tiene una audiencia en el mismo horario."""

class EstadoCasoInvalidoError(ErrorConciliacion):
    """Una transición de estado no está permitida."""
