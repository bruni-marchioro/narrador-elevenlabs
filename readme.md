# Narrador de IA com ElevenLabs

Projeto desenvolvido em Python para transformar roteiros de texto em narrações utilizando a API da ElevenLabs.

O objetivo é facilitar a produção de conteúdos em áudio para vídeos sobre tecnologia, curiosidades, notícias e dicas rápidas, com diferentes estilos de narração.

## Funcionalidades

- Listagem de vozes disponíveis na conta ElevenLabs.
- Demonstração em áudio antes de selecionar uma voz.
- Três estilos predefinidos: Curiosidades, Notícias e Dicas rápidas.
- Personalização de estabilidade, semelhança, expressividade e velocidade.
- Prévia das configurações antes da geração final.
- Leitura de roteiros em arquivos `.txt`.
- Divisão automática de textos longos.
- União dos segmentos em um único arquivo MP3 utilizando FFmpeg.
- Armazenamento das preferências de voz e narração em JSON.
- Tratamento de erros da API, incluindo restrições de vozes para planos pagos.

## Tecnologias utilizadas

- Python 3.14
- ElevenLabs API
- Requests
- ImageIO-FFmpeg
- FFmpeg

## Requisitos

- Python instalado.
- Chave de API da ElevenLabs.
- Acesso à internet.
- Bibliotecas Python indicadas abaixo.

## Instalação

Clone o repositório:

```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
```

Instale as dependências:

```bash
python -m pip install requests imageio-ffmpeg
```

## Configuração da API

No PowerShell do Windows, execute:

```powershell
$env:ELEVENLABS_API_KEY = Read-Host "Cole sua chave do ElevenLabs"
```

Cole sua chave quando solicitado.

**Importante:** nunca publique sua chave de API no GitHub ou a inclua diretamente no código.

A variável de ambiente configurada dessa maneira permanece disponível apenas na sessão atual do PowerShell.

## Como utilizar

Crie um arquivo chamado `roteiro.txt` na mesma pasta de `narrador.py`.

Escreva nele o texto que deseja narrar e salve em UTF-8.

Execute:

```powershell
python narrador.py
```

O programa permitirá selecionar uma voz, escolher o estilo de narração, ouvir uma prévia e informar o arquivo do roteiro.

Ao concluir a geração, o áudio será salvo na pasta do projeto com o sufixo `_narrado.mp3`.

Exemplo:

- Entrada: `roteiro.txt`
- Saída: `roteiro_narrado.mp3`

## Estilos de narração

| Estilo | Características |
|---|---|
| Curiosidades | Expressivo, descontraído e levemente acelerado |
| Notícias | Estável, equilibrado e informativo |
| Dicas rápidas | Dinâmico, amigável e objetivo |
| Personalizado | Parâmetros ajustados manualmente |

Os estilos utilizam configurações de voz da ElevenLabs. O resultado depende também da voz selecionada e da construção do roteiro.

## Configurações salvas

O programa cria automaticamente `config_narrador.json` para armazenar a voz selecionada e os parâmetros utilizados.

Exemplo:

```json
{
  "voice_id": "pqHfZKP75CvOlQylNhV4",
  "voice_name": "Bill - Wise, Mature, Balanced",
  "parametros": {
    "nome": "Noticias",
    "stability": 0.6,
    "similarity_boost": 0.85,
    "style": 0.1,
    "speed": 1.0
  }
}
```

Esse arquivo não contém a chave de API.

## Organização do projeto

```text
narrador-elevenlabs/
├── narrador.py
├── README.md
├── requirements.txt
├── .gitignore
└── roteiro_exemplo.txt
```

Arquivos de configuração pessoal e áudios gerados podem permanecer localmente e não precisam ser versionados.

## Limitações

- A geração de áudio depende da disponibilidade da API ElevenLabs.
- Algumas vozes podem exigir uma assinatura paga.
- Cada prévia ou geração pode consumir créditos da conta.
- A divisão de textos longos pode produzir diferenças de entonação entre segmentos.
- O programa gera áudio, não vídeos.

## Próximas melhorias

- Interface mais acessível e simplificada.
- Melhor divisão de textos por frases.
- Reutilização de narrações já geradas.
- Organização dos arquivos em pastas de entrada e saída.
- Integração futura com ferramentas de edição de vídeo.
- Criação de Shorts verticais com animações sincronizadas com a narração.

## Objetivo

Explorar a inteligência artificial como ferramenta de apoio à criação de conteúdo, mantendo o controle sobre a qualidade, a clareza e a naturalidade da narração.

Projeto em desenvolvimento.