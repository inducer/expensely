from django.apps import AppConfig


class ExpensesConfig(AppConfig):
    name = 'expenses'
    verbose_name = "Expenses"

    def ready(self):
        import expenses.signals  # noqa: F401
