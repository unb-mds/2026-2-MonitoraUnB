import type { DadosHistorico, DadosInscricao } from "../types/inscricao.js";

// ÚNICO arquivo que vai conversar com o back-end (Python/FastAPI).
// Hoje as duas funções são simuladas; quando a API existir, é só trocar
// o corpo delas por um fetch() — as páginas não precisam mudar.

const atraso = (ms: number) => new Promise((resolve) => window.setTimeout(resolve, ms));

// RF-03: extrair os dados do PDF do histórico.
export async function extrairDadosHistorico(_arquivo: File): Promise<DadosHistorico> {
  await atraso(600);
  return {
    aluno: "Lucas Almeida Ferreira",
    matricula: "21/0039482",
    ira: 4.32,
  };
}

// RF-07: registrar a inscrição.
export async function enviarInscricao(_dados: DadosInscricao): Promise<void> {
  await atraso(600);
}
