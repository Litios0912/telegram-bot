#!/usr/bin/env python3
"""
Telegram Bot con IA
Caracteristicas:
- /chat <mensaje> - Chat con Groq AI
- /buscar <query> - Busqueda web
- /recordatorio <texto> en <minutos> - Recordatorio
- /start - Mensaje de bienvenida
"""

import asyncio
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta

from duckduckgo_search import DDGS
from groq import Groq
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_TOKEN no configurado")
    sys.exit(1)

if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY no configurado")
    sys.exit(1)

groq_client = Groq(api_key=GROQ_API_KEY)
recordatorios = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy tu asistente en Telegram.\n\n"
        "Comandos:\n"
        "/chat <mensaje> - Preguntame lo que sea\n"
        "/buscar <consulta> - Buscar en internet\n"
        "/recordatorio <texto> en <minutos> - Crear recordatorio\n"
        "/ayuda - Ver comandos"
    )


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/chat <mensaje> - Chat con IA (Groq Llama 3.1)\n"
        "/buscar <consulta> - Busqueda web via DuckDuckGo\n"
        "/recordatorio <texto> en <minutos> - Ej: /recordatorio llamar en 5\n"
        "/start - Mensaje de bienvenida"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = " ".join(context.args)
    if not mensaje:
        await update.message.reply_text("Usa: /chat <tu mensaje>")
        return

    await update.message.chat.send_action("typing")

    try:
        respuesta = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Eres un asistente util. Responde en espanol de forma clara y concisa."},
                {"role": "user", "content": mensaje}
            ],
            temperature=0.3,
            max_tokens=500,
        )
        texto = respuesta.choices[0].message.content.strip()
        await update.message.reply_text(texto)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def buscar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    consulta = " ".join(context.args)
    if not consulta:
        await update.message.reply_text("Usa: /buscar <consulta>")
        return

    await update.message.chat.send_action("typing")

    try:
        resultados = []
        with DDGS() as ddgs:
            for r in ddgs.text(consulta, max_results=5):
                resultados.append(r.get("body", ""))

        if not resultados:
            await update.message.reply_text("Sin resultados.")
            return

        texto = f"Resultados para: {consulta}\n\n"
        for i, r in enumerate(resultados[:5], 1):
            texto += f"{i}. {r[:200]}\n\n"

        await update.message.reply_text(texto[:4000])
    except Exception as e:
        await update.message.reply_text(f"Error en busqueda: {e}")


async def recordatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("Usa: /recordatorio <texto> en <minutos>")
        return

    match = re.search(r"en\s+(\d+)", texto.lower())
    if not match:
        await update.message.reply_text("Ej: /recordatorio llamar en 5")
        return

    minutos = int(match.group(1))
    mensaje = re.sub(r"\s*en\s+\d+\s*", "", texto, count=1).strip()

    chat_id = update.effective_chat.id
    tiempo = datetime.now() + timedelta(minutes=minutos)

    if chat_id not in recordatorios:
        recordatorios[chat_id] = []
    recordatorios[chat_id].append({"mensaje": mensaje, "tiempo": tiempo})

    if not hasattr(context.application, "_recordatorio_task"):
        async def revisar():
            while True:
                await asyncio.sleep(30)
                for cid in list(recordatorios.keys()):
                    vencidos = [r for r in recordatorios[cid] if r["tiempo"] <= datetime.now()]
                    for r in vencidos:
                        try:
                            await context.application.bot.send_message(
                                chat_id=cid,
                                text=f"Recordatorio: {r['mensaje']}"
                            )
                        except Exception:
                            pass
                    recordatorios[cid] = [r for r in recordatorios[cid] if r not in vencidos]
        context.application._recordatorio_task = asyncio.create_task(revisar())

    await update.message.reply_text(f"Recordatorio '{mensaje}' en {minutos} min.")


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("chat", chat))
    app.add_handler(CommandHandler("buscar", buscar))
    app.add_handler(CommandHandler("recordatorio", recordatorio))

    logger.info("Bot iniciado")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
