import {
    baixarPlanilhaInscricoes,
    listarInscricoes,
    obterProcessoAberto,
} from "../services/inscricao.js";
import type { InscricaoRanking, StatusInscricao } from "../types/inscricao-ranking.js";

type LinhaVisivel = {
    pos: number;
    item: InscricaoRanking;
};

let semestreAtual = "";
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
    const todas = document.createElement("option");
    todas.value = "";
    todas.textContent = "Todas as disciplinas";
    selDisciplina.replaceChildren(todas);

    nomes.forEach((nome) => {
        const opcao = document.createElement("option");
        opcao.value = nome;
        opcao.textContent = nome;
        selDisciplina.append(opcao);
    });
}

function filtradas(): InscricaoRanking[] {
    return inscricoes.filter(
        (i) => !selDisciplina.value || i.disciplina === selDisciplina.value,
    );
}

function porRanking(a: InscricaoRanking, b: InscricaoRanking): number {
    return b.ira - a.ira || b.coef - a.coef;
}

function escaparHtml(valor: string): string {
    return valor.replace(/[&<>"']/g, (caractere) => {
        const entidades: Record<string, string> = {
            "&": "&amp;",
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#39;",
        };
        return entidades[caractere];
    });
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
                `<td>${escaparHtml(i.nome)}</td>` +
                `<td>${escaparHtml(i.disciplina)}</td>` +
                `<td>${escaparHtml(i.professor ?? "Não informado")}</td>` +
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

async function baixarPlanilha(): Promise<void> {
    if (!visiveis.length || !semestreAtual) return;

    btnBaixar.disabled = true;
    try {
        const disciplina = selDisciplina.value || undefined;
        const blob = await baixarPlanilhaInscricoes(semestreAtual, disciplina);

        const hoje = new Date().toISOString().slice(0, 10);
        const escopo = disciplina
            ? disciplina
                .toLowerCase()
                .replace(/[^a-z0-9]+/g, "-")
                .replace(/^-|-$/g, "")
            : "todas-as-disciplinas";

        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");

        a.href = url;
        a.download = `ranking-monitoria-${escopo}-${hoje}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (erro) {
        const mensagem = erro instanceof Error
            ? erro.message
            : "Não foi possível baixar a planilha.";
        alert(mensagem);
    } finally {
        btnBaixar.disabled = !visiveis.length;
    }
}

function ehStatusInscricao(valor: string | undefined): valor is StatusInscricao {
    return valor === "pendente" || valor === "aprovado" || valor === "reprovado";
}

function exibirErroCarregamento(mensagem: string): void {
    contador.textContent = "Não foi possível carregar as inscrições.";
    btnBaixar.disabled = true;

    const linha = document.createElement("tr");
    const celula = document.createElement("td");
    celula.colSpan = 8;
    celula.className = "vazio";
    celula.textContent = mensagem;
    linha.append(celula);
    corpo.replaceChildren(linha);
}

async function carregarInscricoes(): Promise<void> {
    contador.textContent = "Carregando inscrições...";
    btnBaixar.disabled = true;

    try {
        const { semestre } = await obterProcessoAberto();
        semestreAtual = semestre;
        inscricoes.length = 0;
        inscricoes.push(...await listarInscricoes(semestre));
        preencherDisciplinas();
        desenhar();
    } catch (erro) {
        const mensagem = erro instanceof Error
            ? erro.message
            : "Não foi possível carregar as inscrições.";
        exibirErroCarregamento(mensagem);
    }
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

void carregarInscricoes();
