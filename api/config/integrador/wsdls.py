import urllib3
from django.utils import timezone
from requests import HTTPError, ConnectionError
from zeep import Client

from .errors import WsdlError


class SeniorWsdlParams:
    def __init__(self, usuario, senha):
        self.user = usuario
        self.password = senha
        self.encryption = 0
        self.params = dict

    def configure(self, **kwargs):
        self.params = dict(user=self.user, password=self.password, encryption=self.encryption, parameters=kwargs)
        return self.params


class WSDLBase:
    def __init__(self, url):
        self.wsdl_url = url
        self.wsdl_timeout = 100
        self.client_wsdl = None
        self.error = ''
        self._start_client()

        urllib3.disable_warnings()

    def _start_client(self):
        try:
            self.client_wsdl = Client(wsdl=self.wsdl_url)

        except (HTTPError, ConnectionError) as e:
            print(HTTPError)
            print(ConnectionError)
            raise WsdlError('Serviço de integração com ERP está indisponível. Favor verificar com TI!')

        except Exception as e:
            self.error = e
            raise WsdlError(e)

        if self.client_wsdl is None:
            raise WsdlError('Client WSDL não definido!')


class RunWsdlSenior(WSDLBase):
    def __init__(self, url):
        super().__init__(url)

    def get_params(self, params, data_object):
        data = dict()
        for i in params:
            data[i] = getattr(data_object, i)
        return data

    def run(self, data_object, service, params):
        _params = SeniorWsdlParams(data_object.usuario, data_object.senha)
        _params.configure(**self.get_params(params, data_object))

        try:
            data_object.inicio_chamada = timezone.now()
            data_object.wsdl_call = f'Url: {self.wsdl_url}\nServiço: {service}\nParametros: {_params.params}'
            data_object.save()
            result = self.client_wsdl.service[service](**_params.params)
        except Exception as e:
            data_object.erro_execucao = f'Erro na execução do comando wsdl. Erro: \n {e}'
            data_object.save()

            raise WsdlError(e)
        else:
            has_error = result['erroExecucao']

            data_object.termino_chamada = timezone.now()
            data_object.wsdl_retorno = str(result)

            try:
                data_object.retorno = int(result['tipoRetorno'])
            except TypeError:
                data_object.retorno = 0

            if has_error is not None:
                data_object.wsdl_erro = True
                data_object.wsdl_log = has_error
                data_object.status = 5
                data_object.save()
                return None

            if data_object.retorno != 1:
                data_object.wsdl_erro = True
                data_object.wsdl_log = result['mensagemRetorno']
                data_object.status = 5

            data_object.save()
