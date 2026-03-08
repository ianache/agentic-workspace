import os
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, inspect
import pymysql

class DatabaseTools:
    def __init__(self):
        self.mysql_engine = None

    def _get_mysql_engine(self):
        if self.mysql_engine is None:
            host = os.getenv("MYSQL_HOST")
            user = os.getenv("MYSQL_USER")
            password = os.getenv("MYSQL_PASSWORD")
            database = os.getenv("MYSQL_DATABASE")
            self.mysql_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
        return self.mysql_engine

    def get_schema_metadata(self) -> str:
        """
        Retrieves schema metadata for all tables in the MySQL database.
        """
        try:
            engine = self._get_mysql_engine()
            inspector = inspect(engine)
            
            metadata = "Información del Esquema de Base de Datos MySQL:\n"
            for table_name in inspector.get_table_names():
                metadata += f"\nTabla: {table_name}\nColumnas:\n"
                for column in inspector.get_columns(table_name):
                    metadata += f"  - {column['name']} ({column['type']})\n"
            
            return metadata
        except Exception as e:
            return f"Error al obtener el esquema: {str(e)}"

    def describe_table(self, table_name: str) -> str:
        """
        Provides a detailed description of a specific MySQL table.
        """
        try:
            engine = self._get_mysql_engine()
            inspector = inspect(engine)
            columns = inspector.get_columns(table_name)
            
            description = f"Descripción de la tabla MySQL '{table_name}':\n"
            for col in columns:
                description += f"- {col['name']}: {col['type']} (Nullable: {col['nullable']})\n"
            
            return description
        except Exception as e:
            return f"Error al describir la tabla: {str(e)}"
