import type { DadosInscricao } from "../types/inscricao.js";

// Como o site tem várias páginas .html, usamos o sessionStorage do navegador
// pra levar os dados de uma tela pra outra. Some quando a aba é fechada.
const CHAVE = "monitora-unb:inscricao";

export function salvarInscricao(dados: DadosInscricao): void {
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
}
