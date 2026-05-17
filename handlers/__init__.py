from . import start, help, taste_settings, choice, favorites

def setup_handlers(app):
    start.register_handlers(app)
    help.register_handlers(app)
    taste_settings.register_handlers(app)
    choice.register_handlers(app)
    favorites.register_handlers(app)