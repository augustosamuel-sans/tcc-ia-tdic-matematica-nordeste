# Prompt de Repesquisa - PI - Bloco 8/9

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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Água Branca-PI
- municipio_polo_bruto: Água Branca
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://integra.ifpi.edu.br/busca/%22licenciatura%20em%20matem%C3%A1tica%22
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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Bom Jesus-PI
- municipio_polo_bruto: Bom Jesus
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=320
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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Campo Maior-PI
- municipio_polo_bruto: Campo Maior
- curso_alvo: Licenciatura em Matemática
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=463
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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Marcos Parente-PI
- municipio_polo_bruto: Marcos Parente
- curso_alvo: Licenciatura em Matemática
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=735
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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: CAMPUS SENADOR HELVÍDIO NUNES DE BARROS
- municipio_polo_bruto: Picos
- curso_alvo: Licenciatura em Matemática
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: http://bia.ifpi.edu.br:8080/jspui/handle/123456789/4306
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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Redenção do Gurguéia-PI
- municipio_polo_bruto: Redenção do Gurguéia
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

### Item 7
- estado: PI
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - SIMPLICIO MENDES
- municipio_polo_bruto: Simplício Mendes
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=926
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

