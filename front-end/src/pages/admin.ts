// Painel do administrador — Monitora UnB.
// Compile para admin.js (ex.: npx tsc admin.ts --target es2020 --module es2020 --lib es2020,dom)
// Rotas esperadas no backend (todas exigem administrador logado):
//   GET  /admin/processos               -> Processo[]
//   POST /admin/processos               -> { semestre, data_abertura, data_encerramento }
//   POST /admin/processos/{id}/abrir
//   POST /admin/processos/{id}/encerrar
//   POST /admin/processos/{id}/limpar
// Erros: o backend responde JSON { "detail": "mensagem" } e o painel exibe a mensagem.

type Situacao = "AGENDADO" | "ABERTO" | "ENCERRADO";

interface Processo {
  id_processo: number;
  semestre: string;
  data_abertura: string; // AAAA-MM-DD
  data_encerramento: string; // AAAA-MM-DD
  status: Situacao;
}

// Deixe true para ver a tela funcionando sem backend; troque para false ao ligar as rotas.
const USAR_EXEMPLO = true;
const API = ""; // prefixo da API, ex.: "http://localhost:8000"
const SEMESTRE_OK = /^\d{4}\/\d$/;

const $ = <T extends HTMLElement>(id: string): T => document.getElementById(id) as T;

// ---------- comunicação com o backend ----------

async function chamar<T>(metodo: "GET" | "POST", caminho: string, corpo?: unknown): Promise<T> {
  if (USAR_EXEMPLO) return simular<T>(metodo, caminho, corpo);

  const resp = await fetch(API + caminho, {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    credentials: "include", // envia o cookie de sessão do administrador
    body: corpo === undefined ? undefined : JSON.stringify(corpo),
  });
  let dados: any = null;
  try { dados = await resp.json(); } catch { /* resposta sem corpo */ }
  if (!resp.ok) {
    const detalhe = dados && typeof dados.detail === "string" ? dados.detail : `Erro ${resp.status}.`;
    throw new Error(detalhe);
  }
  return dados as T;
}

// ---------- dados de exemplo (só para visualizar a tela) ----------

let exemplo: Processo[] = [
  { id_processo: 1, semestre: "2026/1", data_abertura: "2026-03-01", data_encerramento: "2026-04-10", status: "ENCERRADO" },
  { id_processo: 2, semestre: "2026/2", data_abertura: "2026-11-01", data_encerramento: "2026-12-15", status: "AGENDADO" },
];

async function simular<T>(metodo: string, caminho: string, corpo?: any): Promise<T> {
  await new Promise((r) => setTimeout(r, 250));
  const partes = caminho.split("/"); // ["", "admin", "processos", id?, acao?]
  if (metodo === "GET") return [...exemplo].reverse() as unknown as T;
  if (partes.length === 3) {
    exemplo.push({ id_processo: exemplo.length + 1, status: "AGENDADO", ...corpo });
    return {} as T;
  }
  const p = exemplo.find((x) => x.id_processo === Number(partes[3]))!;
  if (partes[4] === "abrir") {
    if (exemplo.some((x) => x.status === "ABERTO")) throw new Error("Já existe um processo aberto.");
    p.status = "ABERTO";
  } else if (partes[4] === "encerrar") p.status = "ENCERRADO";
  else exemplo = exemplo.filter((x) => x !== p);
  return {} as T;
}

// ---------- interface ----------

const ACOES: Record<Situacao, { rotulo: string; caminho: string; perigo: boolean; confirma?: [string, string] }> = {
  AGENDADO: { rotulo: "Abrir inscrições", caminho: "abrir", perigo: false },
  ABERTO: {
    rotulo: "Encerrar", caminho: "encerrar", perigo: false,
    confirma: ["Encerrar este processo?", "Só é possível encerrar quando todas as inscrições têm resultado e e-mail enviado."],
  },
  ENCERRADO: {
    rotulo: "Apagar dados", caminho: "limpar", perigo: true,
    confirma: ["Apagar os dados deste processo?", "Remove alunos, inscrições, resultados, o processo e as disciplinas do semestre. Esta ação não pode ser desfeita."],
  },
};

