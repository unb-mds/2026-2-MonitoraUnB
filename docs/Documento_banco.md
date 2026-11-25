# Estrutura e Organização do Banco de Dados do Monitora-UnB
 
## 1. Visão geral
 
O banco de dados do sistema Monitora UnB foi desenvolvido utilizando o PostgreSQL e tem como objetivo armazenar, organizar e gerenciar as informações necessárias para o funcionamento dos processos seletivos de monitoria da Universidade de Brasília.
 
Sua estrutura foi planejada para atender às principais etapas do processo, desde a abertura de um edital e a realização das inscrições pelos estudantes até a classificação dos candidatos, o registro das decisões da comissão responsável e o envio dos resultados por e-mail.
 
A modelagem busca garantir a integridade e a consistência das informações, evitando duplicidades e restringindo operações que possam comprometer as regras estabelecidas para o processo seletivo. Além disso, considera que os processos possuem duração semestral e que os dados operacionais dos estudantes não precisam ser mantidos após a conclusão do processo e o envio de todas as notificações.
 
## 2. Organização das tabelas
 
O banco de dados é composto por seis tabelas principais: `aluno`, `usuario_administrador`, `disciplina`, `processo_seletivo`, `inscricao` e `resultado`. Cada uma possui uma responsabilidade específica dentro do sistema.
 
### 2.1. Tabela `aluno`
 
A tabela `aluno` armazena os dados cadastrais dos estudantes que participam do processo seletivo. São registrados o identificador interno do aluno, sua matrícula, seu nome e seu endereço de e-mail.
 
A matrícula é utilizada como identificador acadêmico único, impedindo que um mesmo estudante seja cadastrado mais de uma vez. O endereço de e-mail é utilizado posteriormente para o envio das notificações referentes ao resultado da inscrição.
 
### 2.2. Tabela `usuario_administrador`
 
A tabela `usuario_administrador` armazena as informações de acesso do responsável pela administração do processo seletivo, representando a conta da comissão responsável pela seleção.
 
São armazenados o identificador do usuário, o e-mail utilizado para autenticação, o hash da senha e a situação da conta, que indica se ela está ativa ou inativa.
 
A utilização de uma conta administrativa permite que o acesso ao sistema permaneça associado à comissão, mesmo que ocorra uma substituição do professor responsável.
 
### 2.3. Tabela `disciplina`
 
A tabela `disciplina` contém o cadastro das disciplinas disponíveis para participação no processo seletivo. Cada disciplina possui um identificador interno, um código e um nome.
 
O código da disciplina é único, evitando registros duplicados. Essa tabela permite relacionar cada inscrição à disciplina correspondente e organizar a classificação dos candidatos de acordo com a disciplina escolhida.
 
### 2.4. Tabela `processo_seletivo`
 
A tabela `processo_seletivo` registra os processos seletivos realizados pelo sistema.
 
Cada registro possui um identificador, o usuário administrador responsável, o semestre correspondente, as datas de abertura e encerramento e o status do processo.
 
O status pode assumir três valores: `AGENDADO`, `ABERTO` ou `ENCERRADO`.
 
Essa organização permite controlar o período de funcionamento das inscrições e identificar se determinado processo está disponível para receber novos candidatos. O banco também possui uma restrição que impede a existência de mais de um processo com status `ABERTO` simultaneamente.
 
### 2.5. Tabela `inscricao`
 
A tabela `inscricao` é responsável por armazenar as informações acadêmicas e os dados referentes à participação dos estudantes no processo seletivo.
 
Cada inscrição está relacionada a um aluno, a uma disciplina e a um processo seletivo. Também são armazenados o IRA, a menção obtida na disciplina, o coeficiente calculado, o caminho do arquivo do histórico acadêmico e a data de realização da inscrição.
 
O arquivo PDF do histórico acadêmico é armazenado no servidor da aplicação, enquanto o banco de dados registra apenas o caminho de acesso ao documento.
 
