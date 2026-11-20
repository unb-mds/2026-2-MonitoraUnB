type StatusInscricao = "pendente" | "aprovado" | "reprovado";

type InscricaoRanking = {
  id: number;
  nome: string;
  disciplina: string;
  professor: string;
  ira: number;
  coef: number;
  status: StatusInscricao;
};

type LinhaVisivel = {
  pos: number;
  item: InscricaoRanking;
};

/* ===== DADOS DE EXEMPLO =====
   Quando o banco estiver pronto, esta lista virá dele:
   uma linha por inscrição (status: pendente | aprovado | reprovado) */
const inscricoes: InscricaoRanking[] = [];

const selDisciplina = document.getElementById("filtro-disciplina") as HTMLSelectElement;
const selOrdenar = document.getElementById("ordenar") as HTMLSelectElement;
const corpo = document.getElementById("ranking-corpo") as HTMLTableSectionElement;
const contador = document.getElementById("contador") as HTMLParagraphElement;
const btnBaixar = document.getElementById("btn-baixar") as HTMLButtonElement;

/** Linhas que estão aparecendo agora (usadas na planilha). */
let visiveis: LinhaVisivel[] = [];

const ROTULOS: Record<StatusInscricao, string> = {
  pendente: "Pendente",
  aprovado: "Aprovado",
  reprovado: "Reprovado",
};

function fmt(n: number): string {
  return n.toFixed(2).replace(".", ",");
}

function unicos(lista: string[]): string[] {
  return lista
    .filter((v, i) => lista.indexOf(v) === i)
    .sort((a, b) => a.localeCompare(b, "pt-BR"));
}

function preencherDisciplinas(): void {
  const nomes = unicos(inscricoes.map((i) => i.disciplina));
  selDisciplina.innerHTML =
    '<option value="">Todas as disciplinas</option>' +
    nomes.map((n) => `<option value="${n}">${n}</option>`).join("");
}

function filtradas(): InscricaoRanking[] {
  return inscricoes.filter(
    (i) => !selDisciplina.value || i.disciplina === selDisciplina.value,
  );
}

function porRanking(a: InscricaoRanking, b: InscricaoRanking): number {
  return b.ira - a.ira || b.coef - a.coef;
}

function desenhar(): void {
  const lista = filtradas();

  // posição no ranking (por IRA) dentro do filtro atual
  const posicao: Record<number, number> = {};
  lista
    .slice()
    .sort(porRanking)
    .forEach((i, idx) => {
      posicao[i.id] = idx + 1;
    });

  const ordenada = lista.slice().sort(
    selOrdenar.value === "alfabetica"
      ? (a, b) => a.nome.localeCompare(b.nome, "pt-BR")
      : porRanking,
  );

  contador.textContent =
    lista.length + (lista.length === 1 ? " candidato" : " candidatos");

  visiveis = ordenada.map((i) => ({ pos: posicao[i.id], item: i }));
  btnBaixar.disabled = !ordenada.length;

  if (!ordenada.length) {
    corpo.innerHTML =
      '<tr><td colspan="8" class="vazio">Nenhuma inscrição encontrada.</td></tr>';
    return;
  }

  corpo.innerHTML = ordenada
    .map(
      (i) =>
        `<tr class="${i.status === "pendente" ? "" : i.status}" data-id="${i.id}">` +
        `<td>${posicao[i.id]}</td>` +
        `<td>${i.nome}</td>` +
        `<td>${i.disciplina}</td>` +
        `<td>${i.professor}</td>` +
        `<td>${fmt(i.ira)}</td>` +
        `<td>${fmt(i.coef)}</td>` +
        `<td><span class="situacao">${ROTULOS[i.status]}</span></td>` +
        `<td><div class="botoes-acao">` +
        `<button type="button" class="btn-acao btn-aprovar" data-acao="aprovado" aria-pressed="${i.status === "aprovado"}">Aprovar</button>` +
        `<button type="button" class="btn-acao btn-reprovar" data-acao="reprovado" aria-pressed="${i.status === "reprovado"}">Reprovar</button>` +
        `</div></td>` +
        `</tr>`,
    )
    .join("");
}

function celula(valor: string | number): string {
  let t = String(valor);
  if (/^[=+\-@]/.test(t)) t = "'" + t; // evita fórmulas vindas de texto digitado
  return `"${t.replace(/"/g, '""')}"`;
}

function gerarCSV(): string {
  const linhas: Array<Array<string | number>> = [
    ["Posição", "Nome completo", "Disciplina", "Professor", "IRA", "COEF", "Situação"],
  ];

  visiveis.forEach((v) => {
    const i = v.item;
    linhas.push([
      v.pos,
      i.nome,
      i.disciplina,
      i.professor,
      fmt(i.ira),
      fmt(i.coef),
      ROTULOS[i.status],
    ]);
  });

  // ponto e vírgula + BOM: o Excel em português abre com colunas e acentos corretos
  return (
    "\uFEFF" +
    linhas.map((l) => l.map(celula).join(";")).join("\r\n")
  );
}

function baixarPlanilha(): void {
  if (!visiveis.length) return;

  const hoje = new Date().toISOString().slice(0, 10);
  const escopo = selDisciplina.value
    ? selDisciplina.value
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, "-")
        .replace(/^-|-$/g, "")
    : "todas-as-disciplinas";

  const blob = new Blob([gerarCSV()], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");

  a.href = url;
  a.download = `ranking-monitoria-${escopo}-${hoje}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function ehStatusInscricao(valor: string | undefined): valor is StatusInscricao {
  return valor === "pendente" || valor === "aprovado" || valor === "reprovado";
}

selDisciplina.addEventListener("change", desenhar);
btnBaixar.addEventListener("click", baixarPlanilha);
selOrdenar.addEventListener("change", desenhar);

corpo.addEventListener("click", (e) => {
  const alvo = e.target;
  if (!(alvo instanceof Element)) return;

  const botao = alvo.closest(".btn-acao");
  if (!(botao instanceof HTMLButtonElement)) return;

  const linha = botao.closest("tr");
  if (!linha) return;

  const id = Number(linha.dataset.id);
  const acao = botao.dataset.acao;
  if (!ehStatusInscricao(acao)) return;

  inscricoes.forEach((i) => {
    if (i.id === id) i.status = acao;
  });
  desenhar();
});

preencherDisciplinas();
desenhar();
