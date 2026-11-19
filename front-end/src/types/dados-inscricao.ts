// Formato dos dados que "viajam" entre as telas (inscricao -> revisao -> solicitacao).
export type DadosInscricao = {
  aluno: string;
  matricula: string;
  semestre: string;
  disciplina: string; // código informado (ex.: "MAT0025")
  disciplinaNome: string; // texto exibido na revisão
  professor: string;
  email: string;
  ira: number;
  tokenValidacao: string;
  mencao: string;
  situacaoDisciplina: string;
  periodoDisciplina: string;
  coefMencao: number;
  coeficienteCandidatura: number;
  declaracaoSemOutraBolsa: true;
  arquivoHistorico: string; // só o nome do arquivo enviado
};

// O que o back-end vai devolver depois de ler o PDF do histórico (RF-03).
export type DadosHistorico = {
  aluno: string;
  matricula: string;
  ira: number;
  status: string;
  disciplina: {
    codigo: string;
    nome: string;
    mencao: string;
    situacao: string;
    periodo: string;
    coef_mencao: number;
  };
  coeficiente_candidatura: number;
  token_validacao: string;
};
