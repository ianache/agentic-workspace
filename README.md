# Agente Analítico de IA

Este proyecto es un agente conversacional de Inteligencia Artificial diseñado para permitir que los usuarios realicen preguntas sobre sus datos de negocio en lenguaje natural y reciban respuestas basadas en consultas SQL ejecutadas contra Google BigQuery y Cloud SQL.

## Estructura del Proyecto

- `/backend/agent`: Agente de IA desarrollado en Python utilizando FastAPI, LangChain y Google Vertex AI.
- `/frontend`: Interfaz de usuario web desarrollada con Next.js (React), Tailwind CSS y Lucide Icons.

## Requisitos Previos

- Python 3.12+ (con `uv` instalado).
- Node.js 18+.
- Cuenta de Google Cloud Platform con BigQuery y Vertex AI habilitados.
- Base de Datos MySQL (Cloud SQL).

## Configuración y Ejecución

### Backend (Agente)

1. Navega al directorio del backend:
   ```bash
   cd backend/agent
   ```
2. Crea un archivo `.env` basado en `.env.example` y completa tus credenciales.
3. Instala las dependencias y ejecuta el servidor:
   ```bash
   uv run main.py
   ```
   El API estará disponible en `http://localhost:8000`.

### servidores MCP

#### Servidor MCP Tools for Database

```
px @toolbox-sdk/server --tools-file toolbox_tools.yaml --port 8080 --ui
```

#### Servidor de Graficas
```
npx -y @antv/mcp-server-chart --transport sse --port 8081
npx -y @antv/mcp-server-chart --port 8081
```

### Frontend (UI)

1. Navega al directorio del frontend:
   ```bash
   cd frontend
   ```
2. Instala las dependencias:
   ```bash
   npm install
   ```
3. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```
   La aplicación estará disponible en `http://localhost:3000`.

## SKILLS del Agente

- **Análisis de Estructura:** Utiliza metadatos para entender las tablas y relaciones (Simulación de MCP Toolbox).
- **Ejecución de Consultas:** Traduce lenguaje natural a SQL para BigQuery.
- **Orquestación:** Combina múltiples pasos para responder preguntas complejas.
