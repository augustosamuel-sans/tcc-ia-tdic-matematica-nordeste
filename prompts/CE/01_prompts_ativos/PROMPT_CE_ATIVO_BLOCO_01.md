# Prompt de Pesquisa - CE - Bloco 1/11

Objetivo: completar metadados faltantes de PPC de Licenciatura em Matematica SEM alucinacao.

Regras obrigatorias:
1. Somente fonte oficial verificavel.
2. Sem evidencia literal + URL => retornar NAO_ENCONTRADO.
3. Nao inventar ano, link, status do PPC ou resumo.
4. Se o mesmo PDF atender varios polos, marcar PPC_COMPARTILHADO=SIM.

Formato de saida: YAML por item.

```yaml
estado: "CE"
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
- estado: CE
- instituicao_bruta: UNILAB
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS DAS AURORAS
- municipio_polo_bruto: Redenção
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
- estado: CE
- instituicao_bruta: UFCA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: Campus Brejo Santo
- municipio_polo_bruto: Brejo Santo
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
- estado: CE
- instituicao_bruta: UECE
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS FECIL - ARACATI
- municipio_polo_bruto: Aracati
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
- estado: CE
- instituicao_bruta: UECE
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO ITAREMA
- municipio_polo_bruto: Itarema
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
- estado: CE
- instituicao_bruta: UFCA
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: POLO UAB IGUATU-CE SANTO ANTÔNIO/ASSOCIADO
- municipio_polo_bruto: Iguatu
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
- estado: CE
- instituicao_bruta: UFC
- modalidade_bruta: Educação a Distância
- nome_polo_ou_campus_bruto: Polo UAB - QUITERIANOPOLIS
- municipio_polo_bruto: Quiterianópolis
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
- estado: CE
- instituicao_bruta: URCA
- modalidade_bruta: Educação Presencial
- nome_polo_ou_campus_bruto: CAMPUS CRAJUBAR
- municipio_polo_bruto: Juazeiro do Norte
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
