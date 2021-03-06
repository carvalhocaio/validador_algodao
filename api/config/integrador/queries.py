QR_SERVICO_REALIZADO = """
SELECT CAST(EMP.COD_EMPR_ERP_SEMFILIAL AS NUMBER) AS EMPRESA,
       CAST(EMP.COD_EMPR_ERP_FILIAL AS NUMBER) AS FILIAL,
       REQ.CHAVE_MD5 AS TOKEN,
       REQ.ID_CHAVE AS ID,
       REQ.COD_MATER AS PRODUTO,
       REQ.COD_DEPOS AS DEPOSITO,
       REQ.MOV_DATA AS DATA,
       REQ.QTD_SOLIC AS QUANTIDADE,
       TRUNC(NVL(REQ.COD_CENTRO_CUSTO,'0')) AS CENTRO_CUSTO,
       CAST(SUBSTR(REQ.COD_OS,4) AS NUMBER) AS CODIGO_OS,
       REQ.SAF_ANO_SAFRA AS SAFRA,
       DECODE(
         SUBSTR(REQ.COD_MATER,1,1),
         'S', 'S',
         'P'
       ) AS PRODUTO_SERVICO,
       'DADOS DA OS : ' ||
         SUBSTR(REQ.COD_OS,4) ||
         ' FAZENDA : ' ||
         INITCAP(REPLACE(OSG.DSC_EQP_CC,'FAZENDA ', '')) ||
         DECODE(USU.CODUSU, NULL, ' USUARIO: ' || REQ.REQ_USUARIO, NULL) AS OBSERVACAO,
       USU.CODUSU AS USUARIO_ID
  FROM DB_INTEGRACAO.GATEC_OS_ITENS_REQUISITADOS REQ
       JOIN DB_INTEGRACAO.GATEC_DEPARA_EMPRESA EMP ON EMP.COD_EMPR_GA = REQ.COD_EMPR
       JOIN DB_INTEGRACAO.GATEC_OS OSG ON OSG.COD_EMPR = REQ.COD_EMPR
                                      AND OSG.SAF_ANO_SAFRA = REQ.SAF_ANO_SAFRA
                                      AND OSG.NUM_OS = REQ.COD_OS
       LEFT JOIN SAPIENS.R999USU USU ON UPPER(TRIM(REQ.REQ_USUARIO)) = UPPER(TRIM(USU.NOMUSU))
 WHERE SUBSTR(REQ.COD_OS,1,3) = 'AGR'
   AND NVL(REQ.REQUIS_GERADA,'N') = 'N'
   AND REQ.CHAVE_MD5 = :token
"""

QR_NOTA_FISCAL_VENDA = """
SELECT USU_SEQFAT AS ID,
       TO_NUMBER(B.COD_EMPR_ERP_SEMFILIAL) AS EMPRESA,
       TO_NUMBER(B.COD_EMPR_ERP_FILIAL) AS FILIAL,
       SUBSTR(DECODE(LINHAS, 1, A.COD_TRANSACAO, A.COD_TRANSACAO_REM), 2, 5) AS TRANSACAO,
       USU_TIPNFS AS TIPO_NOTA_FISCAL,
       USU_CODSNF AS SERIE,
       USU_NUMNFV AS NOTA,
       USU_DATEMI AS EMISSAO,
       USU_NUMPED AS PEDIDO_ERP,
       ID_PEDIDO AS PEDIDO_GATEC,
       ROM_ITEM AS ROMANEIO,
       EMB_ITEM AS INSTRUCAO,
       USU_CODCLI AS CLIENTE,
       TO_NUMBER(SUBSTR(USU_SEQENT, 5, LENGTH(USU_SEQENT))) AS ENDERECO_ENTREGA,
       USU_CODTRA AS TRANSPORTADORA,
       USU_CODMOT AS MOTORISTA,
       USU_PLAVEI AS PLACA,
       USU_PLAREB AS PLACA_REBOQUE,
       USU_PESBRU AS PESO_BRUTO,
       USU_PESLIQ AS PESO_LIQUIDO,
       USU_CODCPG AS CONDICAO_PAGApipMENTO,
       USU_CODSAF AS SAFRA,
       USU_OBSNFV AS OBSERVACAO,
       USU_CTRCOM AS CONTRATO_ID,
       USU_FORORI AS FORNECEDOR_ORIGEM,
       USU_FORARM AS FORNECEDOR_ARMAZENAGEM,
       USU_NOMPOR AS PORTO,
       USU_NUMDCO AS DCO,
       USU_CTRVEN AS CONTRATO,
       USU_TIPO_COTACAO AS TIPO_COTACAO,
       NVL(USU_CLIREM,0) AS CLIENTE_REMESSA,
       TO_NUMBER(SUBSTR(USU_ENTREM, 5, LENGTH(USU_ENTREM))) AS ENTREGA_REMESSA,
       SUBSTR(COD_TRANSACAO_REM, 2, 5) AS TRANSACAO_REMESSA,
       NVL(USU_NFVREM,0) AS NOTA_REMESSA,
       DECODE(USU_NUMLOT,                                                                  
              NULL, ' ',                                                                   
              SUBSTR('LOTE' || ' ' || USU_NUMLOT, 1, 30)) AS LOTE,
       USU_NUMFAR AS FARDOS,
       TO_NUMBER(DECODE(LINHAS,                                                            
                        1, T.TRA_CONTA_ORDEM,                                              
                        '0')) AS CONTA_ORDEM
  FROM DB_INTEGRACAO.USU_GATEC_E140NFV A,                                                  
       DB_INTEGRACAO.GATEC_DEPARA_EMPRESA B,                                               
       GATEC_SAF.GA_ALG_TRANSACAO T,                                                       
       (SELECT ROWNUM AS LINHAS FROM DUAL CONNECT BY LEVEL <= 2) LIN                       
 WHERE A.COD_EMPFIL = B.COD_EMPR_ERP                                                       
   AND A.COD_TRANSACAO = T.COD_TRANSACAO                                                   
   AND LIN.LINHAS <= DECODE(T.TRA_CONTA_ORDEM, 3, 2, 1)                                    
   AND A.USU_CHANFV = :token                                                                    
"""

QR_ABASTECIMENTO = """
SELECT ABA.CHAVE AS CHAVE,
       ABA.MOV_ID AS ID,
       ABA.NUM_DOCUM AS DOCUMENTO,
       ABA.COD_EMPR AS EMPRESA,
       ABA.MAT_CODIGO AS PRODUTO,
       ABA.QTD_MATERIAL AS QUANTIDADE,
       ABA.DAT_MOVIMENTO AS DATA_MOVIMENTO,
       ABA.COD_CENTR_CUSTO AS CENTRO_CUSTO,
       ABA.COD_DEPOS AS DEPOSITO,
       ABA.COD_PONTO AS PONTO,
       ABA.IES_INTEGRADO AS INTEGRADO,
       ABA.DAT_EXPORT AS DATA_EXPORTACAO,
       ABA.USER_EXPORT AS USUARIO,
       ABA.REQ AS TIPO,
       ABA.COD_EQUIPAMENTO AS EQUIPAMENTO,
       ABA.OBS_ERRO_ABASTEC AS ERRO,
       ABA.DAT_IMPORT AS DATA_IMPORTACAO
  FROM GATEC_MOV_ABASTEC ABA
 WHERE ABA.CHAVE_MD5 = :token
"""