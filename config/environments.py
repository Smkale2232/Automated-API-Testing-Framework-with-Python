import os


class Environment:
    """Environment configuration helper"""

    @staticmethod
    def get_base_url():
        return os.getenv('API_BASE_URL', 'http://localhost:5000')

    @staticmethod
    def get_timeout():
        return int(os.getenv('REQUEST_TIMEOUT', '10'))

    @staticmethod
    def is_ci():
        return os.getenv('CI', 'false').lower() == 'true'
