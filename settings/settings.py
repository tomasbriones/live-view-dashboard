import os
from dotenv import load_dotenv
from django.utils.module_loading import import_module
load_dotenv()

# local settings
if os.getenv('ENVIRONMENT') == 'AWS':
    local_settings = import_module('settings.aws_settings')
elif os.getenv('ENVIRONMENT') == 'LINUX' in os.environ:
    local_settings = import_module('settings.linux_settings')
elif os.getenv('ENVIRONMENT') == 'WINDOWS' in os.environ:
    local_settings = import_module('settings.windows_settings')
else:
    local_settings = import_module('settings.local_settings')

DB_NAME = local_settings.DB_NAME
DB_HOST = local_settings.DB_HOST
DB_PORT = local_settings.DB_PORT
DB_USER = local_settings.DB_USER
DB_PWD = local_settings.DB_PWD
LOCALHOST = local_settings.LOCALHOST
API_PORT = local_settings.API_PORT
API_URL = local_settings.API_URL
SSH_HOST = local_settings.SSH_HOST
SSH_PORT = local_settings.SSH_PORT
SSH_PK = local_settings.SSH_PK
SSH_USER = local_settings.SSH_USER
SSH_PWD = local_settings.SSH_PWD
# ENVIRONMENT = local_settings.ENVIRONMENT
