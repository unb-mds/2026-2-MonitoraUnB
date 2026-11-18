import { logout, me } from "../services/auth.js";

const LOGIN = "login-professor.html";
const INICIO = "inicio.html";

const botaoSair = document.getElementById("btn-sair") as HTMLButtonElement | null;

async function garantirSessao(): Promise<boolean> {
  try {
    const sessao = await me();
    if (!sessao.authenticated) {
      window.location.replace(LOGIN);
      return false;
    }
    return true;
  } catch {
    window.location.replace(LOGIN);
    return false;
  }
}

async function sair(): Promise<void> {
  if (botaoSair) {
    botaoSair.disabled = true;
  }

  try {
    await logout();
  } catch {
    // mesmo se o logout falhar na API, sai da área do professor
  }

  window.location.href = INICIO;
}

void (async () => {
  const autenticado = await garantirSessao();

  if (autenticado && botaoSair) {
    botaoSair.addEventListener("click", () => {
      void sair();
    });
  }
})();
