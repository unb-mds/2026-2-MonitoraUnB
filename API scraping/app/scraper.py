"""
API Faz scraping das páginas públicas do SIGAA UnB:
  - Componentes curriculares: https://sigaa.unb.br/sigaa/public/componentes/busca_componentes.jsf
  - Turmas e Docentes: https://sigaa.unb.br/sigaa/public/turmas/listar.jsf
"""

import asyncio
import logging
import re
from datetime import datetime
from html import unescape
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from app.config import get_settings
from app.models import Departamento, Disciplina, Professor, Turma, ScrapingLog

logger = logging.getLogger(__name__)
settings = get_settings()

NIVEIS = {
    "F": "FORMAÇÃO COMPLEMENTAR",
    "G": "GRADUAÇÃO",
    "L": "LATO SENSU - ESPECIALIZAÇÃO",
    "R": "LATO SENSU - RESIDÊNCIA",
    "S": "STRICTO SENSU",
}

TIPOS = {
    0: "TODOS",
    1: "ATIVIDADE",
    2: "DISCIPLINA",
    3: "MÓDULO",
    4: "BLOCO",
}

DEPARTAMENTOS = {
    672: "CAMPUS UNB CEILÂNDIA: FACULDADE DE CIÊNCIAS E TECNOLOGIAS EM SAÚDE",
    673: "CAMPUS UNB GAMA: FACULDADE DE CIÊNCIAS E TECNOLOGIAS EM ENGENHARIA",
    640: "CENTRO DE DESENVOLVIMENTO SUSTENTÁVEL",
    314: "CENTRO DE EXCELÊNCIA EM TURISMO",
    650: "CENTRO ESTUDOS AVANÇADOS MULTIDISCIPLIN",
    316: "CENTRO INTEGRADO ORDENAMENTO TERRITORIAL",
    1448: "CENTRO INTERNACIONAL DE BIOÉTICA E HUMANIDADES",
    677: "CENTRO UNB CERRADO",
    130: "DECANATO DE ENSINO DE GRADUACAO / DEG",
    170: "DECANATO DE PÓS-GRADUAÇÃO / DPG",
    158: "DECANATO EXTENSÃO",
    351: "DEPARTAMENTO DE AUDIOVISUAIS E PUBLICIDADE/DAP",
    345: "DEPARTAMENTO DE COMUNICAÇÃO ORGANIZACIONAL/COM",
    660: "DEPARTAMENTO DE DESIGN",
    449: "DEPARTAMENTO DE ENGENHARIA MECANICA",
    479: "DEPARTAMENTO DE ESTUDOS LATINO AMERICANO",
    678: "DEPARTAMENTO DE FARMACIA",
    791: "DEPARTAMENTO DE GESTAO DE POLITICAS PUBL",
    352: "DEPARTAMENTO DE JORNALISMO/JOR",
    518: "DEPARTAMENTO DE MATEMÁTICA",
    390: "DEPARTAMENTO DE MÉTODOS E TÉCNICAS",
    391: "DEPARTAMENTO DE POLÍTICAS PÚBLICAS E GESTÃO DA EDUCAÇÃO",
    592: "DEPARTAMENTO DE PSICOLOGIA CLÍNICA",
    483: "DEPARTAMENTO DE SOCIOLOGIA",
    392: "DEPARTAMENTO DE TEORIA E FUNDAMENTOS",
    327: "DEPTO ADMINISTRAÇÃO",
    481: "DEPTO ANTROPOLOGIA",
    492: "DEPTO ARTES CÊNICAS",
    498: "DEPTO ARTES VISUAIS",
    464: "DEPTO BIOLOGIA CELULAR",
    462: "DEPTO BOTÂNICA",
    333: "DEPTO CIÊNCIAS CONTÁBEIS ATUARIAIS",
    508: "DEPTO CIÊNCIAS DA COMPUTAÇÃO",
    466: "DEPTO CIÊNCIAS FISIOLÓGICAS",
    337: "DEPTO CIÊNCIAS INFORMAÇÃO DOCUMENTAÇÃO",
    467: "DEPTO ECOLOGIA",
    548: "DEPTO ECONOMIA",
    422: "DEPTO ENFERMAGEM",
    437: "DEPTO ENGENHARIA CIVIL E AMBIENTAL",
    760: "DEPTO ENGENHARIA DE PRODUCAO",
    443: "DEPTO ENGENHARIA ELETRICA",
    433: "DEPTO ENGENHARIA FLORESTAL",
    514: "DEPTO ESTATÍSTICA",
    552: "DEPTO FILOSOFIA",
    469: "DEPTO FITOPATOLOGIA",
    471: "DEPTO GENÉTICA E MORFOLOGIA",
    555: "DEPTO GEOGRAFIA",
    539: "DEPTO GEOLOGIA GERAL APLICADA",
    541: "DEPTO GEOQUÍMICA E RECURSOS MINERAIS",
    559: "DEPTO HISTÓRIA",
    578: "DEPTO LINGUISTICA, PORT. LING. CLASSICAS",
    574: "DEPTO LÍNGUAS ESTRANGEIRAS E TRADUÇÃO",
    540: "DEPTO MINERALOGIA E PETROLOGIA",
    495: "DEPTO MÚSICA",
    424: "DEPTO NUTRICAO",
    427: "DEPTO ODONTOLOGIA",
    594: "DEPTO PROCESSOS PSICOLÓGICOS BÁSICOS",
    360: "DEPTO PROJETOS EXPRES REPRES ARQ E URBAN",
    593: "DEPTO PSICOLOGIA ESCOLAR DESENVOLVIMENTO",
    596: "DEPTO PSICOLOGIA SOCIAL E DO TRABALHO",
    420: "DEPTO SAUDE COLETIVA",
    563: "DEPTO SERVIÇO SOCIAL",
    361: "DEPTO TECNOLOGIA ARQUITETURA URBANISMO",
    362: "DEPTO TEORIA HISTORIA ARQUIT E URBANISM",
    580: "DEPTO TEORIA LITERÁRIA E LITERATURA",
    472: "DEPTO ZOOLOGIA",
    643: "DIRETORIA DO CENTRO DE APOIO AO DESENVOLVIMENTO TECNOLÓGICO",
    363: "FACULDADE DE AGRONOMIA E MEDICINA VETERINÁRIA",
    353: "FACULDADE DE ARQUITETURA E URBANISMO",
    674: "FACULDADE DE CIÊNCIA DA INFORMAÇÃO",
    410: "FACULDADE DE CIÊNCIAS DA SAÚDE",
    343: "FACULDADE DE COMUNICAÇÃO",
    370: "FACULDADE DE DIREITO",
    381: "FACULDADE DE EDUCAÇÃO",
    393: "FACULDADE DE EDUCAÇÃO FÍSICA",
    402: "FACULDADE DE MEDICINA",
    666: "FACULDADE DE PLANALTINA",
    429: "FACULDADE DE TECNOLOGIA",
    323: "FACULDADE ECONOMIA, ADMINISTRAÇÃO, CONTABILIDADE E GEST POL PÚBLICAS",
    284: "FAZENDA AGUA LIMPA",
    485: "INSTITUTO DE ARTES",
    668: "INSTITUTO DE CIÊNCIA POLÍTICA",
    455: "INSTITUTO DE CIÊNCIAS BIOLÓGICAS",
    504: "INSTITUTO DE CIÊNCIAS EXATAS",
    544: "INSTITUTO DE CIÊNCIAS HUMANAS",
    473: "INSTITUTO DE CIÊNCIAS SOCIAIS",
    524: "INSTITUTO DE FÍSICA",
    533: "INSTITUTO DE GEOCIÊNCIAS",
    567: "INSTITUTO DE LETRAS",
    583: "INSTITUTO DE PSICOLOGIA",
    610: "INSTITUTO DE QUÍMICA",
    669: "INSTITUTO DE RELAÇÕES INTERNACIONAIS",
    542: "OBSERVATÓRIO SISMOLÓGICO",
    69: "REITORIA",
    140: "SECRETARIA DE ADMINISTRACAO ACADEMICA",
}


