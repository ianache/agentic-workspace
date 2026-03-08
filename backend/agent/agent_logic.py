import os
import asyncio
from typing import List, Optional, Dict, Any
from google.adk.agents.llm_agent import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseConnectionParams
from google.genai import types
from toolbox_core import ToolboxSyncClient
from db_tools import DatabaseTools
from chart_tool import generate_chart_tool
from dotenv import load_dotenv

# Optional: LiteLLM support for Ollama/Custom models
try:
    from google.adk.models.lite_llm import LiteLlm
    LITE_LLM_AVAILABLE = True
except ImportError:
    LITE_LLM_AVAILABLE = False

load_dotenv()

# Initialize MySQL tools
db_tools_instance = DatabaseTools()

def get_schema_metadata_tool() -> str:
    """Returns the schema metadata for the MySQL database."""
    return db_tools_instance.get_schema_metadata()

def describe_table_tool(table_name: str) -> str:
    """Provides a detailed description of the specified MySQL table structure."""
    return db_tools_instance.describe_table(table_name)

class AnalyticalAgent:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()
        self.model_name = os.getenv("LLM_MODEL", "gemini-1.5-flash")
        self.db_toolbox_url = os.getenv("TOOLBOX_URL", "http://127.0.0.1:8080")
        self.chart_toolbox_url = os.getenv("CHART_TOOLBOX_URL", "http://127.0.0.1:8081/sse")
        
        print(f"--- Initializing Multi-Tool ADK Agent ---")
        
        self.all_tools = [get_schema_metadata_tool, describe_table_tool, generate_chart_tool]

        # 1. DB Toolbox
        try:
            db_client = ToolboxSyncClient(url=self.db_toolbox_url)
            self.all_tools.extend(db_client.load_toolset())
            print(f"✅ DB Toolbox connected.")
        except:
            print(f"⚠️ DB Toolbox not found.")

        # 2. AntV Chart Toolset
        try:
            antv_toolset = McpToolset(
                connection_params=SseConnectionParams(url=self.chart_toolbox_url),
                tool_name_prefix="antv_"
            )
            self.all_tools.append(antv_toolset)
            print(f"✅ AntV Toolset registered.")
        except Exception as e:
            print(f"❌ AntV registration failed: {e}")

        self.instruction = """Eres un Agente Analítico de MySQL.
        Tu prioridad es usar 'antv_' para gráficos. 
        SI LAS HERRAMIENTAS 'antv_' FALLAN O DAN ERROR DE CONEXIÓN, usa 'generate_chart_tool' inmediatamente como respaldo.
        Responde siempre en ESPAÑOL."""
        
        model_to_use = self.model_name
        if self.provider == "ollama":
            ollama_model_name = self.model_name
            if not ollama_model_name.startswith("ollama_chat/"):
                ollama_model_name = f"ollama_chat/{ollama_model_name}"
            if "OLLAMA_API_BASE" not in os.environ:
                os.environ["OLLAMA_API_BASE"] = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
            model_to_use = LiteLlm(model=ollama_model_name)

        self.adk_agent = Agent(
            name="AgenteAnalitico",
            instruction=self.instruction,
            model=model_to_use,
            tools=self.all_tools
        )
        
        self.session_service = InMemorySessionService()
        self.runner = Runner(
            agent=self.adk_agent, 
            session_service=self.session_service, 
            app_name="AnalyticalAgentApp",
            auto_create_session=True
        )

    async def ask(self, user_question: str, history: list = None):
        session_id = "default_session"
        user_id = "default_user"
        query = types.UserContent(parts=[types.Part(text=user_question)])
        full_response = ""
        
        try:
            async for event in self.runner.run_async(user_id=user_id, session_id=session_id, new_message=query):
                if hasattr(event, 'content') and event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            full_response += part.text
            
            return full_response if full_response else "No se pudo obtener respuesta."
            
        except Exception as e:
            error_str = str(e)
            print(f"DEBUG ERROR: {error_str}")
            
            # AUTO-RECOVERY LOGIC:
            if "MCP session" in error_str or "TaskGroup" in error_str:
                print("Intentando recuperación automática usando Matplotlib...")
                # Re-intentamos la pregunta pero instruyendo al agente a ignorar AntV
                recovery_query = types.UserContent(parts=[types.Part(text=f"{user_question} (El servidor de AntV no responde, por favor usa EXCLUSIVAMENTE la herramienta interna 'generate_chart_tool' para esta respuesta)")])
                full_response = "⚠️ (Nota: Usando motor de gráficos de respaldo por fallo en AntV)\n\n"
                
                async for event in self.runner.run_async(user_id=user_id, session_id=session_id, new_message=recovery_query):
                    if hasattr(event, 'content') and event.content and event.content.parts:
                        for part in event.content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_response += part.text
                return full_response
            
            return f"Error técnico: {error_str}"