const ROTULO_SITUACAO: Record<Situacao, string> = {
  AGENDADO: "Agendado", ABERTO: "Aberto", ENCERRADO: "Encerrado",
};

function formatarData(iso: string): string {
  const [a, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${a}`;
}

function aviso(texto: string, tipo: "ok" | "erro"): void {
  const el = $("aviso");
  el.textContent = texto;
  el.className = tipo;
  el.hidden = false;
}

function confirmar(titulo: string, texto: string, perigo: boolean): Promise<boolean> {
  const dlg = $<HTMLDialogElement>("dialogo");
  $("d-titulo").textContent = titulo;
  $("d-texto").textContent = texto;
  $("d-ok").className = perigo ? "btn btn-perigo" : "btn btn-pri";
  dlg.returnValue = "";
  return new Promise((resolver) => {
    dlg.addEventListener("close", () => resolver(dlg.returnValue === "sim"), { once: true });
    dlg.showModal();
  });
}

function celula(texto: string): HTMLTableCellElement {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function desenhar(processos: Processo[]): void {
  const corpo = $("lista");
  corpo.replaceChildren();
  $("vazio").hidden = processos.length > 0;

  for (const p of processos) {
    const tr = document.createElement("tr");
    tr.append(celula(p.semestre), celula(formatarData(p.data_abertura)), celula(formatarData(p.data_encerramento)));

    const tdSel = document.createElement("td");
    const selo = document.createElement("span");
    selo.className = `selo selo-${p.status}`;
    selo.textContent = ROTULO_SITUACAO[p.status];
    tdSel.append(selo);

    const acao = ACOES[p.status];
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = acao.perigo ? "btn btn-perigo" : "btn btn-sec";
    btn.textContent = acao.rotulo;
    btn.addEventListener("click", () => executar(p, btn));
    const tdAcao = document.createElement("td");
    tdAcao.append(btn);

    tr.append(tdSel, tdAcao);
    corpo.append(tr);
  }
}

async function carregar(): Promise<void> {
  try {
    desenhar(await chamar<Processo[]>("GET", "/admin/processos"));
  } catch (e) {
    aviso((e as Error).message, "erro");
  }
}

async function executar(p: Processo, btn: HTMLButtonElement): Promise<void> {
  const acao = ACOES[p.status];
  if (acao.confirma && !(await confirmar(acao.confirma[0], acao.confirma[1], acao.perigo))) return;

  btn.disabled = true;
  try {
    await chamar("POST", `/admin/processos/${p.id_processo}/${acao.caminho}`);
    aviso(`${acao.rotulo}: concluído para o semestre ${p.semestre}.`, "ok");
  } catch (e) {
    aviso((e as Error).message, "erro");
  }
  await carregar();
}

async function criar(ev: Event): Promise<void> {
  ev.preventDefault();
  const semestre = $<HTMLInputElement>("semestre").value.trim().replace(/[.\-\s]/g, "/");
  const abertura = $<HTMLInputElement>("abertura").value;
  const encerramento = $<HTMLInputElement>("encerramento").value;

  if (!SEMESTRE_OK.test(semestre)) return aviso("Informe o semestre no formato AAAA/S, por exemplo 2026/2.", "erro");
  if (!abertura || !encerramento) return aviso("Informe as duas datas.", "erro");
  if (encerramento < abertura) return aviso("O fim das inscrições não pode ser antes do início.", "erro");

  try {
    await chamar("POST", "/admin/processos", { semestre, data_abertura: abertura, data_encerramento: encerramento });
    aviso(`Processo ${semestre} criado como agendado.`, "ok");
    (ev.target as HTMLFormElement).reset();
  } catch (e) {
    aviso((e as Error).message, "erro");
  }
  await carregar();
}

$("form-novo").addEventListener("submit", criar);
$("sair").addEventListener("click", () => {
  // TODO (colega do back/front): chamar a rota de logout do projeto e redirecionar para o login.
  window.location.href = "/login";
});
carregar();
