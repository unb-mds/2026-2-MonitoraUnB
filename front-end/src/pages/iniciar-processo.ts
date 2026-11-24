(() => {
  // Se houver prefixo no Nginx (ex.: "/api") ou backend em outra origem (ex.: "http://localhost:8000"), ajuste aqui:
  const PA_API_BASE = "";

  type StatusProcesso = "AGENDADO" | "ABERTO" | "ENCERRADO" | string;

  interface ProcessoSeletivo {
    id: number | string;
    semestre: string;
    data_abertura?: string;
    data_encerramento?: string;
    status: StatusProcesso;
  }

  interface UsuarioAtual {
    role?: string;
    perfil?: string;
    tipo?: string;
    is_admin?: boolean;
    admin?: boolean;
  }

  const bloco = document.getElementById("pa-bloco") as HTMLDivElement | null;
  const btnIniciar = document.getElementById("pa-iniciar") as HTMLButtonElement | null;
  const statusEl = document.getElementById("pa-status") as HTMLSpanElement | null;
  const avisoEl = document.getElementById("pa-aviso") as HTMLParagraphElement | null;
  const dialogo = document.getElementById("pa-dialogo") as HTMLDialogElement | null;
  const form = document.getElementById("pa-form") as HTMLFormElement | null;
  const inputSemestre = document.getElementById("pa-semestre") as HTMLInputElement | null;
  const inputAbertura = document.getElementById("pa-abertura") as HTMLInputElement | null;
  const inputEncerramento = document.getElementById("pa-encerramento") as HTMLInputElement | null;
  const btnCancelar = document.getElementById("pa-cancelar") as HTMLButtonElement | null;
  const btnConfirmar = document.getElementById("pa-confirmar") as HTMLButtonElement | null;

  if (!bloco || !btnIniciar || !dialogo || !form) {
    return;
  }

  function hojeISO(): string {
    const agora = new Date();
    const ano = agora.getFullYear();
    const mes = String(agora.getMonth() + 1).padStart(2, "0");
    const dia = String(agora.getDate()).padStart(2, "0");
    return `${ano}-${mes}-${dia}`;
  }

  function mostrarAviso(mensagem: string, tipo: "erro" | "ok" | "alerta" = "alerta"): void {
    if (!avisoEl) return;
    avisoEl.textContent = mensagem;
    avisoEl.dataset.tipo = tipo;
    avisoEl.hidden = false;
  }

  function limparAviso(): void {
    if (!avisoEl) return;
    avisoEl.textContent = "";
    avisoEl.hidden = true;
    delete avisoEl.dataset.tipo;
  }

  function headersPadrao(): HeadersInit {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };
    const token =
      localStorage.getItem("token") ||
      localStorage.getItem("access_token") ||
      sessionStorage.getItem("token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
    return headers;
  }

  async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
    const url = `${PA_API_BASE}${path}`;
    return fetch(url, {
      ...init,
      credentials: "include",
      headers: {
        ...headersPadrao(),
        ...(init.headers || {}),
      },
    });
  }

  function ehAdmin(usuario: UsuarioAtual | null): boolean {
    if (!usuario) return false;
    if (usuario.is_admin === true || usuario.admin === true) return true;
    const cargo = (usuario.role || usuario.perfil || usuario.tipo || "").toLowerCase();
    return cargo === "admin" || cargo === "administrador";
  }

  async function verificarPermissaoAdmin(): Promise<boolean> {
    try {
      const resMe = await apiFetch("/auth/me", { method: "GET" });
      if (resMe.ok) {
        const data = (await resMe.json()) as UsuarioAtual;
        return ehAdmin(data);
      }
      if (resMe.status === 401 || resMe.status === 403) {
        return false;
      }
    } catch {
      // Se /auth/me não existir ou falhar, tenta sondar a rota protegida de processos
    }

    try {
      const resProcessos = await apiFetch("/admin/processos", { method: "GET" });
      return resProcessos.ok;
    } catch {
      return false;
    }
  }

  async function atualizarEstadoProcessos(): Promise<void> {
    if (!btnIniciar || !statusEl) return;

    btnIniciar.disabled = false;
    statusEl.textContent = "";

    try {
      const res = await apiFetch("/admin/processos", { method: "GET" });
      if (!res.ok) return;

      const processos = (await res.json()) as ProcessoSeletivo[];
      if (!Array.isArray(processos)) return;

      const aberto = processos.find((p) => String(p.status).toUpperCase() === "ABERTO");
      if (aberto) {
        btnIniciar.disabled = true;
        statusEl.textContent = `Processo aberto: ${aberto.semestre}`;
      }
    } catch {
      // Mantém o botão habilitado caso a listagem não bloqueie a criação
    }
  }

  async function extrairMensagemErro(res: Response, fallback: string): Promise<string> {
    try {
      const corpo = await res.json();
      if (typeof corpo?.detail === "string") return corpo.detail;
      if (typeof corpo?.message === "string") return corpo.message;
    } catch {
      // Ignora erro de parse JSON
    }
    return fallback;
  }

  async function abrirProcessoCriado(
    processo: ProcessoSeletivo
  ): Promise<{ aberto: boolean; motivo?: string }> {
    const endpointsCandidatos = [
      `/admin/processos/${processo.id}/abrir`,
      `/admin/processos/${processo.id}/status`,
    ];

    for (const endpoint of endpointsCandidatos) {
      const metodo = endpoint.endsWith("/status") ? "PATCH" : "POST";
      const body = endpoint.endsWith("/status")
        ? JSON.stringify({ status: "ABERTO" })
        : undefined;

      const res = await apiFetch(endpoint, { method: metodo, body });
      if (res.ok) {
        return { aberto: true };
      }
      if (res.status !== 404) {
        const detalhe = await extrairMensagemErro(
          res,
          "O banco recusou a abertura das inscrições (verifique se as disciplinas do semestre já foram carregadas pelo scraper)."
        );
        return { aberto: false, motivo: detalhe };
      }
    }

    return {
      aberto: false,
      motivo: "Não foi possível abrir as inscrições automaticamente pela rota configurada.",
    };
  }

  btnIniciar.addEventListener("click", () => {
    limparAviso();
    if (inputAbertura && !inputAbertura.value) {
      inputAbertura.value = hojeISO();
    }
    if (typeof dialogo.showModal === "function") {
      dialogo.showModal();
    } else {
      dialogo.setAttribute("open", "");
    }
    inputSemestre?.focus();
  });

  btnCancelar?.addEventListener("click", () => {
    dialogo.close();
  });

  form.addEventListener("submit", async (event: Event) => {
    event.preventDefault();
    limparAviso();

    const semestre = inputSemestre?.value.trim() || "";
    const dataAbertura = inputAbertura?.value || "";
    const dataEncerramento = inputEncerramento?.value || "";

    if (!/^\d{4}\/[12]$/.test(semestre)) {
      mostrarAviso("Informe o semestre no formato AAAA/1 ou AAAA/2 (ex.: 2026/2).", "erro");
      return;
    }

    if (!dataAbertura || !dataEncerramento) {
      mostrarAviso("Preencha as datas de início e fim das inscrições.", "erro");
      return;
    }

    if (dataEncerramento < dataAbertura) {
      mostrarAviso("A data de fim das inscrições não pode ser anterior à data de início.", "erro");
      return;
    }

    if (btnConfirmar) btnConfirmar.disabled = true;

    try {
      const resCriar = await apiFetch("/admin/processos", {
        method: "POST",
        body: JSON.stringify({
          semestre,
          data_abertura: dataAbertura,
          data_encerramento: dataEncerramento,
        }),
      });

      if (!resCriar.ok) {
        const msgErro = await extrairMensagemErro(resCriar, "Não foi possível criar o processo seletivo.");
        mostrarAviso(msgErro, "erro");
        return;
      }

      const criado = (await resCriar.json()) as ProcessoSeletivo;
      const resultadoAbertura = await abrirProcessoCriado(criado);

      dialogo.close();
      form.reset();
      await atualizarEstadoProcessos();

      if (resultadoAbertura.aberto) {
        mostrarAviso(`Processo ${semestre} criado e inscrições abertas com sucesso.`, "ok");
      } else {
        mostrarAviso(
          `Processo ${semestre} criado, mas não foi aberto: ${
            resultadoAbertura.motivo || "verifique as disciplinas do semestre."
          }`,
          "alerta"
        );
      }
    } catch {
      mostrarAviso("Falha de comunicação com o servidor ao iniciar o processo seletivo.", "erro");
    } finally {
      if (btnConfirmar) btnConfirmar.disabled = false;
    }
  });

  async function init(): Promise<void> {
    if (!bloco) return;
    bloco.hidden = true;

    const autorizado = await verificarPermissaoAdmin();
    if (!autorizado) {
      bloco.hidden = true;
      return;
    }

    bloco.hidden = false;
    await atualizarEstadoProcessos();
  }

  void init();
})();
