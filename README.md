# Abajur por Palmas

Controle o abajur do quarto batendo palma: **1 palma liga, 2 palmas desligam.**

Um script Python que escuta o microfone em tempo real, detecta palmas por
análise de volume, e controla uma tomada inteligente Tapo P110 via Wi-Fi.

## Como funciona

1. O microfone é monitorado continuamente em pequenos blocos de áudio.
2. Quando o volume de um bloco ultrapassa um limiar, conta como uma palma.
3. O script espera uma janela curta de tempo para ver se vem uma segunda palma.
4. Uma palma → liga a tomada. Duas palmas → desliga.

## Tecnologias

- [`sounddevice`](https://pypi.org/project/sounddevice/) — captura de áudio do microfone
- [`numpy`](https://numpy.org/) — cálculo de volume (RMS)
- [`tapo`](https://pypi.org/project/tapo/) — controle da tomada inteligente TP-Link Tapo P110
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) — carregamento seguro de credenciais

## Pré-requisitos

- Python 3.10+
- Uma tomada inteligente Tapo (testado com o modelo P110)
- No app Tapo, ativar **Eu > Serviços de Terceiros > Compatibilidade com Terceiros**

## Instalação

```bash
git clone https://github.com/SEU-USUARIO/abajur-palmas.git
cd abajur-palmas
pip install -r requirements.txt
```

No Linux, pode ser necessário instalar a biblioteca de áudio do sistema:

```bash
sudo apt install libportaudio2
```

## Configuração

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o `.env`:

```
TAPO_IP=192.168.1.XX
TAPO_EMAIL=seuemail@gmail.com
TAPO_SENHA=suasenha
```

> O arquivo `.env` nunca deve ser commitado — ele já está no `.gitignore`.

## Uso

```bash
python3 abajur_palmas.py
```

Bata uma palma para ligar, duas palmas (em menos de 0.6s) para desligar.
`Ctrl+C` para encerrar.

## Ajustando a sensibilidade

No topo do `abajur_palmas.py`:

| Variável | O que faz |
|---|---|
| `THRESHOLD` | Volume mínimo para contar como palma. Aumente se detectar ruído demais; diminua se não detectar suas palmas. |
| `CLAP_WINDOW` | Tempo máximo entre a 1ª e a 2ª palma para contar como "duas palmas". |
| `COOLDOWN` | Pausa após cada ação, para não confundir o eco com uma nova palma. |

## Licença

Este projeto é livre para uso e modificação.
