# Documento de Visão — Monitora UnB

## 1. Introdução

Este documento define a visão do produto **Monitora UnB**: o problema que será solucionado, seus usuários e as principais funcionalidades do sistema. Ele serve como referência para o desenvolvimento do projeto, mantendo uma visão geral do produto antes do detalhamento dos requisitos e das decisões técnicas.

O projeto é desenvolvido como parte da disciplina de **Métodos de Desenvolvimento de Software (MDS)** da FCTE/UnB.

---

## 2. Posicionamento

### 2.1 Declaração do problema

| Campo | Descrição |
|---|---|
| **O problema de** | processo manual e sujeito a erros nas inscrições e na seleção de monitores |
| **Afeta** | estudantes, professores e responsáveis pelas comissões de monitoria da UnB |
| **E o impacto disso é** | demora na validação dos históricos, erros nas informações e necessidade de tratamento manual dos dados dos candidatos |
| **Uma solução de sucesso seria** | um sistema que automatize a inscrição, valide as informações acadêmicas e organize os dados necessários para a seleção |

### 2.2 Declaração de posicionamento do produto

Para **estudantes e responsáveis pelas monitorias da UnB** que precisam realizar e administrar o processo de inscrição de monitores, o **Monitora UnB** é um sistema que automatiza a inscrição e a validação dos candidatos, utilizando seus dados acadêmicos para auxiliar na classificação.

Diferente do processo manual, o sistema permite o envio e validação do histórico acadêmico, reconhece disciplinas equivalentes, calcula o coeficiente dos candidatos e disponibiliza os dados necessários para a seleção.

---

## 3. Descrição dos stakeholders e usuários

### 3.1 Resumo dos stakeholders

| Stakeholder | Interesse no projeto |
|---|---|
| **Equipe do projeto** | Desenvolver e entregar o sistema dentro do prazo da disciplina, seguindo as práticas de MDS. |
| **Professor(a) da disciplina** | Avaliar o desenvolvimento, a documentação e o produto entregue. |
| **Estudantes da UnB** | Realizar inscrições para vagas de monitoria de forma simples e rápida. |
| **Professores** | Participar e acompanhar o processo de monitoria. |
| **Professor responsável pela comissão** | Controlar as informações dos candidatos e o processo de classificação. |
| **Comissão de monitoria** | Utilizar as informações dos candidatos para realizar a seleção. |

### 3.2 Resumo dos usuários

| Usuário | Descrição | Uso esperado |
|---|---|---|
| **Aluno** | Estudante interessado em uma vaga de monitoria. | Enviar histórico, selecionar disciplina, confirmar inscrição e receber o resultado. |
| **Professor** | Docente relacionado ao processo de monitoria. | Acompanhar o processo de seleção conforme suas responsabilidades. |
| **Responsável pela comissão** | Professor responsável pelo controle da seleção. | Acessar os dados necessários para classificação e seleção dos candidatos. |

### 3.3 Ambiente do usuário

Os alunos poderão acessar o sistema por meio de um navegador, utilizando computadores ou dispositivos móveis.

Os responsáveis pela monitoria utilizarão o sistema para consultar e organizar as informações dos candidatos durante o processo de seleção.

### 3.4 Necessidades dos stakeholders e usuários

| Necessidade | Prioridade | Problema atual | Solução proposta |
|---|---|---|---|
| Realizar inscrição de forma simples | Alta | Processo sujeito a erros e etapas manuais | Formulário de inscrição online |
| Validar aprovação na disciplina | Alta | Conferência manual do histórico | Validação automática do histórico |
| Reconhecer disciplinas equivalentes | Alta | Códigos diferentes podem dificultar a validação | Cadastro e consulta de equivalências |
| Organizar dados dos candidatos | Alta | Informações precisam ser tratadas manualmente | Extração e organização automática |
| Classificar candidatos | Alta | Necessidade de cálculo e organização dos dados | Cálculo do coeficiente e envio para planilha |
| Informar o resultado | Média | Comunicação depende de processos manuais | Envio automático por e-mail |

