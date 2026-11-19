# **Documentação da API \- Scraping de Disciplinas do SIGAA&nbsp;**

## 1\. Como a API Funciona (Arquitetura e Decisões de Projeto)

Nossa API foi construída em **FastAPI** (Python) e não se conecta diretamente ao banco de dados da universidade, pois não temos esse acesso. Em vez disso, ela atua como um "navegador virtual invisível" (Web Scraper) que entra na página pública do SIGAA, extrai os dados do HTML e salva no nosso banco de dados local.

Esse fluxo de funcionamento baseia-se em quatro pilares principais:

## 1.1. "ViewState";

O sistema do SIGAA usa uma tecnologia antiga (JSF) que bloqueia requisições diretas por segurança. Para burlar isso, nosso código não pede a lista de disciplinas logo de cara. Primeiro, ele acessa a página inicial do SIGAA para criar cookies de sessão e extrair um código de segurança obrigatório chamado `ViewState`. Só com esse código anexado é que enviamos o formulário POST pedindo os dados do departamento desejado.

## 1.2. HTTPX e Assincronicidade (Otimizando o Tempo)

Como buscar dados na internet pode ser demorado (o servidor do SIGAA pode estar lento), usamos a biblioteca `httpx` com `asyncio`. Isso permite que a API não "congele" enquanto espera a resposta da UnB. Enquanto uma requisição está pendente, o nosso sistema pode continuar processando outras tarefas simultaneamente.

## 1.3. Banco de Dados e SQLAlchemy (O Tradutor)

Usamos o **SQLAlchemy** como nosso ORM (Object-Relational Mapper). Isso significa que não precisamos escrever comandos SQL puros (como `INSERT INTO...`). Nós apenas manipulamos objetos Python (ex: `nova = Disciplina(...)`), e o SQLAlchemy traduz isso automaticamente para o nosso banco de dados, o qual ainda está em desenvolvimento.

## 1.4. Schemas e Pydantic&nbsp;

Antes de qualquer dado entrar ou sair da nossa API, ele passa pelos nossos "Schemas" construídos com Pydantic. Eles garantem que ninguém consiga enviar parâmetros inválidos (ex: pedir a página \-1 de disciplinas) e formatam exatamente quais campos do banco de dados o Front-End vai receber no JSON final.

## **Testes de Caixa Cinza (Gray Box)**

Como conhecemos a estrutura interna do código, os testes abaixo validam tanto as respostas da API quanto o comportamento do nosso banco de dados.

> Todos os testes serão executados pela interface interativa do Swagger, acessando a rota `http://127.0.0.1:8000/docs` no navegador, clicando no endpoint e depois no botão

**Como acessar o ambiente de testes:**

1. Rode a API no seu terminal (`uvicorn main:app --reload`).  
2. Abra o navegador e acesse: `http://localhost:8000/docs`

---

## Teste 1: Testando a Fila de Background (Não travar a API)

Se pedirmos para a API baixar a UnB inteira, o processo demora muito. O código joga essa tarefa para o "background" (segundo plano). Vamos testar se isso está funcionando corretamente.

**Como testar no Swagger:**

1. Na tela do Swagger, clique na barra verde do **POST** `/api/v1/scraping/iniciar` para expandir.  
2. Clique no botão **"Try it out"** (Tentar agora) no canto direito.  
3. Na caixa de texto de `Request body`, edite o valor do `"departamento_sigaa_id"` e escreva `null` (sem aspas).&nbsp;

```json
{
  "nivel": "G",
  "departamento_sigaa_id": null,
  "tipo": 2
}
```

Clique no botão azul "Execute".

4. **Olhando o Front:** Role um pouco para baixo até a área de *Responses*. A resposta da API tem que vir na mesma hora dizendo `"status": "RUNNING"`.  
5. **Olhando o Banco:** Abra a tabela `scraping_logs` no seu visualizador de banco de dados. O último registro tem que estar como `RUNNING`.  
6. Vá no Swagger, expanda o **GET** `/api/v1/scraping/logs`, clique em **"Try it out"** e depois em **"Execute"**. Veja se o status mudou para `SUCCESS`. Isso prova que a tarefa rodou por trás dos panos\!

---

## Teste 2: Testando se não estamos duplicando disciplinas

O scraper será rodado várias vezes ao longo do semestre. Se a matéria "Cálculo 1" já está no banco, o nosso código (do arquivo `scraper.py`) tem que ser inteligente o suficiente para não criar outra linha e duplicar tudo.