O coeficiente de classificação é calculado de acordo com a seguinte fórmula:
 
```
Coeficiente = (0,6 × IRA) + (0,4 × Nota da menção)
```
 
Para o cálculo, são utilizados os seguintes valores:
 
- MM = 3;
- MS = 4;
- SS = 5.
O banco possui restrições que garantem que o IRA esteja entre 0 e 5, que a menção corresponda a um dos valores aceitos e que o coeficiente registrado esteja de acordo com a fórmula estabelecida.
 
Também existe uma restrição que impede que um mesmo aluno realize mais de uma inscrição dentro do mesmo processo seletivo. Entretanto, o estudante pode participar de novos processos em semestres posteriores.
 
### 2.6. Tabela `resultado`
 
A tabela `resultado` armazena a decisão final da comissão responsável pela seleção de cada candidato.
 
Cada registro está associado a uma inscrição e contém a decisão, a modalidade de participação, a data da decisão e as informações referentes ao envio do e-mail de notificação.
 
A decisão pode ser `APROVADO` ou `REPROVADO`. Quando aprovado, o candidato deve receber uma modalidade, que pode ser `BOLSISTA` ou `VOLUNTARIO`. Para candidatos reprovados, a modalidade permanece nula.
 
A tabela também possui os campos `email_enviado` e `data_envio`, utilizados para acompanhar o envio das notificações. Dessa forma, o sistema consegue identificar quais resultados já foram comunicados e quais ainda precisam de envio ou reenvio.
 
## 3. Relacionamentos entre as tabelas
 
A organização do banco utiliza chaves primárias e estrangeiras para estabelecer os relacionamentos entre as entidades e garantir a integridade referencial.
 
Os principais relacionamentos são:
 
- Um usuário administrador pode ser responsável por diferentes processos seletivos.
- Um processo seletivo pode possuir diversas inscrições.
- Um aluno pode realizar inscrições em diferentes processos seletivos, respeitando a regra de uma inscrição por processo.
- Uma disciplina pode estar relacionada a diversas inscrições.
- Cada inscrição possui, no máximo, um resultado registrado.
Dessa maneira, as tabelas são conectadas de forma que as informações de cada estudante, disciplina, processo e resultado possam ser consultadas sem a necessidade de repetir os mesmos dados em diferentes registros.
 
## 4. Views e consultas auxiliares
 
Além das tabelas, foram desenvolvidas quatro views para facilitar a consulta e a apresentação das informações utilizadas pela aplicação.
 
As views são consultas armazenadas que permitem organizar os dados de acordo com as necessidades do sistema, sem exigir que o backend construa novamente todas as consultas SQL.
 
Foram criadas as seguintes views:
 
- `vw_inscricoes_pendentes`: apresenta as inscrições que ainda não possuem um resultado registrado.
- `vw_ranking_geral`: apresenta a classificação geral dos candidatos, considerando os coeficientes calculados.
- `vw_ranking_por_disciplina`: organiza a classificação dos candidatos individualmente por disciplina.
- `vw_total_inscritos_disciplina`: apresenta a quantidade de inscrições recebidas por cada disciplina no processo aberto, incluindo disciplinas que ainda não possuem candidatos inscritos.
Essas consultas auxiliam a comissão na visualização das inscrições e na análise da classificação dos candidatos.
 
## 5. Funções e gatilhos de validação
 
Para reforçar a integridade das informações, foram implementadas funções e gatilhos (triggers) responsáveis por validar determinadas operações realizadas no banco de dados.
 
Entre as principais regras implementadas, destacam-se:
 
