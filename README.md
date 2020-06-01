# Validador de integração
> Serviço para realizar integração do GATEC com o Sapiens.

Em resumo, o app recebe uma requisição HTTP e através dos parametros, executa uma integração com o ERP Sênior via WSDL.

Para auxiliar no suporte, mantemos as informações da chamada e retorno do WSDL guaradas.

## Módulos

São os tipos de integrações que são possíveis de realizar até o momento pelo validador.

### OS Automotiva
> Integra as OS Automotivas do GATEC com o ERP (Sapiens)

Código: AUT\
Situação: Em produção

### Abastecimento
> Integra as requisições de combustível do GATEC com o ERP (Sapiens).

Código: ABA\
Situação: Em produção

### Nota fiscal da Balança
> Após a pesagem no GATEC envia a NF para integrar com o ERP.

Código: BAL\
Situação: Em implementação

### OS Agricola
> Integra as OS e transferência agricola com o ERP (Sapiens).

Código: GRP\
Situação: Não implementado

### Apontamento de produção
> Quando faz a entrada de produção na tela da balança (GATEC) ele integra com o ERP (Sapiens)

Código: APP\
Situação: Não implementado

## Integrações

As rotinas configuradas para integrações são:

| Chamada | Módulo | URL | Serviço de Consumo |
|---|---|---|---|
| BAL | Balança - Nota Fiscal | g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl | NotaFiscal |
| GRP | Ordem de Serviço Agricola | g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl | OSAgricola |
| ABA | Abastecimento | g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl | GatecAbastecimento |
| AUT | Ordem de Serviço Automotiva | g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl | GatecOSAutomotiva |
| APP | Apontamento de Produção | g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl | ApontamentoProducao |
| GIN | Insumos Gin | g5-senior-services/sapiens_Synccom_gs_g1_co_int_integracoes?wsdl | InsumosGim |

## Status

Toda integração possuem 5 status

| Código | Status |
| --- | --- |
| 1 | Recebendo dados da Origem |
| 2 | Processando dados |
| 3 | Integrado com WSDL |
| 4 | Finalizado |
| 5 | Ocorreu um erro |

## Config

Para iniciar o projeto, são necessários as seguintes configurações

|Chave | Exemplo | Tipo | Descrição |
|---|---|---|---|
|SECRET_KEY | DQ8U3HN21U3216T| string | Chave da aplicação|
|DEBUG | True| Boolean | Indicativo se está em desenvolvimento|
|ALLOWED_HOSTS | 127.0.0.1, .localhost, 192.168.3.21, *| list | Hosts permitidos|
|DB_DEFAULT | mysql://USER:PASSWORD@HOST:PORT/SCHEMA| string | Conexão com banco de log|
|DB_SAPIENS | oracle://USER:PASSWORD@HOST:PORT/SCHEMA?threaded=True| string | Conexão com ERP|
|DB_INTEGRACAO | oracle://USER:PASSWORD@HOST:PORT/SCHEMA?threaded=True| string | Conexão com DB_INTEGRACAO|
|DB_SAFRAS | oracle://USER:PASSWORD@HOST:PORT/SCHEMA?threaded=True| string | Conexão com SAFRAS|
|DB_AUTOMOTIVA | oracle://USER:PASSWORD@HOST:PORT/SCHEMA?threaded=True| string | Conexão com MECANICA|
|LDAP_URL | ldap://192.168.0.16| string | Conexão com ldap|
|LDAP_USE_TLS | False| bool | Usa TSL|
|LDAP_SEARCH_BASE | dc=gruposcheffer,dc=com| string | Base de Pesquisa|
|LDAP_OBJECT_CLASS | person| string | Classe de Objeto|
|LDAP_CLEAN_USER_DATA | django_python3_ldap.utils.clean_user_data| string | Classe de limpeza|
|LDAP_SYNC_USER_RELATIONS | django_python3_ldap.utils.sync_user_relations| string | Classe de relação|
|LDAP_FORMAT_SEARCH_FILTERS | django_python3_ldap.utils.format_search_filters| string | Filtros de Pesquisa|
|LDAP_FORMAT_USERNAME | django_python3_ldap.utils.format_username_active_directory| string | Formato do username|
|LDAP_ACTIVE_DIRECTORY_DOMAIN | gruposcheffer| string | Nome do diretório|
|LDAP_CONNECTION_USERNAME | noreply| string | Usuário para leitura|
|LDAP_CONNECTION_PASSWORD | ****** | string | Senha do usuário|
|MAIL_BACKEND | django.core.mail.backends.smtp.EmailBackend| string | Classe de email|
|MAIL_HOST | smtp.office365.com| string | Host|
|MAIL_DEFAULT_FROM | noreply@gruposcheffer.com.br| string | Default from|
|MAIL_SERVER | gruposcheffer.com.br| string | Servidor|
|MAIL_HOST_USER | noreply@gruposcheffer.com| string | Usuário|
|MAIL_HOST_PASSWORD | ****** | string | Senha|
|MAIL_PORT | 587| int | Porta|
|MAIL_USE_TLS | True| bool | Usa TLS|
|NLS_LANG | .utf8| string | Força encoding conexão oracle |
|BROKER_URL | redis://localhost:6379| string | Conexão com broker|
|CELERY_RESULT_BACKEND | django-db| string | Parametro de tarefas|
|CELERY_TASK_SERIALIZER | json| string | Parametro de tarefas|
|CELERY_RESULT_SERIALIZER | json| string | Parametro de tarefas|
|CELERY_TIMEZONE | America/Cuiaba| string | Parametro de tarefas|
|WSDL_BASE | **** | string | Servidor de glassfish ERP|

## Setup

1. Instale o python 3.6.7 e mysql 5.6+.
1. Instale o pipenv no python `pip install pipenv`
1. Crie um schema no mysql para utilização
1. `git clone https://gitlab.com/s-integracoes/validador.git`
1. Entre no diretório validador/api `cd validador/api`
1. Inicialize o ambiente virtual e instale as dependências `pipenv sync -d`
1. Copie o `env_sample` para `.env` com as configurações necessárias
1. Crie as migrações do banco `python manage.py makemigrations`
1. Aplique as migrações criadas `python manage.py migrate`
1. Crie um usuário administrador `python manage.py createsuperuser`
1. Suba o servidor `python manage.py runserver`
1. Acesse http://localhost:8000/admin
