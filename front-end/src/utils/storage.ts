import type { DadosInscricao } from "../types/dados-inscricao.js";

// Como o site tem várias páginas .html, usamos o sessionStorage do navegador
// pra levar os dados de uma tela pra outra. Some quando a aba é fechada.
const CHAVE = "monitora-unb:inscricao";
const CHAVE_MOTIVO = "monitora-unb:motivo-nao-apto";

export function salvarInscricao(dados: DadosInscricao): void {
  sessionStorage.removeItem(CHAVE_MOTIVO);
  sessionStorage.setItem(CHAVE, JSON.stringify(dados));
}

export function lerInscricao(): DadosInscricao | null {
  const bruto = sessionStorage.getItem(CHAVE);
  if (!bruto) return null;

  try {
    return JSON.parse(bruto) as DadosInscricao;
  } catch {
    return null;
  }
}

export function limparInscricao(): void {
  sessionStorage.removeItem(CHAVE);
  sessionStorage.removeItem(CHAVE_MOTIVO);
}

export function salvarMotivo(motivo: string): void {
  sessionStorage.setItem(CHAVE_MOTIVO, motivo);
}

export function lerMotivo(): string | null {
  return sessionStorage.getItem(CHAVE_MOTIVO);
}
