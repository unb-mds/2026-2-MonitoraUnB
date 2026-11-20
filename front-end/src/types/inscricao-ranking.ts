export type StatusInscricao = "pendente" | "aprovado" | "reprovado";

/** Dados devolvidos por GET /api/inscricoes para a tela do ranking. */
export type InscricaoRanking = {
  id: number;
  nome: string;
  disciplina: string;
  professor: string | null;
  ira: number;
  coef: number;
  status: StatusInscricao;
};
