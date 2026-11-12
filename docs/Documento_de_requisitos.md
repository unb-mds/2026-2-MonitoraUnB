
# DOCUMENTO DE REQUISITOS DE SOFTWARE (DRS)

**Monitora UnB — Sistema de Gestão do Processo Seletivo de Monitoria**

**Versão:** 0.2  
**Status:** Rascunho para revisão da equipe  
**Instituição:** Universidade de Brasília (UnB)

---

## 1. Introdução

### 1.1. Objetivo

Este documento especifica os requisitos funcionais, não funcionais, regras de negócio, restrições e fluxos operacionais do Monitora UnB, sistema destinado a auxiliar a gestão do processo seletivo de monitores da Universidade de Brasília.

O documento servirá como referência para o desenvolvimento, a implementação e a validação do sistema.

### 1.2. Contextualização

O processo seletivo de monitoria envolve a coleta de informações dos candidatos, a conferência dos dados acadêmicos, o cálculo de coeficientes, a classificação dos estudantes e a distribuição de vagas e bolsas.

No procedimento manual, os estudantes preenchem formulários, cujas respostas são posteriormente reunidas em planilhas. Os responsáveis pela comissão calculam os coeficientes, classificam os candidatos e encaminham informações para conferência da situação acadêmica.

O Monitora UnB pretende reduzir o trabalho manual por meio da centralização das inscrições, da leitura automatizada dos históricos escolares e da geração de classificações e resultados.

### 1.3. Objetivos

O sistema deverá:

- Centralizar as inscrições dos estudantes.
- Extrair informações dos históricos escolares enviados em PDF.
- Comparar os dados extraídos dos documentos com os informados pelos candidatos.
- Impedir o avanço da inscrição quando houver erros de leitura ou divergências impeditivas.
- Calcular os coeficientes dos candidatos elegíveis.
- Gerar classificações gerais e por disciplina.
- Auxiliar a distribuição de vagas e bolsas de monitoria.
- Permitir a análise e a decisão da presidência da comissão.
- Encerrar as inscrições automaticamente no prazo estabelecido.

### 1.4. Público-alvo

- **Estudantes:** realizam as inscrições.
- **Presidência da comissão de monitoria:** analisa as candidaturas e confirma as decisões de seleção.
- **Professores responsáveis pelas disciplinas:** informam a quantidade de monitores desejada para suas disciplinas, conforme o procedimento que vier a ser estabelecido.

---

## 2. Escopo do sistema

### 2.1. Funcionalidades incluídas

O escopo contempla:

1. Página inicial com acesso à inscrição e à área administrativa.
2. Formulário de candidatura.
3. Envio e leitura do histórico em PDF.
4. Comparação entre os dados preenchidos e os dados extraídos do documento.
5. Mensagens de erro para arquivos ilegíveis ou informações divergentes.
6. Geração de comprovantes de inscrição.
7. Armazenamento das candidaturas em banco de dados próprio.
8. Cálculo automático dos coeficientes.
9. Classificação geral e por disciplina.
10. Análise, aprovação e rejeição de candidaturas.
11. Registro da quantidade de vagas e bolsas disponíveis.
12. Sugestão de distribuição de bolsas e vagas.
13. Confirmação administrativa dos resultados.
14. Encerramento automático das inscrições.

### 2.2. Funcionalidades fora do escopo inicial

Não fazem parte do escopo inicial:

- Alteração de dados acadêmicos no SIGAA.
- Verificação automática de outras bolsas recebidas pelos estudantes.
- Concessão autônoma de bolsas pelo sistema.
- Gestão acadêmica completa da universidade.
- Manutenção de um histórico permanente de todas as informações institucionais de semestres anteriores.

---

## 3. Descrição geral do sistema

### 3.1. Arquitetura conceitual

O projeto possui dois componentes distintos:

**API acadêmica do projeto:** possui uma base de dados própria, alimentada por um scraper que coleta informações do SIGAA. Sua finalidade é disponibilizar os dados institucionais contemplados em seu escopo, como informações sobre disciplinas, códigos e professores responsáveis. Não será utilizada para consultar informações pessoais dos candidatos para validar suas inscrições.

