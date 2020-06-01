from django.contrib import admin
from config.sapiens.models import Empresa


class BaseAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name not in ['created_at',
                                                                                              'updated_at',
                                                                                              'user']]
        super().__init__(model, admin_site)


@admin.register(Empresa)
class EmpresaAdmin(BaseAdmin):
    search_fields = ('tabela_origem',
                     'tabela_integracao',
                     'tabela_destino',)
