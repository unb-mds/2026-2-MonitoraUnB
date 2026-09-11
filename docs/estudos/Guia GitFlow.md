# Guia de Git Flow, Develop e Feature Branches

Este guia explica como o time deve trabalhar com branches `develop` e `feature` no projeto, para manter o histórico organizado e evitar conflitos entre o trabalho de diferentes membros.

---

## 📌 Estrutura de Branches

```
main
 └── develop
      ├── feature/login
      ├── feature/cadastro-usuario
      └── feature/dashboard
```

- **`main`** → código estável, pronto para entrega/produção. Só recebe merge do `develop` quando algo está finalizado e validado.
- **`develop`** → branch de integração. É onde todas as features se juntam antes de ir para o `main`.
- **`feature/*`** → branch temporário criado para desenvolver **uma funcionalidade específica**. Nasce do `develop` e volta para o `develop` quando pronto.

> ⚠️ Uma feature representa **uma funcionalidade**, não uma pessoa. Se o time tem várias tarefas em paralelo, cada uma ganha sua própria feature branch, independente de quem está trabalhando nela.

---

## 🧭 Convenção de nomes

Use o prefixo `feature/` seguido de um nome curto e descritivo, em minúsculas e com hífen:

```
feature/autenticacao
feature/tela-perfil
feature/api-usuarios
```

---

## 🔄 Fluxo passo a passo

### 1. Atualizar o `develop` antes de começar

```bash
git switch develop
git pull
```

### 2. Criar a feature a partir do `develop`

```bash
git switch -c feature/nome-da-funcionalidade
```

### 3. Trabalhar e commitar normalmente

```bash
git add .
git commit -m "Implementa X"
```

### 4. Enviar a feature para o repositório remoto

```bash
git push -u origin feature/nome-da-funcionalidade
```

O `-u` só é necessário na primeira vez — ele associa o branch local ao remoto. Depois disso, basta `git push`.

### 5. Abrir um Pull Request para o `develop`

Quando a funcionalidade estiver pronta, abra um Pull Request no GitHub de `feature/nome-da-funcionalidade` para `develop` (não direto para `main`). Isso permite revisão de código pelo time antes da integração.

### 6. Após o merge, apagar a feature

```bash
# local
git switch develop
git branch -d feature/nome-da-funcionalidade

# remoto
git push origin --delete feature/nome-da-funcionalidade
```

---

## ✅ Boas práticas

- **Sempre criar a feature a partir do `develop` atualizado**, para evitar trabalhar sobre uma base desatualizada.
- **Nunca commitar direto no `develop` ou no `main`** — todo trabalho passa por uma feature branch e um Pull Request.
- **Manter a feature pequena e focada** em uma única tarefa/funcionalidade, facilitando a revisão.
- **Fazer commits frequentes e descritivos**, em vez de um único commit gigante no final.
- **Atualizar a feature com o `develop`** periodicamente se o desenvolvimento demorar, para reduzir conflitos:
  ```bash
  git switch feature/nome-da-funcionalidade
  git merge develop
  ```

---

## 🔑 Resumo rápido

| Comando | O que faz |
|---|---|
| `git switch develop` | Muda para o branch develop |
| `git pull` | Atualiza o branch atual com o remoto |
| `git switch -c feature/nome` | Cria e muda para uma nova feature |
| `git push -u origin feature/nome` | Envia a feature pro remoto (primeira vez) |
| `git branch -d feature/nome` | Apaga a feature localmente (após merge) |
| `git push origin --delete feature/nome` | Apaga a feature no remoto |

---

## 📚 Referências

- [Documentação oficial do Git — Branching](https://git-scm.com/book/pt-br/v2/Ramifica%C3%A7%C3%B5es-no-Git-O-Que-%C3%A9-uma-Ramifica%C3%A7%C3%A3o)
- [Atlassian — Gitflow Workflow](https://www.atlassian.com/br/git/tutorials/comparing-workflows/gitflow-workflow)
