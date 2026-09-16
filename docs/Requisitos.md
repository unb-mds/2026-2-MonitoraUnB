# Lista de Requisitos do Monitora UnB

## 1. Informações do Projeto

### Nome do software

**Monitora UnB**

### Descrição

O sistema Monitora UnB nasceu a partir da necessidade de automatizar as inscrições da monitoria. O sistema busca resolver os furos que anteriormente havia no processo, como informações erradas e demora na solicitação, verificação e resultado.

### Público-alvo

O público-alvo do Monitora UnB são os docentes e discentes da Universidade de Brasília.

---

## 2. Requisitos Funcionais

* **RF01:** O sistema deve permitir upload do histórico em PDF.
* **RF02:** O sistema deve permitir que o aluno selecione uma disciplina entre as disponíveis para monitoria.
* **RF03:** O sistema deve validar se o aluno foi aprovado na disciplina selecionada, consultando os dados do histórico e qual menção ele obteve quando cursou.
* **RF04:** O sistema deve exibir uma tela de confirmação apresentando as informações extraídas do histórico com nome, matrícula, IRA, menção na disciplina e a disciplina antes da efetivação.
* **RF05:** O sistema deve exibir mensagem de sucesso ou falha ao final do processo.
* **RF06 — Integração:** O sistema deve se conectar, via plugin/API, à base de dados acadêmica da UnB para validar as informações do aluno, evitando fraude ou erro de digitação.

---

## 3. Requisitos Não Funcionais

* **RNF01:** Dados pessoais, como matrícula, nome completo e informações do histórico, devem ser tratados conforme a LGPD (Lei Geral de Proteção de Dados Pessoais), com armazenamento seguro, acesso restrito e não exposição em logs.
* **RNF02:** O sistema deve validar o histórico em tempo hábil, em poucos segundos, sem travar a experiência do usuário.
* **RNF03:** A interface deve ser simples e acessível para qualquer aluno, sem necessidade de treinamento.
* **RNF04:** O sistema deve registrar logs de auditoria das inscrições, contendo informações como quem realizou a inscrição, quando ela ocorreu e qual disciplina foi selecionada.

---

## 4. Regras de Negócio

Regras que o sistema precisa obedecer para pleno funcionamento.

| Código   | Regra                                                                                                                                           |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **RN01** | Um usuário não pode cadastrar duas contas usando o mesmo e-mail.                                                                                |
| **RN02** | Caso a matéria que o aluno solicitou para monitorar não apareça no histórico como **"APROVADO"**, o aluno terá a tentativa de inscrição negada. |

---

## 5. Fluxo Principal

### Visão do Front-end

### Tela 1 — Envio dos Dados

* Upload do histórico escolar em PDF;
* Seleção da disciplina de interesse para monitoria por meio de dropdown/lista, populada a partir das disciplinas disponíveis para monitoria;
* E-mail do aluno para contato;
* Botão **"Enviar"**.

### Validação

A validação ocorre no back-end, mas seus resultados são apresentados no front-end.

O sistema deve:

* Extrair e conferir os dados do histórico enviado;
* Verificar se o aluno foi aprovado na disciplina selecionada.

Caso a validação falhe, o sistema deve exibir uma mensagem de erro clara.

Exemplos:

* **"Você não possui aprovação registrada nesta disciplina."**
* **"Não foi possível validar o histórico enviado."**

### Tela 2 — Confirmação dos Dados

O sistema deve exibir para o aluno, de forma somente leitura:

* Nome completo;
* Matrícula;
* IRA;
* Disciplina selecionada;
* Créditos do semestre.

A tela deve possuir:

* Botão **"Confirmar inscrição"**;
* Opção de **"Voltar/corrigir"**.

### Tela 3 — Resultado

Após a tentativa de efetivação da inscrição, o sistema deve apresentar:

* Mensagem de sucesso: **"Inscrição efetivada com sucesso!"**;
* Ou mensagem de erro, caso algo falhe durante a gravação das informações.

---

## 6. Back-end

O sistema não se limita à parte acessada pelo aluno. A etapa descrita anteriormente representa apenas o processo de inscrição.

Após a inscrição dos alunos, inicia-se a etapa relacionada aos professores e à comissão de monitoria.

### 6.1. Extração das Informações

As informações extraídas do histórico de cada aluno incluem:

* Nome;
* Matrícula;
* IRA;
* Menção na disciplina;
* Disciplina selecionada;
* Créditos do semestre.

### 6.2. Cálculo de Coeficiente

Após a extração das informações do aluno, o sistema realiza um cálculo denominado **cálculo de coeficiente**.

Esse cálculo é necessário para:

* Realizar o ranqueamento dos alunos inscritos;
* Auxiliar na classificação dos candidatos;
* Auxiliar na distribuição de bolsas entre os alunos selecionados.

### 6.3. Classificação dos Alunos

Após o preenchimento dos dados e o cálculo do coeficiente, as informações necessárias para a classificação são enviadas para uma planilha Excel.

Essa planilha:

* Realiza a classificação dos alunos;
* É utilizada para controle do processo seletivo;
* Possui acesso restrito ao professor líder da comissão de monitoria.

### 6.4. Resultado da Seleção

Após o encerramento do período de inscrições e a realização da classificação dos candidatos, o sistema gera um e-mail contendo o resultado da seleção.

Esse e-mail é então enviado aos alunos inscritos, informando o resultado do processo de monitoria.

