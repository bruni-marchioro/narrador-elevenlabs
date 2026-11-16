
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import imageio_ffmpeg
import requests


# ==========================================
# CONFIGURACOES GERAIS
# ==========================================

API = "https://api.elevenlabs.io/v1"
CHAVE = os.getenv("ELEVENLABS_API_KEY")

MODELO = "eleven_multilingual_v2"
FORMATO = "mp3_44100_128"
LIMITE = 3000

PASTA = Path(__file__).resolve().parent
ARQUIVO_CONFIG = PASTA / "config_narrador.json"

FRASE_PREVIA = (
    "Você sabia que pequenos detalhes podem "
    "fazer uma grande diferença na tecnologia? "
    "Hoje eu vou te contar uma curiosidade "
    "que talvez você ainda não conheça!"
)

ESTILOS = {
    "1": {
        "nome": "Curiosidades",
        "stability": 0.40,
        "similarity_boost": 0.85,
        "style": 0.25,
        "speed": 1.05,
    },
    "2": {
        "nome": "Noticias",
        "stability": 0.60,
        "similarity_boost": 0.85,
        "style": 0.10,
        "speed": 1.00,
    },
    "3": {
        "nome": "Dicas rapidas",
        "stability": 0.45,
        "similarity_boost": 0.85,
        "style": 0.20,
        "speed": 1.08,
    },
}

if not CHAVE:
    sys.exit(
        "Chave nao configurada.\n"
        "No PowerShell, execute:\n"
        '$env:ELEVENLABS_API_KEY = '
        'Read-Host "Cole sua chave"'
    )

HEADERS = {"xi-api-key": CHAVE}


# ==========================================
# COMUNICACAO COM A API
# ==========================================

def requisicao(metodo, endereco, **kwargs):
    resposta = requests.request(
        metodo,
        endereco,
        headers=HEADERS,
        timeout=120,
        **kwargs,
    )

    if not resposta.ok:
        try:
            detalhe = resposta.json().get("detail", {})
            if isinstance(detalhe, dict):
                mensagem = detalhe.get(
                    "message", resposta.text
                )
            else:
                mensagem = str(detalhe)
        except ValueError:
            mensagem = resposta.text[:500]

        raise RuntimeError(
            f"Erro {resposta.status_code}: {mensagem}"
        )

    return resposta


def listar_vozes():
    vozes = []
    proxima_pagina = None

    while True:
        parametros = {"page_size": 100}

        if proxima_pagina:
            parametros["next_page_token"] = (
                proxima_pagina
            )

        dados = requisicao(
            "GET",
            f"{API}/voices",
            params=parametros,
        ).json()

        vozes.extend(dados.get("voices", []))

        proxima_pagina = dados.get(
            "next_page_token"
        )

        if not dados.get("has_more"):
            break

        if not proxima_pagina:
            break

    return vozes


# ==========================================
# CONFIGURACOES SALVAS
# ==========================================

def carregar_config():
    if ARQUIVO_CONFIG.exists():
        try:
            return json.loads(
                ARQUIVO_CONFIG.read_text(
                    encoding="utf-8"
                )
            )
        except (ValueError, OSError):
            pass

    return {}


