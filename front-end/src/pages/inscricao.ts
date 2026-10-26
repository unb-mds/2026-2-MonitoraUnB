import { extrairDadosHistorico } from "../services/inscricao.js";
import { salvarInscricao } from "../utils/storage.js";
import { ehPdf } from "../utils/validadores.js";

const SEMESTRE_ATUAL = "2026/2";

const inputHistorico = document.getElementById("historico") as HTMLInputElement;
const campoDisciplina = document.getElementById("disciplina") as HTMLInputElement;
const botaoContinuar = document.querySelector<HTMLAnchorElement>(".continue-button")!;
const textoOriginalBotao = botaoContinuar.textContent;

function mostrarErro(mensagem: string): void {
  let elemento = document.getElementById("mensagem-erro");

  if (!elemento) {
    elemento = document.createElement("p");
    elemento.id = "mensagem-erro";
    elemento.className = "erro";
    botaoContinuar.before(elemento);
  }

  elemento.textContent = mensagem;
}

function limparErro(): void {
  document.getElementById("mensagem-erro")?.remove();
}

function definirCarregando(carregando: boolean): void {
  botaoContinuar.setAttribute("aria-disabled", String(carregando));
  botaoContinuar.textContent = carregando ? "Lendo histórico..." : textoOriginalBotao;
}

botaoContinuar.addEventListener("click", async (evento) => {
  evento.preventDefault(); // o <a> só navega depois de validar
  if (botaoContinuar.getAttribute("aria-disabled") === "true") return;
  limparErro();

  const arquivo = inputHistorico.files?.[0];

  if (!arquivo) {
    mostrarErro("Envie o seu histórico em PDF.");
    return;
  }
  if (!ehPdf(arquivo)) {
    mostrarErro("O histórico precisa estar em formato PDF.");
    return;
  }
  if (!campoDisciplina.value.trim()) {
    mostrarErro("Selecione a disciplina para a monitoria.");
    return;
  }

  definirCarregando(true);

  try {
    const historico = await extrairDadosHistorico(arquivo);
    salvarInscricao({
      ...historico,
      semestre: SEMESTRE_ATUAL,
      disciplina: campoDisciplina.value.trim(),
      disciplinaNome: campoDisciplina.value.trim(),
      arquivoHistorico: arquivo.name,
    });

    window.location.href = botaoContinuar.href;
  } catch (erro) {
    const detalhe = erro instanceof Error ? erro.message : "Falha ao processar o arquivo.";
    mostrarErro(`Não foi possível ler o histórico. ${detalhe}`);
    definirCarregando(false);
  }
});
