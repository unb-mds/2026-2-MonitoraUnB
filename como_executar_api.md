# Como executar o projeto localmente

Este guia resume os comandos necessários para executar o backend, o frontend e o compilador TypeScript durante o desenvolvimento do MonitoraUnB.

---

## 1. Backend / API

Na raiz do projeto, ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
O ambiente virtual `.venv` mantém as dependências Python do projeto isoladas, como:
 - FastAPI
 - Uvicorn
 - pypdf
 - python-multipart

Depois entre na pasta do backend e inicie a API no terminal:
```powershell
cd python_scripts
python -m uvicorn main:app --reload 
```
Se tudo estiver certo, deve aparecer `Uvicorn running on http://127.0.0.1:8000` no terminal.

O parâmetro `--reload` faz com que a API atualize automaticamente após alguma mudança no código Python. 

Para acessar a API, acesse `http://127.0.0.1:8000` em qualquer navegador no seu computador. Para sair do ambiente virtual, use `deactivate`.

---

## 2. Swagger

Para testar se os endpoints estão funcionando, acesse `http://127.0.0.1:8000/docs`.

Por enquanto (14/10/2026), há um endpoint que pode ser testado, que é o `POST /api/historico`. 
Para testar o processamento, clique em "Try it out" na direita, 
preencha os campos "arquivo" e "disciplina" 
com o arquivo de histórico e o código da disciplina, respectivamente.

Depois, clique no botão azul "Execute". Se o histórico for válido, uma mensagem igual a essa deve aparecer:
```json
{
  "aluno": "NOME DO ALUNO",
  "matricula": "MATRICULA",
  "ira": "IRA DO ALUNO"
}
```
O código HTTP esperado deve ser `200 OK`. Também é possível verificar pelo terminal. 

Para algum arquivo que não é um PDF, o resultado esperado deve ser `400 Bad Request`. 

Para arquivos PDF que não correspondem a um histórico válido, o resultado deve ser `422 Unprocessable Entity`.

---

## 3. Frontend / Typescript

Para testar a integração do Frontend, abra outro terminal e entre na pasta do Frontend: `cd front-end`.

Para esse terminal, a `.venv` pode permanecer desligada.

Caso ainda não tenha instalado, execute os seguintes comandos:
```powershell
npm install
npm run build
npm run watch
```
O primeiro comando baixa as dependências; O segundo compila o código TypeScript; 
O terceiro recompila automaticamente após cada alteração em algum arquivo `.ts`

Esse terminal deve permanecer aberto durante o desenvolvimento.

---

## 4. Servidor do Frontend

Abra outro terminal e entre na mesma pasta `cd front-end`. 

Inicie o servidor com o comando `npx serve`.

Feito corretamente, o Frontend ficará aberto em `http://localhost:3000`, e a página inicial pode ser acessada
em `http://localhost:3000/pages/portal.html`.

---

## 5. Organização recomendada dos terminais

Durante o desenvolvimento, é recomendado ter pelo menos quatro terminais abertos.

### Terminal 1 - Backend/API

```powershell
cd python_scripts
python -m uvicorn main:app --reload
```

Mantém a API disponível em:
```text
http://127.0.0.1:8000
```
---

### Terminal 2 - TypeScript

Na pasta `front-end`:

```powershell
npm run watch
```
Mantém o TypeScript sendo recompilado automaticamente.

---

### Terminal 3 - Servidor do frontend

Na pasta `front-end`:

```powershell
npx serve
```
Mantém o frontend disponível normalmente em:

```text
http://localhost:3000
```
---

### Terminal 4 - Comandos gerais

Utilize para comandos como:

```powershell
git status
git fetch origin
git add .
git commit
git push
npm install
python -m pip install ...
```

# 6. Comunicação entre frontend e backend

Durante o desenvolvimento local, normalmente temos:

```text
Frontend
http://localhost:3000

Backend
http://127.0.0.1:8000
```

O frontend envia requisições para a FastAPI.

Exemplo do fluxo atual:

```text
Usuário seleciona histórico
        ↓
Frontend
        ↓
FormData
        ├── arquivo
        └── disciplina
        ↓
POST /api/historico
        ↓
FastAPI
        ↓
Python processa o histórico
        ↓
Nome + matrícula + IRA
        ↓
JSON
        ↓
Frontend
```

Como frontend e backend utilizam portas diferentes, o backend possui configuração de CORS para permitir essa comunicação.

---

# 7. Testando a integração completa

Para testar todo o sistema:

1. Inicie a API;
2. Inicie `npm run watch`;
3. Inicie `npx serve`;
4. Abra:

```text
http://localhost:3000/pages/portal.html
```

5. Acesse a página de inscrição;
6. Selecione uma disciplina;
7. Envie um histórico válido;
8. Continue para a revisão.

Se tudo funcionar corretamente, os dados exibidos devem vir do próprio histórico enviado.

Atualmente são extraídos:

```text
Nome
Matrícula
IRA
```

Também é possível acompanhar a requisição pelo navegador utilizando:
```text
F12
Network
Fetch/XHR
```
Procure pela requisição `POST/api/historico`. 
Ela deve retornar `200 OK`.

Para visualizar a resposta enviada pelo backend:
```text
Network
/api/historico
Response
```

# 8. Encerrando os servidores

Para interromper qualquer processo no terminal, aperte `Ctrl + C`.

Para sair do ambiente virtual, digite `deactivate`.
