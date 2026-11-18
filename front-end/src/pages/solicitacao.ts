import { lerInscricao, limparInscricao } from "../utils/storage.js";
import { formatarIra } from "../utils/validadores.js";

function definirTexto(id: string, valor: string): void {
  const elemento = document.getElementById(id);
  if (elemento) elemento.textContent = valor;
}

const dados = lerInscricao();
const resumo = document.getElementById("resumo-card");

if (dados && resumo) {
  definirTexto("aluno", dados.aluno);
  definirTexto("matricula", dados.matricula);
  definirTexto("semestre", dados.semestre);
  definirTexto("disciplina", dados.disciplinaNome);
  definirTexto("ira", formatarIra(dados.ira));
  resumo.hidden = false;
}

// Inscrição concluída: não precisamos mais guardar os dados no navegador.
limparInscricao();
