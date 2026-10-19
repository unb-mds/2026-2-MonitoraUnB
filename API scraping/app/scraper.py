"""
API Faz scraping da página pública:
  https://sig.unb.br/sigaa/public/componentes/busca_componentes.jsf
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
from app.models import Departamento, Disciplina, ScrapingLog

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
        # 1. estabelecer sessão
        await client.get(self.HOME_URL)

        # 2. Acessar a página de busca com a aba correta
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

        # 1. Obter o ViewState 
        view_state = await self._inicializar_sessao(client, nivel)
        logger.info(f"ViewState obtido: {view_state}")

        # 2. dados do POST
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

        # 3. Enviar o POST
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

        # 4. Parse do HTML da resposta
        disciplinas = self._parse_resultados(html, nivel)

        logger.info(f"Encontradas {len(disciplinas)} disciplinas")
        return disciplinas

    def _parse_resultados(self, html: str, nivel: str) -> list[dict]:
        """
        Extrai as disciplinas do HTML de resultados.
        """
        soup = BeautifulSoup(html, "html.parser")
        disciplinas = []

        # Procurar a tabela de resultados com classe 'listagem'
        tabela = soup.find("table", class_="listagem")
        if not tabela:
            # Tentar busca por atributo id ou padrão alternativo
            tabela = soup.find("table", id=re.compile(r".*listagem.*", re.IGNORECASE))
            if not tabela:
                logger.warning("Tabela de resultados não encontrada no HTML")
                return disciplinas

        # Iterar pelas linhas da tabela
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


def sincronizar_departamentos(db: Session) -> int:
    """
    Sincroniza a lista de departamentos do SIGAA no banco de dados.
    Retorna o número de departamentos inseridos/atualizados.
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


async def executar_scraping(
    db: Session,
    nivel: str = "G",
    tipo: int = 2,
    departamento_sigaa_id: Optional[int] = None,
) -> ScrapingLog:
    """
    Executa o scraping completo e salva os resultados no banco de dados.
    """
    # Criar log de scraping
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

    try:
        # Sincronizar departamentos
        sincronizar_departamentos(db)

        if departamento_sigaa_id:
            # Scraping de um único departamento
            deptos = [departamento_sigaa_id]
        else:
            # Scraping de todos os departamentos
            deptos = list(DEPARTAMENTOS.keys())

        for depto_id in deptos:
            try:
                logger.info(
                    f"Scraping departamento {depto_id}: {DEPARTAMENTOS.get(depto_id, 'Desconhecido')}"
                )

                disciplinas = await scraper.buscar_componentes(
                    nivel=nivel,
                    tipo=tipo,
                    unidade_id=depto_id,
                )

                # Buscar o departamento no banco
                depto_db = db.query(Departamento).filter_by(sigaa_id=depto_id).first()

                for disc_data in disciplinas:
                    total_encontradas += 1
                    novas, atualizadas = _salvar_disciplina(db, disc_data, depto_db)
                    total_novas += novas
                    total_atualizadas += atualizadas

                db.commit()

                # Delay entre requisições para não sobrecarregar o servidor
                await asyncio.sleep(settings.SCRAPER_DELAY)

            except Exception as e:
                logger.error(f"Erro no departamento {depto_id}: {e}")
                continue

        # Atualizar log de sucesso
        log.status = "SUCCESS"
        log.disciplinas_encontradas = total_encontradas
        log.disciplinas_novas = total_novas
        log.disciplinas_atualizadas = total_atualizadas
        log.mensagem = f"Scraping concluído: {total_encontradas} encontradas, {total_novas} novas, {total_atualizadas} atualizadas"
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
        # Atualizar se houver mudanças
        changed = False
        if existing.nome != disc_data["nome"]:
            existing.nome = disc_data["nome"]
            changed = True
        if disc_data["tipo"] and existing.tipo != disc_data["tipo"]:
            existing.tipo = disc_data["tipo"]
            changed = True
        if disc_data["carga_horaria"] and existing.carga_horaria != disc_data["carga_horaria"]:
            existing.carga_horaria = disc_data["carga_horaria"]
            changed = True
        if departamento and existing.departamento_id != departamento.id:
            existing.departamento_id = departamento.id
            changed = True
        return (0, 1 if changed else 0)
    else:
        # Inserir nova disciplina
        nova = Disciplina(
            codigo=disc_data["codigo"],
            nome=disc_data["nome"],
            tipo=disc_data["tipo"],
            nivel=disc_data["nivel"],
            carga_horaria=disc_data["carga_horaria"],
            departamento_id=departamento.id if departamento else None,
        )
        db.add(nova)
        return (1, 0)
