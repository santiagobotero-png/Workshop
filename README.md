# Recruitment Data Warehouse - ETL

## 1. Objetivo del proyecto

El objetivo de este proyecto es diseñar e implementar un proceso ETL para transformar datos transaccionales de un proceso de reclutamiento tecnológico en un Data Warehouse dimensional orientado al análisis.

El proyecto comprende las etapas de extracción, preparación, transformación de reglas de negocio, modelado dimensional, carga en un Data Warehouse y análisis mediante consultas SQL y una herramienta de Business Intelligence.

El Data Warehouse está diseñado para responder cinco requerimientos de negocio relacionados con tendencias de contratación, análisis por tecnología, perfil de los candidatos, efectividad de las evaluaciones técnicas y relación entre tecnologías, evaluaciones y contratación.

## 2. Contexto de negocio

La organización del caso de estudio es una empresa dedicada al reclutamiento de profesionales del área tecnológica. La empresa recibe miles de aplicaciones de candidatos para diferentes perfiles y tecnologías.

Cada aplicación contiene información sobre el candidato, la fecha de aplicación, el país, los años de experiencia, el nivel de seniority, la tecnología asociada y los resultados obtenidos en dos evaluaciones técnicas:

- Code Challenge Score
- Technical Interview Score

La organización necesita transformar estos datos operacionales en información analítica que permita identificar patrones de contratación y apoyar la toma de decisiones.

Para determinar si una aplicación resulta en una contratación se utiliza la siguiente regla de negocio:

HIRED = Code Challenge Score >= 7 AND Technical Interview Score >= 7

Por lo tanto, un candidato es considerado contratado únicamente cuando obtiene una puntuación de al menos 7 en ambas evaluaciones.


## 3. Requerimientos de negocio

### R1 - Hiring Trends

Analizar las tendencias de contratación a lo largo del tiempo para estudiar cómo evoluciona el comportamiento de las aplicaciones y contrataciones entre diferentes períodos.

**Pregunta de negocio:**

¿Cómo ha evolucionado el volumen de aplicaciones y la cantidad de candidatos contratados a lo largo del tiempo?

---

### R2 - Technology Analysis

Comparar los resultados de contratación entre las diferentes tecnologías para identificar cuáles generan el mayor número y proporción de candidatos contratados.

**Pregunta de negocio:**

¿Qué tecnologías presentan la mayor cantidad y proporción de candidatos contratados?

---

### R3 - Candidate Profile Analysis

Analizar los resultados de contratación de acuerdo con el nivel de seniority y los años de experiencia profesional de los candidatos.

**Pregunta de negocio:**

¿Cómo varía el resultado de contratación según el nivel de seniority y los años de experiencia profesional?

---

### R4 - Technical Assessment Effectiveness

Evaluar la efectividad descriptiva de las dos evaluaciones técnicas mediante la comparación de sus resultados entre candidatos contratados y no contratados.

**Pregunta de negocio:**

¿Cuál de las evaluaciones técnicas presenta una mayor diferencia entre candidatos contratados y no contratados?

---

### R5 - Technology-Assessment Analysis

Analizar el desempeño de las evaluaciones técnicas entre las diferentes tecnologías y estudiar su relación descriptiva con los resultados de contratación.

**Pregunta de negocio:**

¿Cómo varía el desempeño en las evaluaciones técnicas entre tecnologías y cómo se relaciona con la contratación?


## 4. Trazabilidad de requerimientos

La siguiente matriz relaciona cada requerimiento de negocio con las tablas del Data Warehouse, las principales métricas utilizadas y el análisis realizado.

| Requerimiento | Tablas DW utilizadas | Principales KPIs / métricas | Visualización / análisis |
|---|---|---|---|
| R1 - Hiring Trends | Fact_Application, Dim_Date | Total Applications, Hired Candidates, Hiring Rate | Tendencia de aplicaciones y contrataciones por año |
| R2 - Technology Analysis | Fact_Application, Dim_Technology | Hired Candidates, Total Applications, Hiring Rate | Comparación de contratación por tecnología |
| R3 - Candidate Profile Analysis | Fact_Application, Dim_Profile | Hiring Rate, Average YOE, Hired Candidates | Comparación por seniority y rangos de experiencia |
| R4 - Technical Assessment Effectiveness | Fact_Application | Average Code Challenge Score, Average Technical Interview Score, Score Difference | Comparación de evaluaciones entre HIRED y NOT HIRED |
| R5 - Technology-Assessment Analysis | Fact_Application, Dim_Technology | Average Code Challenge Score, Average Technical Interview Score, Hiring Rate | Comparación de desempeño técnico y contratación por tecnología |

