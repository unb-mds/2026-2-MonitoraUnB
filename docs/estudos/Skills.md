Agentes de IA, LLMs e Skills

Uma LLM (Large Language Model) é um modelo de inteligência artificial especializado em compreender e gerar linguagem natural. Ela é responsável por interpretar uma entrada do usuário e produzir uma resposta com base no conhecimento e no contexto fornecidos. Exemplos de LLMs são GPT, Claude e Gemini.

Um Agente de IA é um sistema que utiliza uma LLM como componente de raciocínio, mas que também possui acesso a ferramentas, dados e regras que permitem executar tarefas de forma mais autônoma. Diferentemente de uma LLM isolada, o agente pode analisar uma solicitação, decidir quais ações são necessárias, utilizar ferramentas externas, avaliar os resultados e continuar o processo até atingir um objetivo.

As Skills são capacidades específicas disponibilizadas para o agente. Elas normalmente representam uma função, ferramenta ou conjunto de instruções que permite realizar uma determinada tarefa. Uma skill pode, por exemplo, consultar um banco de dados, realizar um cálculo, buscar informações, validar dados ou executar uma operação em outro sistema.

De forma simplificada:

LLM → interpreta e raciocina sobre informações.
Agente → utiliza a LLM para decidir o que fazer e executar ações.
Skill → fornece ao agente uma capacidade específica para realizar uma ação.

Aplicação no projeto "Sua Grade"

No projeto Sua Grade, os agentes de IA poderiam ser utilizados para auxiliar o aluno na construção e organização de sua grade acadêmica. O agente poderia acessar dados reais do sistema e utilizar diferentes skills para realizar as etapas necessárias.

Por exemplo, ao receber uma solicitação como "monte minha grade para o próximo semestre", o agente poderia:

1. Interpretar as preferências e necessidades do aluno utilizando a LLM;
2. Consultar as disciplinas disponíveis;
3. Verificar os pré-requisitos das disciplinas;
4. Identificar os horários disponíveis;
5. Verificar possíveis conflitos de horário;
6. Considerar restrições definidas pelo aluno;
7. Montar uma ou mais opções de grade;
8. Apresentar a melhor alternativa ao usuário.

Nesse cenário, cada uma dessas operações pode ser implementada como uma skill específica, como "consultar_disciplinas", "verificar_pre_requisitos", "verificar_conflitos" e "montar_grade".

Implementação em um site

Em uma aplicação web, a arquitetura pode ser organizada de forma que o usuário interaja com o site, que encaminha a solicitação para o agente. O agente utiliza a LLM para interpretar o pedido e, quando necessário, chama as skills disponíveis. Essas skills podem se comunicar com APIs, bancos de dados ou outros serviços do sistema.

Um fluxo simplificado seria:

Usuário → Site → Agente → LLM → Skills → Banco de dados/APIs → Agente → Resposta ao usuário

Dessa forma, a LLM não precisa possuir todas as informações necessárias internamente. Ela pode utilizar as skills para obter dados atualizados e executar operações específicas.

Onde encontrar ou criar Skills

Skills não precisam necessariamente ser encontradas prontas. Em muitos projetos, elas são desenvolvidas pela própria equipe de acordo com as necessidades da aplicação.

Para o desenvolvimento, é possível pesquisar por ferramentas e projetos relacionados a AI Agents, Agent Skills, Tool Calling, Function Calling e MCP (Model Context Protocol). Também existem frameworks que facilitam a criação de agentes e a integração de ferramentas.

Para o Sua Grade, por exemplo, a equipe poderia desenvolver skills próprias para:

- Consulta de disciplinas;
- Consulta de horários;
- Verificação de pré-requisitos;
- Identificação de conflitos;
- Cálculo de carga horária;
- Montagem e otimização da grade;
- Consulta de informações acadêmicas.

Assim, as skills funcionam como uma camada de integração entre o agente de IA e os recursos reais da aplicação, permitindo que o sistema deixe de apenas gerar respostas e passe a executar tarefas de forma estruturada.
