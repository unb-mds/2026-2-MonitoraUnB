# Documento de Visão — Monitora UnB

| Campo | Informação |
|---|---|
| **Projeto** | Monitora UnB |
| **Disciplina** | Métodos de Desenvolvimento de Software (MDS) |
| **Instituição** | Universidade de Brasília (UnB) — FCTE |
| **Cliente / Patrocinador** | John Lenon (Coordenador do curso de Engenharia de Software) |
| **Elaborado por** | Grupo 11 |
| **Data** | 28/09/2026 |
| **Versão do documento** | 1.0 |

---

## 1. Identificação do Projeto

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

### 2.2 Visão do Produto (Elevator Pitch)

> **Observação:** o DRS ainda registra o tipo de produto como "Plug-in ou um site (a definir)" (seção 6). Como o restante da Visão (item 6 — Integrações) só menciona plugin para a integração com a base acadêmica, assumi abaixo que o produto principal é um **sistema web (site)**. **Confirmem essa decisão com a equipe/PO e alinhem os dois documentos.**

| Elemento | Conteúdo |
|---|---|
| **Para** | Estudantes e responsáveis pelas monitorias da UnB (docentes, comissão de monitoria) |
| **Que** | Enfrentam um processo de inscrição e seleção manual, lento e sujeito a erros, sem validação automática dos dados acadêmicos |
| **O Monitora UnB é** | Um sistema web |
| **Que fornece** | Inscrição on-line, validação automática do histórico escolar, cálculo automático do coeficiente e comunicação automática do resultado |
| **Diferente de** | Formulários genéricos de inscrição (ex.: Microsoft Forms), que não validam dados nem calculam classificação |
| **Nosso produto** | Elimina a conferência manual, reduz erros de digitação/dados falsos e agiliza a divulgação do resultado |

### 2.3 Objetivos de Negócio

| ID | Objetivo |
|---|---|
| O1 | Facilitar a inscrição dos estudantes da UnB na monitoria semestral. |
| O2 | Tornar a divisão de bolsas de monitoria mais igualitária, com critérios objetivos. |
| O3 | Evitar o preenchimento de informações pessoais falsas ou divergentes do histórico. |
| O4 | Reduzir as horas de trabalho manual na verificação das inscrições. |

*(objetivos consistentes com a seção 2 do DRS — mantidos em alto nível aqui; as métricas de sucesso detalhadas ficam no DRS.)*

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

### 5.2 Jornada do Usuário

| Etapa | O que acontece |
|---|---|
| Cadastro | Aluno acessa o sistema com o e-mail vinculado ao SIGAA |
| Envio de documentos | Aluno envia o histórico acadêmico em PDF |
| Seleção | Aluno escolhe a disciplina para a qual deseja se candidatar |
| Validação | Sistema verifica a aprovação na disciplina (ou equivalente) contra o histórico |
| Confirmação | Sistema apresenta os dados encontrados e o aluno confirma a inscrição |
| Classificação | Dados são usados no cálculo do coeficiente; planilha de classificação é organizada |
| Resultado | Após autorização da comissão, resultado é enviado ao aluno por e-mail |

**Fluxo detalhado (passo a passo):**
1. O aluno deve se cadastrar com o e-mail vinculado ao SIGAA.
2. O aluno envia seu histórico acadêmico.
3. Seleciona a disciplina para a qual deseja se candidatar.
4. O sistema valida seus dados e verifica a aprovação na disciplina ou em uma equivalente.
5. O sistema apresenta os dados encontrados para confirmação.
6. O aluno confirma a inscrição.
7. Os dados são utilizados no cálculo do coeficiente.
8. As informações necessárias são disponibilizadas para a classificação.
9. As informações são organizadas em uma planilha enviada por e-mail para a comissão.
10. Após a seleção, o resultado é enviado ao aluno por e-mail.

---

## 6. Integrações

O sistema deverá se relacionar com os seguintes recursos:

- **Base acadêmica da UnB:** utilizada para validar as informações acadêmicas do aluno (via plugin).
- **Planilha Excel:** utilizada pela comissão para armazenar e controlar dados.
- **Serviço de e-mail:** utilizado para comunicar o resultado da seleção para professores e alunos.

---

## 7. Restrições, Qualidade e Requisitos Não Funcionais

- O projeto deve ser desenvolvido dentro do prazo estabelecido pela disciplina de MDS.
- O sistema deve possuir uma interface simples e acessível aos estudantes.
- A validação das informações deve ocorrer em poucos segundos.
- Dados pessoais e acadêmicos devem ser protegidos de acordo com a LGPD.
- O acesso às informações utilizadas na seleção deve ser restrito aos responsáveis.
- As inscrições devem possuir registro para fins de auditoria.

> Os Requisitos Não Funcionais detalhados (RNF-01 a RNF-09, com metas numéricas de desempenho, disponibilidade, escalabilidade etc.) estão no DRS, seção 9 — não duplicados aqui para evitar desalinhamento entre os dois documentos.

---

## 8. Priorização

