'''
Module to load and validate environment variables for Aiven database connection.
Usage:
    1. Copy .env.template to .env
    2. Fill in your actual Aiven database credentials in .env
    3. Import and use the functions in your application
'''

import os
import sys
try:
    import sqlalchemy
    SQLALCHEMY_AVAILABLE = True
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv or sqlalchemy is not installed. Please install them with '(uv) pip install python-dotenv sqlalchemy'.")
    sys.exit(1)

class AivenEnvironment:

    def __init__(self):
        self.env_variables = self.load_environment_variables()
        self.valid = self.validate_environment_variables()
        if not self.valid:
            raise EnvironmentError("Required environment variables are missing. Please check your .env file.")

    def load_environment_variables(self) -> dict:
        print("Loading aiven environment variables...")

        # Load environment variables from .env file
        load_dotenv()

        env_variables = {}

        # Get Aiven database credentials from environment variables
        env_variables['AIVEN_SERVICE_URI'] = os.getenv('AIVEN_SERVICE_URI')
        env_variables['AIVEN_DATABASE_NAME'] = os.getenv('AIVEN_DATABASE_NAME')
        env_variables['AIVEN_HOST'] = os.getenv('AIVEN_HOST')
        env_variables['AIVEN_PORT'] = os.getenv('AIVEN_PORT')
        env_variables['AIVEN_USER'] = os.getenv('AIVEN_USER')
        env_variables['AIVEN_PASSWORD'] = os.getenv('AIVEN_PASSWORD')
        env_variables['AIVEN_CERT_PATH'] = os.getenv('AIVEN_CERT_PATH')

        return env_variables


    def validate_environment_variables(self):
        """
        Validate that all required environment variables are set.

        Returns:
            bool: True if all variables are set, False otherwise
        """
        if not self.env_variables:
            return False
        required_vars = {
            'AIVEN_SERVICE_URI': self.env_variables.get('AIVEN_SERVICE_URI'),
            'AIVEN_DATABASE_NAME': self.env_variables.get('AIVEN_DATABASE_NAME'),
            'AIVEN_HOST': self.env_variables.get('AIVEN_HOST'),
            'AIVEN_PORT': self.env_variables.get('AIVEN_PORT'),
            'AIVEN_USER': self.env_variables.get('AIVEN_USER'),
            'AIVEN_PASSWORD': self.env_variables.get('AIVEN_PASSWORD'),
            'AIVEN_CERT_PATH': os.getenv('AIVEN_CERT_PATH')
        }

        missing_vars = [var_name for var_name, var_value in required_vars.items() if not var_value]

        if missing_vars:
            print("Error: The following environment variables are not set:")
            for var in missing_vars:
                print(f"  - {var}")
            print("\nPlease ensure you have:")
            print("1. Copied .env.template to .env")
            print("2. Filled in your actual Aiven database credentials in .env")
            return False

        return True

    def get_service_uri(self) -> str:
        """Get the Aiven service URI."""
        return self.env_variables.get('AIVEN_SERVICE_URI')

    def get_database_name(self) -> str:
        """Get the Aiven database name."""
        return self.env_variables.get('AIVEN_DATABASE_NAME')

    def get_host(self) -> str:
        """Get the Aiven host."""
        return self.env_variables.get('AIVEN_HOST')

    def get_port(self) -> int:
        """Get the Aiven port."""
        return int(self.env_variables.get('AIVEN_PORT'))

    def get_user(self) -> str:
        """Get the Aiven user."""
        return self.env_variables.get('AIVEN_USER')

    def get_password(self) -> str:
        """Get the Aiven password."""
        return self.env_variables.get('AIVEN_PASSWORD')
    
    def get_cert_path(self) -> str:
        """Get the Aiven certificate path."""
        return self.env_variables.get('AIVEN_CERT_PATH')
    

class AivenDatabase:
    def __init__(self, env: AivenEnvironment):
        self.env = env
        self.engine = None
        self.session = None

    def connect(self):
        """
        Connect to Aiven database using the loaded environment variables.

        Returns:
            connection: sqlalchemy engine object
        """
        if not SQLALCHEMY_AVAILABLE:
            print("Error: sqlalchemy is not installed. Please install it with '(uv) pip install sqlalchemy'.")
            return None

        try:
            timeout = 10
            self.engine = sqlalchemy.create_engine(
                self.env.get_service_uri(),
                connect_args={
                    "connect_timeout": timeout,
                    'ssl_ca': self.env.get_cert_path()
                }
            )
            print("Successfully connected to the Aiven database using environment variables.")
            self.session = sqlalchemy.orm.Session(self.engine)
        except Exception as e:
            print(f"Error connecting to the database using environment variables: {e}")
            return None