Cada requerimiento se encuentra respaldado por atributos y métricas existentes en el Data Warehouse. No se incorporaron dimensiones o atributos únicamente por disponibilidad en el dataset; los elementos del modelo fueron seleccionados de acuerdo con su utilidad analítica.


## 5. Descripción del dataset

El dataset de entrada corresponde al archivo `candidates.csv`, ubicado en:

`data/raw/candidates.csv`

El archivo contiene información transaccional relacionada con aplicaciones de candidatos a procesos de reclutamiento tecnológico.

El archivo utiliza `;` como separador y contiene 50.000 registros y 10 columnas originales:

| Campo | Descripción |
|---|---|
| First Name | Nombre del candidato |
| Last Name | Apellido del candidato |
| Email | Correo electrónico registrado en la aplicación |
| Application Date | Fecha en la que se realizó la aplicación |
| Country | País asociado a la aplicación |
| YOE | Years of Experience; años de experiencia profesional |
| Seniority | Nivel profesional del candidato |
| Technology | Tecnología o perfil tecnológico asociado a la aplicación |
| Code Challenge Score | Puntuación obtenida en el Code Challenge, en una escala de 0 a 10 |
| Technical Interview Score | Puntuación obtenida en la entrevista técnica, en una escala de 0 a 10 |

### Alcance temporal

Las fechas de aplicación se encuentran entre:

- Fecha mínima: `2018-01-01`
- Fecha máxima: `2022-07-04`

Por lo tanto, el año 2022 representa un período parcial y no debe compararse directamente con los años completos anteriores en términos de volumen anual.

### Características de los datos

El dataset representa aplicaciones individuales y no necesariamente candidatos únicos. Durante el perfilamiento se identificaron 49.833 correos electrónicos únicos para 50.000 registros, lo que indica la existencia de candidatos con múltiples aplicaciones según el campo Email.

Debido a que el correo electrónico presenta inconsistencias en algunos registros y no constituye un identificador confiable del candidato, no se utilizó como clave en el modelo dimensional.

El dataset se conserva sin modificaciones en `data/raw/` como fuente original del proceso ETL.



## 6. Hallazgos principales del perfilamiento

Antes de realizar las transformaciones de negocio y la construcción del modelo dimensional se realizó un proceso de perfilamiento sobre el dataset original.

Los principales resultados fueron los siguientes:

| Aspecto | Resultado |
|---|---:|
| Registros | 50.000 |
| Columnas originales | 10 |
| Emails únicos | 49.833 |
| Registros con múltiples aplicaciones | 165 candidatos identificados mediante Email |
| Duplicados exactos | 0 |
| Valores faltantes | 0 |
| Fecha mínima de aplicación | 2018-01-01 |
| Fecha máxima de aplicación | 2022-07-04 |
| Rango Code Challenge Score | 0–10 |
| Rango Technical Interview Score | 0–10 |
| Rango YOE | 0–30 años |
| HIRED | 6.698 |
| NOT HIRED | 43.302 |

### Calidad de los datos

No se encontraron valores faltantes en las columnas del dataset original y tampoco se identificaron registros completamente duplicados.

Las fechas, años de experiencia y puntuaciones fueron convertidos a tipos de datos apropiados durante la etapa de preparación.

Las variables categóricas `Seniority` y `Technology` fueron estandarizadas mediante eliminación de espacios innecesarios.

### Aplicaciones múltiples

El perfilamiento mostró que existen registros asociados al mismo Email en diferentes aplicaciones. Por esta razón, estas filas no fueron eliminadas como duplicados.

