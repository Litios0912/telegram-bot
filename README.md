# Telegram Bot con IA

Bot de Telegram con inteligencia artificial usando Groq (Llama 3.1).

## Caracteristicas

- `/chat <mensaje>` - Chat con IA usando Groq
- `/buscar <consulta>` - Busqueda web via DuckDuckGo
- `/recordatorio <texto> en <minutos>` - Recordatorios temporizados
- `/ayuda` - Lista de comandos

## Desplegar en Railway

1. Crea cuenta en https://railway.com
2. Conecta este repositorio de GitHub
3. Configura variables de entorno:
   - `TELEGRAM_TOKEN` - Token de @BotFather
   - `GROQ_API_KEY` - API key de Groq
4. Railway lo despliega automaticamente

## Uso local

```bash
export TELEGRAM_TOKEN=tu_token
export GROQ_API_KEY=gsk_tu_key
pip install -r requirements.txt
python bot.py
```

## Como obtener el token de Telegram

1. Abre Telegram y busca @BotFather
2. Envia `/newbot` y sigue las instrucciones
3. Copia el token que te da