**Aplicação Monitora UnB:** será responsável pelo formulário, processamento dos arquivos PDF, comparação dos dados informados, armazenamento das candidaturas, cálculo dos coeficientes, classificação dos estudantes e gestão dos resultados.

O Monitora UnB deverá possuir um banco de dados próprio para armazenar as inscrições e as informações necessárias à condução do processo seletivo.

### 3.2. Usuários

#### 3.2.1. Estudante

O estudante poderá:

- Acessar o formulário de inscrição.
- Informar seus dados pessoais e acadêmicos.
- Selecionar uma única disciplina que deseja ser monitor.
- Enviar o histórico escolar em PDF.
- Declarar que não recebe outra bolsa institucional.
- Conferir as informações validadas.
- Submeter definitivamente a candidatura.

Após a submissão definitiva, o estudante não poderá editar os dados enviados nem substituir o arquivo original da candidatura.

#### 3.2.2. Presidência da comissão

A presidência será o único perfil administrativo previsto inicialmente.

Poderá:

- Acessar o sistema por e-mail e senha.
- Consultar as candidaturas.
- Visualizar classificações gerais e por disciplina.
- Aprovar ou rejeitar candidaturas.
- Consultar os dados submetidos pelos estudantes.
- Informar ou confirmar a quantidade de bolsas disponíveis.
- Analisar e confirmar a distribuição sugerida pelo sistema.

A presidência não poderá modificar os dados originalmente submetidos pelos estudantes.

#### 3.2.3. Professores responsáveis pelas disciplinas

Os professores informarão a quantidade de monitores desejada para suas disciplinas. O mecanismo de recebimento e registro dessas informações deverá ser definido pela equipe.

---

## 4. Requisitos funcionais

### 4.1. Acesso e navegação

**RF-001 — Página inicial:** o sistema deverá disponibilizar uma página inicial com uma opção para iniciar a inscrição de estudante e outra para acessar a área administrativa.

**RF-002 — Acesso à inscrição:** ao selecionar a opção de estudante, o usuário deverá ser direcionado ao formulário de candidatura.

**RF-003 — Autenticação administrativa:** o sistema deverá permitir o acesso da presidência da comissão mediante e-mail e senha.

**RF-004 — Controle de acesso:** as funcionalidades administrativas deverão ser acessíveis somente a usuários autenticados e autorizados.

### 4.2. Formulário de inscrição

**RF-005 — Campos da candidatura:** o formulário deverá conter, no mínimo:

- Nome completo.
- Número de matrícula.
- E-mail de contato.
- Disciplina pretendida.
- Menção informada na disciplina.
- Histórico em PDF.
- Declaração de ausência de outra bolsa incompatível.

**RF-006 — Validação de preenchimento:** o sistema deverá verificar o preenchimento dos campos obrigatórios e os formatos aceitos.

**RF-007 — Seleção de disciplina:** o sistema deverá permitir a escolha de apenas uma disciplina por estudante em cada processo seletivo.

**RF-008 — Declaração de não recebimento de bolsa:** o sistema deverá exigir a declaração do estudante sobre o não recebimento de outras bolsas incompatíveis, basta preencher um campo afirmando.

**RF-009 — Envio do histórico:** o sistema deverá permitir o envio de um histórico escolar apenas no formato PDF.

### 4.3. Leitura e validação do histórico escolar

**RF-010 — Extração de dados:** o backend do Monitora UnB deverá utilizar uma biblioteca em Python para extrair do PDF as informações necessárias à validação.

**RF-011 — Comparação de informações:** o sistema deverá comparar os dados extraídos do PDF com os dados correspondentes informados pelo estudante.

**RF-012 — Validação da menção:** o sistema deverá comparar a menção informada com a menção extraída para a disciplina selecionada.

**RF-013 — Validação da disciplina:** o sistema deverá verificar se a disciplina e os dados associados informados pelo estudante correspondem às informações extraídas do documento.

**RF-014 — Tratamento de divergências:** quando os dados preenchidos não corresponderem aos dados extraídos, o sistema deverá exibir uma mensagem de erro e impedir o avanço para a submissão definitiva.

**RF-015 — Tratamento de arquivo ilegível:** quando o sistema não conseguir ler ou extrair as informações necessárias do PDF, deverá impedir o avanço e solicitar que o estudante tente novamente com um arquivo legível.