El análisis del contenido mostró además que algunos correos electrónicos aparecen asociados a diferentes nombres y características de candidatos. Esto indica que el campo Email no puede considerarse un identificador confiable dentro de este dataset.

En consecuencia, se decidió modelar cada registro como una aplicación independiente y no construir una dimensión de candidato basada en Email.

### Regla de contratación

A partir de la regla de negocio:

`HIRED = Code Challenge Score >= 7 AND Technical Interview Score >= 7`

se obtuvo la siguiente distribución:

- HIRED: 6.698 aplicaciones
- NOT HIRED: 43.302 aplicaciones
- Total: 50.000 aplicaciones

Por lo tanto, aproximadamente el 13,40% de las aplicaciones cumplen simultáneamente con los criterios establecidos para contratación.

### Decisiones derivadas del perfilamiento

Los resultados del perfilamiento permitieron establecer varias decisiones para las siguientes etapas del proyecto:

1. Mantener las 50.000 aplicaciones como eventos independientes.
2. No eliminar las aplicaciones múltiples como si fueran duplicados.
3. No utilizar Email como clave del modelo dimensional.
4. Conservar los registros HIRED y NOT HIRED, ya que ambos son necesarios para los análisis de efectividad de las evaluaciones técnicas.
5. Convertir fechas, años de experiencia y puntuaciones a tipos numéricos o temporales apropiados.
6. Estandarizar las variables categóricas antes de construir las dimensiones.


## 6. Hallazgos principales del perfilamiento

Antes de realizar las transformaciones de negocio y la construcción del modelo dimensional se realizó un proceso de perfilamiento sobre el dataset original.

Los principales resultados fueron los siguientes:

| Aspecto | Resultado |
|---|---:|
| Registros | 50.000 |
| Columnas originales | 10 |
| Emails únicos | 49.833 |
| Registros con múltiples aplicaciones | 165 candidatos identificados mediante Email |
| Duplicados exactos | 0 |
| Valores faltantes | 0 |
| Fecha mínima de aplicación | 2018-01-01 |
| Fecha máxima de aplicación | 2022-07-04 |
| Rango Code Challenge Score | 0–10 |
| Rango Technical Interview Score | 0–10 |
| Rango YOE | 0–30 años |
| HIRED | 6.698 |
| NOT HIRED | 43.302 |

### Calidad de los datos

No se encontraron valores faltantes en las columnas del dataset original y tampoco se identificaron registros completamente duplicados.

Las fechas, años de experiencia y puntuaciones fueron convertidos a tipos de datos apropiados durante la etapa de preparación.

Las variables categóricas `Seniority` y `Technology` fueron estandarizadas mediante eliminación de espacios innecesarios.

### Aplicaciones múltiples

El perfilamiento mostró que existen registros asociados al mismo Email en diferentes aplicaciones. Por esta razón, estas filas no fueron eliminadas como duplicados.

El análisis del contenido mostró además que algunos correos electrónicos aparecen asociados a diferentes nombres y características de candidatos. Esto indica que el campo Email no puede considerarse un identificador confiable dentro de este dataset.

En consecuencia, se decidió modelar cada registro como una aplicación independiente y no construir una dimensión de candidato basada en Email.

### Regla de contratación

A partir de la regla de negocio:

`HIRED = Code Challenge Score >= 7 AND Technical Interview Score >= 7`

se obtuvo la siguiente distribución:

- HIRED: 6.698 aplicaciones
- NOT HIRED: 43.302 aplicaciones
- Total: 50.000 aplicaciones

Por lo tanto, aproximadamente el 13,40% de las aplicaciones cumplen simultáneamente con los criterios establecidos para contratación.

### Decisiones derivadas del perfilamiento

Los resultados del perfilamiento permitieron establecer varias decisiones para las siguientes etapas del proyecto:

1. Mantener las 50.000 aplicaciones como eventos independientes.
2. No eliminar las aplicaciones múltiples como si fueran duplicados.
3. No utilizar Email como clave del modelo dimensional.
4. Conservar los registros HIRED y NOT HIRED, ya que ambos son necesarios para los análisis de efectividad de las evaluaciones técnicas.
5. Convertir fechas, años de experiencia y puntuaciones a tipos numéricos o temporales apropiados.
6. Estandarizar las variables categóricas antes de construir las dimensiones.




