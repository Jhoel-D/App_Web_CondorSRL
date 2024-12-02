from django.apps import AppConfig


class AppGralConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_gral'
    
    def ready(self):
        import app_gral.signals