import { enviarInscricao } from "../services/inscricao.js";
import { lerInscricao } from "../utils/storage.js";
import { formatarIra } from "../utils/validadores.js";

function definirTexto(id: string, valor: string): void {
  const elemento = document.getElementById(id);
  if (elemento) elemento.textContent = valor;
}

function iniciar(): void {
  const dados = lerInscricao();

  // Abriu a revisão sem ter passado pela inscrição: volta pro começo.
  if (!dados) {
    window.location.href = ".../pages/inscricao.html";
    return;
  }

  definirTexto("aluno", dados.aluno);
  definirTexto("matricula", dados.matricula);
  definirTexto("semestre", dados.semestre);
  definirTexto("disciplina", dados.disciplinaNome);
  definirTexto("ira", formatarIra(dados.ira));

  const botaoEnviar = document.querySelector<HTMLAnchorElement>(".continuar")!;

  botaoEnviar.addEventListener("click", async (evento) => {
    evento.preventDefault();
    if (botaoEnviar.getAttribute("aria-disabled") === "true") return;

    botaoEnviar.setAttribute("aria-disabled", "true");
    botaoEnviar.textContent = "Enviando...";
    definirTexto("status", "Enviando...");

    try {
      await enviarInscricao(dados);
      window.location.href = botaoEnviar.href;
    } catch {
      botaoEnviar.setAttribute("aria-disabled", "false");
      botaoEnviar.textContent = "Enviar";
      definirTexto("status", "Erro ao enviar. Tente novamente.");
    }
  });
}

iniciar();
