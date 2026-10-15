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
