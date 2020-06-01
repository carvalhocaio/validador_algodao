# Integração automotiva

## OS Automotiva

As OS automotivas são geradas através do módulo oficina, e as mesmas geram requisições de estoque para produtos e no caso de serviços, geram solicitação de compras.

Para retornar as informações de atendimento para o GAtec, temos duas etapas para produtos de estoque.

1. Quando efetuado um atendimento total ou parcial da requisição de estoque, gravar os dados na tabela DB_INTEGRACAO.GATEC_OS_PECAS para retornar as informações de volumes de atendimento.
1. Para a OS receber valor financeiro, é necessário alimentar a tabela DB_INTEGRACAO.GATEC_VALOR_MATERIAL.

Para retornar as informações de atendimento de itens de aplicação direta e serviços, são necessário uma unica etapa.

1. Quando efetuar o atendimento da requisição ou faturamento da nota fiscal, gravar os dados na tabela DB_INTEGRACAO.GATEC_OS_APL_DIRETA para retornar as informações de volumes e valores financeiro.

### Alterações no DB_INTEGRACAO

Alterado a tabela `GATEC_OS_ITENS_REQUISITADOS` para guardas as informações de Requisição e Solicitação do ERP.

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| ERP_CODEMP | NUMERO | Código da empresa no ERP |
| ERP_NUMEME | NUMERO | Número da requisição no ERP |
| ERP_SEQEME | NUMERO | Sequencia da requisição no ERP |
| ERP_NUMSOL | NUMERO | Número da solicitação no ERP |
| ERP_SEQSOL | NUMERO | Sequência da solicitação no ERP |


```sql
ALTER TABLE DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS ADD ERP_CODEMP NUMBER;
ALTER TABLE DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS ADD ERP_NUMEME NUMBER;
ALTER TABLE DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS ADD ERP_SEQEME NUMBER;
ALTER TABLE DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS ADD ERP_NUMSOL NUMBER;
ALTER TABLE DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS ADD ERP_SEQSOL NUMBER;
COMMENT ON COLUMN DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS.ERP_CODEMP IS 'Empresa ERP';
COMMENT ON COLUMN DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS.ERP_NUMEME IS 'Requisição ERP';
COMMENT ON COLUMN DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS.ERP_SEQEME IS 'Sequência da Requisição ERP';
COMMENT ON COLUMN DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS.ERP_NUMSOL IS 'Solicitação ERP';
COMMENT ON COLUMN DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS.ERP_SEQSOL IS 'Sequência da Solicitação ERP';
```

Essas colunas são preenchidas com o retorno do Serviço do ERP, e para atender as necessidades do GATEC de receber as informações de numero de requisição, foi adicionado uma trigger.

```sql
CREATE OR REPLACE TRIGGER TGS_GATEC_OSIR_BU
  BEFORE UPDATE
  ON GATEC_OS_ITENS_REQUISITADOS 
  FOR EACH ROW
DECLARE
BEGIN
  IF SUBSTR(:NEW.COD_OS, 1, 3) = 'AUT' THEN

    IF :NEW.ERP_NUMEME IS NOT NULL THEN
      :NEW.NR_REQUISICAO := :NEW.ERP_CODEMP || '-' || :NEW.ERP_NUMEME || '-' || :NEW.ERP_SEQEME;
    END IF;
    
    IF :NEW.ERP_NUMSOL IS NOT NULL THEN
      :NEW.NR_REQUISICAO := :NEW.ERP_CODEMP || '-' || :NEW.ERP_NUMSOL || '-' || :NEW.ERP_SEQSOL;
    END IF;

  END IF;
END TGS_GATEC_OSIR_BU;
```

### Alterações no ERP

Foi criado um serviço no ERP para efetuar o atendimento da requisição vinda do GATEC.

https://gist.github.com/schefferdev/0c4d1cdfdd3983ce1d8fe0cb3a0c0580

Para atender a necessidade do serviço e padronizar as integrações, foram criados os seguintes campos.

#### E207EME

* USU_CHAINT (U[50]): **Referencia ao campo DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS.CHAVE_MD5**


