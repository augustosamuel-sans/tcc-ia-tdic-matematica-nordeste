# Prompt de Repesquisa - BA - Bloco 2/14

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
- instituicao_bruta: UFBA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO DE PARATINGA
- municipio_polo_bruto: Paratinga
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://nead.uesc.br/cursos/matematica/
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

### Item 2
- estado: BA
- instituicao_bruta: UFOB
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus Reitor Edgard Santos
- municipio_polo_bruto: Barreiras
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
- instituicao_bruta: UFPB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - ESPLANADA
- municipio_polo_bruto: Esplanada
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
- instituicao_bruta: UFPB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Pólo UAB - ESPLANADA
- municipio_polo_bruto: Esplanada
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

### Item 5
- estado: BA
- instituicao_bruta: UFSB
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Sosígenes Costa
- municipio_polo_bruto: Porto Seguro
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
- instituicao_bruta: UNEB
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Cristópolis - CAMPUS IX
- municipio_polo_bruto: Cristópolis
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

### Item 7
- estado: BA
- instituicao_bruta: UNEB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: FEIRA DE SANTANA - UAB
- municipio_polo_bruto: Feira de Santana
- curso_alvo: Licenciatura em Matematica
- status_anterior: HTML_INTERMEDIARIO
- url_fonte_anterior: https://nead.uesc.br/cursos/matematica/
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

