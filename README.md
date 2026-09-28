# 🎓 Monitora-UnB

> **Candidate-se a uma vaga de monitor e contribua com o aprendizado nas disciplinas que você domina.** Um portal para simplificar a inscrição em monitorias da Universidade de Brasília.

---

## 📖 Sobre o Projeto

O **Monitora-UnB** é um sistema web que organiza o processo de inscrição para monitoria na **Universidade de Brasília**, de forma **simples, guiada e transparente**.

O estudante envia o histórico escolar em PDF, escolhe a disciplina desejada, confere os dados extraídos e registra a candidatura, que segue para análise.

O fluxo do sistema é composto por quatro telas:

1. **Portal:** apresentação do sistema e acesso à inscrição;
2. **Inscrição:** envio do histórico em PDF e escolha da disciplina;
3. **Revisão:** conferência dos dados (aluno, matrícula, semestre, disciplina e IRA) antes do envio;
4. **Solicitação:** confirmação de que a inscrição foi registrada e encaminhada para análise.

**Figma do nosso projeto:** [(https://panic-iso-13327902.figma.site/)]

### 👥 Papéis

- **Scrum Master:** [preencher] — [@usuario](https://github.com/usuario)
- **Product Owner:** [preencher] — [@usuario](https://github.com/usuario)

---

## 👥 Equipe

Projeto desenvolvido colaborativamente para a disciplina de **Métodos de Desenvolvimento de Software (MDS)** da **Universidade de Brasília — Faculdade do Gama (FGA)**.

| Nome | GitHub |
| ---- | ------ |
| Ana Beatriz Nogueira Ferreira Guerra | [@AnaBiaGuerra](https://github.com/AnaBiaGuerra) |
| Maria Eduarda Macedo Toledo | [@MariaMaacedoToledo](https://github.com/MariaMacedoToledo) |
| João Áquila | [@Aquila27](https://github.com/Aquila27) |
| Pablo Antonio | [@pablosousaa](https://github.com/pablosousaa) |
| Iuri Capanema Souza Koboldt | [@iurikoboldt](https://github.com/iurikoboldt) |
| Vitor Piau Morhy | [@vitormorhy](https://github.com/vitormorhy) |
| Vinicius Eugênio Montalvão Silva | [@Vinicius-Eugenio-337](https://github.com/Vinicius-Eugenio-337) |


---

## 🛠️ Tecnologias

| Camada | Tecnologia |
| ------ | ---------- |
| Front-end | HTML, CSS e TypeScript |
| Back-end (planejado) | Python com FastAPI |

---

## 🗂️ Estrutura do Repositório

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

## 🚀 Como Executar o Front-end

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

## 🧪 Como Testar

**Fluxo normal**

1. No portal, clique em **Fazer inscrição**;
2. Escolha um PDF e uma disciplina e clique em **Continuar para revisão**;
3. Confira o resumo na tela de revisão;
4. Clique em **Enviar** e verifique a tela de confirmação.

> Enquanto o back-end não existe, os dados do resumo (aluno, matrícula e IRA) são fixos, pois a leitura do PDF é simulada.

## 📚 Documentação

A documentação detalhada do projeto está disponível na pasta `docs/`

* [Documento de Visão](docs/Documento_de_visao.md)
* [Requisitos](docs/Documento_de_requisitos.md)
* [Story Map](https://www.figma.com/board/uMI0chh0NXErrtzv5eDBgr/FigJam-basics?node-id=0-1&p=f)

---

