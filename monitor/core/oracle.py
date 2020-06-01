import cx_Oracle
from decouple import config
from dj_database_url import parse

from core.errors import OracleDBError, OracleQueryError


class OracleDB:

    def __init__(self, string_conn, auto_connect=True, rac=False):
        dbenv = config(string_conn, cast=parse)

        self.host = dbenv['HOST']
        self.port = dbenv['PORT']
        self.service = dbenv['NAME']
        self.user = dbenv['USER']
        self.pwd = dbenv['PASSWORD']
        self.connection = None

        if auto_connect:
            self.connect(rac=rac)

    def _make_tns(self):
        self.tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)

    def connect(self, rac=False):
        self._make_tns()
        try:
            self.connection = cx_Oracle.connect(self.user, self.pwd, self.tns, threaded=rac)
        except cx_Oracle.DatabaseError as e:
            raise OracleDBError(f'Erro de conexão com banco de dados. Erro: {e}')

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def query(self, sql, filters=[]):
        if 'select' not in sql.lower():
            raise OracleQueryError('Comando select inválido!')

        cursor = self.connection.cursor()
        cursor.execute(sql, filters)
        columns = [col[0].lower() for col in cursor.description]

        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()

        for i in enumerate(data):
            for c in columns:
                if type(data[i[0]][c]) == cx_Oracle.LOB:
                    data[i[0]][c] = data[i[0]][c].read()

        return data

    def command(self, command, data={}, commit=True):
        cursor = self.connection.cursor()

        try:
            ret = cursor.execute(command, data)
            if commit:
                self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            raise OracleDBError(f'{e}')
        else:
            return ret
