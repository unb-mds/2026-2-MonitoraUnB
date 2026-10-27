#  Monitora-UnB

> **Candidate-se a uma vaga de monitor e contribua com o aprendizado nas disciplinas que você domina.** Um portal para simplificar a inscrição em monitorias da Universidade de Brasília.

---

##  Sobre o Projeto

O **Monitora-UnB** é um sistema web que organiza o processo de inscrição para monitoria na **Universidade de Brasília**, de forma **simples, guiada e transparente**.

O estudante envia o histórico escolar em PDF, escolhe a disciplina desejada, confere os dados extraídos e registra a candidatura, que segue para análise.

O fluxo do sistema é composto por quatro telas:

1. **Portal:** apresentação do sistema e acesso à inscrição;
2. **Inscrição:** envio do histórico em PDF e escolha da disciplina;
3. **Revisão:** conferência dos dados (aluno, matrícula, semestre, disciplina e IRA) antes do envio;
4. **Solicitação:** confirmação de que a inscrição foi registrada e encaminhada para análise.

**Figma do nosso projeto:** [Acessar Protótipo](https://panic-iso-13327902.figma.site/)

---


##  Tecnologias

**Front-end: **
![TypeScript](https://img.shields.io/badge/TypeScript-00273F?style=for-the-badge&logo=typescript&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

**Back-end: **
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white)
---

##  Estrutura do Repositório

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
- **`src/services`:** único ponto de comunicação com o back-end. Hoje a leitura do histórico e o envio da inscrição são simulados, e a troca por chamadas reais à API não exige mudanças nas telas;
- **`src/types`:** os tipos que descrevem os dados que passam entre as telas;
- **`src/utils`:** funções auxiliares (validação de PDF, formatação do IRA e armazenamento temporário no navegador).

---

##  Como Executar o Front-end

### Pré-requisitos

- [Node.js](https://nodejs.org) (versão LTS)
- [Git](https://git-scm.com)

### 1. Clonar o repositório

```
git clone https://github.com/unb-mds/2026-2-MonitoraUnB.git
cd 2026-2-MonitoraUnB/front-end
```

### 2. Instalar as dependências

```
npm install
```

### 3. Compilar o TypeScript

```
npx tsc
```

Isso gera a pasta `dist` com os arquivos JavaScript usados pelas páginas. Para recompilar automaticamente a cada alteração:

```
npx tsc --watch
```

### 4. Abrir no navegador

Os arquivos HTML não funcionam com duplo clique, porque usam módulos JavaScript. Sirva o projeto por um servidor local:

```
npx serve
```

Depois acesse: <http://localhost:3000/pages/portal.html>

Como alternativa, use a extensão **Live Server** do VS Code.

---

## Como Testar

**Fluxo normal**

1. No portal, clique em **Fazer inscrição**;
2. Escolha um PDF e uma disciplina e clique em **Continuar para revisão**;
3. Confira o resumo na tela de revisão;
4. Clique em **Enviar** e verifique a tela de confirmação.

> Enquanto o back-end não existe, os dados do resumo (aluno, matrícula e IRA) são fixos, pois a leitura do PDF é simulada.

##  Documentação

A documentação detalhada do projeto está disponível na pasta `docs/`

* [Documento de Visão](Documento_de_visao.md)
* [Requisitos](Documento_de_requisitos.md)
* [Story Map](https://www.figma.com/board/uMI0chh0NXErrtzv5eDBgr/FigJam-basics?node-id=0-1&t=rR0RBrdPOzg5dRKE-1)

---
