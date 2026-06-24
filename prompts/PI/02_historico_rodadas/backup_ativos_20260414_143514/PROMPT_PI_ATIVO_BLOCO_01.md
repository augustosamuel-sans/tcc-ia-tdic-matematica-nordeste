# Prompt de Pesquisa - PI - Bloco 1/12

Objetivo: completar metadados faltantes de PPC de Licenciatura em Matematica SEM alucinacao.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

```yaml
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
```

## Itens (maximo 7)

### Item 1
- estado: PI
- instituicao_bruta: UFDPAR
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Unidade SEDE - MINISTRO REIS VELLOSO
- municipio_polo_bruto: Parnaíba
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
- estado: PI
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Gilbués-PI
- municipio_polo_bruto: Gilbués
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
- estado: PI
- instituicao_bruta: UFPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS MINISTRO PETRÔNIO PORTELLA - Unidade SEDE
- municipio_polo_bruto: Teresina
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
- estado: PI
- instituicao_bruta: IFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Campus Pedro II do Instituto Federal do Piauí
- municipio_polo_bruto: Pedro II
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
- estado: PI
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Picos-PI
- municipio_polo_bruto: Picos
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
- estado: PI
- instituicao_bruta: UFPI
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Apoio Presencial - Oeiras-PI
- municipio_polo_bruto: Oeiras
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
- estado: PI
- instituicao_bruta: UESPI
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CANTO DO BURITI
- municipio_polo_bruto: Canto do Buriti
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
