#
# This file is part of Python Module for Cube Builder.
# Copyright (C) 2019-2020 INPE.
#
# Cube Builder is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Python Module for Cube Builder."""

from bdc_db.ext import BDCDatabase
from flask import Flask
from flask_cors import CORS

from . import celery, config


def create_app(config_name='DevelopmentConfig'):
    """Create Brazil Data Cube application from config object.

    Args:
        config_name (string) Config instance name
    Returns:
        Flask Application with config instance scope
    """
    app = Flask(__name__)
    conf = config.get_settings(config_name)
    app.config.from_object(conf)

    with app.app_context():
        # Initialize Flask SQLAlchemy
        BDCDatabase(app)

        # Just make sure to initialize db before celery
        celery_app = celery.create_celery_app(app)
        celery.celery_app = celery_app

        # Setup blueprint
        from .blueprint import bp
        app.register_blueprint(bp)

        CORS(app)

    return app
