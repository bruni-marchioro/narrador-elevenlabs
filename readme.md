# Narrador de IA com ElevenLabs

Projeto desenvolvido em **Python** para transformar roteiros de texto em narrações utilizando a API da ElevenLabs.

O objetivo é facilitar a produção de conteúdos em áudio para vídeos sobre tecnologia, curiosidades, notícias e dicas rápidas, permitindo selecionar vozes e personalizar estilos de narração.

## Funcionalidades

- Consulta das vozes disponíveis na conta ElevenLabs.
- Reprodução de prévias antes de selecionar uma voz.
- Três estilos predefinidos: Curiosidades, Notícias e Dicas rápidas.
- Personalização de estabilidade, similaridade, expressividade e velocidade.
- Teste das configurações de narração antes da geração final.
- Leitura de roteiros em arquivos `.txt`.
- Divisão de textos longos em segmentos.
- União dos segmentos em um único arquivo MP3 utilizando FFmpeg.
- Armazenamento das preferências de voz e estilo em JSON.
- Tratamento de erros da API, incluindo restrições de vozes para determinados planos.

## Tecnologias utilizadas

- Python 3.14
- API ElevenLabs
- Requests
- ImageIO-FFmpeg
- FFmpeg

## Requisitos

- Python instalado.
- Conta na ElevenLabs com uma chave de API válida.
- Conexão com a internet.
- Dependências listadas no arquivo `requirements.txt`.

## Instalação

### 1. Clonar o repositório

Abra o PowerShell e execute:

```powershell
git clone https://github.com/bruni-marchioro/narrador-elevenlabs.git
cd narrador-elevenlabs
```

### 2. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

## Configuração da API

Antes de executar o programa, configure sua chave da ElevenLabs.

No PowerShell:

```powershell
$env:ELEVENLABS_API_KEY = Read-Host "Cole sua chave do ElevenLabs"
```

Cole a chave quando solicitado.

**Importante:** nunca publique sua chave de API no GitHub nem a inclua diretamente no código.

A variável de ambiente configurada dessa maneira permanece disponível apenas durante a sessão atual do PowerShell.

## Como utilizar

### 1. Preparar o roteiro

Crie um arquivo chamado `roteiro.txt` na mesma pasta do arquivo `narrador.py`.

Escreva o texto que deseja narrar e salve o arquivo em UTF-8.

### 2. Executar o programa

No PowerShell:

```powershell
python narrador.py
```

### 3. Configurar a narração

O programa permite:

1. Selecionar uma voz disponível na ElevenLabs.
2. Ouvir uma prévia da voz.
3. Escolher um estilo de narração.
4. Ajustar parâmetros de voz, quando necessário.
5. Testar as configurações.
6. Informar o arquivo de roteiro e gerar a narração.

### 4. Localizar o áudio gerado

O arquivo MP3 é salvo na pasta do projeto, utilizando o sufixo `_narrado.mp3`.

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

Os estilos utilizam configurações da ElevenLabs. O resultado também depende da voz selecionada e da construção do roteiro.

## Configurações salvas

O programa utiliza o arquivo `config_narrador.json` para armazenar as preferências de voz e os parâmetros de narração.

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

Esse arquivo não contém a chave da API e não precisa ser publicado no repositório.

## Organização do projeto

```text
narrador-elevenlabs/
├── narrador.py
├── readme.md
├── requirements.txt
└── .gitignore
```

Arquivos de roteiro, configurações pessoais e áudios gerados podem permanecer apenas no computador.

## Limitações

- A geração de áudio depende da disponibilidade da API ElevenLabs.
- Algumas vozes podem exigir assinatura paga.
- Prévias e gerações podem consumir créditos da conta.
- Textos divididos em segmentos podem apresentar pequenas diferenças de entonação.
- A versão atual gera arquivos de áudio, não vídeos.

## Próximas melhorias

- Interface mais acessível e simplificada.
- Divisão de textos mais inteligente, respeitando frases e pausas.
- Reutilização de narrações já geradas.
- Organização de arquivos em pastas de entrada e saída.
- Integração com ferramentas de edição de vídeo.
- Criação de Shorts verticais com animações sincronizadas com a narração.

## Objetivo

Explorar a inteligência artificial como ferramenta de apoio à criação de conteúdo, mantendo o controle sobre a qualidade, a clareza e a naturalidade da narração.

**Projeto em desenvolvimento.**