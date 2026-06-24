# Prompt de Pesquisa - MA - Bloco 6/9

Objetivo: completar metadados faltantes de PPC de Licenciatura em Matematica SEM alucinacao.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

```yaml
estado: "MA"
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
```

## Itens (maximo 7)

### Item 1
- estado: MA
- instituicao_bruta: UEMA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Instituto Educacional Prof Olga Portela
- municipio_polo_bruto: Brejo
- curso_alvo: Licenciatura em Matematica
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
- estado: MA
- instituicao_bruta: UEMASUL
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus SEDE
- municipio_polo_bruto: Imperatriz
- curso_alvo: Licenciatura em Matematica
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
- estado: MA
- instituicao_bruta: UEMASUL
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Unidade Acadêmica Darcy Ribeiro
- municipio_polo_bruto: Porto Franco
- curso_alvo: Licenciatura em Matematica
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
- estado: MA
- instituicao_bruta: UFMA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO GRAJAU UAB
- municipio_polo_bruto: Grajaú
- curso_alvo: Licenciatura em Matematica
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
- estado: MA
- instituicao_bruta: UFMA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: PÓLO DE ARARI
- municipio_polo_bruto: Arari
- curso_alvo: Licenciatura em Matematica
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
- estado: MA
- instituicao_bruta: UEMA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Polo UAB - ARARI
- municipio_polo_bruto: Arari
- curso_alvo: Licenciatura em Matematica
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
- estado: MA
- instituicao_bruta: IFMA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - SAO JOAO DOS PATOS
- municipio_polo_bruto: São João dos Patos
- curso_alvo: Licenciatura em Matematica
- precisa_ano_ppc: sim
- precisa_url_fonte: sim
- precisa_url_download_pdf: sim
- precisa_status_link: sim
- precisa_ppc_compartilhado: sim
- precisa_polos_relacionados: sim
- precisa_evidencia_minima: sim
- precisa_obs: sim
- precisa_acao_recomendada: sim
