# Arquitetura do Banco de Dados — API de Disciplinas do SIGAA UnB

## 1. Objetivo

Este documento descreve a arquitetura proposta para o banco de dados do projeto da API de Disciplinas do SIGAA da Universidade de Brasília (UnB).

O banco será desenvolvido em MySQL e terá duas responsabilidades principais:

- Armazenar os códigos e nomes das disciplinas coletadas do portal público do SIGAA UnB.
- Armazenar as informações necessárias para o login do presidente da comissão.

As duas funcionalidades serão mantidas em um único banco de dados, com tabelas separadas para organizar as informações.

## 2. Tecnologias

| Tecnologia | Responsabilidade |
|---|---|
| MySQL | Armazenamento persistente dos dados |
| Docker Desktop | Execução do MySQL em um container local |
| Docker Compose | Configuração e inicialização do ambiente |
| Python + SQLAlchemy | Integração do backend com o banco |
| PyMySQL | Driver de conexão entre Python e MySQL |
| FastAPI | API responsável pela sincronização e consulta das disciplinas |

O banco será executado localmente durante o desenvolvimento. O Docker permitirá padronizar o ambiente utilizado pelos integrantes do grupo, independentemente do sistema operacional.

## 3. Estrutura do banco de dados

O banco será denominado provisoriamente `sigaa_unb`. O nome poderá ser alterado conforme a decisão do grupo.

Inicialmente, serão utilizadas duas tabelas: `disciplinas` e `usuarios`.

### 3.1. Tabela `disciplinas`

Responsável por armazenar as disciplinas coletadas pelo módulo de web scraping.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `codigo` | `VARCHAR(20)` | Chave primária | Código único da disciplina |
| `nome` | `VARCHAR(255)` | `NOT NULL` | Nome da disciplina |
| `atualizado_em` | `TIMESTAMP` | Automático | Data e hora da última inserção ou atualização |

**Regras de funcionamento:**

- O código será a chave primária, evitando o cadastro de duas disciplinas com o mesmo código.
- O nome será obrigatório.
- A coluna `atualizado_em` registrará a data e a hora da última inserção ou alteração do registro.
- A tabela utilizará `utf8mb4` para suportar acentos e outros caracteres Unicode.
- A sincronização utilizará a operação `INSERT ... ON DUPLICATE KEY UPDATE`, conhecida como *upsert*, para inserir novas disciplinas e atualizar as já existentes.

A consulta das disciplinas armazenadas será feita diretamente no banco, sem a necessidade de acessar o SIGAA novamente.

### 3.2. Tabela `usuarios`

Responsável por armazenar os dados da conta utilizada pelo presidente da comissão para acessar o sistema.

| Coluna | Tipo | Restrições | Descrição |
|---|---|---|---|
| `id` | `INT` | Chave primária, incremento automático | Identificador do usuário |
| `nome` | `VARCHAR(150)` | `NOT NULL` | Nome do usuário |
| `email` | `VARCHAR(255)` | `NOT NULL`, único | E-mail utilizado no login |
| `senha_hash` | `VARCHAR(255)` | `NOT NULL` | Hash seguro da senha |
| `ativo` | `BOOLEAN` | `NOT NULL`, padrão verdadeiro | Indica se a conta está habilitada |
| `criado_em` | `TIMESTAMP` | Automático | Data de criação da conta |
| `atualizado_em` | `TIMESTAMP` | Automático | Data da última atualização dos dados |

**Regras de funcionamento:**

- O e-mail será único, evitando a criação de contas duplicadas para a mesma identificação.
- A senha nunca será armazenada em texto puro.
- O backend utilizará uma biblioteca de autenticação para gerar e verificar o hash da senha. Recomenda-se Argon2id ou bcrypt.
- A coluna `ativo` permitirá desabilitar a conta sem precisar excluir o registro.
- O cadastro inicial do presidente da comissão deverá ser realizado por um procedimento controlado, sem disponibilizar publicamente um endpoint de criação de usuários desnecessário.

A tabela poderá comportar outros usuários no futuro, embora o requisito atual seja atender ao presidente da comissão.

## 4. Relacionamento entre as tabelas

As tabelas `disciplinas` e `usuarios` não terão relacionamento direto na versão inicial.

A tabela `disciplinas` armazenará informações acadêmicas coletadas do SIGAA, enquanto `usuarios` armazenará os dados de autenticação do sistema.

Essa separação facilita a manutenção e evita misturar informações acadêmicas com credenciais de acesso.

## 5. Esquema SQL inicial

A estrutura poderá ser criada com os seguintes comandos:

```sql
CREATE DATABASE IF NOT EXISTS sigaa_unb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE sigaa_unb;

CREATE TABLE disciplinas (
    codigo VARCHAR(20) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    atualizado_em TIMESTAMP
        NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    ativo BOOLEAN NOT NULL DEFAULT TRUE,
    criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci;
```

Esse script representa a estrutura inicial proposta. Ele não cria automaticamente a conta do presidente da comissão, pois o cadastro deve ser feito por um procedimento seguro.

## 6. Integração com o backend

A conexão entre o backend e o banco será realizada por SQLAlchemy, utilizando o driver PyMySQL.

O backend será responsável por executar as operações de leitura e escrita, enquanto o banco será responsável por armazenar e manter os registros.

### 6.1. Sincronização das disciplinas

O endpoint `POST /sincronizar` será responsável por:

