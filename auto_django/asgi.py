"""
ASGI config for auto_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_django.settings')
# 这里要增加这一行代码，类似于环境变量的path
sys.path.append('/var/www/html/safe')
application = get_asgi_application()
