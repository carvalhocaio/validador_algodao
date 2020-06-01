from .models import (OperacaoBase, Abastecimento, OSAutomotiva, NotaFiscal, Algodao)

class ParserMain:
    def __init__(self, data_object):
        self.data_object = data_object

    def run(self):
        raise NotImplementedError('Should have implemented this')


class ParserDefault(ParserMain):
    def run(self):
        if self.data_object.status_erro():
            return f'Erro! {self.data_object.wsdl_log}'

        return 'Ok - Realizado com sucesso '


class ParserPedido(ParserMain):
    def run(self):
        return 'Ok - Realizado com sucesso'


class ParserAbastecimento(ParserMain):
    def __init__(self, data_object: Abastecimento):
       super().__init__(data_object)

    def run(self):
        data = self.data_object.wsdl_retorno
        st = 'Ok - {}' if not self.data_object.status_erro() else 'Erro - {}'

        try:
            data = eval(data)
        except Exception:
            return st.format(data)
        else:
            if isinstance(data, dict):
                if data.get('mensagemRetorno', None) is not None:
                    return st.format(data['mensagemRetorno'])

            return st.format(data)


class ParserOSAutomotiva(ParserMain):
    def __init__(self, data_object: OSAutomotiva):
       super().__init__(data_object)

    def run(self):
        data = self.data_object.wsdl_retorno
        st = 'Ok - Ordem de Serviço Gerada {}' if not self.data_object.status_erro() else 'Erro - {}'

        try:
            data = eval(data)
        except Exception:
            return st.format(data)
        else:
            if isinstance(data, dict):
                retorno = data.get('retorno', None)
                if retorno is not None and len(retorno) > 0:
                    numero_os = format(retorno[0]['numEme'], ',d').replace(',', '.')
                    return st.format(numero_os)

            return st.format(data)


class ParserNotaFiscal(ParserMain):
    def __init__(self, data_object: NotaFiscal):
       super().__init__(data_object)

    def run(self):
        data = self.data_object.wsdl_retorno
        st = 'Ok - Nota Fiscal e Pedido Gerada {}' if not self.data_object.status_erro() else 'Erro - {}'

        try:
            data = eval(data)
        except Exception:
            return st.format(data)
        else:
            if isinstance(data, dict):
                retorno = data.get('retorno', None)
                if retorno is not None and len(retorno) > 0:
                    num_nfv = retorno[0]['numNfv']
                    num_ped = retorno[0]['numPed']
                    msg = f'- NF {num_nfv}, Pedido {num_ped}'
                    return st.format(msg)

            return st.format(data)


class ParserAlgodao(ParserMain):
    def __init__(self, data_object: Algodao):
        super().__init__(data_object)

    def run(self):
        data = self.data_object.wsdl_retorno
        st = 'Ok - {}' if not self.data_object.status_erro() else 'Erro - {}'

        try:
            data = eval(data)
        except Exception:
            return st.format(data)
        else:
            if isinstance(data, dict):
                if data.get('mensagemRetorno', None) is not None:
                    return st.format(data['mensagemRetorno'])

            return st.format(data)

