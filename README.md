<div align="center">

<h1>Monitora UnB</h1>

<p><strong>Sistema web para gestão do processo seletivo de monitorias da Universidade de Brasília.</strong></p>

<p>
  Candidate-se a uma vaga de monitor de forma simples, guiada e transparente — com validação automática de histórico escolar em PDF, cálculo de coeficiente e ranking para a comissão de monitoria.
</p>

<p>
  <img src="https://img.shields.io/badge/FRONT--END-INTEGRADO-brightgreen?style=flat-square" alt="Front-end: integrado">
  <img src="https://img.shields.io/badge/BACK--END-ATIVO-brightgreen?style=flat-square" alt="Back-end: ativo">
  <img src="https://img.shields.io/badge/DOCKER-COMPOSE-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/MDS-2026%2F2%20%7C%20G11-1736a6?style=flat-square" alt="MDS 2026/2 - Grupo 11">
</p>

<p>
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white" alt="CSS3">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white" alt="Nginx">
</p>

<p>
  <a href="#sobre-o-projeto">Sobre</a> •
  <a href="#funcionalidades">Funcionalidades</a> •
  <a href="#tecnologias">Tecnologias</a> •
  <a href="#estrutura-do-repositório">Estrutura</a> •
  <a href="#como-executar">Como Executar</a> •
  <a href="#como-testar">Como Testar</a> •
  <a href="#status-e-roadmap">Roadmap</a> •
  <a href="#documentação">Documentação</a> •
  <a href="#equipe">Equipe</a> •
  <a href="#uso-de-ia-no-projeto">Uso de IA</a>
</p>

</div>

---

## Sobre o Projeto

O **Monitora UnB** é um sistema web desenvolvido na disciplina de **Métodos de Desenvolvimento de Software (MDS)** da **Universidade de Brasília (UnB) — Faculdade de Ciências e Tecnologias em Engenharia (FCTE, antiga FGA)** para automatizar o processo de inscrição e apoiar a seleção de monitores acadêmicos.

No fluxo tradicional, as inscrições dependem de formulários genéricos e conferência manual de históricos em planilhas. O **Monitora UnB** centraliza toda a jornada para dois perfis principais:

- **Estudantes:** realizam a inscrição on-line enviando o histórico escolar em PDF, têm seus dados acadêmicos extraídos e validados automaticamente e conferem o resumo antes da submissão definitiva.
- **Professores e Comissão de Monitoria:** acessam a área administrativa autenticada para abrir e encerrar processos seletivos, acompanhar o ranking automático de candidatos por disciplina e exportar a planilha consolidada em `.xlsx`.

O coeficiente de classificação é calculado automaticamente conforme a regra do processo seletivo:

$$C = 0{,}6 \times \text{IRA} + 0{,}4 \times M$$

Onde **IRA** é o Índice de Rendimento Acadêmico extraído do histórico e **M** é o valor numérico da menção obtida na disciplina (`MM = 3`, `MS = 4`, `SS = 5`).

---

## Funcionalidades

### Fluxo do Estudante

1. **Início (`inicio.html`):** porta de entrada do sistema com acesso para estudantes e área do professor.
2. **Inscrição (`inscricao.html`):** preenchimento de e-mail, matrícula, código da disciplina, professor opcional, declaração de não recebimento de outra bolsa e envio do histórico escolar em PDF.
3. **Validação automática (`POST /api/historico`):** extração de texto do PDF no back-end com `pypdf`, verificação de vínculo `ATIVO`, conferência de matrícula, validação de aprovação na disciplina (menção mínima `MM`, bloqueando disciplinas em curso `MATR`) e cálculo do coeficiente.
4. **Revisão (`revisao.html`) ou Não Apto (`nao-apto.html`):** se elegível, o estudante confere o resumo dos dados validados antes do envio; caso não atenda aos requisitos, recebe o detalhamento do motivo na tela de inelegibilidade.
5. **Solicitação Registrada (`solicitacao-registrada.html`):** persistência definitiva da candidatura no PostgreSQL (`POST /api/inscricoes`), com prevenção de inscrições duplicadas no mesmo semestre.