**Como testar no Swagger:**

1. Expanda o **POST** `/api/v1/scraping/iniciar` de novo, clique em **"Try it out"**.  
2. No *Request body*, coloque o ID de um departamento específico. Vamos usar a FGA (`673`):

```json
{
  "nivel": "G",
  "departamento_sigaa_id": 673,
  "tipo": 2
}
```

3. Clique em **"Execute"**. Quando carregar a resposta, anote o número que veio em `"disciplinas_novas"`.  
4. Agora, expanda o **GET** `/api/v1/estatisticas`, clique em **"Try it out"** e **"Execute"**. Anote o `"total_disciplinas"` que está no banco.  
5. **A hora da verdade:** Volte no POST do passo 1 e clique em **"Execute"** de novo (enviando os mesmos dados).  
6. **Olhando o Front:** A resposta agora **tem que** vir com `"disciplinas_novas": 0`.  
7. **Olhando o Banco:** Rode o GET de estatísticas mais uma vez. O `"total_disciplinas"` tem que continuar exatamente igual\! Se aumentar, nosso banco está duplicando dados.

---

## Teste 3: Testando a Barra de Pesquisa e Paginação (Filtro iLike)

O usuário do app vai digitar "cic" (minúsculo) na barra de pesquisa e a API tem que achar "CIC0004". Também vamos checar se a matemática que divide as páginas funciona corretamente.

**Como testar no Swagger:**

1. Expanda o **GET** `/api/v1/disciplinas` e clique em **"Try it out"**.  
2. Preencha os campos visuais que apareceram:  
   * **page**: `1`  
   * **per\_page**: `10`  
   * **codigo**: `cic`  
3. Clique em **"Execute"**.  
4. **Validando os Filtros:** Olhe o JSON de resposta na seção `items`. Todas as matérias retornadas devem ter "CIC" no código.  
5. **Validando a Matemática:**  
   * Pegue o número que veio no campo `"total"` (ex: 45).  
   * Divida pelo `"per_page"` que pedimos (10). 45 / 10 \= 4.5.  
   * O código usa a função "teto" (arredonda pra cima), então dá 5\.  
   * Veja se o campo `"pages"` retornou `5`. Isso garante que os botões de paginação no Front-end vão funcionar certinho.

---

## Teste 4: Testando os Limites (Boundary Testing)

Nós definimos regras no arquivo `routes.py` (ex: página não pode ser zero; o máximo de itens por página é 200). Se alguém (ou o front-end por engano) tentar quebrar essas regras, a API tem que barrar na mesma hora, antes mesmo de bater no banco de dados.

**Como testar no Swagger:**

1. Expanda o **GET** `/api/v1/disciplinas` e clique em **"Try it out"**.  
2. **Quebrando o limite superior:** No campo **per\_page**, apague o valor atual e digite `201` (o máximo permitido é 200).  
3. Clique em **"Execute"**.  
4. A API não deve processar\! Ela tem que dar um erro vermelho "422 Validation Error", avisando que o valor deve ser menor ou igual a 200\.  
5. **Quebrando o limite inferior:** Agora mude o **per\_page** para `50` (válido), mas coloque `0` no campo **page** (o mínimo é 1).  
6. Clique em **"Execute"**.  
7. Novamente, a API deve devolver um erro "422", provando que os nossos filtros de segurança (Pydantic) estão blindando o servidor\!

## Teste 5: Teste de Tratamento de Exceções (IDs ou códigos inexistentes)

**Objetivo:** Verificar se o sistema lida de forma elegante com buscas por recursos que não existem no banco de dados, evitando que a aplicação quebre (Erro 500\) e retornando o status HTTP correto (Erro 404).

1. **Teste de Departamento Inexistente:**  
   1. Vá no endpoint `GET /api/v1/departamentos/{depto_id}/disciplinas`.  
   2. Digite um ID impossível, como `999999`.  
   3. Clique em **Execute**.  
   4. **Resultado Esperado:** A API deve retornar um `Status 404 Not Found` com a mensagem `"Departamento não encontrado"`.  
2. **Teste de Código Inexistente:**  
   1. Vá no endpoint `GET /api/v1/disciplinas/codigo/{codigo}`.  
   2. Digite um código de disciplina inventado, como `XYZ9999`.  
   3. Clique em **Execute**.  
   4. **Resultado Esperado:** A API deve retornar um `Status 404 Not Found` com a mensagem `"Nenhuma disciplina encontrada com esse código"`.