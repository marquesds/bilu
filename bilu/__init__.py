import logging
import os

from quart import Quart

logger = logging.getLogger(__name__)


def create_app(environment=os.getenv('ENVIRONMENT', 'Development')):
    app = Quart(__name__)
    app.config.from_object(f'bilu.config.{environment}')

    from bilu.views.api_v1 import api_v1
    app.register_blueprint(api_v1)

    return app
