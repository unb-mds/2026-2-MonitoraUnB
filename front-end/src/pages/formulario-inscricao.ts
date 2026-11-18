import { extrairDadosHistorico } from "../services/inscricao.js";
import { salvarInscricao, salvarMotivo } from "../utils/storage.js";
import { ehPdf } from "../utils/validadores.js";

const SEMESTRE_ATUAL = "2026/2";

const inputHistorico = document.getElementById("historico") as HTMLInputElement;
const campoEmail = document.getElementById("email") as HTMLInputElement;
const campoDisciplina = document.getElementById("disciplina") as HTMLInputElement;
const campoProfessor = document.getElementById("professor") as HTMLInputElement;
const campoMatricula = document.getElementById("matricula") as HTMLInputElement;
const campoConcordo = document.getElementById("concordo") as HTMLInputElement;
const botaoContinuar = document.getElementById("continuar") as HTMLAnchorElement;
const textoOriginalBotao = botaoContinuar.textContent ?? "Continuar para revisão";

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
  botaoContinuar.setAttribute("aria-disabled", carregando ? "true" : "false");
  botaoContinuar.textContent = carregando ? "Lendo histórico..." : textoOriginalBotao;
}

function disciplinaNaoEncontrada(mensagem: string): boolean {
  return /n[aã]o foi encontrada/i.test(mensagem);
}

botaoContinuar.addEventListener("click", async (evento) => {
  evento.preventDefault();
  if (botaoContinuar.getAttribute("aria-disabled") === "true") return;
  limparErro();

  const arquivo = inputHistorico.files?.[0];
  const codigo = campoDisciplina.value.trim().toUpperCase();

  if (!campoEmail.value.trim() || !campoEmail.checkValidity()) {
    mostrarErro("Informe um e-mail válido.");
    campoEmail.focus();
    return;
  }
  if (!arquivo) {
    mostrarErro("Envie o seu histórico em PDF.");
    return;
  }
  if (!ehPdf(arquivo)) {
    mostrarErro("O histórico precisa estar em formato PDF.");
    return;
  }
  if (!codigo) {
    mostrarErro("Informe o código da disciplina.");
    return;
  }
  if (!campoMatricula.value.trim()) {
    mostrarErro("Informe a matrícula.");
    return;
  }
  if (!campoConcordo.checked) {
    mostrarErro("Confirme que você não recebe outra bolsa.");
    return;
  }

  definirCarregando(true);

  try {
    const historico = await extrairDadosHistorico(arquivo, codigo);

    salvarInscricao({
      aluno: historico.aluno,
      matricula: historico.matricula,
      ira: historico.ira,
      semestre: SEMESTRE_ATUAL,
      disciplina: codigo,
      disciplinaNome: codigo,
      professor: campoProfessor.value.trim(),
      email: campoEmail.value.trim(),
      arquivoHistorico: arquivo.name,
    });

    window.location.href = "revisao.html";
  } catch (erro) {
    const detalhe = erro instanceof Error ? erro.message : "Não foi possível ler o histórico.";

    if (disciplinaNaoEncontrada(detalhe)) {
      salvarMotivo(detalhe);
      window.location.href = "nao-apto.html";
      return;
    }

    const mensagem = detalhe === "Failed to fetch"
      ? "Não foi possível conectar à API. Verifique se o servidor está em execução."
      : detalhe;
    mostrarErro(mensagem);
    definirCarregando(false);
  }
});
