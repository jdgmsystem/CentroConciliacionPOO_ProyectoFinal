# Centro de Conciliación — Proyecto Final de Programación Orientada a Objetos

**Universidad de Manizales — Facultad de Ciencias e Ingenierías**  
**Actividad colaborativa N.° 3 — Desarrollo de un Sistema Orientado a Objetos**  
**Autor de esta versión de demostración:** Juan David Gálvez Molina.

## Propósito y límites

Sistema informativo de **consola Python** que, con datos completamente ficticios, simula la gestión de casos, partes, conciliadores, expedientes digitales y actuaciones (revisiones documentales, citaciones y audiencias). Resuelve la duplicidad de radicados, la doble asignación de horarios a un mismo conciliador y las transiciones de estado indebidas.

Es un prototipo académico: **no** envía citaciones, **no** genera audiencias reales, **no** almacena archivos adjuntos, **no** incorpora trámites o plazos normativos y **no** persiste datos entre ejecuciones. No debe utilizarse para administrar expedientes reales.

## Requisitos y ejecución

Requiere **Python 3.10 o superior**, sin bibliotecas externas. Desde la carpeta raíz:

```bash
python main.py
```

En Windows también puede ejecutarse `py main.py`. Para verificar el código:

```bash
python -m unittest discover -s tests -v
```

**Resultado verificado en la elaboración:** 30 pruebas ejecutadas, 30 satisfactorias (`OK`). El programa principal se ejecutó de principio a fin, incluidos los tres errores personalizados capturados.

## Organización del proyecto

```text
CentroConciliacionPOO_ProyectoFinal/
├── main.py
├── centro_conciliacion/
│   ├── __init__.py
│   ├── entidades.py
│   ├── actuaciones.py
│   ├── excepciones.py
│   └── sistema.py
├── tests/
│   └── test_sistema.py
├── docs/
│   ├── Diagrama_UML.png
│   ├── Diagrama_UML.svg
│   ├── Diagrama_UML.dot
│   ├── Diagrama_UML.puml
│   └── Documento_Decisiones_de_Diseno.docx
├── .gitignore
└── README.md
```

## Diseño orientado a objetos

El código utiliza **ocho clases concretas** (`Parte`, `Conciliador`, `ExpedienteDigital`, `CasoConciliacion`, `CentroConciliacion`, `RevisionDocumental`, `Citacion` y `Audiencia`) y **una clase abstracta** (`Actuacion`). Tres clases (`RevisionDocumental`, `Citacion`, `Audiencia`) heredan de `Actuacion`: las tres **son actuaciones** y comparten código, fecha y un método común para presentar la fecha. Cada una sobrescribe `describir()` y `ejecutar()` con datos propios.

Los atributos se mantienen encapsulados mediante `__atributo` y propiedades de consulta. Los métodos de actualización validan campos vacíos, formatos básicos y restricciones de estado. `CasoConciliacion` se relaciona con **dos partes**, **un conciliador** y **varias actuaciones**. La relación de **composición** une `CasoConciliacion` y `ExpedienteDigital`, pues cada caso crea su expediente dentro del constructor, sin recibirlo externamente ni compartirlo.

**Polimorfismo:** en `main.py`, `actuaciones = [r1, t1, a1, r2, t2, a2]` contiene seis instancias de tres clases distintas. Un **único ciclo `for`** llama a `actuacion.describir()` y `actuacion.ejecutar()`, sin `if`, `type()` ni `isinstance()` para escoger la implementación.

**Tres excepciones personalizadas:** `CasoDuplicadoError` se lanza al registrar un radicado existente; `HorarioNoDisponibleError`, cuando el conciliador ya está reservado en la misma fecha y hora; y `EstadoCasoInvalidoError`, al intentar cerrar un caso que no está en trámite o modificar uno cerrado. `main.py` las captura de manera separada y demuestra que el servicio sigue operativo.

El ejemplo crea **más de ocho objetos** (partes, conciliadores, casos, actuaciones y expedientes). Las pruebas abarcan herencia, abstracción, sobrescritura, polimorfismo, composición, reglas, validaciones y errores recuperables.

## UML y decisiones de diseño

El gráfico está en `docs/Diagrama_UML.png`; las versiones editables se incluyen en `.puml` (PlantUML) y `.dot` (Graphviz). El documento técnico `docs/Documento_Decisiones_de_Diseno.docx` integra las decisiones de arquitectura, los métodos y atributos concretos, la evolución del diseño, las pruebas y la declaración de IA, conforme a los quince asuntos de la guía.

## Declaración del uso de inteligencia artificial

**Herramienta utilizada:** ChatGPT de OpenAI. Su contribución fue **sustancial**: selección y delimitación del contexto, modelado de clases y relaciones, generación inicial y revisión de código Python, elaboración de las pruebas, construcción del diagrama y redacción de documentación. Se descartó la posibilidad inicial de reutilizar el sistema académico de la Actividad N.° 1 porque la guía final lo prohíbe. También se revisó que la herencia representara una relación «es un», que la composición construyera el expediente en el propio caso y que las excepciones fuesen del dominio. La responsabilidad académica de revisar, comprender y justificar el trabajo corresponde a quienes lo entreguen.

## Entrega mediante GitHub

Publicar **un nuevo repositorio**, diferente del usado para el Sistema de Gestión Académica. En el directorio del proyecto:

```bash
git init
git add .
git commit -m "Implementa sistema de conciliación con POO y pruebas"
git branch -M main
git remote add origin https://github.com/USUARIO/REPOSITORIO_REAL.git
git push -u origin main
```

La URL anterior es únicamente un **ejemplo para sustituir**, no un enlace publicado. Cada integrante que participe debe registrar **al menos un commit con contribución sustantiva real**. El equipo debe verificar el registro de commits y aportar el **enlace real al repositorio** en la plataforma. Esta versión no modifica la entrega de la Actividad N.° 1.
