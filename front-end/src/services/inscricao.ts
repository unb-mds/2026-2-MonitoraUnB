import type { DadosHistorico, DadosInscricao } from "../types/dados-inscricao.js";

const API_BASE = "/api";

async function obterDetalheErro(resposta: Response, padrao: string): Promise<string> {
    try {
        const erro = await resposta.json() as { detail?: unknown };
        if (typeof erro.detail === "string" && erro.detail.trim()) return erro.detail;
    } catch {
        // A API pode responder sem JSON.
    }
    return padrao;
}

// RF-03: extrair os dados do PDF do histórico.
export async function extrairDadosHistorico(
    arquivo: File,
    disciplina: string,
    matricula: string,
): Promise<DadosHistorico> {

    const formulario = new FormData();
    formulario.append("arquivo", arquivo);
    formulario.append("disciplina", disciplina);
    formulario.append("matricula", matricula);

    const resposta = await fetch(
        `${API_BASE}/historico`,
        {
            method: "POST",
            body: formulario
        }
    );

    if (!resposta.ok) {
        throw new Error(await obterDetalheErro(resposta, "Não foi possível ler o histórico."));
    }

    return await resposta.json() as DadosHistorico;
}

// RF-07: registrar a inscrição.
export async function enviarInscricao(dados: DadosInscricao): Promise<string> {
    const resposta = await fetch(`${API_BASE}/inscricoes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            token_validacao: dados.tokenValidacao,
            semestre: dados.semestre,
            email: dados.email,
            professor: dados.professor || null,
            declaracao_sem_outra_bolsa: dados.declaracaoSemOutraBolsa,
        }),
    });

    if (!resposta.ok) {
        throw new Error(await obterDetalheErro(resposta, "Não foi possível validar a inscrição."));
    }

    const resultado = await resposta.json() as { mensagem?: unknown };
    return typeof resultado.mensagem === "string"
        ? resultado.mensagem
        : "Os dados da inscrição foram validados pela API.";
}