---

## 4. Visão geral do produto

### 4.1 Perspectiva do produto

O **Monitora UnB** é um sistema desenvolvido para automatizar o processo de inscrição e auxiliar na seleção de monitores.

O sistema recebe o histórico acadêmico do aluno, valida suas informações e verifica sua aprovação na disciplina escolhida ou em disciplinas equivalentes.

Após a inscrição, os dados acadêmicos necessários são utilizados no cálculo do coeficiente e encaminhados para a etapa de classificação dos candidatos.

### 4.2 Resumo de funcionalidades

| Funcionalidade | Benefício para o usuário |
|---|---|
| **Envio do histórico em PDF** | Evita o preenchimento manual das informações acadêmicas. |
| **Seleção da disciplina** | Permite indicar a monitoria desejada. |
| **Validação acadêmica** | Verifica se o aluno possui aprovação na disciplina. |
| **Reconhecimento de equivalências** | Permite validar disciplinas equivalentes reconhecidas pela UnB. |
| **Confirmação dos dados** | Permite ao aluno verificar as informações antes da inscrição. |
| **Cálculo do coeficiente** | Auxilia na classificação dos candidatos. |
| **Exportação dos dados para Excel** | Facilita o controle e a classificação pela comissão. |
| **Controle de acesso** | Restringe informações de seleção aos responsáveis. |
| **Envio do resultado por e-mail** | Informa o aluno sobre o resultado da seleção. |

### 4.3 Hipóteses e dependências

- O histórico acadêmico enviado pelo aluno estará disponível em formato PDF e conterá informações suficientes para a validação.
- A base acadêmica da UnB estará disponível para a integração prevista pelo sistema.
- A estrutura das informações acadêmicas necessárias para a validação permanecerá compatível com o sistema.
- A planilha utilizada pela comissão estará disponível para receber os dados necessários à classificação.

---

## 5. Restrições

- O projeto possui prazo definido pelo calendário da disciplina de MDS.
- A equipe possui dedicação parcial ao projeto, paralelamente às demais atividades acadêmicas.
- O sistema depende da disponibilidade das informações acadêmicas necessárias para realizar as validações.
- O tratamento de dados pessoais e acadêmicos deve respeitar a **LGPD**.
- O acesso aos dados utilizados na seleção deve ser restrito aos responsáveis pelo processo.

---

## 6. Faixas de qualidade

| Atributo | Faixa esperada |
|---|---|
| **Desempenho** | A validação do histórico deve ocorrer em poucos segundos, sem prejudicar a experiência do usuário. |
| **Segurança** | Dados pessoais e acadêmicos não devem ser expostos indevidamente. |
| **Usabilidade** | O processo de inscrição deve ser simples e não exigir treinamento. |
| **Confiabilidade** | O sistema deve informar claramente quando uma inscrição foi validada ou quando ocorreu algum erro. |
| **Privacidade** | Os dados dos alunos devem ser tratados de acordo com a LGPD. |
| **Auditoria** | As inscrições devem ser registradas com informações como aluno, data e disciplina. |

---

## 7. Precedência e priorização

| Prioridade | Itens |
|---|---|
| **Essencial (must have)** | Envio do histórico, seleção da disciplina, validação da aprovação, reconhecimento de equivalências, confirmação da inscrição e registro do resultado. |
| **Essencial (must have)** | Integração com a base acadêmica e organização dos dados para a seleção. |
| **Importante (should have)** | Cálculo do coeficiente, envio dos dados para a planilha de classificação e controle de acesso. |
| **Importante (should have)** | Envio automático do resultado da seleção por e-mail. |
| **Fora de escopo (won't have, por ora)** | Alteração de notas, menções ou informações oficiais do histórico acadêmico do aluno. |
| **Fora de escopo (won't have, por ora)** | Substituição dos sistemas acadêmicos oficiais da UnB. |