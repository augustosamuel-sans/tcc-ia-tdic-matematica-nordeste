# Prompt de Repesquisa - PI - Bloco 6/10

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
- instituicao_bruta: IFPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus Uruçuí do Instituto Federal do Piauí
- municipio_polo_bruto: Uruçuí
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: NAO_ENCONTRADO
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
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO UAP DE ALTOS - PI
- municipio_polo_bruto: Altos
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://uespi.br/campi/
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
- nome_polo_ou_campus_bruto: CANTO DO BURITI
- municipio_polo_bruto: Canto do Buriti
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: http://bia.ifpi.edu.br:8080/jspui/handle/123456789/277?offset=20
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
- nome_polo_ou_campus_bruto: ELESBÃO VELOSO
- municipio_polo_bruto: Elesbão Veloso
- curso_alvo: Licenciatura em Matemática
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=817
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
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: ESPERANTINA
- municipio_polo_bruto: Esperantina
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: NAO_ENCONTRADO
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
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB Luís Correia
- municipio_polo_bruto: Luís Correia
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: NAO_ENCONTRADO
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
- nome_polo_ou_campus_bruto: LUZILÂNDIA
- municipio_polo_bruto: Luzilândia
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://admin.pi.gov.br/uploads/EDITAL_Processo_Seletivo_para_Portador_de_Curso_Superior_2025_1_df52630164.pdf
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

