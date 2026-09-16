# Documento de Visão — Monitora UnB

## 1. Identificação do Projeto

**Nome:** Monitora UnB  
**Disciplina:** Métodos de Desenvolvimento de Software (MDS)  
**Instituição:** Universidade de Brasília (UnB) — FCTE

O Monitora UnB é um sistema desenvolvido para automatizar o processo de inscrição e auxiliar na seleção de alunos para monitorias da Universidade de Brasília.

---

## 2. Posicionamento

### 2.1 Problema

| Aspecto | Descrição |
|---|---|
| **Problema** | Processo de inscrição e seleção de monitores com etapas manuais e sujeito a erros. |
| **Afeta** | Estudantes, professores e responsáveis pelas monitorias. |
| **Impacto** | Demora na validação dos históricos, erros nas informações e trabalho manual na organização e classificação dos candidatos. |
| **Solução** | Automatizar a inscrição, validação acadêmica e organização das informações dos candidatos. |

### 2.2 Visão do Produto

Para **estudantes e responsáveis pelas monitorias da UnB**, o **Monitora UnB** é um sistema que automatiza a inscrição e auxilia no processo de seleção de monitores.

O sistema permite que o aluno envie seu histórico acadêmico, selecione uma disciplina e tenha sua aprovação validada automaticamente. Após a inscrição, os dados acadêmicos são utilizados para o cálculo do coeficiente e para a organização das informações necessárias à classificação dos candidatos.

---

## 3. Usuários e Stakeholders

| Usuário/Stakeholder | Interesse |
|---|---|
| **Aluno** | Realizar a inscrição de forma simples e acompanhar o resultado. |
| **Professor** | Participar do processo de monitoria e acompanhar os candidatos. |
| **Professor responsável pela comissão** | Controlar os dados e o processo de classificação. |
| **Comissão de monitoria** | Realizar a seleção dos monitores. |
| **Equipe do projeto** | Desenvolver e entregar o sistema dentro do prazo da disciplina. |

---

## 4. Necessidades dos Usuários

| Necessidade | Prioridade | Solução |
|---|---|---|
| Realizar inscrição de forma simples | Alta | Formulário de inscrição online |
| Verificar aprovação na disciplina | Alta | Validação automática do histórico |
| Considerar disciplinas equivalentes | Alta | Consulta às equivalências reconhecidas |
| Reduzir trabalho manual | Alta | Extração e organização automática dos dados |
| Classificar os candidatos | Alta | Cálculo do coeficiente e organização dos dados |
| Receber o resultado | Média | Envio automático por e-mail |

---

## 5. Visão Geral do Produto

### 5.1 Principais funcionalidades

- Envio do histórico acadêmico em PDF.
- Seleção da disciplina de monitoria.
- Validação da aprovação na disciplina.
- Reconhecimento de disciplinas equivalentes.
- Extração das informações acadêmicas do histórico.
- Confirmação dos dados antes da inscrição.
- Registro da inscrição.
- Cálculo do coeficiente dos candidatos.
- Envio das informações para a planilha utilizada na classificação.
- Controle de acesso aos dados da seleção.
- Envio do resultado da seleção por e-mail.

### 5.2 Fluxo principal

1. O aluno deve se cadastrar com o e-mail vinculado ao SIGAA.
2. O aluno envia seu histórico acadêmico.
3. Seleciona a disciplina para a qual deseja se candidatar.
4. O sistema valida seus dados e verifica a aprovação na disciplina ou em uma equivalente.
5. O sistema apresenta os dados encontrados para confirmação.
6. O aluno confirma a inscrição.
7. Os dados são utilizados no cálculo do coeficiente.
8. As informações necessárias são disponibilizadas para a classificação.
9. Após o processamento, as informações serão organizadas em uma planilha que será enviada por e-mail para a comissão. 
10. Após a seleção, o resultado é enviado ao aluno por e-mail.

---

## 6. Integrações

O sistema deverá se relacionar com os seguintes recursos:

- **Base acadêmica da UnB:** utilizada para validar as informações acadêmicas do aluno (via plugin).
- **Planilha Excel:** utilizada pela comissão para armazenar e controlar dados.
- **Serviço de e-mail:** utilizado para comunicar o resultado da seleção para professores e alunos.

---

## 7. Restrições e Qualidade

- O projeto deve ser desenvolvido dentro do prazo estabelecido pela disciplina de MDS.
- O sistema deve possuir uma interface simples e acessível aos estudantes.
- A validação das informações deve ocorrer em poucos segundos.
- Dados pessoais e acadêmicos devem ser protegidos de acordo com a LGPD.
- O acesso às informações utilizadas na seleção deve ser restrito aos responsáveis.
- As inscrições devem possuir registro para fins de auditoria.

---

## 8. Priorização

| Prioridade | Funcionalidades |
|---|---|
| **Essencial (Must Have)** | Inscrição, envio do histórico, seleção da disciplina, validação da aprovação, reconhecimento de equivalências e confirmação dos dados. |
| **Essencial (Must Have)** | Registro das inscrições e integração necessária para validação acadêmica. |
| **Importante (Should Have)** | Cálculo do coeficiente e organização dos dados para classificação. |
| **Importante (Should Have)** | Integração com planilha e envio do resultado por e-mail. |
| **Fora de escopo** | Alteração de notas, menções ou informações oficiais do histórico acadêmico. |
