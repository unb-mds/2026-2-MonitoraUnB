# Documento de Requisitos de Software (DRS)

**Metodologia Ágil — Scrum**

| Campo | Informação |
|---|---|
| **Projeto** | Monitora UnB |
| **Cliente / Patrocinador** | John Lenon (Coordenador do curso de Engenharia de Software da Universidade de Brasília) |
| **Elaborado por** | Ana Beatriz Nogueira Guerra, Iuri Capanema Souza Koboldt, João Áquila, Maria Eduarda Macedo, Pablo Antônio Martins de Sousa, Vitor Piau Morhy, Vinicius Eugenio Montalvão Silva — Estudantes de Engenharia de Software |
| **Data** | 28/09/2026 |
| **Versão do documento** | 1.0 |

---

## 1. Sumário Executivo

O MonitoraUnB é um sistema web que automatiza o processo de inscrição para vagas de monitoria na UnB. Ele valida automaticamente os dados do candidato contra seu histórico escolar (PDF), calcula o coeficiente de classificação (IRA × 0,6 + Menção × 0,4) e, após autorização da secretaria, notifica cada aluno por e-mail sobre o resultado, assim eliminando a conferência manual e reduzindo erros no processo seletivo.

---

## 2. Objetivos do Projeto

| Objetivo | Descrição | Métrica de Sucesso |
|---|---|---|
| **O1** | Facilitar a inscrição dos estudantes da Universidade de Brasília na monitoria semestral. | Aumento na quantidade de monitores em mais disciplinas |
| **O2** | Tornar a divisão de bolsas de monitoria mais igualitária. | Feedback dos estudantes |
| **O3** | Evitar o preenchimento de informações pessoais falsas. | Informações dadas batendo com os históricos fornecidos |
| **O4** | Diminuir as horas de trabalho manual para verificação das informações de cada inscrição. | Menor período de apuração de cada inscrição e menos erros |

---

## 3. Escopo do Projeto

### 3.1 Dentro do escopo
- Ideia do Front-end / ele já estar parcialmente funcionando
- Leitura do arquivo PDF

### 3.2 Fora do escopo
- Interação do Front-end com o Back-end
- Integração com a API
- Banco de dados / Plug-in

---

## 4. Stakeholders

| Nome/Papel | Responsabilidade | Nível de envolvimento |
|---|---|---|
| Coordenador do curso de Engenharia de Software | Prioriza o backlog, aprova entregas | Alto |
| Scrum Masters | Facilita o processo ágil, remove impedimentos | Alto |
| Grupo 11 | Constrói e testa o incremento | Alto |
| Docentes e Discentes da Universidade de Brasília | Fornece feedback, valida usabilidade | Médio |

---

## 5. Personas

### Persona 1 — Ricardo
- **Perfil:** 50 anos, Docente
- **Objetivo ao usar o sistema:** Facilidade de controle das inscrições dos possíveis monitores e rapidez na escolha dos mesmos
- **Frustração atual:** Necessidade de escrever a lista de inscrições a mão e maior dificuldade no controle de quem efetiva ou cancela a inscrição.

### Persona 2 — Pedro
- **Perfil:** 20 anos, discente
- **Objetivo:** Cadastrar-se na monitoria e poder ter o resultado mais rapidamente
- **Frustração atual:** O aluno encontra dificuldades ao preencher manualmente o formulário, já que algum erro de digitação pode gerar cancelamento da inscrição; além da demora de receber o resultado da seleção.

---

## 6. Visão Geral do Produto (Product Vision)

- **Para:** Docentes e discentes da Universidade de Brasília
- **Que:** Enfrentam dificuldades para o cadastro de seus dados
- **Nosso produto é:** Um Plug-in ou um site (a definir)
- **Que fornece:** Mais conveniência na inscrição e processamento do cadastro de monitoria
- **Diferente de:** Formulário da Microsoft
- **Nosso produto:** Oferece simplicidade e rapidez para aqueles que precisam realizar o processo

---

## 7. Product Backlog

- **Épicos:** Envio, leitura e processamento do arquivo, geração da planilha dos candidatos, criação do e-mail com o resultado.
- **User Stories:** cada épico quebrado em pedaços pequenos, um por comportamento do usuário. Teste: a story cabe em uma sprint? Se não, quebre mais.

### 7.1 Épicos

| ID | Épico |
|---|---|
| EP-01 | Inscrição do candidato |
| EP-02 | Validação de dados via histórico |
| EP-03 | Cálculo e ranqueamento de coeficiente |
| EP-04 | Notificação de resultado |

### 7.2 User Stories (formato padrão)

| ID | User Story | Épico |
|---|---|---|
| US-01 | Como aluno candidato, eu quero preencher um formulário com a matéria desejada, meu nome, matrícula, IRA, menção e e-mail, para que minha inscrição seja registrada. | EP-01 |
| US-02 | Como aluno candidato, eu quero fazer upload do meu histórico em PDF, para que o sistema confirme que meus dados estão corretos. | EP-02 |
| US-03 | Como aluno candidato, eu quero ser avisado caso meus dados estejam incorretos ou eu nunca tenha cursado a disciplina, para que eu possa corrigir e tentar novamente. | EP-02 |
| US-04 | Como professor eu quero ser avisado caso os dados do aluno candidato à monitoria estejam incorretos ou caso ele nunca tenha cursado a disciplina, para que eu possa efetivar as inscrições de alunos que atendem esse pré-requisito. | EP-02 |
| US-05 | Como aluno candidato, eu quero receber um e-mail informando se fui aprovado ou não, para que eu saiba o resultado do processo. | EP-04 |

