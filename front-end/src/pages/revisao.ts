import { enviarInscricao } from "../services/inscricao.js";
import { lerInscricao } from "../utils/storage.js";
import { formatarIra } from "../utils/validadores.js";

function definirTexto(id: string, valor: string): void {
  const elemento = document.getElementById(id);
  if (elemento) elemento.textContent = valor;
}

function iniciar(): void {
  const dados = lerInscricao();

  if (!dados) {
    window.location.href = "inscricao.html";
    return;
  }

  definirTexto("aluno", dados.aluno);
  definirTexto("matricula", dados.matricula);
  definirTexto("semestre", dados.semestre);
  definirTexto("disciplina", `${dados.disciplina} — ${dados.disciplinaNome}`);
  definirTexto("professor", dados.professor || "Não informado");
  definirTexto("ira", formatarIra(dados.ira));

  const botaoEnviar = document.getElementById("enviar");
  if (!(botaoEnviar instanceof HTMLAnchorElement)) return;

  botaoEnviar.addEventListener("click", async (evento) => {
    evento.preventDefault();
    if (botaoEnviar.getAttribute("aria-disabled") === "true") return;

    botaoEnviar.setAttribute("aria-disabled", "true");
    botaoEnviar.textContent = "Enviando...";
    definirTexto("status", "Enviando...");

    try {
      const mensagem = await enviarInscricao(dados);
      botaoEnviar.textContent = "Dados validados";
      definirTexto("status", mensagem);
    } catch (erro) {
      botaoEnviar.setAttribute("aria-disabled", "false");
      botaoEnviar.textContent = "Enviar inscrição";
      definirTexto(
        "status",
        erro instanceof Error ? erro.message : "Erro ao enviar. Tente novamente.",
      );
    }
  });
}

iniciar();