**RF-016 — Falhas de processamento:** o sistema deverá informar quando não for possível concluir a leitura ou a comparação, sem apresentar o resultado como uma validação bem-sucedida.

**RF-017 — Limites da validação automática:** o sistema deverá distinguir a comparação entre os dados preenchidos e os dados extraídos da verificação da autenticidade do documento. A correspondência entre os dados não deverá ser apresentada, isoladamente, como comprovação de autenticidade do histórico escolar ou de matrícula ativa.

### 4.4. Conferência e submissão

**RF-018 — Tela de conferência:** após a validação bem-sucedida, o sistema deverá apresentar os dados da candidatura para conferência do estudante.

**RF-019 — Submissão definitiva:** o sistema deverá disponibilizar uma ação para a submissão definitiva da candidatura.

**RF-020 — Armazenamento:** após a submissão definitiva, o sistema deverá registrar a candidatura no banco de dados próprio do Monitora UnB.

**RF-021 — Bloqueio de alterações:** após a submissão, o sistema deverá impedir que o estudante altere os dados enviados ou substitua o arquivo da candidatura.

**RF-022 — Prevenção de duplicidade:** o sistema deverá impedir que o mesmo estudante registre candidaturas para mais de uma disciplina no mesmo processo seletivo.

O mecanismo técnico de identificação e prevenção de duplicidade deverá ser definido na implementação.

### 4.5. Cálculo e classificação

**RF-023 — Cálculo do coeficiente:** o sistema deverá calcular automaticamente o coeficiente dos candidatos elegíveis pela fórmula:

`C = 0,6 × IRA + 0,4 × M`

Em que (C) representa o coeficiente, (IRA) representa o Índice de Rendimento Acadêmico e (M) representa o valor numérico da menção na disciplina.

**RF-024 — Classificação geral:** o sistema deverá gerar uma classificação geral dos candidatos elegíveis, em ordem decrescente de coeficiente.

**RF-025 — Classificação por disciplina:** o sistema deverá gerar classificações separadas por disciplina, também em ordem decrescente de coeficiente.

**RF-026 — Dados exibidos:** as classificações administrativas deverão apresentar nome completo, matrícula, e-mail, menção e coeficiente do candidato.

**RF-027 — Atualização das classificações:** as classificações deverão refletir os dados válidos e as decisões administrativas aplicáveis.

### 4.6. Área administrativa

**RF-028 — Consulta de candidaturas:** a presidência deverá poder consultar as candidaturas armazenadas.

**RF-029 — Visualização:** o sistema deverá apresentar as informações necessárias à análise das candidaturas.

**RF-030 — Aprovação:** a presidência deverá poder aprovar uma candidatura.

**RF-031 — Rejeição:** a presidência deverá poder rejeitar uma candidatura.

**RF-032 — Preservação dos dados:** o sistema não deverá permitir que a presidência altere diretamente os dados originalmente submetidos pelo estudante.

**RF-033 — Registro de decisões:** o sistema deverá registrar as decisões administrativas relacionadas às candidaturas.

### 4.7. Vagas e bolsas

**RF-034 — Vagas por disciplina:** o sistema deverá permitir registrar ou confirmar a quantidade de monitores desejada para cada disciplina.

**RF-035 — Bolsas disponíveis:** o sistema deverá permitir registrar ou confirmar a quantidade de bolsas disponível no processo seletivo.

**RF-036 — Sugestão de distribuição:** o sistema deverá sugerir a distribuição de bolsas com base na classificação dos candidatos e nas quantidades disponíveis.

**RF-037 — Confirmação da distribuição:** a distribuição sugerida deverá ser submetida à confirmação da presidência da comissão.

**RF-038 — Autoridade administrativa:** o sistema não deverá conceder bolsas nem finalizar a distribuição sem a confirmação exigida da presidência.

**RF-039 — Distinção de resultados:** o sistema deverá distinguir os candidatos selecionados para monitoria com bolsa, os selecionados para monitoria voluntária e os não selecionados.

**RF-040 — Monitoria voluntária:** o sistema deverá permitir identificar candidatos elegíveis para monitoria voluntária após a distribuição das bolsas, respeitando as vagas disponíveis e as regras aplicáveis.

### 4.8. Encerramento e comunicação

