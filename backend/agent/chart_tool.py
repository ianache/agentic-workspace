import os
import matplotlib.pyplot as plt
import pandas as pd
import uuid
from typing import List, Dict, Any

# Ensure charts directory exists
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "static", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

def generate_chart_tool(data: List[Dict[str, Any]], x_label: str, y_label: str, title: str, chart_type: str = "bar") -> str:
    """
    Genera un gráfico a partir de una lista de diccionarios y devuelve el enlace a la imagen.
    
    Args:
        data: Lista de diccionarios con los datos (ej. resultados de una consulta).
        x_label: Nombre de la columna para el eje X.
        y_label: Nombre de la columna para el eje Y (valores numéricos).
        title: Título del gráfico.
        chart_type: Tipo de gráfico: 'bar', 'line', 'pie'.
    """
    try:
        if not data:
            return "Error: No hay datos para graficar."
            
        df = pd.DataFrame(data)
        
        # Validate columns
        if x_label not in df.columns or y_label not in df.columns:
            return f"Error: Las columnas '{x_label}' o '{y_label}' no existen en los datos obtenidos."

        plt.figure(figsize=(10, 6))
        
        if chart_type == "bar":
            plt.bar(df[x_label].astype(str), df[y_label])
        elif chart_type == "line":
            plt.plot(df[x_label].astype(str), df[y_label], marker='o')
        elif chart_type == "pie":
            plt.pie(df[y_label], labels=df[x_label].astype(str), autopct='%1.1f%%')
        else:
            return f"Error: Tipo de gráfico '{chart_type}' no soportado."

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Save to static folder
        filename = f"chart_{uuid.uuid4().hex}.png"
        filepath = os.path.join(CHARTS_DIR, filename)
        plt.savefig(filepath)
        plt.close()

        # Return Markdown link
        # We use http://localhost:8000/static/charts/ because that's where FastAPI will serve it
        chart_url = f"http://localhost:8000/static/charts/{filename}"
        return f"\n\n![Gráfico]({chart_url})\n\nGráfico generado: **{title}**. Puedes verlo aquí: {chart_url}"

    except Exception as e:
        return f"Error generando el gráfico: {str(e)}"
