from logging.config import dictConfig

# Define logging configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
        "api": {
            "format": "[%(asctime)s] [API] [%(levelname)-s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "sqlalchemy": {
            "format": "[%(asctime)s] [SQLALCHEMY] [%(levelname)-s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "uvicorn": {
            "format": "[%(asctime)s] [UVICORN] [%(levelname)-s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console_api": {
            "class": "logging.StreamHandler",
            "formatter": "api",
            "level": "INFO",
        },
        "console_sqlalchemy": {
            "class": "logging.StreamHandler",
            "formatter": "sqlalchemy",
            "level": "INFO",
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console_api"],
            "level": "INFO",
            "propagate": False,
        },
        "sqlalchemy.engine": {
            "handlers": ["console_sqlalchemy"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console_api"],
    }
}

def setup_logging():
    """Configure logging using the defined configuration."""
    dictConfig(LOGGING_CONFIG)
