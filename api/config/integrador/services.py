from inspect import isfunction

from decouple import config

from config.integrador.errors import (OSAutomotivaError,
                                      NotaFiscalErroIntegracao,
                                      AgricolaErroIntegracao,
                                      AbastecimentoErroIntegracao,
                                      ApontamentoProducaoError,
                                      InsumoGinError,
                                      PedidoErroIntegracao)
from config.integrador.models import (OperacaoBase,
                                      OSAgricola,
                                      OSAutomotiva,
                                      NotaFiscal,
                                      Abastecimento,
                                      AbastecimentoItem,
                                      ApontamentoProducao,
                                      InsumoGin,
                                      Pedido)
from config.integrador.queries import (QR_ABASTECIMENTO)
from config.integrador.wsdls import (RunWsdlSenior)
from config.integrador.parsers import (ParserDefault,
                                       ParserAbastecimento,
                                       ParserOSAutomotiva,
                                       ParserNotaFiscal,
                                       ParserPedido)
from config.oracle import OracleDB


def load_abastecimento(data):
    if not isinstance(data, Abastecimento):
        return None

    _db = OracleDB('DB_INTEGRACAO')

    for d in _db.query(QR_ABASTECIMENTO, dict(token=data.token)):
        d['abastecimento_id'] = data.id
        AbastecimentoItem(**d).save()


class HttpGatecRequest:
    def __init__(self, **kwargs):
        self.modulo = self._rem_list(kwargs.get('modulo', None))
        self.operacao = self._rem_list(kwargs.get('operacao', None))
        self.usuario = self._rem_list(kwargs.get('usuario', None))
        self.senha = self._rem_list(kwargs.get('senha', None))
        self.token = self._rem_list(kwargs.get('token', None))
        self.rotina = self._rem_list(kwargs.get('rotina', None))
        self.wsdl = None
        self.data_object = None
        self.mensagem_retorno = 'Ok - Realizado com sucesso'

    def _rem_list(self, obj):
        if isinstance(obj, list):
            return obj[0]

        return obj


class HttpRun(HttpGatecRequest):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.run(**kwargs)

    def retorno(self, data_object, parser):
        self.mensagem_retorno = parser(data_object).run()

    def run(self, **kwargs):
        wsdl_base = config('WSDL_BASE', default='http://argel:8080')

        modulo = dict()

        """
        Após a pesagem no GATEC envia a NF para integrar com o ERP.
        """
        modulo['BAL'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=f'{wsdl_base}/g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl',
                                wsdl_service='GatecNotaFiscal',
                                wsdl_params=('token',),
                                model=NotaFiscal,
                                get_data=None,
                                error_class=NotaFiscalErroIntegracao,
                                parser_retorno=ParserNotaFiscal)


        """
        Ao integrar pedido no commerce executa a rotina para retornar ok e liberar o processo.
        """
        modulo['PED'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=None,
                                wsdl_service=None,
                                wsdl_params=None,
                                model=Pedido,
                                get_data=None,
                                error_class=PedidoErroIntegracao,
                                parser_retorno=ParserPedido)


        """
        Integra as OS e transferência agricola com o ERP (Sapiens).
        """
        modulo['GRP'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=f'{wsdl_base}/g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl',
                                wsdl_service='GatecOsAgricola',
                                wsdl_params=('token', 'operacao'),
                                model=OSAgricola,
                                get_data=None,
                                error_class=AgricolaErroIntegracao,
                                parser_retorno=ParserDefault)

        """
        Integra as requisições de combustível do GATEC com o ERP (Sapiens).
        """
        modulo['ABA'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=f'{wsdl_base}/g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl',
                                wsdl_service='GatecAbastecimento',
                                wsdl_params=('token',),
                                model=Abastecimento,
                                get_data=load_abastecimento,
                                error_class=AbastecimentoErroIntegracao,
                                parser_retorno=ParserAbastecimento)

        """
        Integra as OS Automotivas do GATEC com o ERP (Sapiens)
        """
        modulo['AUT'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=f'{wsdl_base}/g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl',
                                wsdl_service='GatecOSAutomotiva',
                                wsdl_params=('token',),
                                model=OSAutomotiva,
                                get_data=None,
                                error_class=OSAutomotivaError,
                                parser_retorno=ParserOSAutomotiva)

        """
        Quando faz a entrada de produção na tela da balança (GATEC) ele integra com o ERP (Sapiens)
        """
        modulo['APP'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=f'{wsdl_base}/g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl',
                                wsdl_service='GatecApontamentoProducao',
                                wsdl_params=('token', 'operacao'),
                                model=ApontamentoProducao,
                                get_data=None,
                                error_class=ApontamentoProducaoError,
                                parser_retorno=ParserDefault)

        """
        Baixa dos insumos utilizados no beneficiamento no ERP
        Os insumos utilizados na produção do fardinho, são enviados para realizar a baixar no estoque do ERP.
        """
        modulo['GIN'] = dict(wsdl=RunWsdlSenior,
                                wsdl_url=f'{wsdl_base}/g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl',
                                wsdl_service='GatecInsumosGim',
                                wsdl_params=('token', 'operacao'),
                                model=InsumoGin,
                                get_data=None,
                                error_class=InsumoGinError,
                                parser_retorno=ParserDefault)

        runner_params = modulo[self.modulo]

        self.integrate(**runner_params)

    def integrate(self, wsdl, wsdl_url, wsdl_service, wsdl_params, model, error_class, get_data, parser_retorno):
        try:
            self.data_object = model(token=self.token,
                                     operacao=self.operacao,
                                     usuario=self.usuario,
                                     senha=self.senha,
                                     rotina=self.rotina)
            self.data_object.save()

            if isfunction(get_data):
                get_data(self.data_object)

            self.data_object.status = OperacaoBase.STATUS_INTEGRANDO_WSDL
            self.data_object.save()

            if wsdl_url is not None:
                ws = wsdl(wsdl_url)
                ws.run(data_object=self.data_object,
                       service=wsdl_service,
                       params=wsdl_params)

        except (error_class, Exception) as e:
            self.data_object.erro_classe = e.__class__.__name__
            self.data_object.status = OperacaoBase.STATUS_ERRO
            self.data_object.log = e
            self.data_object.save()
            raise error_class(e)

        else:
            if self.data_object.status == OperacaoBase.STATUS_INTEGRANDO_WSDL:
                self.data_object.status = OperacaoBase.STATUS_FINALIZADO
            self.data_object.save()

            if self.data_object.status_erro():
                raise error_class(self.data_object.wsdl_log)

            self.retorno(self.data_object, parser_retorno)