---

# 8. Grain Definition

Aquí quiero que seamos particularmente claros, porque la **granularidad** es uno de los conceptos más importantes del modelo.

```markdown
## 8. Definición de granularidad

La granularidad de la tabla `Fact_Application` se define como:

> **Una fila de `Fact_Application` representa una aplicación individual realizada por un candidato al proceso de reclutamiento.**

Por lo tanto, cada registro de la tabla de hechos corresponde a un evento de aplicación y conserva la información necesaria para analizar el resultado de dicho evento.

La granularidad seleccionada permite analizar:

- Cantidad de aplicaciones.
- Cantidad de aplicaciones contratadas y no contratadas.
- Tasas de contratación.
- Puntuaciones promedio de las evaluaciones técnicas.
- Resultados de contratación por fecha.
- Resultados de contratación por tecnología.
- Resultados de contratación por seniority.
- Resultados de contratación por rangos de años de experiencia.

### Implicaciones de la granularidad

Las aplicaciones múltiples de un mismo candidato no se consideran duplicados automáticamente. Cada aplicación representa un evento independiente dentro del proceso de negocio y, por lo tanto, se conserva como una fila diferente en `Fact_Application`.

El campo `Email` no se utiliza como identificador del candidato ni como clave de la tabla de hechos, debido a las inconsistencias detectadas durante el perfilamiento.

La tabla de hechos utiliza `Application_Key` como clave sustituta para identificar cada registro de aplicación dentro del Data Warehouse.

### Relación entre granularidad y requerimientos

La granularidad seleccionada permite satisfacer los cinco requerimientos de negocio:

| Requerimiento | Información soportada por la granularidad |
|---|---|
| R1 - Hiring Trends | Fecha y resultado de cada aplicación |
| R2 - Technology Analysis | Tecnología y resultado de cada aplicación |
| R3 - Candidate Profile Analysis | Seniority, YOE y resultado |
| R4 - Technical Assessment Effectiveness | Puntuaciones de ambas evaluaciones y resultado |
| R5 - Technology-Assessment Analysis | Tecnología, puntuaciones y resultado |

La elección de esta granularidad permite conservar el nivel de detalle necesario para realizar los análisis sin perder información durante la transformación hacia el modelo dimensional.

---

## 9. Modelo dimensional - Star Schema

El Data Warehouse se implementó mediante un **modelo dimensional tipo Star Schema**. 
La tabla de hechos `Fact_Application` se encuentra en el centro del modelo y contiene 
los eventos de aplicación, mientras que las dimensiones proporcionan el contexto 
necesario para realizar los diferentes análisis.

### Diagrama del modelo

![Star Schema del Data Warehouse](diagrams/star_schema.png)

### Estructura del modelo

El modelo está compuesto por una tabla de hechos y tres dimensiones:

- `Fact_Application`: almacena los eventos de aplicación y sus valores analíticos.
- `Dim_Date`: proporciona el contexto temporal.
- `Dim_Technology`: proporciona el contexto relacionado con la tecnología.
- `Dim_Profile`: proporciona el contexto relacionado con el nivel de seniority.

Las relaciones del modelo son:

```text
Dim_Date          1 ─────── N Fact_Application
Dim_Technology    1 ─────── N Fact_Application
Dim_Profile       1 ─────── N Fact_Application




---

# 10. Descripción de dimensiones y tabla de hechos

Ahora documentamos cada tabla con más detalle.

