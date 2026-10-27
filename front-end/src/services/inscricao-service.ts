import * as pdfjsLib from "pdfjs-dist";
import type { DadosHistorico, DadosInscricao } from "../types/dados-inscricao.js";

// O worker é servido junto com a dependência instalada em front-end/node_modules.
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  "../../node_modules/pdfjs-dist/build/pdf.worker.min.mjs",
  import.meta.url,
).href;

/** Extrai o texto real do PDF e interpreta os campos do histórico da UnB. */
export async function extrairDadosHistorico(arquivo: File): Promise<DadosHistorico> {
  const documento = await pdfjsLib.getDocument({ data: await arquivo.arrayBuffer() }).promise;
  const paginas: string[] = [];

  for (let numero = 1; numero <= documento.numPages; numero += 1) {
    const pagina = await documento.getPage(numero);
    const conteudo = await pagina.getTextContent();
    paginas.push(conteudo.items
      .filter((item): item is typeof item & { str: string } => "str" in item)
      .map((item) => item.str)
      .join(" "));
  }

  const texto = paginas.join("\n").replace(/\s+/g, " ");
  const aluno = capturar(texto, /(?:nome(?:\s+do\s+aluno)?|discente)\s*:?\s*(.+?)(?=\s+(?:matr[ií]cula|ira|índice de rendimento)|$)/i);
  const matricula = capturar(texto, /matr[ií]cula\s*:?\s*([\d./-]+)/i);
  const iraTexto = capturar(texto, /(?:ira|índice de rendimento acad[êe]mico)\s*:?\s*(\d+(?:[,.]\d+)?)/i);
  const ira = Number(iraTexto.replace(",", "."));

  if (!aluno || !matricula || !iraTexto || !Number.isFinite(ira)) {
    throw new Error("Não foi possível identificar nome, matrícula e IRA no histórico.");
  }

  return { aluno: aluno.trim(), matricula: matricula.trim(), ira };
}

function capturar(texto: string, padrao: RegExp): string {
  return texto.match(padrao)?.[1]?.trim() ?? "";
}

// RF-07: o registro definitivo depende da API de inscrições, ainda não implementada.
export async function enviarInscricao(_dados: DadosInscricao): Promise<void> {
  throw new Error("O envio de inscrições ainda não está conectado ao servidor.");
}
