class Transacao:
    """
    Classe de transação do ERP
    """

    def __init__(self, empresa, id, descricao, detalhes, situacao):
        SITUACAO = dict()
        SITUACAO['A'] = 'Ativo'
        SITUACAO['I'] = 'Inativo'

        self.empresa = empresa
        self.id = id
        self.descricao = descricao
        self.detalhes = detalhes
        self.situacao = situacao
        self.situacao_display = SITUACAO[situacao]

    def __repr__(self):
        return f'{self.empresa}/{self.id}'


class TransacaoIntegracao:
    """
    Classe de transação da Integracao
    """

    def __init__(self, id, descricao, baixa_estoque, situacao, empresa):
        self.id = id
        self.descricao = descricao
        self.baixa_estoque = baixa_estoque
        self.situacao = situacao
        self.empresa = empresa

    def __repr__(self):
        return f'{self.empresa}/{self.id}'