**RF-041 — Configuração de encerramento:** o sistema deverá permitir definir a data e o horário de encerramento das inscrições.

**RF-042 — Encerramento automático:** na data e no horário configurados, o sistema deverá bloquear novas inscrições.

**RF-043 — Resultado com bolsa:** os candidatos selecionados com bolsa deverão receber uma comunicação correspondente.

**RF-044 — Resultado voluntário:** os candidatos selecionados para monitoria voluntária deverão receber uma comunicação correspondente.

**RF-045 — Não seleção:** o sistema deverá prever a comunicação dos resultados aos candidatos não selecionados.

---

## 5. Regras de negócio

**RN-001 — Matrícula ativa:** a matrícula ativa na UnB é um requisito de elegibilidade para a monitoria. O mecanismo de verificação desse requisito ainda deverá ser definido, pois não será realizado pela API acadêmica do projeto conforme o escopo atual.

**RN-002 — Aprovação na disciplina:** o estudante deverá ter sido aprovado na disciplina pretendida.

**RN-003 — Menção mínima:** a menção mínima para elegibilidade será MM.

**RN-004 — IRA mínimo:** não haverá IRA mínimo para candidatura, conforme as regras atualmente informadas.

**RN-005 — Disciplina única:** cada estudante poderá se candidatar a somente uma disciplina por processo seletivo.

**RN-006 — Declaração de bolsa:** o estudante deverá declarar não receber outra bolsa incompatível. O sistema não verificará automaticamente essa declaração.

**RN-007 — Fórmula do coeficiente:** o coeficiente será calculado por:

`C = 0,6 × IRA + 0,4 × M`

**RN-008 — Conversão de menções:**

| Menção | Valor numérico |
|---|---:|
| MM | 3 |
| MS | 4 |
| SS | 5 |

**RN-009 — Ordem de classificação:** os candidatos elegíveis serão ordenados por coeficiente decrescente.

**RN-010 — Desempate:** o critério para desempate entre candidatos com coeficientes iguais deverá ser definido.

**RN-011 — Vagas e bolsas:** a distribuição deverá respeitar as quantidades disponíveis para cada processo seletivo e disciplina.

**RN-012 — Autoridade decisória:** a presidência da comissão terá a decisão final sobre a aprovação e rejeição das candidaturas e a confirmação da distribuição de bolsas e vagas.

**RN-013 — Monitoria voluntária:** candidatos elegíveis sem bolsa poderão ser selecionados para monitoria voluntária, conforme a disponibilidade de vagas e as regras aplicáveis.

**RN-014 — Imutabilidade:** os dados submetidos pelo estudante não poderão ser alterados por ele após a submissão definitiva.

**RN-015 — Correspondência dos dados:** divergências entre o formulário e o PDF deverão impedir o avanço para a submissão definitiva até que o procedimento de correção ou tratamento seja definido.

**RN-016 — Limites da conferência documental:** a correspondência entre o formulário e o PDF não comprova, por si só, a autenticidade do documento nem a situação atual da matrícula.

---

## 6. Requisitos não funcionais

### 6.1. Segurança

**RNF-001:** a área administrativa deverá exigir autenticação.

**RNF-002:** as senhas não deverão ser armazenadas em texto puro.

**RNF-003:** as operações administrativas deverão ser protegidas por controle de acesso.

**RNF-004:** a aplicação deverá utilizar HTTPS em ambiente de produção.

**RNF-005:** os arquivos enviados deverão ser validados quanto ao formato e ao tamanho, além de processados de maneira segura.

**RNF-006:** credenciais e configurações sensíveis deverão permanecer fora do código-fonte versionado.

### 6.2. Privacidade e proteção de dados

**RNF-007:** o sistema deverá coletar e armazenar somente os dados necessários à finalidade do processo seletivo.

**RNF-008:** o tratamento dos dados deverá observar a LGPD e as normas institucionais aplicáveis.

**RNF-009:** o acesso aos dados das candidaturas deverá ser restrito a usuários autorizados.

**RNF-010:** deverão ser definidos os períodos de retenção e os procedimentos de exclusão das inscrições, dos dados associados e dos arquivos enviados.

### 6.3. Confiabilidade

**RNF-011:** as candidaturas submetidas deverão permanecer registradas após o encerramento da sessão ou a reinicialização do sistema.