## Abastecimento

Os movimentos de abastecimento serão efetuados por movimento de estoque (direto na e210mvp), validando pro chave para não repitirem.

### Alterações no DB_INTEGRACAO

Para controlar melhor a forma de integração, ficou definido movimento de 1 para 1, ou seja, para cada registro na tabela `gatec_mov_abastec`, será gerado um registro na tabela `e210mvp`. Com isso, estamos unificando as chaves de movimento no db_integracao, adicionando as seguintes colunas para controle.

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| ERP_CODEMP | NUMERO | Código da empresa no ERP |
| ERP_CODPRO | ALFA | Código do produto no ERP |
| ERP_CODDER | ALFA | Código da derivação no ERP |
| ERP_CODDEP | ALFA | Código do depósito no ERP |
| ERP_DATMOV | DATA | Data do movimento no ERP |
| ERP_SEQMOV | NUMERO | Sequência do movimento no ERP |

O script para aplicar essa mudança foi

```SQL
ALTER TABLE GATEC_MOV_ABASTEC ADD ERP_CODEMP NUMBER;
ALTER TABLE GATEC_MOV_ABASTEC ADD ERP_CODPRO VARCHAR2(10);
ALTER TABLE GATEC_MOV_ABASTEC ADD ERP_CODDER VARCHAR2(10);
ALTER TABLE GATEC_MOV_ABASTEC ADD ERP_CODDEP VARCHAR2(10);
ALTER TABLE GATEC_MOV_ABASTEC ADD ERP_DATMOV DATE;
ALTER TABLE GATEC_MOV_ABASTEC ADD ERP_SEQMOV NUMBER;
COMMENT ON COLUMN GATEC_MOV_ABASTEC.ERP_CODEMP IS 'Empresa ERP';
COMMENT ON COLUMN GATEC_MOV_ABASTEC.ERP_CODPRO IS 'Produto ERP';
COMMENT ON COLUMN GATEC_MOV_ABASTEC.ERP_CODDER IS 'Derivação ERP';
COMMENT ON COLUMN GATEC_MOV_ABASTEC.ERP_CODDEP IS 'Depósito ERP';
COMMENT ON COLUMN GATEC_MOV_ABASTEC.ERP_DATMOV IS 'Data de movimento ERP';
COMMENT ON COLUMN GATEC_MOV_ABASTEC.ERP_SEQMOV IS 'Sequência de Movimento ERP';
```

Para evitar erro de numero de documento longo ou com letras e falta de saldo no dia, alteramos a trigger `GAT_BI_SEQ_MOV_ABASTEC`

