import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import List, Optional, Dict, Any
import streamlit as st
from my_daily_stat.config.settings import settings
from my_daily_stat.config.logger import logger
from my_daily_stat.db.base import DatabaseAdapter

class PostgresAdapter(DatabaseAdapter):
    def __init__(self):
        self._connection = None
        self._connection_params = {
            'host': settings.DB_HOST,
            'port': settings.DB_PORT,
            'database': settings.DB_NAME,
            'user': settings.DB_USER,
            'password': settings.DB_PASSWORD,
        }
    
    def connect(self) -> None:
        if self._connection is None or self._connection.closed:
            try:
                self._connection = psycopg2.connect(**self._connection_params)
                logger.info("Connexion PostgreSQL établie")
            except Exception as e:
                logger.error(f"Erreur de connexion : {e}")
                raise
    
    def disconnect(self) -> None:
        if self._connection and not self._connection.closed:
            self._connection.close()
            logger.info("Connexion PostgreSQL fermée")
    
    @contextmanager
    def transaction(self):
        """Context manager pour gérer les transactions"""
        self.connect()
        try:
            yield self._connection
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            logger.error(f"Transaction annulée : {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """SELECT queries"""
        self.connect()
        with self._connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params or {})
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_command(self, command: str, params: Optional[Dict] = None) -> int:
        """INSERT/UPDATE/DELETE"""
        with self.transaction() as conn:
            with conn.cursor() as cursor:
                cursor.execute(command, params or {})
                return cursor.rowcount
    
    # Méthode utilitaire pour Streamlit (connection pooling)
    @staticmethod
    @st.cache_resource
    def get_cached_connection():
        """Connexion mise en cache pour Streamlit"""
        adapter = PostgresAdapter()
        adapter.connect()
        return adapter