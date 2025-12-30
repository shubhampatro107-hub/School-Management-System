from django.apps import AppConfig

class MainAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main_app'

    def ready(self):
        try:
            from .models import CustomUser

            if not CustomUser.objects.filter(email="admin@gmail.com").exists():
                CustomUser.objects.create_superuser(
                    email="admin@gmail.com",
                    password="admin123",
                    user_type=1
                )
        except Exception:
            pass