1. Receber um trecho do nome ou do código de uma disciplina.
2. Solicitar ao módulo de scraping a busca no SIGAA.
3. Receber os códigos e nomes encontrados.
4. Inserir as disciplinas novas no banco.
5. Atualizar os registros existentes quando houver alterações.
6. Retornar informações sobre o resultado da sincronização.

O código da disciplina será utilizado para identificar registros existentes e evitar duplicatas.

### 6.2. Consulta das disciplinas

O endpoint `GET /disciplinas` consultará os registros já armazenados no MySQL.

Poderá receber os seguintes parâmetros opcionais:

- `nome`: filtra disciplinas pelo nome.
- `codigo`: filtra disciplinas pelo código.
- `limite`: limita a quantidade de resultados, com padrão de 100 e máximo de 1000.

Os resultados serão ordenados pelo código da disciplina.

A consulta não deverá realizar scraping. Dessa maneira, a disponibilidade do SIGAA não será necessária para consultar dados previamente armazenados.

### 6.3. Login do presidente da comissão

A tabela `usuarios` será utilizada pelo mecanismo de autenticação do sistema.

O fluxo previsto será:

1. O presidente da comissão informa seu e-mail e sua senha no formulário de login.
2. O backend procura a conta pelo e-mail.
3. O backend verifica a senha informada contra o hash armazenado.
4. Se a senha estiver correta e a conta estiver ativa, o sistema autoriza o acesso conforme as regras de autenticação definidas pelo grupo.

A senha original não será recuperável a partir do hash. Uma eventual alteração de senha deverá gerar um novo hash.

## 7. Configuração e segurança

### 7.1. Variáveis de ambiente

As credenciais de conexão não deverão ser escritas diretamente no código-fonte.

O backend poderá utilizar variáveis de ambiente como:

- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

Os valores serão definidos conforme o ambiente de execução. Em um projeto local com Docker Compose, o endereço do banco dependerá de onde o backend estiver sendo executado: no próprio computador ou em outro container.

Arquivos `.env` que contenham credenciais reais deverão ser excluídos do controle de versão por meio do `.gitignore`. Um arquivo de exemplo poderá documentar os nomes das variáveis sem incluir senhas reais.

### 7.2. Acesso local

Durante o desenvolvimento, a porta do MySQL deverá ser disponibilizada apenas conforme a necessidade do projeto, preferencialmente restrita ao próprio computador quando o acesso ocorrer a partir do sistema operacional hospedeiro.

Quando o backend e o banco estiverem em containers separados, a comunicação deverá ocorrer pela rede Docker apropriada. A configuração deverá considerar o ambiente de execução utilizado por cada integrante do grupo.

As credenciais administrativas do MySQL não deverão ser utilizadas indiscriminadamente pelo backend. Recomenda-se criar um usuário específico para a aplicação, com as permissões necessárias.

### 7.3. Armazenamento de senhas

A senha do presidente da comissão deverá ser protegida com um algoritmo específico para armazenamento de senhas, como Argon2id ou bcrypt.

Não se deve utilizar MD5 ou SHA-256 simples para armazenar senhas, nem guardar a senha original em uma coluna do banco.

## 8. Persistência dos dados no Docker

O MySQL será executado em um container Docker.

Será necessário configurar um volume persistente para que os dados do banco não sejam perdidos quando o container for recriado ou removido.

O Docker Compose poderá centralizar a configuração do serviço MySQL, incluindo imagem, porta, variáveis de ambiente e volume.

As credenciais deverão ser configuradas de forma apropriada para o ambiente de desenvolvimento e não deverão ser publicadas no repositório.

## 9. Plano inicial de testes

Os seguintes testes deverão ser realizados durante o desenvolvimento:

1. Verificar se o banco foi criado corretamente.
2. Verificar se as tabelas `disciplinas` e `usuarios` possuem as colunas e restrições esperadas.
3. Inserir uma disciplina de teste e consultá-la por meio de `SELECT`.
4. Executar a sincronização duas vezes e verificar se não são criadas disciplinas duplicadas.
5. Alterar o nome de uma disciplina de teste e verificar se a sincronização atualiza o registro.
6. Consultar as disciplinas utilizando filtros por nome e código.
7. Testar a persistência dos dados após reiniciar o container.
8. Verificar se os nomes com acentos são armazenados corretamente.
9. Confirmar que as credenciais do banco não estão expostas no código ou no repositório.
10. Testar a autenticação válida, a senha incorreta e a conta desativada.

## 10. Referências técnicas

- [MySQL — documentação oficial](https://dev.mysql.com/doc/)
- [MySQL — INSERT e ON DUPLICATE KEY UPDATE](https://dev.mysql.com/doc/refman/8.4/en/insert.html)
- [Docker Compose — configuração de variáveis de ambiente](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/)
- [OWASP — Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

## 11. Conclusão

A arquitetura proposta utiliza um único banco de dados MySQL, organizado em duas tabelas independentes: `disciplinas`, para armazenar os dados coletados do SIGAA UnB, e `usuarios`, para armazenar os dados necessários à autenticação do presidente da comissão.

A solução mantém a responsabilidade de persistência separada do scraping e da exposição dos endpoints, utiliza mecanismos para evitar duplicatas e prevê cuidados básicos com credenciais, senhas e persistência local.

A estrutura poderá ser ampliada futuramente, caso o projeto passe a armazenar outros dados acadêmicos ou precise oferecer funcionalidades adicionais de autenticação.