```sql
CREATE OR REPLACE TRIGGER GAT_BI_SEQ_MOV_ABASTEC
  BEFORE INSERT ON GATEC_MOV_ABASTEC
  FOR EACH ROW
DECLARE
  ERR_NUM NUMBER;
  ERR_MSG VARCHAR2(2000);
  SSEQ VARCHAR2(30);
  IS_NUMBER NUMBER;
  -- QTD_SALDO NUMBER;
  EMP_ERP NUMBER;
BEGIN
  IF INSERTING THEN
    SELECT TO_CHAR(GASQ_MOV_ABASTEC.NEXTVAL) INTO SSEQ FROM DUAL;
    :NEW.MOV_ID := SSEQ;
  
    IF TRIM(:NEW.NUM_DOCUM) IS NULL THEN
      :NEW.NUM_DOCUM := SSEQ;
    END IF;
    
    IF LENGTH(:NEW.NUM_DOCUM) > 9 THEN
      RAISE_APPLICATION_ERROR('-20001', 'Número de documento muito longo e irá gerar problema na integração. DOC: ' || :NEW.NUM_DOCUM);
    END IF;
    
    SELECT CASE
             WHEN TRIM(TRANSLATE(:NEW.NUM_DOCUM, '0123456789-,.', ' ')) IS NULL THEN
               1
             ELSE
               0
           END
      INTO IS_NUMBER 
      FROM DUAL;
        
    IF IS_NUMBER = 0 THEN
      RAISE_APPLICATION_ERROR('-20001', 'Não é permitido letras no numero de documento. DOC: ' || :NEW.NUM_DOCUM);
    END IF;

    -- VALIDA SALDO POR DIA NO ERP
    IF :NEW.REQ = 'R' THEN
      BEGIN
        SELECT EMP.COD_EMPR_ERP_SEMFILIAL
          INTO EMP_ERP
          FROM GATEC_DEPARA_EMPRESA EMP
         WHERE EMP.COD_EMPR_GA = :NEW.COD_EMPR;
      EXCEPTION
        WHEN OTHERS THEN
          RAISE_APPLICATION_ERROR('-20001', 'Não encontramos empresa vinculada no ERP');
      END;
      
      -- 
      -- 18/03/2019
      -- Regra retirada pelo Paulo para atender Erico (Coord. Automotivo)
      -- Problema: Estava travando o processo, não realizava a integração, pois gerava saldo negativo.
      --
      -- BEGIN
      --  SELECT SUM(DECODE(ESTEOS, 'S', MVP.QTDMOV *-1, MVP.QTDMOV)) AS QTDSLD
      --    INTO QTD_SALDO 
      --    FROM SAPIENS.E210MVP MVP
      --   WHERE MVP.CODEMP = EMP_ERP
      --     AND MVP.CODPRO = :NEW.MAT_CODIGO
      --     AND MVP.CODDEP = :NEW.COD_DEPOS
      --     AND MVP.DATMOV <= :NEW.DAT_MOVIMENTO
      --     AND MVP.ESTMOV = 'NO';
      --  
      --  IF QTD_SALDO - :NEW.QTD_MATERIAL < 0 THEN
      --    RAISE_APPLICATION_ERROR('-20001', chr(13) || 'O movimento irá gerar saldo negativo no dia ' || :NEW.DAT_MOVIMENTO || chr(13) || 
      --                                      'Doc.: ' || :NEW.NUM_DOCUM || chr(13) ||
      --                                      'Saldo no dia: ' || QTD_SALDO || chr(13) ||
      --                                    'Qtd Movimento: ' || :NEW.QTD_MATERIAL || chr(13));
      --  END IF;
      -- EXCEPTION
      --    WHEN OTHERS THEN
      --      RAISE_APPLICATION_ERROR('-20001', 'Não foi possível calcular o saldo de estoque por dia no ERP. Erro: ' || chr(13) || sqlerrm);  
      -- END;
    END IF;
  END IF;
EXCEPTION
  WHEN OTHERS THEN
    ERR_NUM := SQLCODE;
    ERR_MSG := SQLERRM;
    GAP_LOG(SYS_CONTEXT('USERENV', 'CURRENT_SCHEMA'),
            'GAT_BI_SEQ_MOV_ABASTEC',
            'INTEGRAC?O',
            'ERRO: ' || ERR_NUM || ' - ' || ERR_MSG,
            0);
END;
```

### Alterações no Gatec

Após atualizar os módulos, rode o seguinte script.

```SQL
-- Habilita a configuração do WS no modulo GIT
UPDATE GATEC_GIT_CONFIG_PARAM SET VALOR = '1' WHERE PARAMETRO = 'CFG_USAR_BAIXA_WEBSERVICE';
-- Mostra menu para configura no Senhas (Liberação de Usuário)
UPDATE GAM_MODULOS_FORMS SET MOD_DATA = NULL WHERE MOD_MODULO = 346
```

Agora libere para o usuário poder efetuar a configuração do webservice.

Agora a integração dos módulos automotívos será via HTTP, e para configura, vá no módulo GIT (Integração), no menu Utilitários -> Configuração do WEBService.

Vamos configurar o Módulo de abastecimento, para isso informe

