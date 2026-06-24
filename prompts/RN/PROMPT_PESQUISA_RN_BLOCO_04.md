# Prompt de Pesquisa - RN - Bloco 4/5

Objetivo: completar metadados faltantes de PPC de Licenciatura em Matematica SEM alucinacao.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

```yaml
estado: "RN"
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB São Gonçalo do Amarante
- municipio_polo_bruto: São Gonçalo do Amarante
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Lajes
- municipio_polo_bruto: Lajes
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - LUIS GOMES
- municipio_polo_bruto: Luís Gomes
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: NOVA CRUZ.NESA - CAMPUS DE NOVA CRUZ
- municipio_polo_bruto: Nova Cruz
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Macau
- municipio_polo_bruto: Macau
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Extremoz
- municipio_polo_bruto: Extremoz
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
- estado: RN
- instituicao_bruta: UFRN
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo de Martins
- municipio_polo_bruto: Martins
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
