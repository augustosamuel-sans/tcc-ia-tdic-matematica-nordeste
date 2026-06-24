# Análise Automatizada de Projetos Pedagógicos de Curso (PPCs) de Matemática no Nordeste via Inteligência Artificial

[![Open Science](https://img.shields.io/badge/Open%20Science-Garantido-blue.svg)](https://ouves.github.io/)
[![Python Version](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Resumo do Escopo

Este repositório reúne os dados, os scripts de automação, os prompts estruturados e o pipeline analítico que compõem o trabalho de conclusão de curso (TCC) intitulado **"TECNOLOGIAS DIGITAIS E INTELIGÊNCIA ARTIFICIAL NA LICENCIATURA EM MATEMÁTICA: UMA ANÁLISE CURRICULAR DOS CURSOS DAS IES PÚBLICAS NORDESTINAS"**.

A pesquisa baseia-se na extração e avaliação qualitativa/quantitativa de **95 Projetos Pedagógicos de Curso (PPCs)** de Matemática, confrontando-os com uma base consolidada de **344 ofertas de vagas do sistema e-MEC**. A etapa analítica utiliza o modelo de linguagem **Perplexity Pro** para a extração cirúrgica de dados estruturados das diretrizes curriculares e identificação de tendências regionais.

---

## 📂 Arquitetura do Repositório

A estrutura de diretórios foi desenhada seguindo as melhores práticas de Engenharia de Software e Open Science, dividindo dados brutos (gerados sob demanda), lógica de processamento, prompts e interfaces:

```
├── scripts/                                 # Scripts de coleta, triagem e automação (Python e PowerShell)
│   ├── app_triagem_download_manual.py       # Interface gráfica de suporte ao download de PDFs
│   ├── util_reconciliar_mapeamento_por_estado.py # Script de reconciliação cadastral
│   └── util_baixar_pdfs_atualizar_planilha.ps1 # Download automático de PPCs via PowerShell
├── prompts/                                 # Modelos de prompts cirúrgicos estruturados separados por estado (UF)
│   ├── AL/, BA/, CE/, MA/, PB/...            # Subdiretórios com prompts específicos regionais
├── app_IA/                                  # Aplicação local para integração de análise de IA
│   ├── app.py                               # Interface gráfica (Tkinter) para parse das respostas da IA
│   ├── core.py                              # Motor de parseamento, regex e consistência lógica dos dados
│   └── requirements.txt                     # Dependências do interpretador Python
├── data/                                    # Base de dados analíticos e corpus documental
│   ├── output_csv/                          # Planilhas canônicas consolidadas de ofertas e-MEC
│   │   ├── mapeamento_ppc_polos.csv         # Planilha mestre consolidada com as URLs das PPCs
│   │   ├── SEGURANCA_PDF_POLOS_TODOS_ESTADOS.csv # Mapeamento detalhado de segurança
│   │   └── RESUMO_SEGURANCA_POR_UF.csv      # Sumarização quantitativa por estado
│   └── pdfs_baixados/                       # Destino local das matrizes curriculares brutas em PDF
│       └── README_PPCs.md                   # Justificativa técnica e jurídica da exclusão de binários no Git
├── auditar_secrets.py                       # Utilitário local para auditoria e prevenção de vazamento de credenciais
├── .gitignore                               # Regras de exclusão do Git (ignora dados > 100MB, PDFs locais e caches)
└── README.md                                # Esta documentação técnica
```

> [!NOTE]
> Os documentos PDF brutos baixados (`data/pdfs_baixados/`) estão ignorados no controle de versão Git por razões de armazenamento e direitos autorais. O download deve ser realizado localmente conforme as instruções de reprodução abaixo.

---

## 🔧 Pré-requisitos e Dependências

Para rodar os scripts de extração, triagem e a interface gráfica de análise, é necessário ter instalado na sua máquina:

1. **Python 3.8+**
2. **PowerShell 7+** (caso queira executar os scripts de utilitários do Windows `.ps1`)

### Como instalar as dependências de Python

Recomendamos criar um ambiente virtual dedicado antes de instalar as bibliotecas:

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/tcc-matematica-nordeste.git
cd tcc-matematica-nordeste

# 2. Criar ambiente virtual
python -m venv .venv

# 3. Ativar o ambiente virtual
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
# No Linux/macOS:
source .venv/bin/activate

# 4. Instalar as dependências
pip install -r app_IA/requirements.txt
```

> [!TIP]
> Caso adicione novas bibliotecas durante o seu desenvolvimento, você pode atualizar o arquivo de dependências rodando:
> `pip freeze > app_IA/requirements.txt`

---

## 🚀 Guia de Reprodução Passo a Passo

Siga os passos a seguir para reproduzir o pipeline analítico da pesquisa curricular:

### Passo 1: Preparação da Base e-MEC
A base de referência com as 344 ofertas de cursos de Matemática no Nordeste está localizada em `data/output_csv/` sob o nome de planilha consolidada. Ela serve como base canônica para verificar quais PPCs precisam ser baixados.

### Passo 2: Download em Lote dos PPCs (PDFs)
1. Para baixar os PDFs das matrizes curriculares identificadas na planilha, execute o script PowerShell:
   ```powershell
   cd scripts
   .\util_baixar_pdfs_atualizar_planilha.ps1
   ```
2. Caso URLs específicas falhem devido a captcha ou instabilidade nos portais das universidades, execute a ferramenta de suporte visual em Python para download assistido:
   ```bash
   python app_triagem_download_manual.py
   ```
   Os PDFs baixados serão armazenados localmente na pasta `data/pdfs_baixados/` (que está no `.gitignore` para não ocupar espaço no GitHub).

### Passo 3: Triagem e Processamento de Texto
Com as PPCs locais, o script de leitura de metadados executa a extração do texto e prepara os arquivos parciais para processamento. Execute:
```bash
python util_reconciliar_mapeamento_por_estado.py
```

### Passo 4: Submissão dos Prompts ao Perplexity Pro
1. Os prompts estruturados e cirúrgicos estão localizados na pasta `prompts/`.
2. Para consolidar as respostas estruturadas das análises curriculares usando a interface desenvolvida para a pesquisa:
   ```bash
   cd ../app_IA
   python app.py
   ```
3. Cole as respostas obtidas no Perplexity Pro na interface para que o motor `core.py` realize o parseamento sintático dos campos, valide a integridade dos dados curriculares e exporte o CSV consolidado.

### Passo 5: Geração de Relatórios e Consolidação Científica
Para gerar as tabelas estatísticas agregadas e as métricas de qualidade curricular apresentadas no TCC, execute:
```powershell
cd ../scripts
.\util_consolidar_yaml_csv.ps1
```

---

## 🛡️ Auditoria de Segurança

Como garantia de conformidade de código aberto (Open Science) e segurança da informação, este repositório conta com um script de auditoria estática preventiva.

Antes de realizar qualquer commit ou push público, execute:
```bash
python auditar_secrets.py
```
Esse script fará a varredura local de chaves de API, senhas, tokens ou dados pessoais e gerará alertas de impedimento em caso de inconsistências.

---

## 📄 Licença

* **Código Fonte**: Distribuído sob a licença **MIT** (consulte o arquivo `LICENSE` para detalhes).
* **Dados e Relatórios**: Distribuídos sob a licença **Creative Commons Attribution 4.0 International (CC BY 4.0)**, permitindo o compartilhamento e adaptação desde que atribuído o crédito original.

---

## ✍️ Como Citar este Trabalho (ABNT)

Se você utilizar os dados, os prompts ou os scripts deste repositório em sua pesquisa acadêmica, cite-os da seguinte forma:

```text
PAULO, Samuel Augusto de Freitas. TECNOLOGIAS DIGITAIS E INTELIGÊNCIA ARTIFICIAL NA LICENCIATURA EM MATEMÁTICA: UMA ANÁLISE CURRICULAR DOS CURSOS DAS IES PÚBLICAS NORDESTINAS. 2026. Trabalho de Conclusão de Curso (Graduação em Matemática) - Universidade do Estado do Rio Grande do Norte (UERN), Mossoró, 2026. Disponível em: https://github.com/augustosamuel-sans/tcc-ia-tdic-matematica-nordeste. Acesso em: [Data de Acesso].
```

---
*Este repositório foi higienizado e estruturado visando a reprodutibilidade integral sob os pilares da Ciência Aberta.*