| Parâmetro | Valor | Descrição |
| --- | --- | --- |
| Módulo | 50 | Código do módulo que irá efetuar a integração |
| URL | `http://<SERVIDOR>:<PORTA>/integrador/?modulo=AUT&operacao=<OPERACAO>&usuario=<USUARIO>&senha=<SENHA>&token=<CHAVE>&rotina=abastecimento` | Url da integração |
| SERVIDOR WEBSERVICE | 192.168.2.171 | Endereço do servidor de Integração |
| PORTA WEBSERVICE | 80 | Endereço da porta do servidor de Integração |
| USUARIO | * | Usuário do ERP que ira efetuar a integração |
| SENHA | * | Senha do usuário de integração |
| REGRA | 805 | Regra que utilizara para efetuar a integração |
| TIMEOUT | 1000 | Tempo de espera máximo caso o servidor não responda |


### Alterações no ERP

Para atender essa necessidade, foi desenvolvido um serviço (com.gs.g1.co.int.integracoes.GatecAbastecimento).

https://gist.github.com/schefferdev/9d507c62bf1acdff4deb2b4e127ff476

Para evitar problemas de alterações de movimentos ou exclusão, foram criados as seguintes triggers.

Quando excluir

```sql
CREATE OR REPLACE TRIGGER TGS_E210MVP_ABASTEC_AD
  AFTER DELETE
  ON E210MVP 
  FOR EACH ROW
DECLARE
  vMovId NUMBER;
BEGIN
  BEGIN
  SELECT A.MOV_ID
    INTO vMovId
    FROM DB_INTEGRACAO.GATEC_MOV_ABASTEC A
   WHERE A.ERP_CODEMP = :OLD.CODEMP
     AND A.ERP_CODPRO = :OLD.CODPRO
     AND A.ERP_CODDER = :OLD.CODDER
     AND A.ERP_CODDEP = :OLD.CODDEP
     AND A.ERP_DATMOV = :OLD.DATMOV
     AND A.ERP_SEQMOV = :OLD.SEQMOV;
  EXCEPTION
    WHEN OTHERS THEN
      vMovId := 0;
  END;
  
  IF VMOVID <> 0 THEN
    UPDATE DB_INTEGRACAO.GATEC_MOV_ABASTEC A
       SET A.OBS_ERRO_ABASTEC = 'Movimento excluido no ERP',
           A.IES_INTEGRADO = 'N'
     WHERE A.MOV_ID = vMovId;
  END IF;
END TGS_E210MVP_AD;
```

Quando Alterar

```sql
CREATE OR REPLACE TRIGGER TGS_E210MVP_ABASTEC_BU
  BEFORE UPDATE
  ON E210MVP
  FOR EACH ROW
DECLARE
  vMovId NUMBER;
  vQtdMov NUMBER;
  vCodDep VARCHAR2(10);
  vCodCcu VARCHAR2(10);
BEGIN
  BEGIN
  SELECT A.MOV_ID,
         A.QTD_MATERIAL,
         A.COD_DEPOS,
         A.COD_CENTR_CUSTO
    INTO vMovId,
         vQtdMov,
         vCodDep,
         vCodCcu
    FROM DB_INTEGRACAO.GATEC_MOV_ABASTEC A
   WHERE A.ERP_CODEMP = :NEW.CODEMP
     AND A.ERP_CODPRO = :NEW.CODPRO
     AND A.ERP_CODDER = :NEW.CODDER
     AND A.ERP_CODDEP = :NEW.CODDEP
     AND A.ERP_DATMOV = :NEW.DATMOV
     AND A.ERP_SEQMOV = :NEW.SEQMOV;
  EXCEPTION
    WHEN OTHERS THEN
      vMovId := 0;
  END;

  IF VMOVID <> 0 THEN
    IF vQtdMov <> :NEW.QTDMOV THEN
      RAISE_APPLICATION_ERROR('-20001', 'Não é permitido alterar a quantidade por essa tela. Registro com origem no Gatec');
    END IF;
    
    IF vCodDep <> :NEW.CODDEP THEN
      RAISE_APPLICATION_ERROR('-20001', 'Não é permitido alterar o depósito por essa tela. Registro com origem no Gatec');
    END IF;
    
    IF vCodCcu <> :NEW.CODCCU THEN
      RAISE_APPLICATION_ERROR('-20001', 'Não é permitido alterar o centro de custo por essa tela. Registro com origem no Gatec');
    END IF;
  END IF;
END TGS_E210MVP_AD;
```