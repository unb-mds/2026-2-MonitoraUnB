# Git e Github

## Configuracao e criar e clonar repositorios
'git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
git config --global core.editor "code --wait" # define o editor (VS Code neste caso)

git config --list # lista todas as configurações

git init # inicia um repositório novo na pasta atual
git init nome-do-projeto # cria uma nova pasta e inicia o repositório nela

git clone <url> # clona um repositório remoto
git clone <url> nome-local # clona e renomeia a pasta local
'


## Termos
### Commit
Commit e uma mudanca que foi feita em um projeto em um determinado momento sendo adicionada a um historico do projeto

### Branches
Branches sao ramificacoes no projeto para que as coisas nao sejam adicionadas de uma vez, sendo mais comum o uso para criar novas features em um ambiente controlado sem outros commits


## Branches
'
git branch #listar branches locais
git branch -a #listar branches locais e remotas
git branch nome #criar uma nova branch
git branch -d nome #deletar branch (seguro apenas depois de mergeada com a main)
git branch -D nome #força a deleçao da branch
git branch -m nome-novo #renomeia a branch atual

git switch nome #muda para uma branch existente
git switch -c nome #cria e muda para uma nova branch
'

## Adicionar e commitar
'
git add <arquivo> #adiciona um arquivo a uma lista (staging area)
git add . #adiciona todos os arquivos modificados/novos
git add -p #adiciona interativamente (pedaco por pedaco)

git commit -m "mensagem" #cria um commit seguido de uma mensagem
git commit -am "mensagem" # add + commit de arquivos ja rastreados (nao novos)
git commit --ammend #reescreve o ultimo commit
git commit --ammend --no-edit #reescreve o ultimo commit mantendo a mesma mensagem
'

## Merge
'
git merge nome-da-branch #merge da branch indicada na branch atual
git rebase main #reaplica commits da branch atual sobre main

'
