## Sobre o projeto
 
O **Monitora-UnB** é um sistema web que organiza o processo de inscrição para monitoria na **Universidade de Brasília (UnB)**, de forma **simples, guiada e transparente**.
 
Hoje, candidatar-se a uma vaga de monitoria costuma envolver etapas dispersas, informações digitadas manualmente e pouca visibilidade sobre o andamento da candidatura. O Monitora-UnB reúne esse processo em um único fluxo: o estudante envia o histórico escolar em PDF, escolhe a disciplina desejada, confere os dados extraídos automaticamente e registra a candidatura, que segue para análise.
 
O projeto busca incentivar a participação de estudantes na monitoria, valorizando quem domina uma disciplina e deseja contribuir com o aprendizado de outros alunos, ao mesmo tempo em que reduz erros de preenchimento e torna o processo mais claro para quem se candidata e para quem avalia.
 
Projeto desenvolvido colaborativamente para a disciplina de **Métodos de Desenvolvimento de Software (MDS)** da **Universidade de Brasília, Faculdade do Gama (FGA)**, no semestre 2026/2.
 
**Figma do projeto:** [Protótipo navegável](https://panic-iso-13327902.figma.site/)
 
## Tecnologias
 
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white) ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
 
| Camada | Tecnologia |
| ------ | ---------- |
| Front-end | HTML, CSS e TypeScript |
| Back-end (planejado) | Python com FastAPI |
 
![Status](https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-yellow?style=flat-square) ![Front-end](https://img.shields.io/badge/FRONT--END-CONCLU%C3%8DDO-brightgreen?style=flat-square) ![Back-end](https://img.shields.io/badge/BACK--END-EM%20DESENVOLVIMENTO-yellow?style=flat-square)
 
## Documentação
 
A documentação detalhada do projeto está disponível na pasta [`docs/`](https://github.com/unb-mds/2026-2-MonitoraUnB/tree/main/docs).
 
## Funcionalidades
 
O fluxo do sistema é composto por quatro telas:
 
## Papéis
 
- **Scrum Master:** João Áquila ([@Aquila27](https://github.com/Aquila27))
- **Product Owner:** Ana Beatriz ([@AnaBiaGuerra](https://github.com/AnaBiaGuerra))
## Participantes
 
Projeto desenvolvido colaborativamente pelos integrantes do Grupo 11.
 
## Estrutura do repositório
 
```
2026-2-MonitoraUnB/
├── docs/
├── front-end/
│   ├── pages/
│   ├── src/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   ├── styles/
│   ├── package.json
│   └── tsconfig.json
├── python_scripts/
└── README.md
```
 
- **`front-end/pages`:** as telas HTML (`portal`, `inscricao`, `revisao` e `solicitacao`);
- **`src/pages`:** o código TypeScript de cada tela;
- **`src/services`:** extrai texto real dos PDFs no navegador com PDF.js. O envio definitivo ainda depende da API de inscrições, que não está implementada;
- **`src/types`:** os tipos que descrevem os dados que passam entre as telas;
- **`src/utils`:** funções auxiliares (validação de PDF, formatação do IRA e armazenamento temporário no navegador).
## Como executar o front-end
 
### Pré-requisitos
 
- [Node.js](https://nodejs.org) (versão LTS)
- [Git](https://git-scm.com)
### 1. Clonar o repositório
 
```bash
git clone https://github.com/unb-mds/2026-2-MonitoraUnB.git
cd 2026-2-MonitoraUnB/front-end
```
 
### 2. Instalar as dependências
 
```bash
npm install
```
 
### 3. Compilar o TypeScript
 
```bash
npm run build
```
 
Isso gera a pasta `dist` com os arquivos JavaScript usados pelas páginas. Para recompilar automaticamente a cada alteração:
 
```bash
npm run watch
```
 
### 4. Abrir no navegador
 
Os arquivos HTML não funcionam com duplo clique, porque usam módulos JavaScript. Sirva o projeto por um servidor local:
 
```bash
npx serve .
```
 
Execute o comando dentro de `front-end`. Depois abra o endereço mostrado no terminal, seguido de `/pages/portal.html` (por exemplo: <http://localhost:3000/pages/portal.html>).
 
Como alternativa, use a extensão **Live Server** do VS Code. Mantenha as pastas `dist` e `node_modules` dentro de `front-end`, pois a página de inscrição carrega os módulos compilados e o PDF.js a partir delas.
 
## Como testar
 
**Fluxo normal**
 
1. No portal, clique em **Fazer inscrição**;
2. Escolha um PDF e uma disciplina e clique em **Continuar para revisão**;
3. Confira o resumo na tela de revisão;
4. O botão **Enviar** informa que a gravação ainda depende da API de inscrições.
> A leitura usa o texto embutido no PDF e procura nome, matrícula e IRA. PDFs digitalizados como imagem precisam de OCR, que ainda não está implementado. O envio definitivo também depende da API de inscrições.
 
## Uso de IA no projeto
 
Usamos IA (Claude) como ferramenta de apoio, principalmente para **revisão e correção** do que o grupo já produziu, e não para gerar os artefatos do zero.
 
**Como usamos:**
 
- Revisar documentos (requisitos, story map, documento de visão) contra os critérios da disciplina;
- Apontar inconsistências, requisitos mal escritos e lacunas;
- Sugerir reescritas, que o grupo avalia antes de aceitar.
**O que continua sendo feito pelo grupo:**
 
- Decisões de escopo, regras de negócio e arquitetura;
- Definição dos requisitos e do fluxo do produto;
- Implementação e testes do código.
Todo conteúdo sugerido pela IA é revisado e validado pelo grupo antes de entrar no projeto.
 
