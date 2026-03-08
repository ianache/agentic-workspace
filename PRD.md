# Product Requirements Document (PRD): Agente Analítico de IA

**Versión:** 1.0
**Fecha:** 7 de Marzo de 2026
**Autor:** Gemini CLI Agent

---

## 1. Introducción y Visión General

### 1.1. Problema
Los responsables de la toma de decisiones y analistas de negocio necesitan acceder y analizar datos de la empresa que residen en bases de datos MySQL. Sin embargo, a menudo carecen de las habilidades técnicas para escribir consultas SQL complejas o no tienen acceso directo a las herramientas de bases de datos. Esto crea un cuello de botella, ralentizando el análisis y la obtención de insights.

### 1.2. Visión del Producto
Crear un **agente conversacional de Inteligencia Artificial** que actúe como un analista de datos virtual. Este agente permitirá a los usuarios autorizados realizar preguntas sobre los datos del negocio en lenguaje natural (español) y recibir respuestas precisas y contextualizadas, eliminando la barrera técnica y democratizando el acceso a la información.

---

## 2. Objetivos del Producto

*   **Empoderar a usuarios no técnicos:** Permitir que cualquier usuario, independientemente de su conocimiento de SQL, pueda realizar análisis de datos.
*   **Acelerar la toma de decisiones:** Proporcionar respuestas rápidas a preguntas de negocio basadas en datos.
*   **Garantizar la precisión:** Utilizar un "metamodelo" y herramientas de base de datos especializadas ("MCP Toolbox") para asegurar que el agente comprende la estructura de los datos y genera consultas fiables.
*   **Crear una experiencia de usuario intuitiva:** Ofrecer una interfaz de chat simple y directa como punto de interacción principal.

---

## 3. Audiencia Objetivo

*   **Analistas de Negocio:** Para realizar análisis exploratorios rápidos sin necesidad de escribir scripts complejos.
*   **Gerentes y Directores:** Para obtener resúmenes de rendimiento, KPIs y respuestas a preguntas de negocio sobre la marcha.
*   **Equipos de Ventas y Marketing:** Para consultar datos de rendimiento de campañas, ventas por región, etc.

---

## 4. Requisitos Funcionales y Características (SKILLS)

El agente operará en base a un conjunto de "SKILLS" (habilidades) que combinan diferentes herramientas para cumplir con las solicitudes del usuario.

### 4.1. SKILL: Comprensión de Lenguaje Natural
*   **Descripción:** El agente debe ser capaz de interpretar preguntas formuladas en español, identificando intenciones (ej. resumir, comparar, contar), entidades (ej. productos, regiones, fechas) y filtros.
*   **Ejemplo de usuario:** `¿Cuál fue el total de ventas en la región norte durante el último trimestre?`

### 4.2. SKILL: Ejecución de Consultas Analíticas
*   **Descripción:** El agente debe ser capaz de traducir la pregunta del usuario en una consulta SQL válida y ejecutarla contra el datalake analítico (Google BigQuery). Debe poder realizar agregaciones (SUM, AVG, COUNT), agrupaciones (GROUP BY) y filtrados (WHERE).
*   **Herramienta subyacente:** API de Google BigQuery.

### 4.3. SKILL: Análisis de Estructura de Base de Datos (Metamodelo)
*   **Descripción:** El agente debe tener un conocimiento profundo del esquema de la base de datos. Utilizará "MCP Toolbox for Databases" para comprender las tablas, campos, relaciones y, lo más importante, el contexto de negocio de cada elemento (el "metamodelo").
*   **Ejemplo de usuario:** `Describe la tabla de clientes` o `¿Qué campos contiene la tabla de pedidos?`
*   **Herramienta subyacente:** Wrapper API sobre "MCP Toolbox for Databases".

### 4.4. SKILL: Orquestación y Combinación de Herramientas
*   **Descripción:** Para preguntas complejas, el agente debe ser capaz de diseñar un plan y ejecutar múltiples SKILLS en secuencia.
*   **Ejemplo de usuario:** `Resume las ventas del producto "Laptop Pro" y compáralas con el promedio de su categoría.`
*   **Proceso del agente:**
    1.  Usar el SKILL `Análisis de Estructura` para encontrar la categoría del "Laptop Pro".
    2.  Usar el SKILL `Ejecución de Consultas` para obtener las ventas del "Laptop Pro".
    3.  Usar el SKILL `Ejecución de Consultas` para calcular las ventas promedio de la categoría obtenida en el paso 1.
    4.  Sintetizar los resultados en una respuesta coherente en lenguaje natural.

---

## 5. Arquitectura Técnica (Requisitos No Funcionales)

*   **Plataforma del Agente:** Google Vertex AI Search and Conversation.
*   **Base de Datos Primaria:** Google Cloud SQL for MySQL.
*   **Plataforma Analítica:** Google BigQuery.
*   **Pipeline de Datos:** Google Dataflow o Datastream para replicar datos de Cloud SQL a BigQuery.
*   **Integración de Herramientas:** Un microservicio (wrapper) en Node.js o Python que expone las funcionalidades de "MCP Toolbox for Databases" a través de una API REST, para que Vertex AI pueda consumirla como una "Tool".
*   **Backend (BFF):** Node.js con Express para servir la interfaz y orquestar las llamadas a la API de Vertex AI.
*   **Frontend:** Aplicación web de una sola página (SPA) desarrollada con React (Next.js) y estilizada con Material Design.

---

## 6. Supuestos y Dependencias

*   Se dispone de acceso y documentación completa para "MCP Toolbox for Databases" para desarrollar el wrapper de API.
*   Se cuenta con un proyecto de Google Cloud Platform con facturación habilitada y los permisos necesarios para activar los servicios mencionados.
*   El esquema de la base de datos MySQL está bien estructurado.
*   El "metamodelo" contiene descripciones y metadatos de alta calidad que el agente puede utilizar para entender el contexto del negocio.

---

## 7. Fuera del Alcance (Para la Versión 1.0)

*   **Modificación de datos:** El agente será de solo lectura. No permitirá realizar inserciones, actualizaciones o eliminaciones en la base de datos.
*   **Autenticación y autorización de usuarios:** La primera versión operará en un entorno de confianza. La gestión de roles y permisos se considerará para futuras versiones.
*   **Generación de visualizaciones complejas:** Las respuestas se limitarán a texto y tablas de resumen. Los gráficos avanzados no están en el alcance de la v1.0.
