// Regras puras, sem mexer no DOM.

// RNF-09: só aceitamos PDF no upload do histórico.
export function ehPdf(arquivo: File): boolean {
  return arquivo.type === "application/pdf" || arquivo.name.toLowerCase().endsWith(".pdf");
}

export function formatarIra(ira: number): string {
  return ira.toFixed(2).replace(".", ",");
}
