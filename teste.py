import re
import sqlite3
from pathlib import Path
from urllib.parse import urljoin, urlencode

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://community.sap.com"
SEARCH_BASE = "https://community.sap.com/t5/forums/searchpage/tab/message"

# Parâmetros da busca: 50 tópicos por página, conforme solicitado
SEARCH_PARAMS = {
    "filter": "location",
    "q": "mdg",
    "noSynonym": "false",
    "advanced": "true",
    "location": "qanda-board:technology-questions",
    "collapse_discussion": "true",
    "search_type": "thread",
    "search_page_size": "50",
}

# pasta para salvar imagens
IMG_DIR = Path("fotos")
IMG_DIR.mkdir(exist_ok=True)

# headers p/ evitar bloqueio
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

# Session reaproveita conexões
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# Criação do banco SQLite (SEM ALTERAÇÕES DE CAMPOS)
conn = sqlite3.connect("sap_mdg_posts.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id_sap TEXT UNIQUE,
    url TEXT,
    descricao TEXT,
    texto TEXT,
    fotos TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    comentario TEXT,
    fotos TEXT,
    FOREIGN KEY (post_id) REFERENCES posts(id)
)
""")

conn.commit()


def extrair_post_id(url: str) -> str | None:
    """
    Extrai o ID único da URL do SAP Community.
    Cobre tanto /qaq-p/<id> quanto /m-p/<id>.
    """
    m = re.search(r"/(?:qaq-p|m-p)/(\d+)", url)
    return m.group(1) if m else None


def baixar_imagem(url: str, prefixo: str, idx: int) -> str | None:
    """
    Baixa a imagem e retorna o caminho salvo (ou None).
    Conserta src relativo e ignora data URLs.
    """
    try:
        if not url or url.startswith("data:"):
            return None
        # Normaliza URL relativa
        full_url = url if url.startswith("http") else urljoin(BASE_URL, url)
        resp = SESSION.get(full_url, timeout=20)
        if resp.status_code == 200 and resp.content:
            # tenta inferir extensão pela URL; fallback p/ jpg
            ext = full_url.split(".")[-1].split("?")[0].lower()
            if not ext or len(ext) > 5:
                ext = "jpg"
            filename = IMG_DIR / f"{prefixo}_img{idx}.{ext}"
            with open(filename, "wb") as f:
                f.write(resp.content)
            return str(filename)
    except Exception as e:
        print("Erro baixando imagem:", e)
    return None


def get_body_divs(soup: BeautifulSoup) -> list[BeautifulSoup]:
    """
    Retorna todos os DIVs de corpo de mensagem.
    O primeiro é o post principal; os demais costumam ser respostas/comentários.
    """
    # seletor mais genérico e resiliente
    body_divs = soup.select("div.lia-message-body-content")
    # fallback (algumas páginas usam classe extra)
    if not body_divs:
        body_divs = soup.find_all("div", class_=re.compile(r"lia-message-body-content"))
    return body_divs


def extrair_texto_e_fotos(div_body: BeautifulSoup, prefixo_img: str) -> tuple[str, list[str]]:
    """
    Extrai texto e baixa imagens que estejam dentro do bloco div do corpo.
    """
    texto = div_body.get_text(strip=True) if div_body else ""
    fotos = []
    if div_body:
        imgs = div_body.find_all("img")
        for i, img in enumerate(imgs):
            src = img.get("src")
            caminho = baixar_imagem(src, prefixo_img, i)
            if caminho:
                fotos.append(caminho)
    return texto, fotos


def processar_post(link: str, descricao: str, post_id_sap: str):
    """Processa uma postagem e salva no banco."""
    try:
        resp = SESSION.get(link, timeout=30)
    except Exception as e:
        print("❌ Erro ao acessar post:", link, e)
        return
    if resp.status_code != 200:
        print("❌ Erro ao acessar post:", link, resp.status_code)
        return

    soup = BeautifulSoup(resp.text, "html.parser")
    body_divs = get_body_divs(soup)

    # Post principal
    texto_post, fotos_post = ("", [])
    if body_divs:
        texto_post, fotos_post = extrair_texto_e_fotos(body_divs[0], f"post{post_id_sap}")

    # Inserir post
    cursor.execute("""
        INSERT OR IGNORE INTO posts (post_id_sap, url, descricao, texto, fotos)
        VALUES (?, ?, ?, ?, ?)
    """, (post_id_sap, link, descricao, texto_post, ";".join(fotos_post)))
    conn.commit()

    # Garantir que temos o ID do post (pode ter sido inserido agora)
    cursor.execute("SELECT id FROM posts WHERE post_id_sap=?", (post_id_sap,))
    row = cursor.fetchone()
    if not row:
        print("⚠ Não consegui obter id do post após inserir:", link)
        return
    post_id = row[0]

    # Comentários (demais blocos)
    if len(body_divs) > 1:
        for idx_c, div_c in enumerate(body_divs[1:]):
            comentario_txt, fotos_coment = extrair_texto_e_fotos(div_c, f"post{post_id_sap}_c{idx_c}")
            cursor.execute("""
                INSERT INTO comments (post_id, comentario, fotos)
                VALUES (?, ?, ?)
            """, (post_id, comentario_txt, ";".join(fotos_coment)))
        conn.commit()


def buscar_posts(pagina: int = 1) -> list[tuple[str, str, str]]:
    """
    Busca posts na página especificada e já filtra:
    - Âncoras que contenham /qaq-p/ ou /m-p/
    - Remove duplicados por post_id_sap
    - Pula os que já existem no banco (antes de acessar o link)
    Retorna lista de (url, descricao, post_id_sap)
    """
    params = SEARCH_PARAMS.copy()
    params["page"] = pagina
    url = f"{SEARCH_BASE}?{urlencode(params)}"
    print(f"🔎 Buscando página {pagina}: {url}")

    try:
        resp = SESSION.get(url, timeout=30)
    except Exception as e:
        print("❌ Erro ao acessar resultados de busca:", e)
        return []

    if resp.status_code != 200:
        print("❌ Erro ao acessar resultados de busca:", resp.status_code)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    # Seletor robusto por href, independente de classes
    anchors = soup.select('a[href*="/qaq-p/"], a[href*="/m-p/"]')

    posts = []
    vistos = set()

    for a in anchors:
        href = a.get("href")
        if not href:
            continue
        link = urljoin(BASE_URL, href)
        post_id_sap = extrair_post_id(link)
        if not post_id_sap:
            continue
        if post_id_sap in vistos:
            continue
        vistos.add(post_id_sap)

        # pula se já existe no banco (sem abrir o link)
        cursor.execute("SELECT 1 FROM posts WHERE post_id_sap=?", (post_id_sap,))
        if cursor.fetchone():
            print("⏭ Já existe no banco, pulando:", link)
            continue

        descricao = a.get_text(strip=True) or ""
        posts.append((link, descricao, post_id_sap))

    return posts


def main():
    # Varre sempre da página 1 até a 100 (inclusive), mesmo que alguma venha vazia
    for pagina in range(1, 101):
        posts = buscar_posts(pagina)
        if not posts:
            print(f"ℹ Página {pagina} sem itens (seguindo).")
            continue

        for link, descricao, post_id_sap in posts:
            print("Processando:", link)
            processar_post(link, descricao, post_id_sap)


if __name__ == "__main__":
    main()
