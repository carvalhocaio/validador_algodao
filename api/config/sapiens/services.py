from config.oracle import OracleDB


class CheckIntegracao:
    _url_origem = 'DB_SAPIENS'
    _url_integracao = 'DB_INTEGRACAO'
    _url_destino = 'DB_SAFRAS'

    def __init__(self, modelo):
        self.modelo = modelo
        self.db_origem = OracleDB(self._url_origem)
        self.db_integracao = OracleDB(self._url_integracao)
        self.db_destino = OracleDB(self._url_destino)

    def _make_sql(self, **kwargs):
        coluns = kwargs.get('coluns', '*')
        table = kwargs.get('table', None)
        where = kwargs.get('where', '1 = 1')

        return f'SELECT {coluns} FROM {table} WHERE {where}'

    def start(self):
        for i in self.modelo.objects.all():
            s_validar = self._make_sql(table=i.tabela_origem, coluns=i.pk_origem)
            l_validar = self.db_origem.query(s_validar, [])

            for v in l_validar:
                s2_validar = self._make_sql(table=i.tabela_integracao,
                                            where=f'{i.pk_integracao} = {v[i.pk_origem.lower()]}')
                l2_validar = self.db_integracao.query(s2_validar, [])
                if (len(l2_validar) == 0):
                    print('Erro, não possui registro na integração')
                else:
                    print(v, 'Ok ')


a = CheckIntegracao(Empresa)
a.start()
