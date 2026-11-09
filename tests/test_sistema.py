"""Pruebas automatizadas de la Actividad N.° 3."""
import unittest
from datetime import datetime
from centro_conciliacion import (
    Actuacion, Audiencia, CasoConciliacion, CasoDuplicadoError,
    CentroConciliacion, Citacion, Conciliador,
    EstadoCasoInvalidoError, ExpedienteDigital,
    HorarioNoDisponibleError, Parte, RevisionDocumental,
)


class PruebasSistema(unittest.TestCase):
    def setUp(self):
        self.p1 = Parte('1', 'Ana', 'ana@ejemplo.test')
        self.p2 = Parte('2', 'Luis', 'luis@ejemplo.test')
        self.p3 = Parte('3', 'Diana', 'diana@ejemplo.test')
        self.conciliador = Conciliador('C1', 'Andrés', 'Civil')
        self.conciliador2 = Conciliador('C2', 'María', 'Familia')
        self.c1 = CasoConciliacion('CC-1', 'Diferencia civil', self.p1, self.p2, self.conciliador)
        self.c2 = CasoConciliacion('CC-2', 'Diferencia vecinal', self.p2, self.p3, self.conciliador)
        self.c3 = CasoConciliacion('CC-3', 'Otro asunto', self.p1, self.p3, self.conciliador2)
        self.centro = CentroConciliacion('Centro de pruebas')
        for caso in (self.c1, self.c2, self.c3):
            self.centro.registrar_caso(caso)
        self.fecha = datetime(2026, 11, 19, 9)

    def test_01_constructores(self):
        self.assertEqual(self.p1.nombre, 'Ana')
        self.assertEqual(self.conciliador.especialidad, 'Civil')
        self.assertEqual(self.c1.estado, 'RADICADO')

    def test_02_email_actualizable(self):
        self.p1.actualizar_correo('nuevo@ejemplo.test')
        self.assertEqual(self.p1.correo, 'nuevo@ejemplo.test')

    def test_03_cadena_vacia_no_modifica_correo(self):
        with self.assertRaises(ValueError):
            self.p1.actualizar_correo('  ')
        self.assertEqual(self.p1.correo, 'ana@ejemplo.test')

    def test_04_email_sin_arroba_invalido(self):
        with self.assertRaises(ValueError):
            self.p1.actualizar_correo('sin-arroba')
        self.assertEqual(self.p1.correo, 'ana@ejemplo.test')

    def test_05_atributo_correo_sin_setter(self):
        with self.assertRaises(AttributeError):
            self.p1.correo = 'invalido@ejemplo.test'

    def test_06_partes_distintas(self):
        with self.assertRaises(ValueError):
            CasoConciliacion('C4', 'Asunto', self.p1, self.p1, self.conciliador)

    def test_07_conciliador_requerido(self):
        with self.assertRaises(TypeError):
            CasoConciliacion('C4', 'Asunto', self.p1, self.p2, self.p1)

    def test_08_asunto_actualizacion_valida(self):
        self.c1.actualizar_asunto('Asunto nuevo')
        self.assertEqual(self.c1.asunto, 'Asunto nuevo')

    def test_09_asunto_vacio_no_modifica(self):
        with self.assertRaises(ValueError):
            self.c1.actualizar_asunto('')
        self.assertEqual(self.c1.asunto, 'Diferencia civil')

    def test_10_composicion_creacion_interna(self):
        self.assertIsInstance(self.c1.expediente, ExpedienteDigital)
        self.assertEqual(self.c1.expediente.radicado, self.c1.radicado)
        self.assertIsNot(self.c1.expediente, self.c2.expediente)

    def test_11_expediente_control_de_documentos(self):
        self.c1.expediente.anexar_documento('Solicitud')
        self.assertEqual(self.c1.expediente.documentos, ('Solicitud',))
        with self.assertRaises(ValueError):
            self.c1.expediente.anexar_documento('Solicitud')

    def test_12_expediente_no_expone_lista(self):
        with self.assertRaises(AttributeError):
            self.c1.expediente.documentos.append('Alteración')

    def test_13_clase_abstracta(self):
        with self.assertRaises(TypeError):
            Actuacion('A1', self.fecha)

    def test_14_tres_especializaciones(self):
        objetos = [RevisionDocumental('R', self.fecha, ['Solicitud']),
                   Citacion('C', self.fecha, self.p2, 'Correo'),
                   Audiencia('A', self.fecha, 'Sala 1')]
        self.assertTrue(all(isinstance(o, Actuacion) for o in objetos))

    def test_15_polimorfismo_dos_metodos(self):
        objetos = [RevisionDocumental('R', self.fecha, ['Solicitud']),
                   Citacion('C', self.fecha, self.p2, 'Correo'),
                   Audiencia('A', self.fecha, 'Sala 1')]
        self.assertEqual(len({o.describir() for o in objetos}), 3)
        self.assertEqual(len({o.ejecutar() for o in objetos}), 3)

    def test_16_revision_documental_vacia(self):
        with self.assertRaises(ValueError):
            RevisionDocumental('A1', self.fecha, [])

    def test_17_citacion_destinatario_tipo(self):
        with self.assertRaises(TypeError):
            Citacion('A1', self.fecha, 'nombre', 'Correo')

    def test_18_fecha_invalida(self):
        with self.assertRaises(TypeError):
            Audiencia('A1', 'mañana', 'Sala 1')

    def test_19_registro_actuacion_cambia_estado(self):
        self.c1.registrar_actuacion(RevisionDocumental('R1', self.fecha, ['Solicitud']))
        self.assertEqual(self.c1.estado, 'EN_TRAMITE')

    def test_20_registro_de_objeto_no_actuacion(self):
        with self.assertRaises(TypeError):
            self.c1.registrar_actuacion(self.p1)

    def test_21_codigo_actuacion_duplicado(self):
        self.c1.registrar_actuacion(RevisionDocumental('R1', self.fecha, ['Solicitud']))
        with self.assertRaises(ValueError):
            self.c1.registrar_actuacion(Citacion('R1', self.fecha, self.p2, 'Correo'))

    def test_22_error_dominio_caso_duplicado(self):
        with self.assertRaises(CasoDuplicadoError):
            self.centro.registrar_caso(self.c1)
        self.assertEqual(len(self.centro.casos), 3)

    def test_23_error_dominio_horario_conflictivo(self):
        self.centro.programar_audiencia('CC-1', Audiencia('A1', self.fecha, 'Sala 1'))
        with self.assertRaises(HorarioNoDisponibleError):
            self.centro.programar_audiencia('CC-2', Audiencia('A2', self.fecha, 'Sala 2'))
        self.assertEqual(self.c2.estado, 'RADICADO')
        self.assertEqual(len(self.c2.actuaciones), 0)

    def test_24_hora_diferente_permitida(self):
        self.centro.programar_audiencia('CC-1', Audiencia('A1', self.fecha, 'Sala 1'))
        self.centro.programar_audiencia('CC-2', Audiencia('A2', datetime(2026, 11, 19, 11), 'Sala 2'))
        self.assertIn('2 audiencias', self.centro.resumen())

    def test_25_conciliador_diferente_misma_hora(self):
        self.centro.programar_audiencia('CC-1', Audiencia('A1', self.fecha, 'Sala 1'))
        self.centro.programar_audiencia('CC-3', Audiencia('A3', self.fecha, 'Sala 2'))
        self.assertEqual(len(self.c3.actuaciones), 1)

    def test_26_error_dominio_estado_cierre_prematuro(self):
        with self.assertRaises(EstadoCasoInvalidoError):
            self.c1.cerrar('No procede')
        self.assertEqual(self.c1.estado, 'RADICADO')

    def test_27_cierre_valido(self):
        self.c1.registrar_actuacion(RevisionDocumental('R1', self.fecha, ['Solicitud']))
        self.c1.cerrar('Cierre de prueba')
        self.assertEqual(self.c1.estado, 'CERRADO')
        self.assertEqual(self.c1.expediente.contar_documentos(), 1)

    def test_28_no_alterar_caso_cerrado(self):
        self.c1.registrar_actuacion(RevisionDocumental('R1', self.fecha, ['Solicitud']))
        self.c1.cerrar('Cierre de prueba')
        with self.assertRaises(EstadoCasoInvalidoError):
            self.c1.actualizar_asunto('Nuevo')
        with self.assertRaises(EstadoCasoInvalidoError):
            self.c1.registrar_actuacion(Audiencia('A1', self.fecha, 'Sala 1'))

    def test_29_conflicto_sin_ocupar_cupo(self):
        self.c1.registrar_actuacion(RevisionDocumental('R1', self.fecha, ['Solicitud']))
        self.c1.cerrar('Cierre de prueba')
        with self.assertRaises(EstadoCasoInvalidoError):
            self.centro.programar_audiencia('CC-1', Audiencia('A1', self.fecha, 'Sala 1'))
        self.centro.programar_audiencia('CC-2', Audiencia('A2', self.fecha, 'Sala 1'))
        self.assertEqual(len(self.c2.actuaciones), 1)

    def test_30_sistema_continua_despues_de_excepciones(self):
        atrapados = []
        try:
            self.centro.registrar_caso(self.c1)
        except CasoDuplicadoError as error:
            atrapados.append(str(error))
        try:
            self.c1.cerrar('No procede')
        except EstadoCasoInvalidoError as error:
            atrapados.append(str(error))
        self.centro.programar_audiencia('CC-2', Audiencia('A1', self.fecha, 'Sala 1'))
        self.assertEqual(len(atrapados), 2)
        self.assertEqual(self.c2.estado, 'EN_TRAMITE')


if __name__ == '__main__':
    unittest.main()
