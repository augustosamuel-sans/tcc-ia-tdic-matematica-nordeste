# Prompt de Repesquisa - PI - Bloco 7/9

Objetivo: converter casos NAO_OK para OK_PDF com fonte oficial verificavel e evidencia literal.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

~~~yaml
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
~~~

## Itens (maximo 7)

### Item 1
- estado: PI
- instituicao_bruta: IFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB Professora Concita Mendes
- municipio_polo_bruto: São José do Peixe
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://uespi.br/graduacao-inicio/
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
- instituicao_bruta: IFPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS SÃO RAIMUNDO NONATO DO INSTITUTO FEDERAL DO PIAUI
- municipio_polo_bruto: São Raimundo Nonato
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

### Item 3
- estado: PI
- instituicao_bruta: IFPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus Teresina Central
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matemática
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://uespi.br/wp-content/uploads/2021/Downloads/guias/PDI_FINAL_GRAFICA_2017.pdf
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
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO UAP DE ALTOS - PI
- municipio_polo_bruto: Altos
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: http://www.ceepi.pro.br/CADASTRO%20superiores/uespi.geral-RE_TOTAL.htm
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
- nome_polo_ou_campus_bruto: Campus Prof. Barros Araújo
- municipio_polo_bruto: Picos
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ojs.brazilianjournals.com.br/index.php/BRJD/article/download/25195/20087
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
- nome_polo_ou_campus_bruto: PROFº ANTONIO GIOVANNE ALVES DE SOUSA
- municipio_polo_bruto: Piripiri
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://editorarealize.com.br/editora/anais/conedu/2025/TRABALHO_COMPLETO_EV214_ID4332_TB876_24102025201757.pdf
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
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: CAMPUS  - TERESINA - PIRAJÁ
- municipio_polo_bruto: Teresina
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

