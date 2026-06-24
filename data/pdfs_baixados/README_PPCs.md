# Metodologia de Distribuição de Corpus Documental (Open Science)

Este diretório (`data/pdfs_baixados/`) é o local de destino para o armazenamento temporário local dos arquivos PDF brutos correspondentes aos 95 Projetos Pedagógicos de Curso (PPCs) de Matemática analisados nesta pesquisa.

Em conformidade com as diretrizes internacionais de **Ciência Aberta (Open Science)**, as melhores práticas de **Engenharia de Dados** e as restrições regulatórias vigentes, estes documentos binários de grande porte **não foram incluídos** no controle de versão deste repositório público pelas seguintes razões fundamentais:

---

## 1. Justificativa Técnica (Controle de Versão e Limites de Armazenamento)
O Git foi projetado especificamente para gerenciar e versionar código-fonte baseado em linhas de texto. Ele é ineficiente para processar e versionar arquivos binários compactados ou documentos PDF de dezenas de megabytes. 
*   **Limitações do GitHub**: Arquivos individuais acima de 50 MB recebem avisos e arquivos acima de 100 MB são sumariamente bloqueados pela plataforma sem a instalação de dependências externas (como Git LFS). O limite recomendado para um repositório inteiro é de 1 GB a 5 GB.
*   **Performance**: Rastrear 95 arquivos PDF pesados (muitos deles gerados por escaneamento de imagens não otimizados) tornaria a clonagem (`git clone`) excessivamente demorada e desperdiçaria recursos de rede de outros pesquisadores acadêmicos.

---

## 2. Justificativa de Propriedade Intelectual (Direitos Autorais e Copyright)
Os Projetos Pedagógicos de Curso (PPCs) são de autoria intelectual das respectivas Instituições de Ensino Superior (IES) públicas do Nordeste que os emitiram. 
*   Embora sejam documentos públicos, a redistribuição direta de todo o corpus bruto compilado em um repositório pessoal ou de terceiros pode violar políticas internas de uso de marca ou restrições legais das instituições.
*   O repositório age em conformidade ética ao **não se apropriar** e redistribuir documentos oficiais não licenciados para fins de replicação fora dos canais institucionais.

---

## 3. Justificativa Metodológica (Boas Práticas de Reprodutibilidade)
Na ciência aberta e reprodutível moderna, a integridade científica não exige o armazenamento estático e redundante do corpus na nuvem do código, mas sim a transparência do **processo e dos metadados**:
*   **Metadados Públicos**: Disponibilizamos a planilha canônica em [`data/output_csv/mapeamento_ppc_polos.csv`](../output_csv/mapeamento_ppc_polos.csv) contendo as URLs originais públicas e os metadados de cada oferta e curso analisado.
*   **Pipeline Automatizado**: Fornecemos o script de download em lote [`scripts/util_baixar_pdfs_atualizar_planilha.ps1`](../../scripts/util_baixar_pdfs_atualizar_planilha.ps1). Qualquer pesquisador pode executar este script para baixar diretamente os mesmos arquivos do repositório oficial de cada IES.
*   **Auditoria de Origem**: Baixar os documentos diretamente da fonte oficial garante ao auditor a certeza de que os arquivos analisados são exatamente os mesmos homologados e vigentes nas instituições, sem manipulações intermediárias.

---

## 🚀 Como Recriar o Corpus de PDFs Localmente
Para povoar esta pasta e executar os pipelines de triagem e análise curricular localmente, siga o roteiro:

1.  Certifique-se de que o interpretador PowerShell esteja ativo.
2.  Execute o script de download a partir do diretório de scripts:
    ```powershell
    cd scripts
    .\util_baixar_pdfs_atualizar_planilha.ps1
    ```
    O script lerá as URLs contidas nos metadados, fará a requisição HTTP e salvará os PDFs de forma estruturada dentro desta pasta `data/pdfs_baixados/`.
