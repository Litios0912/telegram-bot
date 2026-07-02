# Telegram Bot con IA

Bot de Telegram con inteligencia artificial integrada usando Groq (Llama 3.1), busqueda web via DuckDuckGo y recordatorios temporizados.

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1-1a9e5f)](https://groq.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?logo=telegram)](https://core.telegram.org/bots)
[![Deploy](https://img.shields.io/badge/Railway-Ready-7C3AED)](https://railway.com)

## Caracteristicas

- **Chat con IA** - Conversaciones naturales usando Groq API (Llama 3.1 8B)
- **Busqueda web** - Consulta DuckDuckGo directamente desde Telegram
- **Recordatorios** - Programa recordatorios con tiempo en minutos
- **Comandos intuitivos** - Disenado para ser usado sin manual

## Comandos

| Comando | Descripcion | Ejemplo |
|---|---|---|
| `/start` | Mensaje de bienvenida | `/start` |
| `/chat <mensaje>` | Pregunta a la IA | `/chat que es FastAPI?` |
| `/buscar <consulta>` | Busca en internet | `/buscar python 3.13 novedades` |
| `/recordatorio <texto> en <min>` | Crea recordatorio | `/recordatorio llamar en 10` |
| `/ayuda` | Lista completa de comandos | `/ayuda` |

## Instalacion local

```bash
git clone https://github.com/Litios0912/telegram-bot.git
cd telegram-bot
pip install -r requirements.txt

# Configurar variables
export TELEGRAM_TOKEN=tu_token_de_botfather
export GROQ_API_KEY=gsk_tu_key_de_groq

# Iniciar
python bot.py
```

## Despliegue en Railway

[![Deploy on Railway](https://img.shields.io/badge/Railway-Deploy-7C3AED?logo=railway)](https://railway.com)

1. Crea cuenta en [railway.com](https://railway.com) (con GitHub)
2. Clic en "New Project" -> "Deploy from GitHub repo"
3. Selecciona este repositorio
4. Agrega variables de entorno:
   - `TELEGRAM_TOKEN`
   - `GROQ_API_KEY`
5. Railway despliega automaticamente

O usa la CLI:

```bash
npm i -g @railway/cli
railway login
railway init
railway variables --set TELEGRAM_TOKEN=tu_token --set GROQ_API_KEY=gsk_tu_key
railway up
```

## Como obtener tokens

### Token de Telegram
1. Abre Telegram y busca [@BotFather](https://t.me/BotFather)
2. Envia `/newbot` y sigue las instrucciones
3. Copia el token que recibes

### API Key de Groq
1. Registrate en [console.groq.com](https://console.groq.com)
2. Ve a API Keys y crea una nueva
3. Copia la clave `gsk_...`

## Estructura

```
telegram-bot/
  bot.py              # Logica principal del bot
  requirements.txt    # Dependencias Python
  .env.example        # Template de variables de entorno
  README.md           # Este archivo
```

## Licencia

MIT