```markdown
## 10. Descripción de dimensiones y tabla de hechos

### 10.1 Dim_Date

La dimensión `Dim_Date` contiene la información temporal asociada a cada fecha de 
aplicación.

Su objetivo es facilitar el análisis de las aplicaciones y contrataciones a través 
del tiempo sin tener que realizar transformaciones sobre la fecha almacenada en la 
tabla de hechos.

| Campo | Tipo | Clave | Descripción |
|---|---|---|---|
| `Date_Key` | INT | PK | Clave sustituta de la fecha. |
| `Application_Date` | DATE | - | Fecha en la que se realizó la aplicación. |
| `Day` | INT | - | Día correspondiente a la fecha. |
| `Month` | INT | - | Mes correspondiente a la fecha. |
| `Quarter` | INT | - | Trimestre correspondiente a la fecha. |
| `Year` | INT | - | Año correspondiente a la fecha. |

La dimensión se construye a partir de las fechas únicas presentes en las 
aplicaciones. Para cada fecha se genera una **surrogate key** (`Date_Key`).

Esta dimensión permite responder principalmente al requerimiento **R1 - Hiring 
Trends**.

---

### 10.2 Dim_Technology

La dimensión `Dim_Technology` contiene las tecnologías asociadas a las aplicaciones.

Su objetivo es permitir el análisis y comparación de los resultados de contratación 
entre diferentes tecnologías.

| Campo | Tipo | Clave | Descripción |
|---|---|---|---|
| `Technology_Key` | INT | PK | Clave sustituta de la tecnología. |
| `Technology` | VARCHAR(150) | - | Nombre de la tecnología o área tecnológica. |

Los valores de tecnología se deduplican antes de generar las claves sustitutas. 
De esta manera, cada tecnología aparece una sola vez en la dimensión.

Esta dimensión permite responder principalmente a:

- **R2 - Technology Analysis**
- **R5 - Technology–Assessment Analysis**

---

### 10.3 Dim_Profile

La dimensión `Dim_Profile` contiene el nivel de seniority asociado a cada aplicación.

Su objetivo es proporcionar el contexto necesario para analizar los resultados de 
contratación según el perfil profesional del candidato.

| Campo | Tipo | Clave | Descripción |
|---|---|---|---|
| `Profile_Key` | INT | PK | Clave sustituta del perfil. |
| `Seniority` | VARCHAR(50) | - | Nivel de seniority del candidato. |

Los valores de `Seniority` se deduplican antes de generar las claves sustitutas.

Esta dimensión permite responder principalmente al requerimiento:

- **R3 - Candidate Profile Analysis**

Los años de experiencia (`YOE`) no se almacenan en esta dimensión. Se mantienen en 
`Fact_Application` debido a que representan un valor numérico de cada aplicación y 
pueden utilizarse para calcular promedios, rangos y tasas de contratación.

---

### 10.4 Fact_Application

`Fact_Application` es la tabla central del modelo dimensional. Cada fila representa 
una aplicación individual, de acuerdo con la granularidad definida anteriormente.

Contiene las claves que relacionan cada aplicación con las dimensiones y los valores 
cuantitativos necesarios para realizar los análisis.

| Campo | Tipo | Clave | Descripción |
|---|---|---|---|
| `Application_Key` | INT | PK | Clave sustituta única de la aplicación. |
| `Date_Key` | INT | FK | Referencia a `Dim_Date`. |
| `Technology_Key` | INT | FK | Referencia a `Dim_Technology`. |
| `Profile_Key` | INT | FK | Referencia a `Dim_Profile`. |
| `YOE` | INT | - | Años de experiencia profesional. |
| `Code_Challenge_Score` | INT | - | Puntuación obtenida en Code Challenge. |
| `Technical_Interview_Score` | INT | - | Puntuación obtenida en Technical Interview. |
| `Hiring_Outcome` | TINYINT | - | Indicador del resultado de contratación: `1 = HIRED`, `0 = NOT HIRED`. |

La tabla conserva tanto las aplicaciones contratadas como las no contratadas. Esto es 
necesario porque varios requerimientos requieren comparar ambos grupos.

Por ejemplo, el requerimiento **R4** necesita comparar el promedio de las evaluaciones 
técnicas entre candidatos contratados y no contratados. Si las aplicaciones no 
contratadas fueran eliminadas durante el proceso ETL, este análisis no sería posible.

Por esta razón, `Hiring_Outcome` funciona como un indicador analítico que permite 
calcular:

- Total de aplicaciones.
- Total de aplicaciones contratadas.
- Total de aplicaciones no contratadas.
- Tasa de contratación.
- Promedios de las evaluaciones técnicas.
- Diferencias entre candidatos contratados y no contratados.
