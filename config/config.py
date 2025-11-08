import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    TESTING = False
    DEBUG = False
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
    TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    API_BASE_URL = 'http://localhost:5000'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    API_BASE_URL = 'http://localhost:5000'


class ProductionConfig(Config):
    """Production configuration"""
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('ENVIRONMENT', 'development')

    configs = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }

    return configs.get(env, DevelopmentConfig)()
