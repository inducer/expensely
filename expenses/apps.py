from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    name = "expenses"
    verbose_name = "Expenses"

    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        import expenses.signals  # noqa: F401
