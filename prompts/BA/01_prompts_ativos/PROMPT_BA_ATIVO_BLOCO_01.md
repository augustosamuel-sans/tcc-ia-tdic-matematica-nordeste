# Prompt de Repesquisa - BA - Bloco 1/14

Objetivo: converter casos NAO_OK para OK_PDF com fonte oficial verificavel e evidencia literal.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

~~~yaml
estado: "BA"
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
- estado: BA
- instituicao_bruta: IFBA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB de Salvador IAT
- municipio_polo_bruto: Salvador
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sigaa.ufpb.br/sigaa/public/curso/ppp.jsf?lc=pt_BR&id=1626785
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
- estado: BA
- instituicao_bruta: IFBA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB de São Francisco do Conde
- municipio_polo_bruto: São Francisco do Conde
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sead.ufba.br/cursos/licenciatura-em-matematica-3a-oferta
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
- estado: BA
- instituicao_bruta: IFBA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB de Seabra
- municipio_polo_bruto: Seabra
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sead.ufba.br/cursos/licenciatura-em-matematica-3a-oferta
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
- estado: BA
- instituicao_bruta: UEFS
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Universidade Estadual de Feira de Santana - UEFS
- municipio_polo_bruto: Feira de Santana
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://dedc.senhordobonfim.uneb.br/matematica/
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
- estado: BA
- instituicao_bruta: UESB
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus de Jequié
- municipio_polo_bruto: Jequié
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sead.ufba.br/cursos/licenciatura-em-matematica-3a-oferta
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
- estado: BA
- instituicao_bruta: UESC
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: CAMPUS  - ILHÉUS - SALOBRINHO
- municipio_polo_bruto: Ilhéus
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sigaa.ufpb.br/sigaa/public/curso/portal.jsf?id=1626841&lc=pt_BR
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
- estado: BA
- instituicao_bruta: UFBA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO JACARACI
- municipio_polo_bruto: Jacaraci
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://sigaa.ufpb.br/sigaa/public/curso/ppp.jsf?lc=pt_BR&id=1626785
- url_download_anterior: https://drive.google.com/file/d/1ol4FpIFKOqr0J0bfdn16P7IUispxeM09/view?usp=sharing
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim

