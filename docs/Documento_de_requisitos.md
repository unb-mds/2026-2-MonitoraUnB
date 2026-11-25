# Documento de Requisitos de Software — Monitora-UnB
 
Universidade de Brasília (UnB)
Disciplina: Métodos de Desenvolvimento de Software
Grupo 11
Versão: 2.0
Professor(a) orientador(a): Carla Rocha
Brasília, 2026
 
Este documento detalha os requisitos funcionais, não funcionais e inversos do sistema Monitora-UnB, organizados por épico e com rastreabilidade até as regras de negócio e as decisões do grupo.
 
## 1. Introdução
 
### 1.1 Propósito
 
Este documento especifica, de forma detalhada e verificável, os requisitos funcionais (RF), não funcionais (RNF) e inversos (RI) do sistema Monitora-UnB. Serve de referência para o desenvolvimento, o teste e a avaliação do produto, e para a integração entre as frentes do grupo (front-end, back-end, banco de dados, scraper e e-mail).
 
### 1.2 Escopo
 
O Monitora-UnB gerencia o processo seletivo de vagas de monitoria. O estudante se inscreve em uma disciplina e escolhe o professor com quem quer ser monitor, caso haja mais de um professor ofertando a matéria. O sistema realiza a automação da leitura e validação dos históricos enviados de cada candidato, dispensando o trabalho manual e cansativo antes usado. O Monitor-UnB também gera o ranking dos inscritos com base no coeficiente de cada um (que o sistema também calcula). Quem decide o resultado (bolsista ou voluntário) é o professor chefe da comissão de monitoria. Terminados o período de inscrição e a decisão, cada estudante que passou recebe o resultado por e-mail.
 
Fora do escopo: acesso ao sistema pelos demais professores (RI02), decisão automática de aprovação (RI03) e limite de monitores por professor (RI08).
 
### 1.3 Convenções deste documento
 
| Elemento | Convenção |
|---|---|
| ID de requisito funcional | RF + dois dígitos sequenciais, únicos no documento (ex.: RF01, RF02, ...) |
| ID de subrequisito | RFxx.y: parte verificável de um RF. O RF que cobre um único comportamento não tem subrequisitos |
| ID de requisito não funcional | RNF + dois dígitos sequenciais |
| ID de requisito inverso | RI + dois dígitos sequenciais |
| ID de regra de negócio | RN + dois dígitos sequenciais. As regras estão no Anexo B e os requisitos as citam em vez de repetilas |
| ID de limitação ou risco | L + dois dígitos sequenciais |
| Critério de aceite | Escrito em Dado/Quando/Então. Cada subrequisito tem um cenário (no máximo dois) |
| Prioridade (proposta) | Essencial (sem ele o sistema não cumpre seu objetivo), Importante (melhora a operação ou a experiência), Desejável (pode ficar para depois). O grupo deve confirmar |
| Parâmetros | Valores ajustáveis sem alterar o requisito estão no Anexo A |
| Numeração | Os IDs são únicos, seguem a ordem de criação e não mudam |
 
### 1.4 Termos
 
| Termo | Significado |
|---|---|
| Estudante | Aluno que se inscreve para uma vaga de monitoria. Não precisa de conta: a inscrição é identificada pela matrícula |
| Chefe da comissão | Professor que chefia a comissão de monitoria. É o único usuário com login. A conta está ligada ao cargo, não à pessoa |
| Demais professores | Professores que aparecem como opção de orientação na inscrição, mas não têm login nem acesso (RN05) |
| Processo seletivo | Período de inscrições de um semestre, identificado no formato 2026/2 |
| Matrícula | Identificador do estudante, usado para impedir mais de uma inscrição por semestre (UK) |
| Coeficiente | Valor usado para ordenar o ranking. Maior coeficiente, melhor posição |
| Inscrição | Pedido de um estudante para ser monitor de uma disciplina, com um professor escolhido, dentro de um processo seletivo |
| Ranking | Lista dos inscritos ordenada por coeficiente (maior primeiro), gerada pelo sistema |
| Aprovado / Rejeitado | Decisão do chefe da comissão sobre uma inscrição, tomada pelos botões do ranking |
| Não apto | Situação do candidato rejeitado, exibida na página "não apto" |
| Bolsista / Voluntário | Tipos de monitoria. O chefe da comissão decide quem recebe a bolsa (maior coeficiente) e quem é voluntário |
| Scraper | Rotina que lê o SIGAA e carrega disciplinas e professores no banco a cada semestre |
| SMTP | Serviço usado para enviar os e-mails de resultado |
| Limpeza do semestre | Apagamento dos dados do semestre ao fim do processo, preservando a conta do chefe da comissão |
 
### 1.5 Stack tecnológica
 
O front-end é em HTML e CSS, com TypeScript para preencher as páginas com os dados. O back-end é em Python e é desenvolvido por outro integrante do grupo. O banco de dados é PostgreSQL; a aplicação se conecta com a role dedicada monitora_app. As disciplinas e os professores vêm do scraper, e os e-mails de resultado saem por SMTP.
 
## 2. Requisitos Funcionais
 
Cada requisito funcional tem identificador, descrição e prioridade. O RF que cobre mais de um comportamento independente é dividido em subrequisitos (RFxx.y), cada um com uma frase e um cenário de aceite. As regras detalhadas estão no Anexo B (RN01 a RN13) e os valores ajustáveis, no Anexo A. A origem de cada requisito está na Matriz de Rastreabilidade (Seção 6).
 
### Épico 1 — Inscrição do estudante
 
#### RF01 — Página inicial
 
**Descrição:** O sistema deve exibir uma página inicial com as informações do processo seletivo em andamento e o acesso à inscrição. O estudante não precisa de login para acessá-la.
**Prioridade:** Essencial
 
#### RF02 — Inscrição em vaga de monitoria
 
**Descrição:** O sistema deve permitir que o estudante preencha o formulário de inscrição com seus dados, escolha a disciplina e o professor com quem quer ser monitor. A inscrição só é aceita se houver processo seletivo aberto e se a matrícula ainda não tiver inscrição no semestre.
**Prioridade:** Essencial
 
**RF02.1 — Dados do estudante.** O sistema deve receber os dados do estudante definidos no Anexo A, incluindo a matrícula e o coeficiente, e rejeitar o envio com campo obrigatório vazio ou fora do formato.
 
- Dado que deixo um campo obrigatório vazio, quando envio, então o formulário é rejeitado com mensagem que indica o campo.
- Dado que preencho todos os campos no formato correto, quando avanço, então sigo para a revisão (RF03).
**RF02.2 — Escolha da disciplina.** O sistema terá um campo destinado a escolha da disciplina em que o aluno terá de digitar e só poderá escolher uma(RN09).
 
**RF02.3 — Escolha do professor.** O sistema também terá um espaço dedicado para escrever o nome do professor da escolha do candidato, o que será opcional, pois não é de conhecimento público quais professores querem ter ou não monitores e quantidade.
 
**RF02.4 — Uma inscrição por semestre.** O sistema deve recusar a inscrição de uma matrícula que já tem inscrição no processo seletivo corrente, em qualquer disciplina (RN03, RI01).
 
- Dado que a matrícula X já se inscreveu em uma disciplina em 2026/2, quando tento me inscrever com X em outra disciplina do mesmo semestre, então a inscrição é recusada com mensagem informando o motivo.
#### RF03 — Revisão da inscrição
 
**Descrição:** O sistema deve exibir uma página de revisão com os dados informados, a disciplina e o professor escolhidos, antes do envio definitivo.
**Prioridade:** Essencial
 
**Critérios de aceite:**
 
- Dado que preenchi a inscrição, quando avanço, então vejo todos os dados, a disciplina e o professor escolhidos, com a opção de voltar e corrigir ou de confirmar o envio.
- Dado que voltou para corrigir, quando avançou de novo, então os dados já preenchidos continuam no formulário.
- Dado que confirmo o envio, quando o sistema registra a inscrição, então a inscrição fica ligada ao processo seletivo corrente (RN11).
#### RF04 — Confirmação da inscrição
 
**Descrição:** O sistema deve exibir uma página de confirmação quando a inscrição for registrada com sucesso.
**Prioridade:** Essencial
 
**Critérios de aceite:**
 
- Dado que confirmei o envio na revisão, quando a inscrição é registrada no banco, então vejo a página de confirmação com a disciplina e o professor escolhidos.
- Dado que o registro falha (por exemplo, por erro do servidor), quando isso ocorre, então não vejo a confirmação e recebo uma mensagem de erro com a orientação de tentar de novo.
#### RF05 — Inscrição somente com processo seletivo aberto
 
**Descrição:** O sistema deve aceitar inscrições apenas enquanto houver um processo seletivo aberto (RN06, RI06).
**Prioridade:** Essencial
 
**Critérios de aceite:**
 
- Dado que não há processo seletivo aberto, quando tento enviar uma inscrição, então ela é recusada com mensagem informando que as inscrições estão encerradas, e nada é gravado.
- Dado que o processo seletivo do semestre foi aberto, quando envio uma inscrição válida, então ela é aceita.
### Épico 2 — Área do chefe da comissão de monitoria
 
#### RF06 — Login do chefe da comissão
 
**Descrição:** O sistema deve permitir que o chefe da comissão de monitoria se autentique com e-mail e senha. É o único login do sistema (RN05).
**Prioridade:** Essencial
 
**RF06.1 — Autenticação.** O sistema deve autenticar a conta do chefe da comissão (ex:admin@monitora.unb.br) com a senha cadastrada e levá-lo ao ranking.
 
- Dado e-mail e senha corretos, quando entro, então a sessão é iniciada e vejo o ranking (RF07).
- Dado e-mail ou senha incorretos, quando envio, então vejo mensagem genérica, sem indicar qual dos dois está errado.
**RF06.2 — Senha única e permanente.** O sistema não deve exigir a troca da senha no primeiro login (RN07).
 
- Dado que entro pela primeira vez, quando a autenticação é aceita, então vejo o ranking direto, sem tela de troca de senha.
**RF06.3 — Acesso restrito.** O sistema não deve oferecer login nem acesso à área do chefe a nenhum outro usuário (RN05, RI02).
 
- Dado um e-mail que não seja o da conta do chefe, quando tento entrar, então o login é recusado.
- Dado que não estou logado, quando abro diretamente a URL do ranking, então sou levado ao login.
**RF06.4 — Sair.** O sistema deve permitir encerrar a sessão do chefe.
 
- Dado que estou logado, quando toco em "Sair", então a sessão termina e a área do ranking deixa de ser acessível.
#### RF07 — Ranking dos inscritos
 
**Descrição:** O sistema deve exibir ao chefe da comissão o ranking dos inscritos, gerado a partir do coeficiente, com filtro por disciplina e opções de ordenação.
**Prioridade:** Essencial
 
**RF07.1 — Exibição do ranking.** O sistema deve listar os inscritos do processo seletivo corrente do maior para o menor coeficiente (RN04).
 
- Dado inscritos com coeficientes diferentes, quando abro o ranking, então a lista aparece do maior para o menor coeficiente, com os botões de aprovar e rejeitar (RF08).
**RF07.2 — Filtro por disciplina.** O sistema deve permitir filtrar o ranking por disciplina e mostrar o número de inscritos por professor dentro dela.
 
- Dado a disciplina D com dois professores, quando a filtro, então vejo só os inscritos de D e, para cada professor, o número de candidatos que o escolheram.
- Dado que limpo o filtro, quando confirmo, então volto a ver todos os inscritos.
**RF07.3 — Ordenação.** O sistema deve permitir ordenar a lista em ordem alfabética (pelo nome do estudante) ou por posição no ranking, com o maior coeficiente primeiro.
 
- Dado a lista exibida, quando escolho "ordem alfabética", então os nomes aparecem de A a Z; quando escolho "ranking", então volto à ordem do maior coeficiente para o menor.
#### RF08 — Aprovar ou rejeitar candidato
 
**Descrição:** O sistema deve oferecer, para cada inscrito no ranking, os botões de aprovar e rejeitar, e guardar a decisão do chefe da comissão (RN04).
**Prioridade:** Essencial
 
**Critérios de aceite:**
 
- Dado um inscrito no ranking, quando toco em "aprovar", então a decisão fica registrada como aprovado e o candidato continua na lista de aprovados.
- Dado um inscrito no ranking, quando toco em "rejeitar", então a decisão fica registrada como rejeitado e o candidato passa para a página "não apto" (RF09).
- Dado uma decisão já tomada, quando o período de decisão ainda não terminou, então posso alterá-la.
#### RF09 — Página "não apto"
 
**Descrição:** O sistema deve ter uma página que lista os candidatos considerados não aptos, com a disciplina e o professor de cada um. (Interpretação do grupo a confirmar: não apto = rejeitado.)
**Prioridade:** Essencial
 
**Critérios de aceite:**
 
- Dado candidatos rejeitados, quando abro a página "não apto", então vejo a lista deles com disciplina e professor escolhidos.
- Dado que desfaço uma rejeição (RF08), quando abro a página, então o candidato não aparece mais nela.
#### RF10 — Definir bolsista e voluntário
 
**Descrição:** O sistema deve permitir que o chefe da comissão defina, entre os aprovados, quem recebe a bolsa (maior coeficiente) e quem é voluntário. O sistema não faz essa definição sozinho (RN04, RI03).
**Prioridade:** Essencial
 
**RF10.1 — Registro do tipo de monitoria.** O sistema deve registrar para cada aprovado se ele é bolsista ou voluntário.
 
- Dado um aprovado, quando o chefe escolhe "bolsista" ou "voluntário", então a escolha fica registrada e aparece no ranking.
**RF10.2 — Sugestão pelo coeficiente.** O sistema deve destacar o aprovado de maior coeficiente de cada disciplina como candidato natural à bolsa, sem atribuí-la automaticamente.
 
- Dado aprovados em uma disciplina, quando abro o ranking, então o de maior coeficiente aparece destacado, e o tipo de monitoria dele continua em branco até o chefe decidir.
### Épico 3 — Processo seletivo e dados do semestre
 
#### RF11 — Processo seletivo do semestre
 
**Descrição:** O sistema deve manter um processo seletivo por semestre, identificado no formato 2026/2, com situação aberta ou encerrada. Sem processo aberto, nenhuma inscrição é aceita (RN06).
**Prioridade:** Essencial
 
**RF11.1 — Abertura.** O sistema deve ter um processo seletivo aberto antes de o período de inscrições começar.
 
- Dado o setup do banco do semestre, quando ele termina, então existe um processo seletivo aberto com o semestre no formato 2026/2.
**RF11.2 — Encerramento.** O sistema deve encerrar o processo seletivo ao fim do período de inscrições, mantendo o ranking e as decisões disponíveis ao chefe.
 
- Dado o fim do período de inscrições, quando o processo é encerrado, então novas inscrições são recusadas e o ranking continua acessível para a decisão (RF05).
#### RF12 — Carga de disciplinas e professores
 
**Descrição:** O sistema deve carregar as disciplinas e os professores do SIGAA por meio do scraper, já integrado ao banco, a cada semestre (RN08).
**Prioridade:** Essencial
 
**Critérios de aceite:**
 
- Dado o início de um semestre, quando o scraper executa, então as disciplinas e os professores do semestre ficam no banco e aparecem na inscrição (RF02.2 e RF02.3).
- Dado que a leitura do SIGAA falha, quando isso ocorre, então nenhuma disciplina incompleta é gravada e a falha fica registrada para a equipe.
#### RF13 — Limpeza ao fim do semestre
 
**Descrição:** O sistema deve permitir apagar os dados do semestre depois do período de inscrição e da decisão, incluindo as disciplinas, preservando a conta do chefe da comissão (RN10, RN12).
**Prioridade:** Importante
 
**RF13.1 — Apagar dados do semestre.** A limpeza deve remover inscrições, decisões, processo seletivo e as disciplinas e os professores encarregados naquele semestre.
 
- Dado um semestre encerrado e decidido, quando executo a limpeza, então inscrições, decisões, processo seletivo e disciplinas do semestre deixam de existir no banco.
**RF13.2 — Preservar a conta do chefe.** A limpeza nunca deve remover a conta do chefe da comissão (RN12, RI05).
 
- Dado que executou a limpeza, quando ela termina, então admin@monitora.unb.br continua existindo e consegue entrar com a mesma senha.
### Épico 4 — Comunicação do resultado
 
#### RF14 — E-mail de resultado
 
**Descrição:** O sistema deve enviar por e-mail o resultado a cada estudante que passou, depois do encerramento do período de inscrição e da decisão do chefe da comissão (RN13).
**Prioridade:** Essencial
 
**RF14.1 — Momento do envio.** O sistema só deve enviar os e-mails depois do encerramento do processo seletivo e da decisão (RI07).
 
- Dado um processo ainda aberto, quando consulto os envios, então nenhum email de resultado foi enviado.
**RF14.2 — Destinatários e conteúdo.** O e-mail deve ir a cada estudante aprovado, informando o resultado (bolsista ou voluntário), a disciplina e o professor.
 
- Dado um aprovado como bolsista, quando os e-mails são enviados, então ele recebe a mensagem com o resultado, a disciplina e o professor; rejeitados também recebem e-mail com o resultado.
**RF14.3 — Falha de envio.** O sistema deve registrar os envios que falharam e permitir reenviá-los.
 
- Dado que o SMTP recusa um envio, quando isso ocorre, então a falha fica registrada com o estudante e o motivo, e o envio pode ser repetido sem duplicar os já entregues.
## 3. Requisitos Não Funcionais
 
Os valores marcados como Proposto foram sugeridos para este documento e precisam ser confirmados pelo grupo. Os marcados como Definido pelo grupo vêm de decisões já tomadas.
 
### RNF01 — Desempenho (Proposto)
 
O sistema deve responder às requisições das páginas do estudante e do ranking do chefe em até 3 segundos, em condições normais de operação, para o volume de acessos esperado no pico das inscrições (valor em aberto no Anexo A).
 
Justificativa: o pico de acessos ocorre perto do fim do período de inscrição, e uma meta verificável evita lentidão justamente nesse momento.
 
### RNF02 — Usabilidade (Proposto)
 
O fluxo do estudante deve ter quatro telas (início, inscrição, revisão e confirmação) e ser funcional em telas a partir de 360 px de largura. As mensagens de erro devem dizer o que aconteceu (inscrição duplicada, processo encerrado, campo inválido) e o que fazer em seguida.
 
### RNF03 — Segurança (Definido pelo grupo e Proposto)
 
A aplicação deve se conectar ao banco com a role dedicada monitora_app (Definido pelo grupo), que deve ter apenas as permissões necessárias (Proposto). A senha do chefe da comissão deve ser guardada com hash, nunca em texto puro (RI04). A comunicação deve usar HTTPS, as consultas ao banco devem ser parametrizadas, e as rotas da área do chefe só respondem a sessão autenticada.
 
Justificativa: como a senha é única e permanente (RN07), a proteção dela e da rota do ranking é o principal controle de segurança do sistema.
 
### RNF04 — Privacidade e proteção de dados pessoais (Proposto)
 
O sistema trata como dados pessoais os dados do formulário de inscrição (incluindo nome, matrícula, e-mail e coeficiente), conforme a Lei Geral de Proteção de Dados (Lei nº 13.709/2018). Esses dados só podem ser vistos pelo chefe da comissão (RI09), são usados só para o processo seletivo e o envio do resultado, e são apagados na limpeza do semestre (RF13).
 
### RNF05 — Compatibilidade (Proposto)
 
O site deve funcionar nas duas versões mais recentes do Chrome, Firefox, Edge e Safari, em computador e em celular.
 
### RNF06 — Manutenibilidade e testes (Definido pelo grupo)
 
O banco de dados deve ser criado por scripts SQL versionados e executáveis em ordem: schema, setup/seed e testes. Os scripts rodam no pgAdmin e devem poder ser repetidos sem erro. O código deve separar front-end (HTML, CSS e TypeScript), back-end (Python) e banco (PostgreSQL), de modo que uma mudança em uma frente não obrigue a alterar as outras.
 
### RNF07 — Integridade dos dados (Definido pelo grupo)
 
O banco deve garantir por restrições, e não só pela aplicação: matrícula única por processo seletivo (RN03), professor escolhido pertencente à disciplina escolhida (RN09) e inscrição ligada a um processo seletivo (RN11). A limpeza do semestre nunca pode remover a conta do chefe (RN12).
 
### RNF08 — Confiabilidade do envio de e-mails (Proposto)
 
O envio dos resultados (RF14) deve ser repetível sem duplicar os e-mails já entregues, e cada falha deve ficar registrada com o estudante e o motivo.
 
## 4. Requisitos Inversos
 
Requisitos inversos definem explicitamente o que o sistema não deve fazer.
 
| ID | Descrição |
|---|---|
| RI01 | O sistema não deve aceitar mais de uma inscrição da mesma matrícula no mesmo semestre, nem em disciplinas diferentes. |
| RI02 | O sistema não deve oferecer login nem acesso a professores que não sejam o chefe da comissão, nem a estudantes. |
| RI03 | O sistema não deve decidir sozinho quem é aprovado, bolsista ou voluntário. Ele só gera o ranking. |
| RI04 | O sistema não deve armazenar a senha do chefe da comissão em texto puro, sob nenhuma circunstância. |
| RI05 | O sistema não deve apagar a conta do chefe da comissão, nem na limpeza do semestre. |
| RI06 | O sistema não deve aceitar inscrições quando não houver processo seletivo aberto. |
| RI07 | O sistema não deve enviar e-mail de resultado antes do encerramento do período de inscrição e da decisão do chefe da comissão. |
| RI08 | O sistema não deve impor limite de monitores por professor. |
| RI09 | O sistema não deve exibir os dados dos inscritos a quem não seja o chefe da comissão. |
| RI10 | O sistema não deve exigir troca de senha do chefe da comissão no primeiro login. |
 
## 5. Limitações e Riscos Conhecidos
 
| ID | Limitação ou risco | Mitigação |
|---|---|---|
| L01 | Senha única e permanente. Como a mesma senha é usada por quem ocupa o cargo ao longo do tempo, ela pode circular entre pessoas. | Senha com hash (RNF03). Troca manual feita pela equipe quando o cargo mudar de mãos. |
| L02 | Um único professor com acesso. Se o chefe da comissão ficar indisponível, ninguém mais consegue decidir o resultado. | Conta ligada ao cargo, não à pessoa (RN12), e e-mail dedicado admin@monitora.unb.br. |
| L03 | Dependência do scraper e do SIGAA. Mudanças no SIGAA podem quebrar a carga de disciplinas e professores. | Falha registrada, sem gravar dados incompletos (RF12). Último semestre não é mantido (RN10), por isso é preciso reexecutar o scraper a cada semestre. |
| L04 | Processo seletivo aberto é pré-requisito. Sem ele, todas as inscrições falham. Isso já ocorreu quando o script de seed estava vazio. | Seed passa a abrir o processo do semestre (RF11.1), e os testes do banco verificam essa condição. |
| L05 | A limpeza apaga o histórico. Depois dela, não há como consultar quem se inscreveu ou foi aprovado em semestres anteriores. | Exportar o ranking e as decisões antes de limpar (Proposto). |
| L06 | Dependência do SMTP. Se o serviço de e-mail estiver fora do ar, os resultados não chegam. | Registro de falhas e reenvio (RF14.3, RNF08). Configuração do SMTP em andamento com o Macedo. |
| L07 | Critério de "não apto" em aberto. O grupo ainda precisa confirmar se a página reúne os rejeitados ou também candidatos que não cumprem critérios objetivos. | Resolver na revisão deste documento (Anexo A). |
 
## 6. Matriz de Rastreabilidade
 
| ID | Subrequisitos | Épico | Origem / regras ligadas | Prioridade |
|---|---|---|---|---|
| RF01 | — | Inscrição | Fluxo de telas do estudante (início) | Essencial |
| RF02 | RF02.1 a RF02.4 | Inscrição | Fluxo de telas (inscrição); RN01, RN02, RN03, RN09 | Essencial |
| RF03 | — | Inscrição | Fluxo de telas (revisão); RN11 | Essencial |
| RF04 | — | Inscrição | Fluxo de telas (confirmação) | Essencial |
| RF05 | — | Inscrição | RN06 | Essencial |
| RF06 | RF06.1 a RF06.4 | Chefe da comissão | Fluxo de telas (login); RN05, RN07, RN12 | Essencial |
| RF07 | RF07.1 a RF07.3 | Chefe da comissão | Fluxo de telas (ranking); RN01, RN04; pedido do chefe de filtrar e ordenar | Essencial |
| RF08 | — | Chefe da comissão | Fluxo de telas (aprovar e rejeitar); RN04 | Essencial |
| RF09 | — | Chefe da comissão | Fluxo de telas (página "não apto") | Essencial |
| RF10 | RF10.1, RF10.2 | Chefe da comissão | RN04 | Essencial |
| RF11 | RF11.1, RF11.2 | Processo seletivo | RN06, RN11; correção do seed vazio | Essencial |
| RF12 | — | Processo seletivo | RN08 | Essencial |
| RF13 | RF13.1, RF13.2 | Processo seletivo | RN10, RN12 | Importante |
| RF14 | RF14.1 a RF14.3 | Comunicação | RN13; tarefa de SMTP da reunião de 16/11/2026 | Essencial |
| RF15 | RF15.1, RF15.2 | Transversal | Tarefa de modo escuro da reunião de 16/11/2026 | Importante |
| RNF01 a RNF08 | — | Transversal | Decisão do grupo ou proposta deste documento (ver cada item) | — |
 
## 7. Resumo por Prioridade
 
| Prioridade | Requisitos funcionais |
|---|---|
| Essencial | RF01 a RF12, RF14 |
| Importante | RF13, RF15 |
| Desejável | Nenhum até agora (a definir na revisão) |
 
Todos os requisitos não funcionais (RNF01 a RNF08) e inversos (RI01 a RI10) valem desde a primeira versão do sistema.
 
## Anexo A — Parâmetros configuráveis
 
Valores ajustáveis sem alterar os requisitos. Os marcados como A definir ainda não foram decididos pelo grupo.
 
| Parâmetro | Valor inicial | Usado em |
|---|---|---|
| Formato do semestre | 2026/2 | RF01, RF11 |
| Fonte de disciplinas e professores | SIGAA, via scraper | RF12 (RN08) |
| E-mail da conta do chefe da comissão | (ex:admin@monitora.unb.br) | RF06, RF13 (RN12) |
| Role do banco usada pela aplicação | monitora_app | RNF03 |
| Limite de monitores por professor | Sem limite | RN02, RI08 |
| Inscrições por matrícula por semestre | 1 | RN03 |
| Campos do formulário de inscrição e quais são obrigatórios | Todos meno o campo de escrita do nome do professor que é opcional | RF02.1 |
| Formato aceito para a matrícula | Formato seguido pela UnB de nove números (012345678) | RF02.1 |
| Origem do coeficiente | Coef= (0,6 x IRA) +( 0,4 x Menção) [MM=3; MS =4; SS=5] | RF02.1, RF07 |
| Critério para considerar um candidato "não apto" | Não ter concluído a disciplina que deseja monitorar em semestres anteriores | RF08, RF09 |
| Datas de abertura e de encerramento das inscrições | Depende do administrador | RF11 |
| Tempo máximo de resposta das páginas | A definir | RNF01 |
| Volume de acessos simultâneos esperado no pico | A definir | RNF01 |
| Conteúdo e remetente do e-mail de resultado | A definir (configuração SMTP) | RF14 |
 
## Anexo B — Regras de negócio
 
Regras citadas pelos requisitos funcionais. Os valores ajustáveis estão no Anexo A.
 
### RN01 — Vários professores por disciplina
 
Uma disciplina pode ter vários professores. O estudante escolhe com qual deles quer ser monitor.
 
### RN02 — Sem limite de monitores por professor
 
O limite de monitores não é uma informação que o grupo detém e é algo que está sempre em mudança, portanto cabe ao chefe da comissão de monitoria conversar com os professores e escolher os candidatos de acordo com o decidido
 
### RN03 — Uma inscrição por semestre
 
O estudante só pode se inscrever em uma disciplina por semestre. A verificação é feita pela matrícula.
 
### RN04 — O sistema gera o ranking, o chefe decide
 
- O sistema só gera o ranking, ordenado pelo coeficiente, do maior para o menor.
- O chefe da comissão decide quem é aprovado e quem recebe a bolsa (maior coeficiente) ou fica como voluntário.
### RN05 — Acesso restrito ao chefe da comissão
 
Só um professor tem acesso ao sistema: o chefe da comissão de monitoria. Os outros professores não têm login e não têm acesso.
 
### RN06 — Inscrição só com processo seletivo aberto
 
O sistema só aceita inscrições enquanto existir um processo seletivo aberto.
 
### RN07 — Senha permanente
 
A senha do chefe da comissão é única e permanente. Não há troca obrigatória no primeiro login (a ideia anterior de um modal de troca de senha foi descartada).
 
### RN08 — Origem de disciplinas e professores
 
Disciplinas e professores vêm do scraper (SIGAA), que já está integrado ao banco, e são carregados a cada semestre.
 
### RN09 — Disciplina e professor da inscrição
 
Cada inscrição refere-se a uma única disciplina e a um único professor(opcional informar o professor), que deve ser um dos professores dessa disciplina.
 
### RN10 — Limpeza ao fim do semestre
 
Depois do período de inscrição e da decisão, todo o banco pode ser apagado, porque o semestre seguinte tem estudantes novos ou que voltam, e as disciplinas e os professores podem mudar (código da disciplina, nome do professor). A limpeza inclui as disciplinas do semestre, que o scraper recarrega do SIGAA. A única exceção é a conta do chefe da comissão (RN12).
 
### RN11 — Inscrição ligada ao processo seletivo
 
Toda inscrição pertence a um processo seletivo, identificado pelo semestre no formato 2026/2.
 
### RN12 — Conta do chefe da comissão
 
A conta do chefe da comissão nunca é descartada entre semestres, porque está ligada ao cargo (chefe da comissão de monitoria) e não à pessoa que o ocupa no momento. Usa o email dedicado admin@monitora.unb.br, criado só para isso.
 
### RN13 — E-mail de resultado
 
Depois do período de inscrição e da decisão do chefe da comissão, o sistema envia um email com o resultado a cada estudante, tendo passado ou não.
 
