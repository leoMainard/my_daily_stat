import os

class Environnement:
    _configuration = None

    @classmethod
    def _load_config(cls):
        if cls._configuration is None:
            cls._configuration = {
                "DB_NAME": os.getenv("DB_NAME"),
                "DB_HOSTNAME": os.getenv("DB_HOSTNAME"),
                "DB_PORT": os.getenv("DB_PORT"),
                "DB_USER": os.getenv("DB_USER"),
                "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            }

    @classmethod
    def config(cls, name):
        cls._load_config()
        try:
            return cls._configuration[name]
        except KeyError:
            raise KeyError(f"Configuration '{name}' not found.")