### Área do Professor / Comissão de Monitoria

1. **Autenticação segura (`login-professor.html`):** login protegido por hash `bcrypt` e cookie de sessão assinado (`POST /api/auth/login`).
2. **Gestão de processos seletivos (`/api/admin/processos`):** criação, abertura, encerramento e limpeza de processos seletivos por semestre diretamente pela interface.
3. **Ranking de candidatos (`ranking.html`):** listagem das inscrições do semestre aberto com filtro por disciplina e ordenação por coeficiente ou ordem alfabética.
4. **Exportação de planilhas (`GET /api/inscricoes/planilha`):** geração e download de planilha Excel (`.xlsx`) com os candidatos classificados.
5. **Coleta de dados do SIGAA (`/api/v1`):** módulo de web scraping integrado para sincronização de departamentos, disciplinas e docentes públicos da UnB.

---

## Tecnologias

| Camada / Área | Tecnologia | Finalidade |
| --- | --- | --- |
| Front-end | HTML5, CSS3 e TypeScript (`tsc`) | Interface web do estudante e da área do professor |
| Servidor web / Proxy | Nginx | Servir arquivos estáticos e fazer proxy reverso de `/api/` para o back-end |
| Back-end / API | Python 3.12, FastAPI e Uvicorn | API REST, regras de negócio, autenticação e documentação Swagger/ReDoc |
| Leitura de PDF | `pypdf` *(e `pdfjs-dist` no front-end)* | Extração de texto e validação de históricos escolares em PDF |
| Banco de dados | PostgreSQL 17, SQLAlchemy 2 e `psycopg` | Persistência de processos seletivos, disciplinas e candidaturas |
| Scraping do SIGAA | `httpx`, BeautifulSoup4 e `lxml` | Coleta de dados públicos de departamentos, disciplinas e turmas da UnB |
| Segurança e Relatórios | `bcrypt`, `itsdangerous` e `openpyxl` | Hash de credenciais, sessões/tokens assinados e exportação `.xlsx` |
| Notificações | SMTP (`smtplib`) | Envio de e-mails de notificação do processo seletivo |
| Testes | `pytest` | Testes automatizados de serviços do back-end |
| Infraestrutura | Docker e Docker Compose | Orquestração dos serviços (`db`, `api`, `frontend` e `scraping`) |
| Prototipação | Figma e FigJam | Protótipo navegável e Story Map do produto |

---

## Estrutura do Repositório

```text
2026-2-MonitoraUnB/
├── backend/
│   ├── database/               # Conexão SQLAlchemy, modelos ORM, setup e scripts SQL
│   ├── dependencies/           # Dependências FastAPI (ex.: guarda de autenticação)
│   ├── requirements/           # Dependências Python separadas por módulo
│   ├── routers/                # Rotas REST (auth, historico, inscricoes, admin, scraping)
│   ├── schemas/                # Contratos Pydantic de entrada e saída
│   ├── scraping/               # Coletor de dados públicos do SIGAA UnB
│   ├── scripts/                # Utilitários (hash de senha do professor e processo seletivo)
│   ├── services/               # Regras de negócio (leitura de PDF, coeficiente, ranking, SMTP, xlsx)
│   ├── tests/                  # Testes unitários em pytest
│   ├── Dockerfile              # Imagem Docker do back-end FastAPI
│   ├── config.py               # Leitura tipada das variáveis de ambiente (.env)
│   └── main.py                 # Ponto de entrada da API FastAPI
├── front-end/
│   ├── nginx/                  # Configuração de proxy reverso (/api/) e rotas estáticas
│   ├── pages/                  # Páginas HTML (início, inscrição, revisão, ranking, login, etc.)
│   ├── src/
│   │   ├── pages/              # Controladores TypeScript de cada tela
│   │   ├── services/           # Comunicação HTTP com a API (/api)
│   │   ├── types/              # Tipagens compartilhadas de inscrição e ranking
│   │   └── utils/              # Validadores e armazenamento temporário em sessão
│   ├── styles/                 # Folhas de estilo CSS (identidade visual e responsividade)
│   ├── Dockerfile              # Build TypeScript + servidor Nginx
│   ├── package.json            # Dependências e scripts npm do front-end
│   └── tsconfig.json           # Configuração do compilador TypeScript
├── docs/                       # Visão, DRS, arquitetura, banco de dados, sprints e estudos
├── scripts/                    # Scripts de setup interativo (setup.sh e setup.bat)
├── compose.yaml                # Orquestração Docker Compose (db, api, frontend, scraping)
├── .env.example                # Modelo de variáveis de ambiente
├── como_executar_api.md        # Guia detalhado para execução local passo a passo
└── README.md
```