class SigaaScraper:
    """Scraper para o portal público do SIGAA UnB."""

    HOME_URL = f"{settings.SIGAA_BASE_URL}/public/home.jsf"
    BUSCA_URL = f"{settings.SIGAA_BASE_URL}/public/componentes/busca_componentes.jsf"
    TURMAS_URL = f"{settings.SIGAA_BASE_URL}/public/turmas/listar.jsf?aba=p-ensino"

    ABA_POR_NIVEL = {
        "G": "p-graduacao",
        "S": "p-stricto",
        "L": "p-lato",
        "T": "p-tecnico",
    }

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": f"{settings.SIGAA_BASE_URL}/public/componentes/busca_componentes.jsf",
        "Origin": "https://sigaa.unb.br",
    }

    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Retorna um cliente HTTP reutilizável."""
        if self.client is None or self.client.is_closed:
            self.client = httpx.AsyncClient(
                headers=self.HEADERS,
                timeout=httpx.Timeout(45.0),
                follow_redirects=True,
                verify=True,
            )
        return self.client

    async def close(self):
        """Fecha o cliente HTTP."""
        if self.client and not self.client.is_closed:
            await self.client.aclose()

    async def _inicializar_sessao(self, client: httpx.AsyncClient, nivel: str = "G") -> str:
        """
        Garante que a sessão JSF do SIGAA está inicializada e retorna o ViewState.
        """
        await client.get(self.HOME_URL)

        aba = self.ABA_POR_NIVEL.get(nivel, "p-ensino")
        url_com_aba = f"{self.BUSCA_URL}?nivel={nivel}&aba={aba}"
        response = await client.get(url_com_aba)
        response.raise_for_status()

        html = response.content.decode("iso-8859-1", errors="replace")
        soup = BeautifulSoup(html, "html.parser")
        view_state_input = soup.find("input", {"name": "javax.faces.ViewState"})
        if view_state_input:
            return view_state_input.get("value", "j_id1")
        return "j_id1"

    async def buscar_componentes(
        self,
        nivel: str = "G",
        tipo: int = 2,
        unidade_id: int = 0,
    ) -> list[dict]:
        """
        Faz a busca das disciplinas no SIGAA.
        """
        client = await self._get_client()

        view_state = await self._inicializar_sessao(client, nivel)
        logger.info(f"ViewState obtido: {view_state}")

        form_data = {
            "form": "form",
            "form:nivel": nivel,
            "form:checkTipo": "on",
            "form:tipo": str(tipo),
            "form:btnBuscarComponentes": "Buscar Componentes",
            "javax.faces.ViewState": view_state,
        }

        if unidade_id and unidade_id != 0:
            form_data["form:checkUnidade"] = "on"
            form_data["form:unidades"] = str(unidade_id)
        else:
            form_data["form:unidades"] = "0"

        logger.info(
            f"Buscando componentes: nivel={nivel}, tipo={tipo}, unidade={unidade_id}"
        )
        response = await client.post(
            self.BUSCA_URL,
            data=form_data,
            headers={
                **self.HEADERS,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response.raise_for_status()

        html = response.content.decode("iso-8859-1", errors="replace")
        disciplinas = self._parse_resultados(html, nivel)

        logger.info(f"Encontradas {len(disciplinas)} disciplinas")
        return disciplinas

    def _parse_resultados(self, html: str, nivel: str) -> list[dict]:
        """
        Extrai as disciplinas do HTML de resultados da busca de componentes.
        """
        soup = BeautifulSoup(html, "html.parser")
        disciplinas = []

        tabela = soup.find("table", class_="listagem")
        if not tabela:
            tabela = soup.find("table", id=re.compile(r".*listagem.*", re.IGNORECASE))
            if not tabela:
                logger.warning("Tabela de resultados não encontrada no HTML")
                return disciplinas

        linhas = tabela.find_all("tr")
        for linha in linhas:
            celulas = linha.find_all("td")
            if len(celulas) < 2:
                continue

            try:
                disciplina = self._extrair_disciplina(celulas, nivel)
                if disciplina:
                    disciplinas.append(disciplina)
            except Exception as e:
                logger.warning(f"Erro ao processar linha: {e}")
                continue

        return disciplinas

    def _extrair_disciplina(self, celulas: list, nivel: str) -> Optional[dict]:
        col0 = unescape(celulas[0].get_text(strip=True))
        col1 = unescape(celulas[1].get_text(strip=True)) if len(celulas) > 1 else ""

        codigo = None
        nome = None
        tipo = None
        carga_horaria = None

        padrao_codigo = re.compile(r"^[A-Z]{2,6}\d{3,6}$")
        if padrao_codigo.match(col0) and col1:
            codigo = col0
            nome = re.sub(r"\s+", " ", col1).strip()
            if len(celulas) > 2:
                tipo = celulas[2].get_text(strip=True)
            if len(celulas) > 3:
                ch_text = celulas[3].get_text(strip=True)
                ch_match = re.search(r"(\d+)", ch_text)
                if ch_match:
                    carga_horaria = int(ch_match.group(1))

        if not codigo:
            padrao_combinado = re.compile(r"([A-Z]{2,6}\d{3,6})\s*[-–]\s*(.+)")
            match = padrao_combinado.search(col0)
            if match:
                codigo = match.group(1).strip()
                nome = re.sub(r"\s+", " ", match.group(2)).strip(" -–")
                if len(celulas) > 1:
                    tipo_texto = celulas[1].get_text(strip=True)
                    if tipo_texto in ("DISCIPLINA", "ATIVIDADE", "BLOCO", "MÓDULO"):
                        tipo = tipo_texto
                for celula in celulas:
                    ch_m = re.search(r"(\d+)\s*h", celula.get_text(strip=True))
                    if ch_m:
                        carga_horaria = int(ch_m.group(1))
                        break

        if not codigo or not nome:
            return None

        return {
            "codigo": codigo,
            "nome": nome,
            "tipo": tipo or "DISCIPLINA",
            "nivel": NIVEIS.get(nivel, nivel),
            "carga_horaria": carga_horaria,
        }

    async def buscar_turmas(
        self,
        nivel: str = "G",
        unidade_id: int = 673,
        ano: Optional[str] = None,
        periodo: Optional[str] = None,
    ) -> list[dict]:
        """
        Busca as turmas e professores de um departamento no SIGAA.
        Retorna lista de disciplinas com suas turmas e professores.
        """
        client = await self._get_client()

        # 1. Obter a página de turmas para ViewState e defaults
        await client.get(self.HOME_URL)
        resp = await client.get(self.TURMAS_URL)
        resp.raise_for_status()

        html = resp.content.decode("iso-8859-1", errors="replace")
        soup = BeautifulSoup(html, "html.parser")

        view_state_input = soup.find("input", {"name": "javax.faces.ViewState"})
        view_state = view_state_input.get("value", "j_id1") if view_state_input else "j_id1"

        # Defaults de ano e período se não fornecidos
        if not ano:
            ano_input = soup.find("input", id=lambda x: x and "inputAno" in str(x))
            ano = ano_input.get("value", "2026") if ano_input else "2026"

        if not periodo:
            periodo_select = soup.find("select", id=lambda x: x and "inputPeriodo" in str(x))
            if periodo_select:
                sel_opt = periodo_select.find("option", selected=True)
                periodo = sel_opt.get("value") if sel_opt else "2"
            else:
                periodo = "2"

        # Localizar botão Buscar do formulário
        form = soup.find("form", id="formTurma") or soup.find("form")
        submit_btn = form.find("input", {"type": "submit", "value": "Buscar"}) if form else None
        btn_name = submit_btn.get("name", "formTurma:j_id_jsp_1370969402_11") if submit_btn else "formTurma:j_id_jsp_1370969402_11"
        btn_value = submit_btn.get("value", "Buscar") if submit_btn else "Buscar"

        form_data = {
            "formTurma": "formTurma",
            "formTurma:inputNivel": nivel,
            "formTurma:inputDepto": str(unidade_id),
            "formTurma:inputAno": str(ano),
            "formTurma:inputPeriodo": str(periodo),
            btn_name: btn_value,
            "javax.faces.ViewState": view_state,
        }

        logger.info(
            f"Buscando turmas/professores: depto={unidade_id}, nivel={nivel}, ano={ano}, periodo={periodo}"
        )
        response = await client.post(
            f"{settings.SIGAA_BASE_URL}/public/turmas/listar.jsf",
            data=form_data,
            headers={
                **self.HEADERS,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        response.raise_for_status()

        html_res = response.content.decode("iso-8859-1", errors="replace")
        disciplinas_turmas = self._parse_turmas(html_res, nivel)

        logger.info(
            f"Encontradas {len(disciplinas_turmas)} disciplinas com turmas no depto {unidade_id}"
        )
        return disciplinas_turmas

    def _parse_turmas(self, html: str, nivel: str) -> list[dict]:
        """
        Extrai disciplinas, turmas e professores do HTML de turmas/listar.jsf.
        """
        soup = BeautifulSoup(html, "html.parser")
        tabela = soup.find("table", class_="listagem")
        if not tabela:
            return []

        resultado = []
        disc_atual = None
        padrao_titulo = re.compile(r"([A-Z0-9]+)\s*[-–]\s*(.+)")

        for tr in tabela.find_all("tr"):
            classes = tr.get("class", [])

            # Linha agrupador (Título da disciplina)
            if "agrupador" in classes:
                texto = tr.get_text(" ", strip=True)
                m = padrao_titulo.search(texto)
                if m:
                    cod = m.group(1).strip()
                    nome = m.group(2).strip()
                    disc_atual = {
                        "codigo": cod,
                        "nome": nome,
                        "nivel": NIVEIS.get(nivel, nivel),
                        "professores": set(),
                        "turmas": [],
                    }
                    resultado.append(disc_atual)
                else:
                    disc_atual = None

            # Linha de turma (linhaPar / linhaImpar)
            elif ("linhaPar" in classes or "linhaImpar" in classes) and disc_atual:
                tds = tr.find_all(["th", "td"])
                if len(tds) >= 3:
                    cod_turma = tds[0].get_text(strip=True)
                    ano_periodo = tds[1].get_text(strip=True)
                    td_docente = tds[2]

                    # Extrair os nomes dos professores da turma
                    docentes = []
                    for part in td_docente.stripped_strings:
                        doc = re.sub(r"\s*\(\d+h\)", "", part).strip()
                        doc = re.sub(r"\s+", " ", doc).strip()
                        if doc and doc not in ["--", "A DEFINIR"]:
                            docentes.append(doc)
                            disc_atual["professores"].add(doc)

                    horario = tds[3].get_text(" ", strip=True) if len(tds) > 3 else None
                    if horario:
                        horario = re.sub(r"\s+", " ", horario).strip()

                    vagas_ofertadas = None
                    vagas_ocupadas = None
                    if len(tds) > 5:
                        m_vof = re.search(r"\d+", tds[5].get_text(strip=True))
                        if m_vof:
                            vagas_ofertadas = int(m_vof.group(0))
                    if len(tds) > 6:
                        m_voc = re.search(r"\d+", tds[6].get_text(strip=True))
                        if m_voc:
                            vagas_ocupadas = int(m_voc.group(0))

                    local = tds[7].get_text(" ", strip=True) if len(tds) > 7 else None
                    if local:
                        local = re.sub(r"\s+", " ", local).strip()

                    disc_atual["turmas"].append({
                        "codigo": cod_turma,
                        "ano_periodo": ano_periodo,
                        "horario": horario,
                        "local": local,
                        "vagas_ofertadas": vagas_ofertadas,
                        "vagas_ocupadas": vagas_ocupadas,
                        "docentes": docentes,
                    })

        # Converter set de professores para lista ordenada
        for item in resultado:
            item["professores"] = sorted(list(item["professores"]))

        return resultado

    async def buscar_detalhes_disciplina(
        self,
        codigo: str,
        nivel: str = "G",
    ) -> Optional[dict]:
        """
        Busca detalhes completos de uma disciplina no SIGAA pelo código:
        - Ementa / Descrição
        - Pré-requisitos
        - Co-requisitos
        - Equivalências e lista de disciplinas equivalentes
        """
        client = await self._get_client()
        view_state = await self._inicializar_sessao(client, nivel)

        aba = self.ABA_POR_NIVEL.get(nivel, "p-ensino")
        url_com_aba = f"{self.BUSCA_URL}?nivel={nivel}&aba={aba}"
        resp_busca = await client.get(url_com_aba)
        soup_busca = BeautifulSoup(resp_busca.text, "html.parser")

        check_cod = soup_busca.find("input", id=lambda x: x and "checkCodigo" in str(x))
        if not check_cod:
            return None
        input_cod = check_cod.find_next("input", {"type": "text"})
        if not input_cod:
            return None

        post_data = {
            "form": "form",
            "form:nivel": nivel,
            "form:tipo": "0",
            "form:checkCodigo": "on",
            input_cod["name"]: codigo.strip().upper(),
            "form:unidades": "0",
            "form:btnBuscarComponentes": "Buscar Componentes",
            "javax.faces.ViewState": view_state,
        }

        resp_result = await client.post(
            self.BUSCA_URL,
            data=post_data,
            headers={
                **self.HEADERS,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        soup_res = BeautifulSoup(resp_result.text, "html.parser")
        t = soup_res.find("table", class_="listagem")
        if not t:
            return None

        rows = t.find_all("tr")
        if len(rows) < 2:
            return None

        target_row = rows[1]
        links = target_row.find_all("a")
        if not links:
            return None

        onclick = links[0].get("onclick", "")
        m = re.search(r"\{([^}]+)\}", onclick)
        if not m:
            return None

        vs2_elem = soup_res.find("input", {"name": "javax.faces.ViewState"})
        vs2 = vs2_elem["value"] if vs2_elem else view_state

        post_details = {
            "formListagemComponentes": "formListagemComponentes",
            "javax.faces.ViewState": vs2,
        }
        for item in m.group(1).split(","):
            sub = item.strip(" {}").split("':")
            if len(sub) == 2:
                post_details[sub[0].strip("' \"")] = sub[1].strip("' \"")

        resp_det = await client.post(
            self.BUSCA_URL,
            data=post_details,
            headers={
                **self.HEADERS,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        soup_det = BeautifulSoup(resp_det.text, "html.parser")
        tbl_vis = soup_det.find("table", class_="visualizacao")
        if not tbl_vis:
            return None

        info = {
            "codigo": codigo.strip().upper(),
            "pre_requisitos": None,
            "co_requisitos": None,
            "equivalencias": None,
            "disciplinas_equivalentes": [],
            "ementa": None,
        }

        for tr in tbl_vis.find_all("tr"):
            th = tr.find("th")
            td = tr.find("td")
            if not th or not td:
                continue
            campo = th.get_text(strip=True).lower().replace(":", "")
            valor = td.get_text(" ", strip=True)

            if "pré-requisito" in campo:
                info["pre_requisitos"] = None if valor == "-" else valor
            elif "co-requisito" in campo:
                info["co_requisitos"] = None if valor == "-" else valor
            elif campo in ("equivalência", "equivalências"):
                if valor != "-":
                    info["equivalencias"] = valor

                    eq_map = {}
                    for acr in td.find_all("acronym"):
                        cod_eq = acr.get_text(strip=True)
                        nome_eq = acr.get("title", "")
                        if " - " in nome_eq:
                            nome_eq = nome_eq.split(" - ", 1)[1].strip()
                        if cod_eq and cod_eq != codigo.strip().upper():
                            eq_map[cod_eq] = nome_eq

                    if not eq_map:
                        codes = re.findall(r"\b[A-Z]{2,6}\d{3,6}\b", valor)
                        for c in codes:
                            if c != codigo.strip().upper():
                                eq_map[c] = ""

                    info["disciplinas_equivalentes"] = [
                        {"codigo": c, "nome": n} for c, n in eq_map.items()
                    ]
            elif "ementa" in campo or "descrição" in campo:
                info["ementa"] = valor

        return info


def sincronizar_departamentos(db: Session) -> int:
    """
    Sincroniza a lista de departamentos do SIGAA no banco de dados.
    """
    count = 0
    for sigaa_id, nome in DEPARTAMENTOS.items():
        existing = db.query(Departamento).filter_by(sigaa_id=sigaa_id).first()
        if existing:
            if existing.nome != nome:
                existing.nome = nome
                count += 1
        else:
            db.add(Departamento(sigaa_id=sigaa_id, nome=nome))
            count += 1

    db.commit()
    logger.info(f"Departamentos sincronizados: {count} novos/atualizados")
    return count


def _salvar_disciplina(
    db: Session, disc_data: dict, departamento: Optional[Departamento]
) -> tuple[int, int]:
    """
    Salva ou atualiza uma disciplina no banco de dados.
    """
    existing = (
        db.query(Disciplina)
        .filter_by(codigo=disc_data["codigo"], nivel=disc_data["nivel"])
        .first()
    )

    if existing:
        changed = False
        if existing.nome != disc_data["nome"]:
            existing.nome = disc_data["nome"]
            changed = True
        if disc_data.get("tipo") and existing.tipo != disc_data["tipo"]:
            existing.tipo = disc_data["tipo"]
            changed = True
        if disc_data.get("carga_horaria") and existing.carga_horaria != disc_data["carga_horaria"]:
            existing.carga_horaria = disc_data["carga_horaria"]
            changed = True
        if departamento and existing.departamento_id != departamento.id:
            existing.departamento_id = departamento.id
            changed = True
        return (0, 1 if changed else 0)
    else:
        nova = Disciplina(
            codigo=disc_data["codigo"],
            nome=disc_data["nome"],
            tipo=disc_data.get("tipo"),
            nivel=disc_data.get("nivel"),
            carga_horaria=disc_data.get("carga_horaria"),
            departamento_id=departamento.id if departamento else None,
        )
        db.add(nova)
        return (1, 0)


def _salvar_professores_e_turmas(
    db: Session,
    disc_turmas: list[dict],
    departamento: Optional[Departamento],
    nivel: str,
) -> tuple[int, int]:
    """
    Salva ou atualiza professores, turmas e seus relacionamentos com disciplinas.
    Retorna (total_professores_novos, total_turmas_novas).
    """
    professores_novos = 0
    turmas_novas = 0
    nivel_str = NIVEIS.get(nivel, nivel)

    for item in disc_turmas:
        # 1. Localizar ou criar a disciplina
        disciplina = (
            db.query(Disciplina)
            .filter_by(codigo=item["codigo"], nivel=nivel_str)
            .first()
        )
        if not disciplina:
            disciplina = db.query(Disciplina).filter_by(codigo=item["codigo"]).first()

        if not disciplina:
            disciplina = Disciplina(
                codigo=item["codigo"],
                nome=item["nome"],
                tipo="DISCIPLINA",
                nivel=nivel_str,
                departamento_id=departamento.id if departamento else None,
            )
            db.add(disciplina)
            db.flush()
        else:
            if departamento and not disciplina.departamento_id:
                disciplina.departamento_id = departamento.id

        # 2. Salvar professores e associar à disciplina
        professores_map = {}
        for prof_nome in item["professores"]:
            prof = db.query(Professor).filter_by(nome=prof_nome).first()
            if not prof:
                prof = Professor(
                    nome=prof_nome,
                    departamento_id=departamento.id if departamento else None,
                )
                db.add(prof)
                db.flush()
                professores_novos += 1
            elif departamento and not prof.departamento_id:
                prof.departamento_id = departamento.id

            professores_map[prof_nome] = prof

            if prof not in disciplina.professores:
                disciplina.professores.append(prof)

        # 3. Salvar turmas e associar professores
        for t_data in item["turmas"]:
            turma = (
                db.query(Turma)
                .filter_by(
                    disciplina_id=disciplina.id,
                    codigo=t_data["codigo"],
                    ano_periodo=t_data["ano_periodo"],
                )
                .first()
            )
            if not turma:
                turma = Turma(
                    disciplina_id=disciplina.id,
                    codigo=t_data["codigo"],
                    ano_periodo=t_data["ano_periodo"],
                    horario=t_data["horario"],
                    local=t_data["local"],
                    vagas_ofertadas=t_data["vagas_ofertadas"],
                    vagas_ocupadas=t_data["vagas_ocupadas"],
                )
                db.add(turma)
                db.flush()
                turmas_novas += 1
            else:
                turma.horario = t_data["horario"]
                turma.local = t_data["local"]
                turma.vagas_ofertadas = t_data["vagas_ofertadas"]
                turma.vagas_ocupadas = t_data["vagas_ocupadas"]

            # Associar professores da turma específica
            for doc_nome in t_data["docentes"]:
                doc_obj = professores_map.get(doc_nome)
                if not doc_obj:
                    doc_obj = db.query(Professor).filter_by(nome=doc_nome).first()
                if doc_obj and doc_obj not in turma.professores:
                    turma.professores.append(doc_obj)

    return professores_novos, turmas_novas


async def executar_scraping(
    db: Session,
    log_id: Optional[int] = None,
    nivel: str = "G",
    tipo: int = 2,
    departamento_sigaa_id: Optional[int] = None,
    buscar_professores: bool = True,
    ano: Optional[str] = None,
    periodo: Optional[str] = None,
) -> ScrapingLog:
    """
    Executa o scraping e salva disciplinas, turmas e professores no banco de dados.
    """
    if log_id:
        log = db.query(ScrapingLog).filter_by(id=log_id).first()
        if not log:
            log = ScrapingLog(
                departamento_sigaa_id=departamento_sigaa_id,
                nivel=NIVEIS.get(nivel, nivel),
                status="RUNNING",
            )
            db.add(log)
    else:
        log = ScrapingLog(
            departamento_sigaa_id=departamento_sigaa_id,
            nivel=NIVEIS.get(nivel, nivel),
            status="RUNNING",
        )
        db.add(log)
    db.commit()

    scraper = SigaaScraper()
    total_encontradas = 0
    total_novas = 0
    total_atualizadas = 0
    total_professores = 0
    total_turmas = 0

    try:
        sincronizar_departamentos(db)

        if departamento_sigaa_id:
            deptos = [departamento_sigaa_id]
        else:
            deptos = list(DEPARTAMENTOS.keys())

        for depto_id in deptos:
            try:
                logger.info(
                    f"Scraping departamento {depto_id}: {DEPARTAMENTOS.get(depto_id, 'Desconhecido')}"
                )
                depto_db = db.query(Departamento).filter_by(sigaa_id=depto_id).first()

                # 1. Buscar catálogo de componentes
                disciplinas = await scraper.buscar_componentes(
                    nivel=nivel,
                    tipo=tipo,
                    unidade_id=depto_id,
                )

                for disc_data in disciplinas:
                    total_encontradas += 1
                    novas, atualizadas = _salvar_disciplina(db, disc_data, depto_db)
                    total_novas += novas
                    total_atualizadas += atualizadas

                db.commit()

                # 2. Se habilitado, buscar turmas e professores
                if buscar_professores:
                    await asyncio.sleep(settings.SCRAPER_DELAY)
                    disc_turmas = await scraper.buscar_turmas(
                        nivel=nivel,
                        unidade_id=depto_id,
                        ano=ano,
                        periodo=periodo,
                    )
                    novos_profs, novas_turmas = _salvar_professores_e_turmas(
                        db=db,
                        disc_turmas=disc_turmas,
                        departamento=depto_db,
                        nivel=nivel,
                    )
                    total_professores += novos_profs
                    total_turmas += novas_turmas
                    db.commit()

                await asyncio.sleep(settings.SCRAPER_DELAY)

            except Exception as e:
                logger.error(f"Erro no departamento {depto_id}: {e}")
                continue

        log.status = "SUCCESS"
        log.disciplinas_encontradas = total_encontradas
        log.disciplinas_novas = total_novas
        log.disciplinas_atualizadas = total_atualizadas
        log.professores_encontrados = total_professores
        log.turmas_encontradas = total_turmas
        log.mensagem = (
            f"Scraping concluído: {total_encontradas} disciplinas catalogadas "
            f"({total_novas} novas, {total_atualizadas} atualizadas), "
            f"{total_professores} novos professores, {total_turmas} novas turmas."
        )
        log.finished_at = datetime.utcnow()

    except Exception as e:
        logger.error(f"Erro durante o scraping: {e}")
        log.status = "ERROR"
        log.mensagem = str(e)[:500]
        log.finished_at = datetime.utcnow()

    finally:
        await scraper.close()
        db.commit()

    return log
