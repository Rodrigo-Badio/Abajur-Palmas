# 👏 Abajur por Palmas

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

- Python 3.10+ ([baixe aqui](https://www.python.org/downloads/) caso ainda não tenha)
- Uma tomada inteligente Tapo (testado com o modelo P110)
- No app Tapo, ativar **Eu > Serviços de Terceiros > Compatibilidade com Terceiros**

## Instalação

```bash
git clone https://github.com/SEU-USUARIO/abajur-palmas.git
cd abajur-palmas
```

**Instalando as dependências:**

O `pip` (instalador de pacotes do Python) normalmente já vem junto com o Python.
Se o comando `pip` não for reconhecido no seu terminal (comum em instalações do
Windows), use o próprio Python para chamá-lo, em vez de instalar o pip separado:

```bash
python -m pip install -r requirements.txt
```

No Windows, caso nem isso funcione, primeiro garanta que o pip existe dentro da
sua instalação do Python:

```bash
python -m ensurepip --upgrade
```

e tente o comando de instalação novamente.

No Linux, pode ser necessário instalar também a biblioteca de áudio do sistema:

```bash
sudo apt install libportaudio2
```

## Configuração

Crie um arquivo chamado `.env` (esse é o nome completo — começa com ponto e
não tem mais nada depois) dentro da mesma pasta do `abajur_palmas.py`. Duas
formas de fazer isso:

**Opção 1 — copiando o arquivo de exemplo pelo terminal:**

```bash
cp .env.example .env
```

No Windows (PowerShell), use:

```powershell
copy .env.example .env
```

**Opção 2 — criando manualmente pelo editor de código:**

Crie um arquivo novo na pasta do projeto e salve ele com o nome `.env`
(atenção: alguns editores, ao salvar no Windows, podem adicionar uma extensão
escondida tipo `.env.txt` sem avisar — depois de salvar, confira o nome exato
do arquivo na pasta pra garantir que ficou só `.env`).

Depois de criado (por qualquer uma das opções), edite o `.env`:

```
TAPO_IP=192.168.1.XX
TAPO_EMAIL=seuemail@gmail.com
TAPO_SENHA=suasenha
```

> ⚠️ O arquivo `.env` nunca deve ser commitado — ele já está no `.gitignore`.

> ✅ **Antes de rodar o projeto**, confirme que o arquivo `.env` está de fato
> salvo dentro da mesma pasta do `abajur_palmas.py` (não em Downloads, não na
> Área de Trabalho, nem em outra pasta separada). Liste os arquivos da pasta
> (`ls -la` no Linux/Mac, ou `dir /a` no Windows) e verifique se `.env`
> aparece na lista, ao lado de `abajur_palmas.py`.

## Testando a sensibilidade do microfone

Antes de rodar o projeto completo, vale calibrar o quão sensível a detecção de
palma deve ser — cada microfone capta volumes diferentes. Use o script
auxiliar incluído no repositório:

```bash
python3 teste_volume.py
```

Ele mostra o volume captado pelo microfone em tempo real, sem controlar a
tomada. Fale ou bata palma perto do microfone e observe os números na tela —
esse é o valor que você deve usar no `THRESHOLD` do `abajur_palmas.py` (veja a
seção abaixo).

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
| `THRESHOLD` | Volume mínimo para contar como palma. Use o valor descoberto com o `teste_volume.py`. Aumente se detectar ruído demais; diminua se não detectar suas palmas. |
| `CLAP_WINDOW` | Tempo máximo entre a 1ª e a 2ª palma para contar como "duas palmas". |
| `COOLDOWN` | Pausa após cada ação, para não confundir o eco com uma nova palma. |

## Licença

Este projeto é livre para uso e modificação.
