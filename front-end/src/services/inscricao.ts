import type { DadosHistorico, DadosInscricao } from "../types/dados-inscricao.js";

const atraso = (ms: number) => new Promise((resolve) => window.setTimeout(resolve, ms));

// RF-03: extrair os dados do PDF do histórico.
export async function extrairDadosHistorico(
  arquivo: File, 
  disciplina: string
):Promise<DadosHistorico> {
                                            
  const formulario = new FormData();                                        
  formulario.append("arquivo", arquivo);
  formulario.append("disciplina", disciplina);
  
  const resposta = await fetch(
    "http://127.0.0.1:8000/api/historico",
    {
      method: "POST",
      body: formulario
    }
  );

  if (!resposta.ok) {
    let detalhe = "Não foi possível ler o histórico.";
    try {
      const erro = await resposta.json() as { detail?: unknown };
      if (typeof erro.detail === "string" && erro.detail.trim()) detalhe = erro.detail;
    } catch {
      // a API respondeu sem JSON
    }
    throw new Error(detalhe);
  }

  const dados = await resposta.json();

  return dados;
}

// RF-07: registrar a inscrição.
export async function enviarInscricao(_dados: DadosInscricao): Promise<void> {
  await atraso(600);
}
