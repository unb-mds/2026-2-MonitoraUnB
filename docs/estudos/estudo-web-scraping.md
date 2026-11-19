# Estudo sobre Web Scraping

## 1. Introdução

Web scraping é uma técnica utilizada para extrair informações de páginas da internet de maneira automatizada. Em vez de acessar cada página manualmente e copiar os dados necessários, um programa pode realizar essa tarefa e organizar as informações obtidas.

Essa técnica pode ser útil em projetos que precisam coletar informações disponíveis em sites para posterior análise, armazenamento ou apresentação.

## 2. O que é Web Scraping?

Web scraping é o processo de acessar páginas web por meio de um programa e identificar os dados desejados dentro do conteúdo recebido.

Geralmente, o processo envolve realizar uma requisição a uma página, analisar o HTML retornado e localizar os elementos que contêm as informações necessárias. Os dados extraídos podem então ser organizados em estruturas como listas, tabelas ou arquivos.

## 3. Como funciona o Web Scraping?

De maneira geral, o processo pode ser dividido nas seguintes etapas:

1. **Acesso à página:** o programa realiza uma requisição para obter o conteúdo de uma página web.
2. **Recebimento do conteúdo:** o servidor pode retornar HTML contendo textos, links e outros elementos da página.
3. **Análise do HTML:** o programa interpreta a estrutura do documento para localizar as informações desejadas.
4. **Extração dos dados:** as informações identificadas são coletadas e organizadas.
5. **Armazenamento:** os dados podem ser salvos em um arquivo ou enviados para um banco de dados.

Essas etapas podem variar conforme a estrutura do site e a forma como as informações são disponibilizadas.

## 4. HTML e extração de informações

HTML é a linguagem de marcação utilizada para estruturar o conteúdo de páginas web. Ele organiza elementos como títulos, parágrafos, tabelas, links e outros componentes.

No web scraping, conhecer a estrutura HTML é importante para identificar onde estão os dados desejados. Por exemplo, uma informação pode estar dentro de uma tabela, de um parágrafo ou de um elemento identificado por uma classe ou um atributo específico.

Quando a página utiliza JavaScript para carregar informações dinamicamente, pode ser necessário um método adicional para acessar os dados que não aparecem diretamente no HTML inicial.

## 5. Bibliotecas utilizadas em Python

Python possui bibliotecas que facilitam a coleta e a análise de informações de páginas web. Entre as mais conhecidas estão:

- **Requests:** permite realizar requisições HTTP para acessar recursos disponibilizados por servidores.
- **Beautiful Soup:** facilita a análise de documentos HTML e XML e a localização de elementos específicos.
- **Selenium:** permite automatizar um navegador, sendo útil em situações que exigem interação com páginas ou carregamento de conteúdo dinâmico.

A escolha da ferramenta depende das características do site e das necessidades da coleta. Nem todo projeto precisa utilizar todas essas bibliotecas.

## 6. Diferença entre Web Scraping e API

Embora possam ser utilizadas para obter informações de sistemas externos, APIs e web scraping funcionam de maneiras diferentes.

Uma API disponibiliza uma interface definida para que outros programas acessem determinados dados ou funcionalidades. Já o web scraping extrai informações a partir do conteúdo de páginas web.

Quando um site disponibiliza uma API adequada e autorizada para o uso pretendido, ela pode ser uma alternativa mais estável e estruturada. O scraping pode ser considerado quando os dados necessários estão disponíveis em páginas web e não existe uma interface apropriada para obtê-los.

## 7. Cuidados ao realizar Web Scraping

Antes de realizar uma coleta automatizada, é importante considerar alguns cuidados:

- Verificar os termos de uso do site e as regras aplicáveis à coleta.
- Consultar o arquivo `robots.txt` como uma referência sobre as orientações de acesso automatizado do site, lembrando que ele não substitui os termos de uso nem a legislação aplicável.
- Evitar requisições excessivas que possam sobrecarregar o servidor.
- Respeitar mecanismos de autenticação, controles de acesso e medidas de segurança.
- Avaliar se os dados coletados podem ser utilizados para a finalidade pretendida, especialmente quando envolverem informações pessoais.
- Considerar que mudanças na estrutura da página podem fazer o programa deixar de localizar os dados corretamente.

## 8. Conclusão

Web scraping é uma técnica de automação que permite coletar e organizar informações disponíveis em páginas web. Seu funcionamento envolve acessar o conteúdo de uma página, analisar sua estrutura, extrair os dados desejados e, quando necessário, armazená-los para uso posterior.

A escolha das ferramentas e dos métodos depende das características do site, dos dados necessários e das regras aplicáveis à coleta.

## 9. Referências

- Requests — documentação oficial: https://requests.readthedocs.io/en/latest/
- Beautiful Soup — documentação oficial: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- Selenium — documentação oficial: https://www.selenium.dev/documentation/
- MDN Web Docs — HTML: https://developer.mozilla.org/pt-BR/docs/Web/HTML
