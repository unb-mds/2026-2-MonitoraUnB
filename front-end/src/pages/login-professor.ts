import { login } from "../services/auth.js";

const DESTINO = "ranking.html";

const formLogin = document.getElementById("form-login") as HTMLFormElement;
const campoLogin = document.getElementById("login") as HTMLInputElement;
const campoSenha = document.getElementById("senha") as HTMLInputElement;
const erroLogin = document.getElementById("erro-login") as HTMLParagraphElement;
const botaoEntrar = formLogin.querySelector(
  'button[type="submit"]',
) as HTMLButtonElement;
const toggleSenha = document.getElementById("toggle-senha");
const textoOriginalBotao = botaoEntrar.textContent ?? "Entrar no Portal";

function mostrarErro(mensagem: string): void {
  erroLogin.textContent = mensagem;
}

function limparErro(): void {
  erroLogin.textContent = "";
}

function definirCarregando(carregando: boolean): void {
  botaoEntrar.disabled = carregando;
  botaoEntrar.textContent = carregando ? "Entrando..." : textoOriginalBotao;
}

if (toggleSenha instanceof HTMLButtonElement) {
  toggleSenha.addEventListener("click", () => {
    const revelado = campoSenha.type === "text";
    campoSenha.type = revelado ? "password" : "text";
    toggleSenha.setAttribute(
      "aria-label",
      revelado ? "Mostrar senha" : "Ocultar senha",
    );
    toggleSenha.title = revelado ? "Mostrar senha" : "Ocultar senha";
  });
}

formLogin.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  if (botaoEntrar.disabled) return;

  limparErro();

  const username = campoLogin.value.trim();
  const password = campoSenha.value;

  if (!username || !password) {
    mostrarErro("Preencha o usuário e a senha.");
    return;
  }

  definirCarregando(true);

  try {
    await login(username, password);
    window.location.href = DESTINO;
  } catch (erro) {
    const mensagem =
      erro instanceof Error && erro.message.trim()
        ? erro.message
        : "Não foi possível entrar. Tente de novo.";
    mostrarErro(mensagem);
    definirCarregando(false);
  }
});
