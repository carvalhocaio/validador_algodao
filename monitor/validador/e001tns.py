import timeit

from core.oracle import OracleDB
from validador.models import Transacao, TransacaoIntegracao
from datetime import datetime

SQL_ERP = """
SELECT CODEMP AS EMPRESA,
       CODTNS AS ID,
       DESTNS AS DESCRICAO,
       DETTNS AS DETALHES,
       SITTNS AS SITUACAO
  FROM E001TNS 
 WHERE CODEMP = 1
   AND LISMOD IN ('VEP', 'VEO', 'VEC', 'VEF', 'VEN')
 ORDER BY 1, 2
"""

SQL_INTEGRACAO = """
SELECT COD_TRANSACAO AS ID,
       DSC_TRANSACAO AS DESCRICAO,
       TRA_BAIXA_EST AS BAIXA_ESTOQUE,
       SIT_TRANSACAO AS SITUACAO,
       COD_EMPR AS EMPRESA
  FROM GATEC_TRANSACAO
 WHERE COD_EMPR = :empresa
   AND COD_TRANSACAO = :transacao
"""


class E001tns:
    _str_db_erp = 'DB_ERP'
    _str_db_integracao = 'DB_INTEGRACAO'
    _str_db_safras = 'DB_SAFRAS'

    def __init__(self):
        self.db_erp = OracleDB(self._str_db_erp)
        self.db_integracao = OracleDB(self._str_db_integracao)
        self.db_safras = OracleDB(self._str_db_safras)
        self.data_erp = []
        self.output = []

        self.output.append(f'Classe {self.__class__.__name__} iniciada em {datetime.now()}')

    def _load_erp(self):
        start_time = timeit.default_timer()
        self.output.append('Consulta SQL Iniciada')
        self.output.append(f'SQL: {SQL_ERP}')
        self.output.append(f'Inicio: {datetime.now()}')
        self.data_erp = [Transacao(**t) for t in self.db_erp.query(SQL_ERP)]
        self.output.append(f'Termino: {datetime.now()}')
        self.output.append(f'Tempo: {timeit.default_timer() - start_time}')
        self.output.append(f'Registros: {len(self.data_erp)}')

    def _load_integracao(self, empresa, transacao):
        self.output.append('Parametros:')
        self.output.append(f'Empresa: {empresa}')
        self.output.append(f'Transação: {transacao}')

        data = self.db_integracao.query(SQL_INTEGRACAO, dict(empresa=empresa, transacao=transacao))

        if len(data) == 0:
            return None

        return TransacaoIntegracao(**data[0])

    def validar(self):
        self._load_erp()

        for d in self.data_erp:
            start_time = timeit.default_timer()
            self.output.append('Validação do registro de transação')
            self.output.append(f'{d.__dict__}')
            self.output.append(f'SQL: {SQL_INTEGRACAO}')
            integracao = self._load_integracao(d.empresa, d.id)

            self.output.append(f'Termino: {datetime.now()}')
            self.output.append(f'Tempo: {timeit.default_timer() - start_time}')
            self.output.append(f'Registros: {len(self.data_erp)}')


a = E001tns()
a.validar()
print('\n'.join(a.output))
