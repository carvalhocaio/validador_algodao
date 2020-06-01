from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.utils.http import urlencode

from .models import Abastecimento, OSAutomotiva
from .services import HttpRun


class TestOSAutomotiva(TestCase):

    def setUp(self):
        self.token = 'C03BA81DCA3BB81FC27CE893D6B6660C'
        self.param = dict(modulo='AUT',
                          operacao='I',
                          usuario='agendador1',
                          senha='agendador1',
                          token=self.token,
                          rotina='os_automotiva', )
        self.url = f'http://servidor:porta/integrador?{urlencode(self.param)}'
        print(f'Url para consumo. {self.url}')
        try:
            self.gr = HttpRun(**self.param)
        except Exception as e:
            self.gr = None
            self.fail(f'Falha ao executar a integração. Erro: \n {e} \n Tente aplicar efetuar a chamada: {self.url}')

    def test_runner(self):
        self.assertNotEqual(self.gr, None)

    def test_object_exist(self):
        try:
            a = OSAutomotiva.objects.get(token=self.token)
        except ObjectDoesNotExist:
            self.fail(f'Token ({self.token}) não encontrado no integrador. \n {self.url}')
        else:
            self.assertEqual(self.token, a.token)


class TestAbastecimento(TestCase):

    def setUp(self):
        self.token = 'A35E9984B5E9C2FFE493F17384692491'
        self.param = dict(modulo='ABA',
                          operacao='I',
                          usuario='agendador1',
                          senha='agendador1',
                          token=self.token,
                          rotina='abastecimento', )
        try:
            self.gr = HttpRun(**self.param)
        except Exception as e:
            self.gr = None
            self.fail(f'Falha ao executar a integração. Erro: \n {e}')

    def test_runner(self):
        self.assertNotEqual(self.gr, None)

    def test_object_exist(self):
        try:
            a = Abastecimento.objects.get(token=self.token)
        except ObjectDoesNotExist:
            self.fail(f'Token ({self.token}) não encontrado no integrador.')
        else:
            self.assertEqual(self.token, a.token)
