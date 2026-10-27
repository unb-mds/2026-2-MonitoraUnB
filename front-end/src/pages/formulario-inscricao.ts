import { extrairDadosHistorico } from "../services/inscricao-service.js";
import { salvarInscricao } from "../utils/storage.js";
import { ehPdf } from "../utils/validadores.js";

const SEMESTRE_ATUAL = "2026/2";

const inputHistorico = document.getElementById("historico") as HTMLInputElement;
const campoDisciplina = document.getElementById("disciplina") as HTMLInputElement;
const botaoContinuar = document.querySelector<HTMLButtonElement>(".continue-button")!;
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
  botaoContinuar.disabled = carregando;
  botaoContinuar.textContent = carregando ? "Lendo histórico..." : textoOriginalBotao;
}

botaoContinuar.addEventListener("click", async (evento) => {
  evento.preventDefault(); // o botão só avança depois de validar
  if (botaoContinuar.disabled) return;
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
<<<<<<< HEAD:front-end/src/pages/inscricao.ts
    const historico = await extrairDadosHistorico(arquivo, selectDisciplina.value);
    const opcao = selectDisciplina.selectedOptions[0];

=======
    const historico = await extrairDadosHistorico(arquivo);
>>>>>>> origin/develop:front-end/src/pages/formulario-inscricao.ts
    salvarInscricao({
      ...historico,
      semestre: SEMESTRE_ATUAL,
      disciplina: campoDisciplina.value.trim(),
      disciplinaNome: campoDisciplina.value.trim(),
      arquivoHistorico: arquivo.name,
    });

<<<<<<< HEAD:front-end/src/pages/inscricao.ts
    window.location.href = botaoContinuar.href;
  } catch (erro) {
    if (erro instanceof Error) {
      mostrarErro(erro.message)
    } else {
    mostrarErro("Não foi possível ler o histórico. Tente novamente.");
=======
    window.location.href = "./revisao.html";
  } catch (erro) {
    const detalhe = erro instanceof Error ? erro.message : "Falha ao processar o arquivo.";
    mostrarErro(`Não foi possível ler o histórico. ${detalhe}`);
    definirCarregando(false);
>>>>>>> origin/develop:front-end/src/pages/formulario-inscricao.ts
  }
  definirCarregando(false);
 }
});
