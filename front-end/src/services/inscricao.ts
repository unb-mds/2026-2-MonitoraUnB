import type { DadosHistorico, DadosInscricao } from "../types/inscricao.js";

const atraso = (ms: number) => new Promise((resolve) => window.setTimeout(resolve, ms));

// RF-03: extrair os dados do PDF do histórico.
export async function extrairDadosHistorico(arquivo: File): Promise<DadosHistorico> {
  await atraso(600);
  const formulario = new FormData();
  formulario.append("arquivo", arquivo);
  
  const resposta = await fetch(
    "http://127.0.0.1:8000/api/historico",
    {
      method: "POST",
      body: formulario
    }
  );

  if (!resposta.ok) {
    const erro = await resposta.json();
    throw new Error(erro.detail);
  }

  const dados = await resposta.json();

  return dados;
}

// RF-07: registrar a inscrição.
export async function enviarInscricao(_dados: DadosInscricao): Promise<void> {
  await atraso(600);
}
