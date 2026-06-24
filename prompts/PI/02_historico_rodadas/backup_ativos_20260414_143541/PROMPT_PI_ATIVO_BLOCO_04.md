# Prompt de Repesquisa - PI - Bloco 4/10

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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Redenção do Gurguéia-PI
- municipio_polo_bruto: Redenção do Gurguéia
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://legcead.ufpi.br/index.php/matematica
- url_download_anterior: https://sigaa.ufpi.br/sigaa/verProducao?idProducao=210544&key=6ac3fbdec53a0d9391908017fbeebc43
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
- nome_polo_ou_campus_bruto: Polo UAB - SIMPLICIO MENDES
- municipio_polo_bruto: Simplício Mendes
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sigaa.ufpi.br/sigaa/verProducao?idProducao=210544&key=6ac3fbdec53a0d9391908017fbeebc43
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
- nome_polo_ou_campus_bruto: CAMPUS MINISTRO PETRÔNIO PORTELLA - Unidade SEDE
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://legcead.ufpi.br/index.php/matematica
- url_download_anterior: https://sigaa.ufpi.br/sigaa/verProducao?idProducao=210544&key=6ac3fbdec53a0d9391908017fbeebc43
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
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS MINISTRO PETRÔNIO PORTELLA - Unidade SEDE
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://legcead.ufpi.br/index.php/matematica
- url_download_anterior: https://sigaa.ufpi.br/sigaa/verProducao?idProducao=210544&key=6ac3fbdec53a0d9391908017fbeebc43
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
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS MINISTRO PETRÔNIO PORTELLA - Unidade SEDE
- municipio_polo_bruto: Teresina
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://legcead.ufpi.br/index.php/matematica
- url_download_anterior: https://sigaa.ufpi.br/sigaa/verProducao?idProducao=210544&key=6ac3fbdec53a0d9391908017fbeebc43
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
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - União-PI
- municipio_polo_bruto: União
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://legcead.ufpi.br/index.php/matematica
- url_download_anterior: https://sigaa.ufpi.br/sigaa/verProducao?idProducao=210544&key=6ac3fbdec53a0d9391908017fbeebc43
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
- instituicao_bruta: IFPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus Angical do Instituto Federal do Piauí
- municipio_polo_bruto: Angical do Piauí
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

