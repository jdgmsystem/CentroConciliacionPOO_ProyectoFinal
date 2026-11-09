# Verificación de los requisitos de la Actividad colaborativa N.° 3

**Fuente:** Documento de actividad proporcionado por la Universidad de Manizales. **Alcance:** código y documentación de este paquete, sin incluir publicación del repositorio.

| Requisito de la guía | Evidencia verificable |
|---|---|
| Contexto distinto a biblioteca, comercio y gestión académica | Centro de conciliación, descrito en `README.md` y el documento de diseño |
| Al menos seis clases concretas | Ocho clases concretas del dominio en `entidades.py`, `actuaciones.py`, `sistema.py` |
| Una clase abstracta | `Actuacion(ABC)` en `actuaciones.py`, con `@abstractmethod` |
| Tres clases derivadas de una común | `RevisionDocumental`, `Citacion` y `Audiencia` heredan de `Actuacion` |
| Constructores y encapsulamiento | `__init__`, atributos con `__`, propiedades y actualizaciones validadas |
| Métodos propios por clase | Métodos para correo, expedientes, casos, agenda y actuaciones |
| Sobrescritura de dos métodos | `describir()` y `ejecutar()` en las tres hijas |
| Polimorfismo sin condicionales por tipo | Lista `actuaciones` y único `for` en `main.py` |
| Dos relaciones entre objetos | Caso–Partes; Caso–Conciliador; caso–actuaciones; Citación–Parte |
| Una composición | `CasoConciliacion.__init__` crea `ExpedienteDigital` |
| Tres excepciones personalizadas | `CasoDuplicadoError`, `HorarioNoDisponibleError`, `EstadoCasoInvalidoError` |
| Ocho objetos como mínimo | Cuatro partes, dos conciliadores, tres casos, seis actuaciones y tres expedientes |
| Casos normales y excepcionales en principal | `main.py`, bloques `try/except` y continuación de la ejecución |
| Diagrama UML | `docs/Diagrama_UML.png`, `.svg`, `.dot` y `.puml` |
| Documento de Decisiones de Diseño | `docs/Documento_Decisiones_de_Diseno.docx`, con portada y desarrollo continuo |
| AI declarada y ajustada | Apartado específico del `README.md` y del documento de diseño |
| Ejecución y pruebas | `python main.py` y `python -m unittest discover -s tests -v`; 30/30 aprobadas |
| Repositorio y commits de todos los integrantes | **Acción externa no realizada en este paquete.** Deben publicarse en GitHub y crearse contribuciones auténticas de cada integrante. |

## Limitaciones intencionales del prototipo

Los registros son volátiles (solo en memoria) y la programación de sala no comprueba colisiones físicas de salas distintas del conflicto de conciliador. Los métodos `ejecutar()` simulan operaciones; no notifican a terceros ni acreditan actuaciones reales. Son límites coherentes con el alcance académico declarado.