---

## Como Executar

### Opção 1 — Docker Compose (Recomendada)

Esta é a forma mais rápida e fiel de executar o sistema completo (PostgreSQL, API FastAPI, Front-end com Nginx e inicialização do banco).

#### Pré-requisitos

- [Git](https://git-scm.com)
- [Docker](https://www.docker.com/) com Docker Compose
- [Python 3](https://www.python.org/) (usado pelo script de configuração inicial do `.env`)

#### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-2-MonitoraUnB.git
cd 2026-2-MonitoraUnB
```

#### 2. Configurar as variáveis de ambiente

Execute o script de configuração correspondente ao seu sistema operacional. Ele cria o arquivo `.env` a partir do `.env.example`, gera o hash `bcrypt` da senha do professor, cria a chave de sessão (`SESSION_SECRET`) e define a senha do PostgreSQL:

**Linux / macOS:**

```bash
bash scripts/setup.sh
```

**Windows (Prompt de Comando / PowerShell):**

```bat
scripts\setup.bat
```

> [!IMPORTANT]
> Nunca versione o arquivo `.env` nem salve senhas em texto puro no repositório. O arquivo `.env.example` lista todas as variáveis suportadas (incluindo configurações opcionais de SMTP para envio de e-mails).

#### 3. Iniciar os containers

```bash
docker compose up -d --build
```

Após a inicialização, acesse os serviços no navegador:

| Serviço | Endereço |
| --- | --- |
| Aplicação Web (Monitora UnB) | <http://localhost:3000/pages/inicio.html> *(ou <http://localhost:3000/>)* |
| Documentação da API (Swagger UI) | <http://localhost:8000/docs> |
| Documentação da API (ReDoc) | <http://localhost:8000/redoc> |

Para encerrar os containers:

```bash
docker compose down
```

### Opção 2 — Desenvolvimento Local (Sem Docker para Front-end / Back-end)

Para desenvolver e depurar o front-end e o back-end separadamente em terminais locais, consulte o guia completo em [como_executar_api.md](como_executar_api.md).

#### Scripts disponíveis no `front-end/package.json`

Execute os comandos abaixo dentro da pasta `front-end/`:

| Comando | Descrição |
| --- | --- |
| `npm install` | Instala as dependências do front-end (`typescript`, `pdfjs-dist`) |
| `npm run build` | Compila os arquivos TypeScript (`src/`) para JavaScript (`dist/`) |
| `npm run watch` | Recompila automaticamente o TypeScript a cada alteração |

> [!NOTE]
> Em execução local sem Docker, os arquivos `.html` **não funcionam com duplo clique**, pois utilizam ES Modules. Sirva a pasta `front-end/` por um servidor HTTP local (como `npx serve .` ou a extensão **Live Server** do VS Code) com a API FastAPI rodando em `http://127.0.0.1:8000`.

---

## Como Testar

### 1. Fluxo do Professor (Abrir Processo Seletivo e Ver Ranking)

1. Acesse <http://localhost:3000/pages/inicio.html> e clique em **Sou professor**.
2. Entre com o usuário e a senha configurados no script de setup.
3. Na tela de **Ranking**, clique em **Iniciar processo seletivo**, informe o semestre (ex.: `2026/2`) e as datas de início e fim, e confirme para abrir as inscrições.
4. Após receber candidaturas, filtre por disciplina, alterne a ordenação (ranking ou alfabética) e clique em **Baixar planilha** para gerar o arquivo `.xlsx`.

### 2. Fluxo do Estudante (Inscrição e Validação de Histórico)

1. Com um processo seletivo aberto, acesse <http://localhost:3000/pages/inicio.html> e clique em **Sou aluno**.
2. Preencha seu e-mail, matrícula, código da disciplina, envie o histórico escolar em PDF e marque a declaração sobre bolsa.
3. Clique em **Continuar para revisão**:
   - Se o histórico atender aos critérios (status `ATIVO`, matrícula compatível e aprovação na disciplina), o sistema exibe o resumo em **Revisão**.
   - Caso contrário, o sistema redireciona para a tela **Não apto** exibindo o motivo.
4. Na tela de revisão, confira os dados e clique em **Enviar inscrição** para concluir o registro.

> [!NOTE]
> A validação utiliza o texto embutido no PDF exportado do SIGAA. Históricos digitalizados como imagem ainda não são suportados (OCR previsto no roadmap).

### 3. Testes Automatizados do Back-end

Com o ambiente virtual Python ativo e as dependências instaladas (`pip install -r requirements.txt`), execute na raiz do repositório:

```bash
pytest backend/tests
```

---

## Status e Roadmap

- [x] Protótipo navegável e Story Map no Figma
- [x] Documentação de Visão, Requisitos (DRS), Arquitetura e Banco de Dados
- [x] Fluxo completo do estudante (Início, Inscrição, Revisão, Solicitação e Não Apto)
- [x] API REST em Python + FastAPI integrada ao PostgreSQL 17
- [x] Extração e validação de históricos em PDF (`pypdf`) com cálculo automático de coeficiente
- [x] Scraping de departamentos, disciplinas e docentes do SIGAA UnB
- [x] Autenticação do professor (`bcrypt` + sessão) e gestão de processos seletivos
- [x] Tela de ranking de candidatos com filtro por disciplina e exportação de planilha `.xlsx`
- [x] Containerização com Docker Compose e scripts de setup para Linux/macOS e Windows
- [x] Serviço de notificações por e-mail (SMTP) e suíte inicial de testes em `pytest`
- [ ] Integração do botão de disparo de e-mails aos aprovados na tela de ranking
- [ ] Persistência das decisões individuais de aprovação/reprovação na interface administrativa
- [ ] Reconhecimento automático de disciplinas equivalentes na validação do histórico
- [ ] Suporte a PDFs digitalizados como imagem via OCR

---

## Documentação

| Documento | Descrição |
| --- | --- |
| [Documento de Visão](docs/Documento_de_visao.md) | Problema, público-alvo, visão do produto, releases e riscos |
| [Documento de Requisitos (DRS)](docs/Documento_de_requisitos.md) | Requisitos funcionais, não funcionais, regras de negócio e critérios de aceitação |
| [Documento de Arquitetura](docs/arquitetura.md) | Visão geral da arquitetura, componentes e comunicação do sistema |
| [Arquitetura do Banco de Dados](docs/Documento_banco.md) | Modelagem inicial e responsabilidades do banco de dados |
| [API de Scraping do SIGAA](docs/Documentação%20da%20API%20de%20Scraping.md) | Endpoints e funcionamento da coleta pública de disciplinas e docentes |
| [Guia de Execução Local da API](como_executar_api.md) | Passo a passo para rodar back-end, Swagger e front-end localmente |
| [Protótipo Navegável (Figma)](https://panic-iso-13327902.figma.site/) | Protótipo de interface e fluxo das telas |
| [Story Map (FigJam)](https://www.figma.com/board/uMI0chh0NXErrtzv5eDBgr/FigJam-basics?node-id=0-1&p=f&t=BSS0Q8BY5yVRBwKL-0) | Mapeamento de histórias de usuário e entregas |

---

## Equipe

Projeto desenvolvido colaborativamente pelo **Grupo 11** para a disciplina de **Métodos de Desenvolvimento de Software (MDS)** da **Universidade de Brasília (UnB) — FCTE (antiga FGA)**.

<table align="center">
  <tr>
    <td align="center" width="180">
      <a href="https://github.com/AnaBiaGuerra">
        <img src="https://github.com/AnaBiaGuerra.png?size=100" width="90" alt="Ana Beatriz Nogueira Ferreira Guerra"><br>
        <sub><b>Ana Beatriz Guerra</b></sub>
      </a><br>
      <sub>Product Owner</sub>
    </td>
    <td align="center" width="180">
      <a href="https://github.com/Aquila27">
        <img src="https://github.com/Aquila27.png?size=100" width="90" alt="João Áquila"><br>
        <sub><b>João Áquila</b></sub>
      </a><br>
      <sub>Scrum Master</sub>
    </td>
    <td align="center" width="180">
      <a href="https://github.com/MariaMacedoToledo">
        <img src="https://github.com/MariaMacedoToledo.png?size=100" width="90" alt="Maria Eduarda Macedo Toledo"><br>
        <sub><b>Maria Eduarda Toledo</b></sub>
      </a><br>
      <sub>Desenvolvedora</sub>
    </td>
    <td align="center" width="180">
      <a href="https://github.com/pablosousaa">
        <img src="https://github.com/pablosousaa.png?size=100" width="90" alt="Pablo Antonio"><br>
        <sub><b>Pablo Antonio</b></sub>
      </a><br>
      <sub>Desenvolvedor</sub>
    </td>
  </tr>
</table>

<table align="center">
  <tr>
    <td align="center" width="180">
      <a href="https://github.com/iurikoboldt">
        <img src="https://github.com/iurikoboldt.png?size=100" width="90" alt="Iuri Capanema Souza Koboldt"><br>
        <sub><b>Iuri Koboldt</b></sub>
      </a><br>
      <sub>Desenvolvedor</sub>
    </td>
    <td align="center" width="180">
      <a href="https://github.com/vitormorhy">
        <img src="https://github.com/vitormorhy.png?size=100" width="90" alt="Vitor Piau Morhy"><br>
        <sub><b>Vitor Piau Morhy</b></sub>
      </a><br>
      <sub>Desenvolvedor</sub>
    </td>
    <td align="center" width="180">
      <a href="https://github.com/Vinicius-Eugenio-337">
        <img src="https://github.com/Vinicius-Eugenio-337.png?size=100" width="90" alt="Vinicius Eugênio Montalvão Silva"><br>
        <sub><b>Vinicius Eugênio</b></sub>
      </a><br>
      <sub>Desenvolvedor</sub>
    </td>
  </tr>
</table>

---

## Uso de IA no Projeto

Utilizamos ferramentas de IA como apoio ao desenvolvimento, principalmente para **revisão e correção** do que o grupo já produziu, e não para gerar os artefatos sem participação ativa da equipe.

**Como usamos:**

- Revisar documentos (requisitos, story map, documento de visão e documentação técnica) contra os critérios da disciplina;
- Apontar inconsistências, requisitos mal escritos e lacunas técnicas;
- Sugerir reescritas, refatorações e melhorias de clareza, que o grupo avalia antes de aceitar.

**O que continua sendo feito pelo grupo:**

- Decisões de escopo, regras de negócio e arquitetura;
- Definição dos requisitos e do fluxo do produto;
- Implementação, integração e validação do código.

Todo conteúdo sugerido por IA é revisado e validado pelo grupo antes de entrar no projeto.

---

<div align="center">

<strong>Monitora UnB</strong> | Grupo 11 | Métodos de Desenvolvimento de Software — UnB / FCTE (2026/2)

</div>
