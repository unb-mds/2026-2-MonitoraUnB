const API_BASE = "http://127.0.0.1:8000";

export type LoginResultado = {
  mensagem: string;
  username: string;
};

export type MeResultado = {
  authenticated: boolean;
  username: string | null;
};

async function lerDetalheErro(resposta: Response, fallback: string): Promise<string> {
  try {
    const erro = (await resposta.json()) as { detail?: unknown };
    if (typeof erro.detail === "string" && erro.detail.trim()) {
      return erro.detail;
    }
  } catch {
    // resposta sem JSON
  }
  return fallback;
}

export async function login(username: string, password: string): Promise<LoginResultado> {
  const resposta = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ username, password }),
  });

  if (!resposta.ok) {
    const detalhe = await lerDetalheErro(
      resposta,
      resposta.status === 401
        ? "Login ou senha inválidos."
        : "Não foi possível entrar. Tente de novo.",
    );
    throw new Error(detalhe);
  }

  return (await resposta.json()) as LoginResultado;
}

export async function logout(): Promise<void> {
  const resposta = await fetch(`${API_BASE}/api/auth/logout`, {
    method: "POST",
    credentials: "include",
  });

  if (!resposta.ok) {
    const detalhe = await lerDetalheErro(resposta, "Não foi possível sair.");
    throw new Error(detalhe);
  }
}

export async function me(): Promise<MeResultado> {
  const resposta = await fetch(`${API_BASE}/api/auth/me`, {
    method: "GET",
    credentials: "include",
  });

  if (!resposta.ok) {
    const detalhe = await lerDetalheErro(resposta, "Não foi possível verificar a sessão.");
    throw new Error(detalhe);
  }

  return (await resposta.json()) as MeResultado;
}