**RNF-012:** o sistema deverá tratar erros de leitura e processamento sem apresentar validações incorretas.

**RNF-013:** deverá ser definida uma política de backup e recuperação do banco de dados das inscrições.

**RNF-014:** as operações de submissão e registro de resultados deverão preservar a integridade dos dados.

### 6.4. Usabilidade e compatibilidade

**RNF-015:** as mensagens de erro deverão ser claras e indicar o problema encontrado.

**RNF-016:** a interface deverá ser responsiva e compatível com os navegadores modernos definidos como alvo do projeto.

**RNF-017:** a interface deverá observar boas práticas de acessibilidade, incluindo identificação de campos e navegação por teclado.

### 6.5. Manutenibilidade

**RNF-018:** o código deverá separar a interface, a lógica de negócio, o processamento dos arquivos e o acesso ao banco de dados.

**RNF-019:** erros relevantes deverão ser registrados para diagnóstico, sem exposição desnecessária de dados pessoais.

**RNF-020:** a estrutura deverá permitir a manutenção dos critérios de seleção e dos parâmetros de cada processo seletivo.

---

## 7. Dados e integrações

### 7.1. Banco de dados do Monitora UnB

O sistema deverá possuir banco de dados próprio para armazenar as informações necessárias à gestão das candidaturas, incluindo:

- Identificação e contato dos candidatos.
- Disciplina escolhida.
- Dados acadêmicos utilizados na seleção.
- Coeficiente calculado.
- Estado da validação.
- Estado da análise administrativa.
- Decisões da presidência.
- Resultado final.

O modelo de dados, as tabelas, os relacionamentos e a tecnologia de armazenamento deverão ser definidos durante o desenvolvimento.

### 7.2. API acadêmica do projeto

A API acadêmica possui base de dados própria, alimentada por um scraper que coleta informações do SIGAA.

A API disponibilizará os dados institucionais contemplados em seu escopo, como informações sobre disciplinas, códigos e professores responsáveis.

A API não será utilizada para consultar informações pessoais dos estudantes para validação das candidaturas. A leitura do histórico escolar e a comparação com os dados informados serão responsabilidades do próprio Monitora UnB.

### 7.3. Histórico em PDF

O sistema deverá processar o histórico escolar enviado para extrair as informações necessárias à conferência.

Ainda deverá ser definido se o PDF original será armazenado após o processamento ou se será mantido apenas durante a validação.

---

## 8. Fluxos principais

### 8.1. Inscrição do estudante

1. O estudante acessa a página inicial.
2. Seleciona a opção de inscrição.
3. Preenche os dados solicitados.
4. Seleciona uma única disciplina.
5. Envia o histórico escolar em PDF.
6. Registra a declaração sobre bolsas incompatíveis.
7. O sistema verifica o preenchimento dos campos.
8. O sistema extrai os dados do PDF.
9. O sistema compara os dados extraídos com os dados informados.
10. Se o arquivo for ilegível ou houver divergências impeditivas, o sistema informa o erro e interrompe o fluxo.
11. Se a comparação for bem-sucedida, o sistema apresenta os dados para conferência.
12. O estudante poderá baixar o comprovante e submeter a candidatura.
13. O sistema armazena a candidatura.
14. A candidatura fica disponível para análise administrativa.

### 8.2. Análise e seleção

1. A presidência acessa a área administrativa.
2. Consulta as candidaturas.
3. Analisa as informações submetidas e o estado da validação.
4. Aprova ou rejeita as candidaturas.
5. O sistema calcula os coeficientes dos candidatos elegíveis.
6. O sistema gera as classificações gerais e por disciplina.
7. A presidência informa ou confirma as vagas e bolsas disponíveis.
8. O sistema sugere a distribuição.
9. A presidência confirma a distribuição.
10. O sistema registra os resultados finais.

### 8.3. Encerramento

1. O sistema atinge a data e o horário configurados.
2. Novas inscrições são bloqueadas.
3. O sistema verifica se os resultados estão confirmados.

---

## 9. Restrições e premissas

### 9.1. Restrições