def salvar_config(voz, parametros):
    dados = {
        "voice_id": voz["voice_id"],
        "voice_name": voz["name"],
        "parametros": parametros,
    }

    ARQUIVO_CONFIG.write_text(
        json.dumps(
            dados,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ==========================================
# GERACAO DE AUDIO
# ==========================================

def gerar_audio(texto, voz_id, parametros, destino):
    configuracoes = {
        "stability": parametros["stability"],
        "similarity_boost": parametros[
            "similarity_boost"
        ],
        "style": parametros["style"],
        "speed": parametros["speed"],
        "use_speaker_boost": True,
    }

    resposta = requisicao(
        "POST",
        f"{API}/text-to-speech/{voz_id}",
        params={
            "output_format": FORMATO
        },
        json={
            "text": texto,
            "model_id": MODELO,
            "voice_settings": configuracoes,
        },
    )

    Path(destino).write_bytes(
        resposta.content
    )


def reproduzir_audio(arquivo):
    caminho = Path(arquivo).resolve()

    if sys.platform == "win32":
        os.startfile(str(caminho))
    else:
        print(f"Arquivo: {caminho}")


# ==========================================
# ESCOLHA DA VOZ
# ==========================================

def escolher_voz(vozes, config):
    voz_salva = None

    for voz in vozes:
        if voz["voice_id"] == config.get(
            "voice_id"
        ):
            voz_salva = voz
            break

    if voz_salva:
        print(
            f"\nUltima voz utilizada: "
            f"{voz_salva['name']}"
        )

        usar = input(
            "Deseja reutilizar essa voz? (S/N): "
        ).strip().lower()

        if usar == "s":
            return voz_salva

    bloqueadas = set()

    while True:
        print("\nVOZES DISPONIVEIS\n")

        for numero, voz in enumerate(vozes, 1):
            bloqueada = (
                " - exige plano pago"
                if voz["voice_id"] in bloqueadas
                else ""
            )

            print(
                f"{numero}. {voz['name']}"
                f"{bloqueada}"
            )

        escolha = input(
            "\nDigite o numero da voz "
            "(ou S para sair): "
        ).strip().lower()

        if escolha == "s":
            sys.exit("Programa encerrado.")

        if not escolha.isdigit():
            print("Digite um numero valido.")
            continue

        indice = int(escolha) - 1

        if indice < 0 or indice >= len(vozes):
            print("Voz nao encontrada.")
            continue

        voz = vozes[indice]

        if voz["voice_id"] in bloqueadas:
            print(
                "Essa voz ja apresentou "
                "restricao de plano."
            )
            continue

        print(
            f"\nGerando demonstracao: "
            f"{voz['name']}..."
        )

        parametros = {
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.20,
            "speed": 1.00,
        }

        try:
            previa = PASTA / "previa_voz.mp3"

            gerar_audio(
                FRASE_PREVIA,
                voz["voice_id"],
                parametros,
                previa,
            )

        except RuntimeError as erro:
            mensagem = str(erro)

            if (
                "402" in mensagem
                or "paid_plan_required" in mensagem
            ):
                bloqueadas.add(voz["voice_id"])

                print(
                    "\nEssa voz exige um plano "
                    "pago para uso pela API."
                )
                continue

            print(f"\n{erro}")
            continue

        reproduzir_audio(previa)

        resposta = input(
            "\nGostou dessa voz? (S/N): "
        ).strip().lower()

        if resposta == "s":
            return voz


# ==========================================
# ESCOLHA DO ESTILO
# ==========================================

def escolher_estilo(config):
    print("\nESTILOS DE NARRACAO\n")

    for numero, estilo in ESTILOS.items():
        print(
            f"{numero}. {estilo['nome']}"
        )

    print("4. Personalizado")

    escolha = input(
        "\nEscolha o estilo [1]: "
    ).strip() or "1"

    if escolha in ESTILOS:
        parametros = ESTILOS[escolha].copy()
        print(
            f"\nEstilo selecionado: "
            f"{parametros['nome']}"
        )
        return parametros

    if escolha == "4":
        anterior = config.get("parametros", {})

        parametros = {
            "nome": "Personalizado",
            "stability": anterior.get(
                "stability", 0.45
            ),
            "similarity_boost": anterior.get(
                "similarity_boost", 0.85
            ),
            "style": anterior.get(
                "style", 0.20
            ),
            "speed": anterior.get(
                "speed", 1.00
            ),
        }

        return ajustar_parametros(parametros)

    print("Opcao invalida. Usando Curiosidades.")
    return ESTILOS["1"].copy()


# ==========================================
# AJUSTE MANUAL
# ==========================================

def perguntar_numero(nome, atual, minimo, maximo):
    while True:
        entrada = input(
            f"{nome} [{atual}]: "
        ).strip()

        if not entrada:
            return atual

        try:
            valor = float(
                entrada.replace(",", ".")
            )
        except ValueError:
            print("Digite um numero valido.")
            continue

        if minimo <= valor <= maximo:
            return valor

        print(
            f"Valor permitido: "
            f"{minimo} a {maximo}"
        )


def ajustar_parametros(parametros):
    print("\nPERSONALIZAR NARRACAO")
    print("Pressione Enter para manter o valor.")

    parametros["stability"] = perguntar_numero(
        "Estabilidade (0 a 1)",
        parametros["stability"],
        0,
        1,
    )

    parametros["similarity_boost"] = (
        perguntar_numero(
            "Semelhanca (0 a 1)",
            parametros["similarity_boost"],
            0,
            1,
        )
    )

    parametros["style"] = perguntar_numero(
        "Expressividade (0 a 1)",
        parametros["style"],
        0,
        1,
    )

    parametros["speed"] = perguntar_numero(
        "Velocidade (0.7 a 1.2)",
        parametros["speed"],
        0.7,
        1.2,
    )

    return parametros


# ==========================================
# PREVIA COM O ESTILO ESCOLHIDO
# ==========================================

def testar_estilo(voz, parametros):
    while True:
        print(
            "\nGerando previa com "
            "as configuracoes escolhidas..."
        )

        previa = PASTA / "previa_estilo.mp3"

        gerar_audio(
            FRASE_PREVIA,
            voz["voice_id"],
            parametros,
            previa,
        )

        reproduzir_audio(previa)

        print("\nO que deseja fazer?")
        print("1. Confirmar configuracoes")
        print("2. Ajustar configuracoes")
        print("3. Escolher outro estilo")

        escolha = input(
            "\nOpcao: "
        ).strip()

        if escolha == "1":
            return parametros

        if escolha == "2":
            parametros = ajustar_parametros(
                parametros
            )

        elif escolha == "3":
            parametros = escolher_estilo({})

        else:
            print("Opcao invalida.")


# ==========================================
# DIVIDIR ROTEIRO
# ==========================================

def dividir_texto(texto):
    texto = re.sub(
        r"\s+",
        " ",
        texto,
    ).strip()

    if not texto:
        raise ValueError("O roteiro esta vazio.")

    partes = []
    atual = ""

    for palavra in texto.split():
        candidato = (
            f"{atual} {palavra}".strip()
        )

        if len(candidato) > LIMITE:
            if atual:
                partes.append(atual)

            atual = palavra
        else:
            atual = candidato

    if atual:
        partes.append(atual)

    return partes


# ==========================================
# UNIR AUDIOS COM FFMPEG
# ==========================================

def unir_audios(arquivos, destino):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    with tempfile.TemporaryDirectory() as pasta:
        lista = Path(pasta) / "lista.txt"

        linhas = []

        for arquivo in arquivos:
            caminho = Path(arquivo).resolve()

            caminho_seguro = (
                caminho.as_posix()
                .replace("'", "'\\''")
            )

            linhas.append(
                f"file '{caminho_seguro}'"
            )

        lista.write_text(
            "\n".join(linhas),
            encoding="utf-8",
        )

        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(lista),
                "-c:a", "libmp3lame",
                "-b:a", "128k",
                str(Path(destino).resolve()),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )


# ==========================================
# GERAR NARRACAO COMPLETA
# ==========================================

def gerar_narracao(voz, parametros):
    nome = input(
        "\nNome do arquivo do roteiro "
        "[roteiro.txt]: "
    ).strip() or "roteiro.txt"

    roteiro = Path(nome)

    if not roteiro.is_absolute():
        roteiro = PASTA / roteiro

    if not roteiro.exists():
        print("\nArquivo nao encontrado.")
        return

    texto = roteiro.read_text(
        encoding="utf-8-sig"
    )

    partes = dividir_texto(texto)

    print(
        f"\nRoteiro dividido em "
        f"{len(partes)} partes."
    )

    print(
        f"Total de caracteres: {len(texto)}"
    )

    confirmar = input(
        "\nGerar a narracao completa? (S/N): "
    ).strip().lower()

    if confirmar != "s":
        return

    destino = (
        PASTA
        / f"{roteiro.stem}_narrado.mp3"
    )

    with tempfile.TemporaryDirectory() as pasta:
        arquivos = []

        for numero, parte in enumerate(
            partes, 1
        ):
            print(
                f"Gerando parte {numero} "
                f"de {len(partes)}..."
            )

            arquivo = (
                Path(pasta)
                / f"parte_{numero:03d}.mp3"
            )

            gerar_audio(
                parte,
                voz["voice_id"],
                parametros,
                arquivo,
            )

            arquivos.append(arquivo)

        print("\nUnindo os audios...")

        unir_audios(arquivos, destino)

    print("\nNARRACAO CONCLUIDA!")
    print(f"Arquivo: {destino}")

    ouvir = input(
        "\nDeseja ouvir o resultado? (S/N): "
    ).strip().lower()

    if ouvir == "s":
        reproduzir_audio(destino)


# ==========================================
# PROGRAMA PRINCIPAL
# ==========================================

def main():
    print("\nOLHAR DE QUALIDADE")
    print("Gerador de narracoes com ElevenLabs")

    config = carregar_config()
    vozes = listar_vozes()

    if not vozes:
        sys.exit("Nenhuma voz encontrada.")

    voz = escolher_voz(vozes, config)

    parametros = escolher_estilo(config)

    parametros = testar_estilo(
        voz,
        parametros,
    )

    salvar_config(voz, parametros)

    print(
        f"\nVoz selecionada: {voz['name']}"
    )
    print(
        f"Estilo: {parametros['nome']}"
    )

    gerar_narracao(voz, parametros)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nPrograma interrompido.")

    except (
        requests.RequestException,
        RuntimeError,
        ValueError,
        OSError,
        subprocess.CalledProcessError,
    ) as erro:
        print(f"\nOcorreu um erro: {erro}")
        sys.exit(1)
