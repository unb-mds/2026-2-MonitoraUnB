
# Estudo sobre APIs

## 1. Introdução

Durante o desenvolvimento de um sistema, é comum que diferentes aplicações precisem trocar informações entre si. É nesse contexto que entram as APIs, que permitem a comunicação entre sistemas e facilitam o acesso a determinados dados e funcionalidades.

Este estudo tem como objetivo explicar o que é uma API, como ela funciona e de que maneira pode ser utilizada no projeto Monitora UnB.

## 2. O que é uma API?

API é a sigla para *Application Programming Interface*, ou Interface de Programação de Aplicações, em português.

De forma simples, uma API funciona como um meio de comunicação entre programas. Ela define como uma aplicação pode solicitar informações ou utilizar funcionalidades disponibilizadas por outro sistema, sem precisar conhecer todos os detalhes de seu funcionamento interno.

Um exemplo cotidiano seria um aplicativo de previsão do tempo. Em vez de coletar todas as informações meteorológicas por conta própria, ele pode consultar uma API que fornece os dados necessários e depois apresentá-los ao usuário de maneira organizada.

Assim, as APIs ajudam diferentes sistemas a trabalhar em conjunto, tornando o desenvolvimento de aplicações mais organizado e facilitando o reaproveitamento de informações.

## 3. Como uma API funciona?

Uma API funciona, geralmente, por meio de uma comunicação entre um cliente e um servidor.

O cliente é o sistema que solicita uma informação ou serviço, enquanto o servidor recebe a solicitação, realiza o processamento necessário e devolve uma resposta.

Em APIs web, essa comunicação costuma acontecer por meio do protocolo HTTP, utilizado na troca de informações pela internet.

O funcionamento básico pode ser dividido em três etapas:

1. **Solicitação:** o cliente envia uma requisição para a API, informando o que deseja consultar ou realizar.
2. **Processamento:** a API interpreta a solicitação e executa a operação necessária, que pode envolver uma consulta ao banco de dados ou a outro serviço.
3. **Resposta:** a API devolve o resultado ao cliente, geralmente em um formato estruturado.

Uma resposta bastante utilizada é o JSON (*JavaScript Object Notation*), um formato de texto que organiza informações em pares de chave e valor. Por ser simples de ler e interpretar, ele é comum na comunicação entre aplicações.

## 4. O que são endpoints?

Os endpoints são os endereços específicos pelos quais uma API disponibiliza suas funcionalidades. Cada endpoint pode ser utilizado para uma finalidade, como consultar informações, cadastrar dados ou realizar alguma operação.

Por exemplo, uma API responsável por organizar informações sobre disciplinas poderia disponibilizar um endereço para listar as disciplinas cadastradas e outro para consultar uma disciplina específica.

Além do endereço, as APIs podem utilizar diferentes métodos HTTP para indicar o tipo de operação desejada. Entre os mais comuns estão:

- **GET:** utilizado para consultar informações.
- **POST:** utilizado para enviar dados ou solicitar a criação de um recurso ou a execução de uma operação.
- **PUT:** utilizado geralmente para substituir ou atualizar um recurso.
- **DELETE:** utilizado para excluir um recurso.

Esses métodos ajudam a organizar as operações disponíveis e tornam mais claro o funcionamento da API.

## 5. Vantagens do uso de APIs

O uso de APIs pode trazer diversas vantagens para o desenvolvimento de aplicações:

- **Integração:** permite que diferentes partes de um sistema ou aplicações distintas troquem informações.
- **Organização:** separa responsabilidades e facilita a manutenção do projeto.
- **Reutilização:** possibilita que diferentes componentes utilizem os mesmos dados e funcionalidades.
- **Padronização:** define maneiras consistentes de solicitar e receber informações.
- **Flexibilidade:** permite modificar uma parte do sistema sem necessariamente alterar todas as outras, desde que a interface de comunicação seja mantida.

Apesar dessas vantagens, uma API também precisa ser planejada considerando segurança, tratamento de erros, validação dos dados e disponibilidade dos serviços dos quais depende.

## 6. Considerações finais

O estudo permitiu compreender que as APIs são importantes para a comunicação entre aplicações e para a disponibilização organizada de dados e funcionalidades.

Também foi possível distinguir o papel de uma API do papel do web scraping. Enquanto o scraping pode ser utilizado para coletar informações de páginas da web, uma API própria pode oferecer uma forma padronizada de consultar os dados obtidos.

Para o Monitora UnB, compreender esses conceitos é uma etapa importante para planejar a integração entre a coleta de informações e as demais partes do sistema. A implementação deverá considerar as necessidades do projeto, a origem dos dados e a maneira como eles serão utilizados.

## 7. Referências

- MDN Web Docs. **Uma introdução ao HTTP.** Disponível em: https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Overview
- FastAPI. **Documentação oficial.** Disponível em: https://fastapi.tiangolo.com/
- MDN Web Docs. **Trabalhando com JSON.** Disponível em: https://developer.mozilla.org/pt-BR/docs/Learn_web_development/Core/Scripting/JSON