- A aplicação utilizará a API acadêmica do projeto para os dados institucionais previstos em seu escopo.
- A API não será responsável por verificar dados pessoais dos candidatos.
- O banco de dados das inscrições ainda deverá ser desenvolvido.
- A presidência será o único perfil administrativo previsto inicialmente.
- Os dados não poderão ser alterados pelo estudante após a submissão definitiva.
- O sistema não verificará automaticamente a existência de outras bolsas incompatíveis.
- A distribuição final das bolsas dependerá da confirmação da presidência.
- A comparação entre formulário e PDF não será tratada como comprovação automática de autenticidade documental.

### 9.2. Premissas

- A equipe possui autorização para realizar a coleta institucional prevista pelo scraper.
- Os históricos escolares enviados poderão ser processados pelo backend em Python, desde que estejam em formato legível.
- A comissão disponibilizará as quantidades de vagas e bolsas necessárias à seleção.

---

## 10. Critérios gerais de aceitação

O sistema deverá demonstrar que:

1. O estudante consegue preencher e enviar uma candidatura.
2. O sistema extrai as informações necessárias de um PDF legível.
3. O sistema impede o avanço quando não consegue ler o documento.
4. O sistema identifica divergências entre os dados preenchidos e os dados extraídos.
5. O sistema não utiliza a API acadêmica para verificar dados pessoais dos candidatos.
6. A submissão definitiva registra a candidatura no banco de dados próprio.
7. O sistema impede candidaturas para mais de uma disciplina pelo mesmo estudante.
8. O coeficiente é calculado corretamente.
9. As classificações gerais e por disciplina são geradas corretamente.
10. A presidência consegue aprovar ou rejeitar candidaturas sem editar os dados originais.
11. O sistema sugere a distribuição de bolsas e permite sua confirmação administrativa.
12. Os resultados distinguem monitoria com bolsa, monitoria voluntária e não seleção.
13. O sistema bloqueia novas inscrições no encerramento configurado.
14. O acesso aos dados e às funções administrativas é protegido.

---

## 11. Pendências para validação

**P-001 — Tecnologia do banco:** definir a tecnologia do banco de dados das inscrições.

**P-002 — Duplicidade:** definir como identificar o mesmo estudante em tentativas diferentes.

**P-003 — Desempate:** definir critérios para candidatos com coeficientes iguais.

**P-004 — Distribuição de bolsas:** definir como combinar a classificação geral e os rankings por disciplina.

**P-005 — Quantidade de monitores:** definir como os professores informarão a quantidade desejada por disciplina.

**P-006 — Justificativas de rejeição:** definir se a presidência deverá informar uma justificativa e se ela será comunicada ao estudante.

**P-007 — Correção de divergências:** definir como o estudante poderá corrigir dados após uma tentativa bloqueada.

**P-008 — Matrícula ativa e autenticidade documental:** definir como serão verificadas a situação atual da matrícula e a autenticidade do histórico, se esses controles forem exigidos no processo. A API acadêmica do projeto não será utilizada para consultar dados pessoais dos candidatos.

**P-009 — Atualização da base da API:** definir periodicidade, mecanismo e responsáveis pela atualização dos dados institucionais.

**P-010 — Retenção:** definir por quanto tempo serão mantidos os registros das inscrições e os arquivos enviados.

**P-011 — Encerramento:** definir o comportamento quando houver candidaturas pendentes ou resultados não confirmados na data de encerramento.

**P-012 — PDF:** decidir se o histórico original será armazenado após a validação.

**P-013 — Conta administrativa:** definir como a conta da presidência será criada e como será feita a recuperação de senha.

**P-014 — Formato das menções:** confirmar os formatos de menção presentes nos históricos e os critérios de extração.

**P-015 — Regras institucionais:** confirmar as regras oficiais de elegibilidade, bolsas incompatíveis, monitoria voluntária e distribuição de vagas.

---

## 12. Considerações finais

Esta versão descreve o funcionamento planejado do Monitora UnB com base nas informações disponíveis durante a elaboração do documento.

Os requisitos deverão ser revisados pela equipe e validados com os responsáveis pelo processo seletivo. As pendências deverão ser resolvidas ou formalmente registradas antes da implementação das funcionalidades correspondentes.

O modelo do banco de dados, os contratos da API, os protótipos de interface e os casos de teste deverão ser desenvolvidos em conformidade com os requisitos aprovados.
