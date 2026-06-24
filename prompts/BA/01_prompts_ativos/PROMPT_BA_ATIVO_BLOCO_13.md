# Prompt de Repesquisa - BA - Bloco 13/14

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
- instituicao_bruta: UNEB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - REMANSO
- municipio_polo_bruto: Remanso
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
- estado: BA
- instituicao_bruta: UNEB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: CAMPUS I
- municipio_polo_bruto: Salvador
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://unead.uneb.br/index.php/matematica/
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
- instituicao_bruta: UNEB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: SANTO ESTEVÃO - UAB
- municipio_polo_bruto: Santo Estêvão
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://nead.uesc.br/cursos/matematica/
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
- instituicao_bruta: UNEB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - SEABRA
- municipio_polo_bruto: Seabra
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
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

### Item 5
- estado: BA
- instituicao_bruta: UNEB
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Senhor do Bonfim
- municipio_polo_bruto: Senhor do Bonfim
- curso_alvo: Licenciatura em Matemática
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://www2.uesb.br/curso/matematica/matematicajq/?page_id=102
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
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - SERRINHA
- municipio_polo_bruto: Serrinha
- curso_alvo: Licenciatura em Matemática
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
- estado: BA
- instituicao_bruta: UNEB
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo Sítio do Quinto
- municipio_polo_bruto: Sítio do Quinto
- curso_alvo: Licenciatura em Matematica
- status_anterior: NAO_ENCONTRADO
- url_fonte_anterior: https://nead.uesc.br/cursos/matematica/
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

