# Arquitetura

## Visão Geral

A arquitetura do **MonitoraUnB** é composta por duas aplicações principais: o **backend** e o **frontend**.

O backend será responsável por fornecer uma **API REST**, que permitirá o acesso às informações necessárias para o funcionamento do sistema de monitorias. Entre essas informações estão os dados das disciplinas da Universidade de Brasília, obtidos a partir do SIGAA.

O frontend será responsável por consumir a API REST e apresentar essas informações ao usuário por meio da interface do MonitoraUnB.

De forma geral, a comunicação do sistema seguirá o seguinte fluxo:

```text
SIGAA → Backend/API → Frontend → Usuário
```

---

## Design do Sistema

O sistema será estruturado de forma que o frontend seja responsável pela interação com o usuário, enquanto o backend será responsável pelo processamento das requisições, leitura dos históricos escolares e acesso aos dados das disciplinas.

O fluxo da aplicação ocorrerá da seguinte forma:

1. O usuário acessa o MonitoraUnB.
2. O frontend apresenta a interface da aplicação.
3. O usuário insere seu histórico escolar na aplicação.
4. O histórico é enviado para o backend, onde sua leitura e processamento são realizados utilizando Python.
5. O sistema extrai do histórico as informações necessárias, incluindo os códigos das disciplinas.
6. O backend utiliza os códigos identificados para consultar as disciplinas disponíveis no banco de dados.
7. O banco de dados contém as informações das disciplinas obtidas previamente do SIGAA, principalmente o código e o nome de cada disciplina.
8. A API retorna para o frontend as informações necessárias após o processamento.
9. O frontend apresenta o resultado ao usuário.

O fluxo de processamento do histórico pode ser representado da seguinte forma:

```text
Histórico Escolar
       ↓
Frontend
       ↓
Backend (Python)
       ↓
Leitura e extração dos códigos
       ↓
Banco de Dados
       ↓
Identificação das disciplinas
       ↓
API REST
       ↓
Frontend
       ↓
Usuário
```

Os dados das disciplinas utilizados nesse processo serão obtidos previamente a partir do SIGAA e armazenados no banco de dados, evitando a necessidade de realizar uma nova consulta ao SIGAA para cada histórico processado.

---

## Backend e API REST

O backend do MonitoraUnB será responsável pelo processamento dos dados utilizados pela aplicação e pela comunicação entre o frontend e o banco de dados.

A comunicação entre o frontend e o backend será realizada através de uma **API REST**.

Entre as principais responsabilidades do backend estão:

- Receber o histórico escolar enviado pelo usuário;
- Realizar a leitura e o processamento do histórico utilizando Python;
- Identificar os códigos das disciplinas presentes no histórico;
- Consultar no banco de dados as informações correspondentes às disciplinas identificadas;
- Disponibilizar os dados das disciplinas para o frontend através da API REST;
- Realizar a coleta e o tratamento dos dados de disciplinas provenientes do SIGAA.

### API de Disciplinas

A API permitirá consultar as informações das disciplinas armazenadas no banco de dados.

Inicialmente, poderão ser disponibilizadas operações como:

```http
GET /api/disciplinas
```

Retorna as disciplinas disponíveis no banco de dados.

Também será possível realizar a consulta de uma disciplina específica utilizando seu código:

```http
GET /api/disciplinas/{codigo}
```

Por exemplo:

```http
GET /api/disciplinas/FGA0001
```

A resposta da API poderá seguir uma estrutura semelhante a:

```json
{
  "codigo": "FGA0001",
  "nome": "Nome da Disciplina"
}
```

### Processamento do Histórico

O backend também será responsável por receber e processar o histórico escolar enviado pelo usuário.

O processamento será realizado utilizando Python, que fará a leitura do documento e identificará os códigos das disciplinas presentes no histórico.

Após a identificação dos códigos, o backend poderá utilizar os dados armazenados no banco para relacionar cada código à sua respectiva disciplina.

O histórico escolar será utilizado para processamento das informações necessárias para a aplicação, não sendo necessário armazenar o documento no banco de dados.

---

## Obtenção dos Dados do SIGAA

Para que o MonitoraUnB consiga identificar as disciplinas presentes no histórico escolar do usuário, será necessário manter uma base contendo as disciplinas da Universidade de Brasília.

Essas informações serão obtidas a partir do SIGAA e utilizadas para relacionar o código de uma disciplina ao seu respectivo nome.

Inicialmente, serão coletadas principalmente as seguintes informações:

- Código da disciplina;
- Nome da disciplina.

O processo de obtenção dos dados seguirá, de forma geral, o seguinte fluxo:

```text
SIGAA
  ↓
Coleta dos dados
  ↓
Tratamento com Python
  ↓
Código + Nome da disciplina
  ↓
Banco de Dados
```

Após a coleta, os dados serão tratados e organizados antes de serem armazenados no banco de dados.

Dessa forma, quando o backend identificar um código de disciplina durante a leitura de um histórico escolar, poderá consultar a base de dados do MonitoraUnB para identificar a disciplina correspondente.

A coleta dos dados do SIGAA será realizada separadamente das requisições dos usuários. Assim, não será necessário acessar o SIGAA sempre que um histórico for processado ou uma disciplina for consultada.
