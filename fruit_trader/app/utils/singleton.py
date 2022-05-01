"""Provides the Singleton Class"""
from fruit_trader.app.data_handler import Database


class Singleton:
    """The Singleton class."""

    __database = None

    def __init__(self):
        """Initialize database."""
        if not Singleton.__database:
            self.__database = Database()
            Singleton.__database = self.__database

    @staticmethod
    def get_database_instance():
        """Get database instance."""
        if Singleton.__database is None:
            Singleton()

        return Singleton.__database
