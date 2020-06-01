from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.pk}'


class BaseIntegracao(BaseModel):
    MODO_INTEGRACAO = (
        (1, 'Regra LSP'),
        (2, 'Trigger banco de dados'),
        (3, 'Procedure banco de dados'),
    )
    tabela_origem = models.CharField(max_length=100)
    tabela_integracao = models.CharField(max_length=100)
    modo_integracao = models.IntegerField(choices=MODO_INTEGRACAO)
    objeto_integracao = models.TextField()
    tabela_destino = models.CharField(max_length=100)
    modo_destino = models.IntegerField(choices=MODO_INTEGRACAO)
    objeto_destino = models.TextField()


class Empresa(BaseIntegracao):
    pk_origem = models.CharField(max_length=50)
    pk_integracao = models.CharField(max_length=50)
    pk_destino = models.CharField(max_length=50)
