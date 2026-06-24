# Prompt de Repesquisa - PI - Bloco 9/10

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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: CAMPUS AMILCAR FERREIRA SOBRAL
- municipio_polo_bruto: Floriano
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
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Gilbués-PI
- municipio_polo_bruto: Gilbués
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ead.ifpi.edu.br/course/index.php?categoryid=457
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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Inhuma-PI
- municipio_polo_bruto: Inhuma
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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Jaicós-PI
- municipio_polo_bruto: Jaicós
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://uespi.br/preg-dap-dpae/
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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - José de Freitas-PI
- municipio_polo_bruto: José de Freitas
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://integra.ifpi.edu.br/busca/%22matem%C3%A1tica%20aplicada%22
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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Marcos Parente-PI
- municipio_polo_bruto: Marcos Parente
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://ufpi.br/cursos-e-vagas
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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Oeiras-PI
- municipio_polo_bruto: Oeiras
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