- **Controle de inscrições:** impede que sejam realizadas inscrições em processos que não estejam com status `ABERTO`.
- **Proteção dos resultados enviados:** impede alterações na decisão ou na modalidade de um candidato depois que o e-mail de notificação já foi enviado.
- **Validação do encerramento:** impede que um processo seja encerrado enquanto existirem inscrições sem resultado registrado ou notificações pendentes de envio.
- **Proteção contra exclusões indevidas:** impede a exclusão de processos que ainda não foram encerrados e de alunos que possuam inscrições vinculadas a processos ainda ativos.
- **Controle da limpeza dos dados:** garante que a exclusão dos dados operacionais ocorra somente após o encerramento do processo e a confirmação do envio de todas as notificações.
Essas validações permitem que parte das regras de negócio seja garantida diretamente pelo banco de dados, reduzindo a possibilidade de inconsistências provocadas por operações indevidas da aplicação.
 
## 6. Gerenciamento e limpeza dos dados
 
Considerando que o sistema será utilizado em processos seletivos semestrais, a estrutura foi planejada para não manter indefinidamente os dados operacionais dos estudantes.
 
Após o encerramento do processo seletivo e a confirmação de que todos os resultados foram enviados por e-mail, uma função específica permite realizar a limpeza dos registros relacionados àquele processo.
 
Essa operação verifica se o processo está encerrado, se não existem inscrições sem resultado ou notificações pendentes e se os alunos envolvidos não possuem inscrições vinculadas a outros processos.
 
Após a validação dessas condições, são excluídos os registros dos alunos e as informações relacionadas às inscrições e aos resultados. O processo seletivo também é removido.
 
Os arquivos PDF dos históricos acadêmicos, armazenados no servidor da aplicação, deverão ser excluídos pelo backend durante essa etapa, uma vez que o banco de dados armazena apenas os caminhos dos documentos.
 
As informações da conta administrativa e o cadastro das disciplinas são mantidos, pois são necessários para a continuidade dos processos seletivos seguintes.
 
## 7. Controle de acesso
 
Para a conexão da aplicação com o PostgreSQL, foi criado um usuário específico denominado `monitora_app`.
 
Esse usuário possui permissões próprias para acessar o banco de dados e realizar as operações necessárias ao funcionamento do sistema, sem utilizar a conta administrativa do PostgreSQL.
 
A separação entre o usuário administrador do banco e o usuário utilizado pela aplicação contribui para a segurança do sistema, reduzindo a exposição de permissões administrativas durante a execução do backend.
 
As permissões iniciais foram concedidas de acordo com as operações previstas para a aplicação e ainda devem ser revisadas conforme as necessidades identificadas durante a integração com o backend.
 
## 8. Considerações finais
 
A estrutura do banco de dados do Monitora UnB foi desenvolvida para atender às necessidades de gerenciamento das inscrições e dos resultados dos processos seletivos de monitoria.
 
A separação das informações em tabelas específicas, a utilização de relacionamentos, restrições de integridade, views, funções e gatilhos permite organizar os dados e garantir que as principais regras do processo sejam respeitadas.
 
Com a estrutura inicial implementada no PostgreSQL, o banco está preparado para a etapa de integração com o backend em Python, que será responsável por realizar as operações da aplicação, processar os históricos acadêmicos, gerenciar as inscrições e decisões e efetuar o envio das notificações por e-mail.
 
---
 
## 1. Escopo definitivo do sistema
 
O Monitora UnB terá estas responsabilidades:
 
1. Receber as inscrições dos alunos.
2. Receber os históricos escolares em PDF.
3. Extrair e validar as informações dos históricos.
4. Calcular o coeficiente de classificação.
5. Gerar uma planilha com o ranking dos candidatos por disciplina.
6. Permitir que o professor responsável consulte a classificação.
7. Permitir que o professor envie o resultado por e-mail aos candidatos aprovados.
O sistema NÃO será responsável por:
 
- Definir quantidade de vagas.
- Definir quantidade de bolsas.
- Escolher quem recebe bolsa.
- Escolher quem será voluntário.
- Decidir quem será aprovado.
- Distribuir monitores entre professores.
 
