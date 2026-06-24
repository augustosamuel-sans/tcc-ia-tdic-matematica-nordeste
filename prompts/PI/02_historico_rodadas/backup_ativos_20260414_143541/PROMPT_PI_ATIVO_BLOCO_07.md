# Prompt de Repesquisa - PI - Bloco 7/10

Objetivo: converter casos NAO_OK para OK_PDF com fonte oficial verificavel e evidencia literal.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

`yaml
estado: "PI"
instituicao: "..."
modalidade: "..."
nome_polo_ou_campus: "..."
municipio_polo: "..."
curso: "Licenciatura em Matematica"
ano_ppc: "..."
url_fonte: "..."
url_download_pdf: "..."
status_link: "OK_PDF|HTML_INTERMEDIARIO|404|BLOQUEADO|NAO_ENCONTRADO"
ppc_compartilhado: "SIM|NAO"
polos_relacionados:
  - "..."
evidencia_minima: "..."
obs: "..."
confianca: "alta|media|baixa"
acao_recomendada: "OK|NOVA_BUSCA|VALIDACAO_MANUAL"
fontes:
  - url: "..."
    evidencia_literal: "..."
`

## Itens (maximo 7)

### Item 1
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Oeiras
- municipio_polo_bruto: Oeiras
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=337
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

### Item 2
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: PEDRO II
- municipio_polo_bruto: Pedro II
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: http://bia.ifpi.edu.br:8080/jspui/handle/123456789/751
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

### Item 3
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: PROFº ANTONIO GIOVANNE ALVES DE SOUSA
- municipio_polo_bruto: Piripiri
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://www.ceepi.pro.br/Portarias%202022/099-UESPI-LUZIL%C3%82NDIA-%20%20LIC.%20MATEM%C3%81TICA-PARFOR.pdf
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

### Item 4
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: PROF. ARISTON DIAS LIMA - SÃO RDO. NONATO
- municipio_polo_bruto: São Raimundo Nonato
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: http://bia.ifpi.edu.br:8080/jspui/handle/123456789/808
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

### Item 5
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: CAMPUS  - TERESINA - PIRAJÁ
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://uespi.br/wp-content/uploads/2023/09/EDITAL_E_RESULTADO_FINAL.pdf
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

### Item 6
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS  - TERESINA - PIRAJÁ
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://neadseletivos.uespi.br/uploads/edital003202133/Edital0032021.pdf
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

### Item 7
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS  - TERESINA - PIRAJÁ
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://sapl.al.pi.leg.br/norma/pesquisar
- url_download_anterior: NAO_ENCONTRADO
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

