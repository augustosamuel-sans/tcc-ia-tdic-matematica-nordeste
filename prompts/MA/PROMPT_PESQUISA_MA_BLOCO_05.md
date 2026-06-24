# Prompt de Pesquisa - MA - Bloco 5/9

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
- instituicao_bruta: IFMA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS ACAILANDIA
- municipio_polo_bruto: Açailândia
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
- instituicao_bruta: UEMA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Vitória do Mearim Escola Municipal Maria Celeste Barros
- municipio_polo_bruto: Vitória do Mearim
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
- instituicao_bruta: UFMA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo Paraibano
- municipio_polo_bruto: Paraibano
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
- instituicao_bruta: UEMA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: SÃO LUIS
- municipio_polo_bruto: São Luís
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
- instituicao_bruta: IFMA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS CODÓ
- municipio_polo_bruto: Codó
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
- nome_polo_ou_campus_bruto: Bacabal - CESBA
- municipio_polo_bruto: Bacabal
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
- instituicao_bruta: UFMA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo Alto Parnaíba
- municipio_polo_bruto: Alto Parnaíba
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
