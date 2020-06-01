from django.db import models
from django.utils import timezone


class OperacaoBase(models.Model):
    STATUS_RECEBENDO = 1
    STATUS_INTEGRANDO_DADOS = 2
    STATUS_INTEGRANDO_WSDL = 3
    STATUS_FINALIZADO = 4
    STATUS_ERRO = 5

    STATUS = (
        (STATUS_RECEBENDO, 'Recebendo'),
        (STATUS_INTEGRANDO_DADOS, 'Integrando Dados'),
        (STATUS_INTEGRANDO_WSDL, 'Integrando WSDL'),
        (STATUS_FINALIZADO, 'Finalizado'),
        (STATUS_ERRO, 'Erro'),
    )

    status = models.IntegerField(choices=STATUS, default=1)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    log = models.TextField(null=True)
    erro_classe = models.CharField(max_length=100, null=True, blank=True)

    def status_erro(self):
        return self.status == self.STATUS_ERRO

    class Meta:
        abstract = True


class WSDLBase(models.Model):
    inicio_chamada = models.DateTimeField(null=True, blank=True)
    termino_chamada = models.DateTimeField(null=True, blank=True)
    wsdl_call = models.TextField(null=True, blank=True)
    wsdl_erro = models.BooleanField(default=False)
    wsdl_retorno = models.TextField(null=True, blank=True)
    wsdl_log = models.TextField(null=True, blank=True)

    @property
    def tempo_processamento(self):
        if self.termino_chamada is not None:
            return self.termino_chamada - self.criado_em
        return timezone.now() - self.criado_em

    class Meta:
        abstract = True


class Abastecimento(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=1, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'abastecimentos'

    def __str__(self):
        return self.token


class AbastecimentoItem(models.Model):
    INTEGRADO = (
        ('S', 'Sim'),
        ('N', 'Não'),
    )

    TIPO = (
        ('R', 'Requisição'),
        ('D', 'Devolução'),
    )
    abastecimento = models.ForeignKey('integrador.Abastecimento', related_name="abastecimento_items", on_delete=models.CASCADE, null=True)
    chave = models.CharField(max_length=100, null=True, blank=True)
    documento = models.IntegerField(null=True, blank=True)
    empresa = models.IntegerField(null=True, blank=True)
    produto = models.CharField(max_length=10, null=True, blank=True)
    quantidade = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    data_movimento = models.DateTimeField(null=True, blank=True)
    centro_custo = models.CharField(max_length=10, null=True, blank=True)
    deposito = models.CharField(max_length=10, null=True, blank=True)
    ponto = models.IntegerField(null=True, blank=True)
    integrado = models.CharField(max_length=1, null=True, blank=True, choices=INTEGRADO, default='N')
    data_exportacao = models.DateTimeField(null=True, blank=True)
    usuario = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=1, null=True, blank=True, choices=TIPO)
    equipamento = models.CharField(max_length=100, null=True, blank=True)
    erro = models.TextField(null=True, blank=True)
    data_importacao = models.DateTimeField(null=True, blank=True)


class ApontamentoProducao(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=25, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'apontamentos de produção'

    def __str__(self):
        return self.token


class InsumoGin(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=25, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'insumos do beneficiamento'

    def __str__(self):
        return self.token


class OSAutomotiva(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=25, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'ordens de serviços automotiva'

    def __str__(self):
        return self.token


class OSAgricola(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'ordens de serviços agricola'

    def __str__(self):
        return self.token


class NotaFiscal(OperacaoBase, WSDLBase):
    OPERACAO = (
        ('R', 'Requisição'),
        ('E', 'Estorno'),
    )

    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=1, choices=OPERACAO)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'nota fiscal'

    def __str__(self):
        return self.token



class Pedido(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=50)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'pedido'

    def __str__(self):
        return self.token



class Algodao(OperacaoBase, WSDLBase):
    token = models.CharField(max_length=100)
    operacao = models.CharField(max_length=25, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    rotina = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'algodao'

    def __str__(self):
        return self.token

