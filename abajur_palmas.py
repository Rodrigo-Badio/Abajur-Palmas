"""
Detector de palmas para controlar o abajur.

- 1 palma  -> liga
- 2 palmas -> desliga

Como funciona:
1. Ouve o microfone continuamente em pequenos blocos de áudio.
2. Quando o volume de um bloco ultrapassa um limiar (THRESHOLD), conta como "uma palma".
3. Espera uma janela curta (CLAP_WINDOW) pra ver se vem uma segunda palma.
4. Se só veio 1 -> liga. Se vieram 2 -> desliga.

Requisitos: veja requirements.txt
Configuração: copie .env.example para .env e preencha com seus dados.
"""

import asyncio
import os
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
from dotenv import load_dotenv
from tapo import ApiClient

# Path(__file__).parent é a pasta onde ESTE arquivo .py está salvo.
# Assim o .env é encontrado não importa de onde você rode o script.
load_dotenv(Path(__file__).parent / ".env")

# ---------- Configurações que você pode ajustar ----------
THRESHOLD = 0.4          # volume mínimo pra considerar "palma" (0.0 a 1.0). Se não detectar, baixe. Se detectar demais (ruído), suba.
CLAP_WINDOW = 0.6        # segundos: tempo máximo entre a 1ª e a 2ª palma pra contar como "duas palmas"
COOLDOWN = 1.0           # segundos de pausa após processar uma ação, pra não contar eco/reverberação como nova palma
SAMPLE_RATE = 44100
BLOCK_DURATION = 0.05    # segundos por bloco de áudio analisado

TAPO_IP = os.environ["TAPO_IP"]
TAPO_EMAIL = os.environ["TAPO_EMAIL"]
TAPO_SENHA = os.environ["TAPO_SENHA"]
# -----------------------------------------------------------


async def _conectar_tomada():
    client = ApiClient(TAPO_EMAIL, TAPO_SENHA)
    dispositivo = await client.p110(TAPO_IP)
    return dispositivo


tomada = asyncio.run(_conectar_tomada())


def ligar():
    asyncio.run(tomada.on())
    print(">>> ABAJUR LIGADO")


def desligar():
    asyncio.run(tomada.off())
    print(">>> ABAJUR DESLIGADO")


def volume_do_bloco(indata):
    """Calcula o volume (RMS normalizado) de um bloco de áudio."""
    return float(np.sqrt(np.mean(indata**2)))


def esperar_palma():
    """Bloqueia até detectar um pico de volume acima do THRESHOLD. Retorna quando detecta."""
    block_size = int(SAMPLE_RATE * BLOCK_DURATION)
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=block_size) as stream:
        while True:
            indata, _ = stream.read(block_size)
            if volume_do_bloco(indata) > THRESHOLD:
                return


def main():
    print("Escutando... bata 1 palma para ligar, 2 palmas para desligar. (Ctrl+C pra sair)")
    while True:
        esperar_palma()
        inicio = time.time()

        segunda_palma = False
        block_size = int(SAMPLE_RATE * BLOCK_DURATION)
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, blocksize=block_size) as stream:
            while time.time() - inicio < CLAP_WINDOW:
                indata, _ = stream.read(block_size)
                if volume_do_bloco(indata) > THRESHOLD:
                    segunda_palma = True
                    break

        if segunda_palma:
            desligar()
        else:
            ligar()

        time.sleep(COOLDOWN)


if __name__ == "__main__":
    main()
