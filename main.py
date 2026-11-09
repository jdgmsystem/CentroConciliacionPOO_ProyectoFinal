"""Demostración de casos normales, tres excepciones y polimorfismo real."""
from datetime import datetime
from centro_conciliacion import (
    Audiencia, CasoConciliacion, CasoDuplicadoError, CentroConciliacion,
    Citacion, Conciliador, EstadoCasoInvalidoError,
    HorarioNoDisponibleError, Parte, RevisionDocumental,
)


def demostracion() -> None:
    print("SISTEMA DE GESTIÓN DE CASOS Y AUDIENCIAS - DEMO ACADÉMICA")
    centro = CentroConciliacion("Centro de Conciliación de Demostración")
    p1 = Parte("P01", "Ana Pérez", "ana@ejemplo.test")
    p2 = Parte("P02", "Luis Rojas", "luis@ejemplo.test")
    p3 = Parte("P03", "Diana León", "diana@ejemplo.test")
    p4 = Parte("P04", "Carlos Mora", "carlos@ejemplo.test")
    profesional1 = Conciliador("C01", "Andrea Ruiz", "Civil")
    profesional2 = Conciliador("C02", "Felipe Torres", "Familia")
    c1 = CasoConciliacion("CC-001", "Diferencia contractual", p1, p2, profesional1)
    c2 = CasoConciliacion("CC-002", "Incumplimiento de acuerdo", p3, p4, profesional1)
    c3 = CasoConciliacion("CC-003", "Conflicto de convivencia", p1, p4, profesional2)
    for caso in (c1, c2, c3):
        centro.registrar_caso(caso)
    c1.expediente.anexar_documento("Solicitud inicial")
    c1.expediente.anexar_documento("Documentos aportados")
    p1.actualizar_correo("ana.actualizado@ejemplo.test")
    c2.actualizar_asunto("Diferencia por incumplimiento de acuerdo")
    print("\nCREACIÓN / ENCAPSULAMIENTO / COMPOSICIÓN")
    print(centro.resumen())
    print("Correo actualizado:", p1.correo)
    print("Asunto actualizado:", c2.asunto)
    print("Expediente:", c1.expediente.radicado, c1.expediente.documentos)

    r1 = RevisionDocumental("ACT-01", datetime(2026, 11, 18, 8), ["Solicitud inicial", "Documentos aportados"])
    t1 = Citacion("ACT-02", datetime(2026, 11, 18, 9), p2, "correo")
    a1 = Audiencia("ACT-03", datetime(2026, 11, 19, 9), "Sala 1")
    r2 = RevisionDocumental("ACT-04", datetime(2026, 11, 18, 10), ["Petición inicial"])
    t2 = Citacion("ACT-05", datetime(2026, 11, 18, 11), p4, "comunicación")
    a2 = Audiencia("ACT-06", datetime(2026, 11, 19, 11), "Sala 2")
    c1.registrar_actuacion(r1)
    c1.registrar_actuacion(t1)
    c2.registrar_actuacion(r2)
    c2.registrar_actuacion(t2)
    centro.programar_audiencia(c1.radicado, a1)
    centro.programar_audiencia(c2.radicado, a2)

    print("\nPOLIMORFISMO: UNA COLECCIÓN HETEROGÉNEA Y UN ÚNICO CICLO")
    actuaciones = [r1, t1, a1, r2, t2, a2]
    for actuacion in actuaciones:
        print(actuacion.describir())
        print("  " + actuacion.ejecutar())

    print("\nTRES EXCEPCIONES PERSONALIZADAS CAPTURADAS")
    try:
        centro.registrar_caso(c1)
    except CasoDuplicadoError as error:
        print("[Radicado duplicado]", error)
    try:
        centro.programar_audiencia(c2.radicado, Audiencia("ACT-07", datetime(2026, 11, 19, 9), "Sala 3"))
    except HorarioNoDisponibleError as error:
        print("[Conflicto de agenda]", error)
    try:
        c3.cerrar("Cierre prematuro")
    except EstadoCasoInvalidoError as error:
        print("[Estado incompatible]", error)

    try:
        p1.actualizar_correo("")
    except ValueError as error:
        print("[Validación de dato encapsulado]", error)
    print("El correo conserva el valor válido:", p1.correo)
    c1.cerrar("Cierre administrativo simulado")
    print("\nCONTINUIDAD DESPUÉS DE LOS ERRORES")
    for caso in centro.casos:
        print(caso.resumen())
    print(centro.resumen())
    print("FIN DE LA DEMOSTRACIÓN")


if __name__ == '__main__':
    demostracion()
