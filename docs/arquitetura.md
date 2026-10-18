# Documento de Arquitetura — MonitoraUnB

## 1. Introdução

Este documento apresenta a arquitetura de software do MonitoraUnB, descrevendo seus componentes, responsabilidades, tecnologias e formas de comunicação.

O objetivo é estabelecer uma estrutura modular que facilite o desenvolvimento, a manutenção, os testes e a expansão do sistema.

## 2. Visão Geral da Arquitetura

O sistema adota uma arquitetura cliente-servidor, com separação entre frontend, backend, processamento de históricos acadêmicos e persistência de dados.

**Fluxo principal:**

```text
Usuário
   │
   ▼
Frontend
   │ HTTP/JSON
   ▼
API REST (FastAPI)
   │
   ├── Processamento de históricos PDF
   │
   ├── Regras de negócio de monitoria
   │
   ├── Integração com scraping do SIGAA
   │
   └── Banco de dados MySQL
```

## 3. Componentes do Sistema

### 3.1 Frontend

Responsável pela interface com o usuário, incluindo seleção de disciplinas, envio de históricos acadêmicos e inscrição em monitorias.

Comunica-se com o backend por meio de requisições HTTP.

### 3.2 Backend — API REST

Desenvolvido em Python com FastAPI.

Responsabilidades:

- Disponibilizar endpoints REST.
- Receber e validar requisições.
- Coordenar a execução dos serviços.
- Aplicar as regras de negócio.
- Retornar respostas estruturadas ao frontend.

### 3.3 Processamento de Históricos

Responsável pela leitura e interpretação dos históricos acadêmicos em PDF, utilizando Python, `pypdf` e expressões regulares.

Principais módulos:

- `leiturapdf.py`: extrai dados acadêmicos do estudante.
- `leitura_creditos.py`: identifica disciplinas, menções, créditos e períodos.
- `calcular_coeficiente.py`: calcula o coeficiente utilizado na inscrição, conforme a regra de negócio definida.

### 3.4 Scraping do SIGAA

Responsável pela coleta de informações públicas sobre disciplinas disponibilizadas pelo SIGAA da UnB.

A integração deve ser modular, permitindo sua manutenção e eventual execução independente do restante do backend.

### 3.5 Banco de Dados

O MySQL será utilizado para armazenar informações persistentes do sistema, incluindo disciplinas e outros registros necessários às funcionalidades futuras.

## 4. Organização do Código

```text
backend/
├── main.py
├── routers/
│   ├── historico.py
│   ├── disciplinas.py
│   └── inscricoes.py
├── services/
│   └── historico/
│       ├── leiturapdf.py
│       ├── leitura_creditos.py
│       └── calcular_coeficiente.py
├── scraping/
│   └── sigaa.py
└── database/
```

## 5. Comunicação entre Componentes

O frontend envia requisições HTTP para a API REST.

Os endpoints delegam o processamento aos serviços correspondentes, evitando concentrar regras de negócio diretamente nas rotas.

Após o processamento, a API retorna respostas JSON, incluindo os dados extraídos ou mensagens de erro.

## 6. Decisões Arquiteturais

- **FastAPI:** framework escolhido para implementar a API REST.
- **Python:** linguagem utilizada no backend e no processamento dos históricos.
- **MySQL:** banco de dados relacional planejado para persistência.
- **Modularização:** separação entre rotas, serviços, scraping e persistência.
- **Separação de responsabilidades:** a lógica acadêmica permanece independente da camada HTTP.

## 7. Evolução da Arquitetura

A estrutura proposta deve permitir a incorporação gradual de novas funcionalidades, como autenticação de professores e administradores, gerenciamento de inscrições, integração com banco de dados e ampliação da coleta de dados do SIGAA.

O scraping poderá futuramente ser executado como serviço independente, caso seus requisitos de processamento ou implantação justifiquem essa separação.

## 8. Considerações Finais

A arquitetura proposta busca manter o MonitoraUnB organizado e expansível, permitindo que diferentes integrantes desenvolvam e testem seus componentes de maneira independente, com menor acoplamento entre as funcionalidades.
