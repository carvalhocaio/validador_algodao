import sys, os
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from decouple import config as parser
from dj_database_url import parse

from .services import HttpRun


def hide_pwd_db_url(url):
    cfg = parse(url)
    engine = cfg.get("ENGINE")
    user = cfg.get("USER")
    pwd = "*" * len(cfg.get("PASSWORD", 'A'))
    host = cfg.get("HOST")
    port = cfg.get("PORT")
    name = cfg.get("NAME")
    options = cfg.get("OPTIONS")

    def parse_options(options):
        if not isinstance(options, dict):
            return ''
        return '?' + '&'.join([f'{i}={options[i]}' for i in options])

    return f'{engine}://{user}:{pwd}@{host}:{port}/{name}{parse_options(options)}'


def config(request):
    """
    Página raiz que exibe as configurações do ambiente
    """
    cfg = dict(debug=parser('DEBUG'),
               wsdl_root=parser('WSDL_BASE'),
               db_sapiens=hide_pwd_db_url(parser('DB_SAPIENS')),
               db_integracao=hide_pwd_db_url(parser('DB_INTEGRACAO')),
               db_safras=hide_pwd_db_url(parser('DB_SAFRAS')),
               db_automotiva=hide_pwd_db_url(parser('DB_AUTOMOTIVA')),
               db_default=hide_pwd_db_url(parser('DB_DEFAULT')))
    return JsonResponse(cfg, json_dumps_params={'indent': 2})


def integrador(request):
    """
    Função responsável por realizar a integrar com sapiens
    """
    params = request.GET
    try:
        a = HttpRun(**params)
    except Exception as e:
        data = dict(situacao=f'Erro: {e}')
    else:
        data = dict(situacao=f'{a.mensagem_retorno}')

    return render(request, 'index.html', data)