| Prioridade | Funcionalidades |
|---|---|
| **Essencial (Must Have)** | Inscrição, envio do histórico, seleção da disciplina, validação da aprovação, reconhecimento de equivalências e confirmação dos dados. |
| **Essencial (Must Have)** | Registro das inscrições e integração necessária para validação acadêmica. |
| **Importante (Should Have)** | Cálculo do coeficiente e organização dos dados para classificação. |
| **Importante (Should Have)** | Integração com planilha e envio do resultado por e-mail. |

---

## 9. Fora do Escopo

- Alteração de notas, menções ou informações oficiais do histórico acadêmico.
- Nesta primeira entrega (conforme DRS, seção 3.2): interação real entre front-end e back-end, integração com a API institucional e banco de dados/plug-in — a entrega atual cobre a ideia do front-end (parcialmente funcional) e a leitura do arquivo PDF.

---

## 10. Dimensionamento

Estimativa relativa (T-shirt size) das principais funcionalidades, para orientar o planejamento das sprints:

| Funcionalidade | Porte estimado | Observação |
|---|---|---|
| Formulário de inscrição | P | Tela de cadastro simples |
| Upload e leitura do histórico em PDF | G | Extração de dados de PDF é o maior risco/esforço técnico |
| Validação cruzada de dados e bloqueio de inscrição inválida | M | Depende da qualidade da extração do PDF |
| Cálculo do coeficiente e ranqueamento | P | Fórmula simples e já definida |
| Autorização da secretaria para liberar resultado | P | Etapa/tela de aprovação |
| Envio automático de e-mail de resultado | M | Depende de serviço de e-mail configurado |

> Estimativas ilustrativas (P/M/G) — recomenda-se reestimar com a equipe (ex.: Planning Poker) durante o refinamento do backlog.

---

## 11. Planejamento (Plano de Releases)

| Release | Escopo sugerido |
|---|---|
| **Release 1 (MVP)** | Ideia de front-end funcional; upload e leitura do histórico em PDF |
| **Release 2** | Validação cruzada de dados, bloqueio de inscrição inválida, mensagens de erro |
| **Release 3** | Cálculo do coeficiente, ranqueamento e controle do período de inscrição |
| **Release 4** *(fora do escopo da entrega atual da disciplina)* | Liberação de resultado pela secretaria e envio automático de e-mails — dependem da integração front-end/back-end e de banco de dados, hoje fora do escopo (seção 9) |

---

## 12. Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Atraso na integração com API externa | Média | Alto | Atenção às datas de entrega |
| Atraso da comunicação front-end com back-end | Média | Alto | Atenção às datas de entrega |
| Incompatibilidade de agendas para realização de sprints | Baixa | Médio | Melhora na comunicação |
| Baixa qualidade na extração automática de dados do PDF do histórico | Média | Alto | Testar com históricos reais variados; ter fluxo de correção manual como fallback |

*(as três primeiras linhas replicam a matriz de riscos do DRS, seção 12; a última é uma sugestão de risco específico da Visão — validar com a equipe.)*

---

## 13. Premissas

- Todo aluno candidato possui e-mail institucional válido vinculado ao SIGAA.
- O histórico acadêmico exportado pelo SIGAA está em formato PDF com texto extraível (não é um documento escaneado/imagem).
- A fórmula do coeficiente (IRA × 0,6 + Menção × 0,4) já está validada e aprovada pela coordenação.
- A comissão/secretaria terá um canal para autorizar a divulgação dos resultados antes do envio dos e-mails.

---

## 14. Mapa de Tecnologias

| Camada | Tecnologia proposta |
|---|---|
| Front-end | HTML, CSS, TypeScript |
| Back-end | Python, FastAPI |
| Banco de dados | A definir |
| Infraestrutura | Docker |
| Controle de versão | Git, GitHub, GitLab |
| Integração/Entrega Contínua | GitHub Actions |

*(replicado do DRS, seção 10, para manter a Visão autocontida.)*

---

## 15. Definition of Ready (DOR) e Definition of Done (DOD)

**DOR (pronta para entrar na sprint):**
- User story escrita no formato "Como... eu quero... para que..."
- Critérios de aceitação definidos
- Dependências e integrações identificadas
- Estimativa de esforço feita pelo time

**DOD (pronta para ser considerada concluída):**
- Código revisado (code review) pelo time
- Funcionalidade testada (manual ou automatizada)
- Critérios de aceitação validados pelo Product Owner
- Sem bugs críticos conhecidos em aberto

*(modelo padrão sugerido — ajustar com os critérios que o grupo/PO definir.)*

---

## 16. Backlog Futuro

- Integração completa entre front-end e back-end via API.
- Persistência em banco de dados (definição do SGBD).
- Reconhecimento automático de disciplinas equivalentes (mencionado na Visão, ainda não detalhado no DRS).
- Painel/dashboard para a comissão de monitoria acompanhar candidatos.

---

## 17. Action List

- Decidir e alinhar entre os dois documentos se o produto é "site" ou "plugin" (hoje o DRS deixa "a definir" e a Visão assume "site").
- Validar com a coordenação a fórmula do coeficiente e o formato oficial do histórico (PDF exportado do SIGAA).
- Confirmar com o PO se os RNFs detalhados devem ser resumidos aqui na Visão ou permanecer só no DRS.
- Conferir a numeração dos RNFs no DRS (o próprio documento já sinaliza que RNF-07 a 09 estavam numerados como "RF-" por engano).
