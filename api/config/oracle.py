import datetime

import cx_Oracle
from decouple import config
from dj_database_url import parse
from django.utils import timezone


class OracleDB:

    def __init__(self, env, auto_connect=True):
        dbenv = config(env, cast=parse)

        self.host = dbenv['HOST']
        self.port = dbenv['PORT']
        self.service = dbenv['NAME']
        self.user = dbenv['USER']
        self.pwd = dbenv['PASSWORD']
        self.connection = None
        self.erro = None

        if auto_connect:
            self.open(rac=True)

    def _make_tns(self):
        self.tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)

    def open(self, rac=False):
        self._make_tns()

        try:
            self.connection = cx_Oracle.connect(self.user, self.pwd, self.tns, threaded=rac)
        except cx_Oracle.DatabaseError as e:
            self.erro = f'{e}'
            self.connection = None
            raise Exception(f'Error on connect database.\n {self.tns}\nUSER: {self.user}\nERROR: {e}')

    def disconnect(self):
        self.connection.close()

    def query(self, sql, filters=[], parse_tz=False):
        if self.connection is None:
            raise Exception('Não foi possível executar a query, por favor verifique a conexão.')

        if 'select' not in sql.lower():
            raise Exception('Comando SQL Inválido')

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, filters)
            columns = [col[0].lower() for col in cursor.description]

            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()

            for i in enumerate(data):
                for c in columns:
                    if type(data[i[0]][c]) == cx_Oracle.LOB:
                        data[i[0]][c] = data[i[0]][c].read()
                    if type(data[i[0]][c]) == datetime.datetime and parse_tz:
                        data[i[0]][c] = timezone.make_aware(data[i[0]][c], timezone.get_current_timezone())

            return data
        except Exception as e:
            self.erro = f'{e}'
            raise Exception(self.erro)

    def update(self, sql, data={}, commit=True):
        if 'update' not in sql.lower():
            print('Comando SQL inválido!')
            return {}

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, data)
            if commit:
                self.connection.commit()
        except cx_Oracle.DatabaseError as e:
            self.erro = f'{e}'
            raise Exception(self.erro)

        return True