---

## 8. Requisitos Funcionais (RF)

| ID | Requisito | Descrição |
|---|---|---|
| RF-01 | Formulário de inscrição | O sistema deve permitir que o aluno preencha: matéria, matrícula, IRA e menção na disciplina. |
| RF-02 | Upload do histórico | O sistema deve permitir upload de arquivo em formato PDF contendo o histórico escolar do aluno. |
| RF-03 | Extração de dados do histórico | O sistema deve extrair do PDF as informações necessárias para validação (disciplinas cursadas, menções, matrícula, nome). |
| RF-04 | Validação cruzada de dados | O sistema deve comparar os dados preenchidos manualmente pelo aluno com os dados extraídos do histórico oficial. |
| RF-05 | Bloqueio de inscrição inválida | O sistema deve impedir o registro da inscrição caso haja divergência entre os dados informados e o histórico, ou caso o aluno nunca tenha cursado a disciplina. |
| RF-06 | Exibição de mensagem de erro | O sistema deve exibir um aviso claro ao aluno informando o motivo da falha na inscrição. |
| RF-07 | Registro de inscrição válida | O sistema deve registrar toda inscrição bem-sucedida. |
| RF-08 | Cálculo automático do coeficiente | O sistema deve calcular o coeficiente de cada candidato usando a fórmula (IRA × 0,6 + MENÇÃO × 0,4). |
| RF-09 | Ordenação de ranking | O sistema deve ordenar automaticamente a planilha de candidatos em ordem decrescente de coeficiente. |
| RF-10 | Controle do período de inscrição | O sistema deve permitir inscrições apenas dentro do período configurado (data de início e fim). |
| RF-11 | Liberação de resultado pela secretaria | O sistema deve permitir que a secretaria autorize a divulgação dos resultados antes do envio dos e-mails. |
| RF-12 | Envio automático de e-mail de resultado | O sistema deve enviar automaticamente um e-mail a cada candidato informando se foi aprovado ou reprovado, após autorização da secretaria. |

---

## 9. Requisitos Não-Funcionais (RNF)

| ID | Categoria | Requisito |
|---|---|---|
| RNF-01 | Usabilidade | O formulário de inscrição deve ser preenchido por um aluno sem instruções externas, em no máximo 5 minutos. |
| RNF-02 | Segurança | Dados pessoais acadêmicos dos alunos (histórico, matrícula) devem ser armazenados e transmitidos de forma protegida, em conformidade com a LGPD. |
| RNF-03 | Desempenho | A validação do histórico em PDF deve ser processada em até 120 segundos por submissão. |
| RNF-04 | Disponibilidade | O sistema deve estar disponível durante todo o período de inscrições, com disponibilidade mínima de 99%. |
| RNF-05 | Escalabilidade | O sistema deve suportar no mínimo 60 usuários simultâneos. |
| RNF-06 | Compatibilidade | O sistema deve funcionar nos principais navegadores utilizados pelos alunos da UnB. |
| RNF-07 | Confiabilidade | O cálculo do coeficiente deve ter 100% de precisão em relação à fórmula definida, sem arredondamentos incorretos. |
| RNF-08 | Auditabilidade | Toda tentativa de inscrição (bem-sucedida ou não) deve ficar registrada em log, para fins de auditoria da secretaria. |
| RNF-09 | Formato de arquivo | O sistema deve aceitar apenas arquivos PDF para upload de histórico, rejeitando outros formatos com mensagem clara. |

> **Nota:** no documento original, os itens de RNF-07 a RNF-09 estavam numerados como "RF-" por engano; a numeração foi corrigida acima para manter a sequência de RNF.

---

## 10. Arquitetura e Stack Tecnológica (visão geral)

| Camada | Tecnologia proposta |
|---|---|
| Front-end | HTML, CSS, TypeScript |
| Back-end | Python, FastAPI |
| Banco de dados | A definir |
| Infraestrutura | Docker |
| Controle de versão | Git, GitHub, GitLab |
| Integração/Entrega Contínua | GitHub Actions |

---

## 11. Estrutura Ágil do Projeto

### 11.1 Papéis (Scrum)

- **Product Owner:** Coordenador do curso de Engenharia de Software — define prioridades e aceita entregas.
- **Scrum Master:** Ana Beatriz Nogueira Ferreira Guerra — garante o processo e remove impedimentos.
- **Time de Desenvolvimento:** Iuri Capanema Souza Koboldt, João Áquila, Maria Eduarda Macedo, Pablo Antônio Martins de Sousa, Vitor Piau Morhy, Vinicius Eugenio Montalvão Silva — implementa as user stories.

### 11.2 Cerimônias

| Cerimônia | Frequência | Objetivo |
|---|---|---|
| Sprint Planning | Início de cada sprint | Selecionar e detalhar itens do backlog |
| Sprint Review | Fim de cada sprint | Demonstrar incremento ao Product Owner |
| Sprint Retrospective | Fim de cada sprint | Melhorar processo da equipe |
| Backlog Refinement | Semanal | Detalhar e reestimar itens futuros |

---

## 12. Matriz de Riscos

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Atraso na integração com API externa | Média | Alto | Atenção às datas de entrega |
| Atraso da comunicação front-end com back-end | Médio | Alto | Atenção às datas de entrega |
| Incompatibilidade de agendas para realização de sprints | Baixa | Médio | Melhora na comunicação |

---

## 13. Aprovação

| Papel | Nome |
|---|---|
| Product Owner | Docentes |
| Scrum Master | Ana Beatriz, Maria Eduarda e João Áquila |
| Grupo 11 | Integrantes do grupo |
