import os
import sys
from datetime import datetime
import docker
import requests

# 1. Carregar a URL do webhook a partir da variável de ambiente
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not DISCORD_WEBHOOK_URL:
    print(
        "ERRO: A variável de ambiente DISCORD_WEBHOOK_URL não está configurada!\n"
        "Configure-a antes de iniciar o script executando:\n"
        "  export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'",
        file=sys.stderr
    )
    sys.exit(1)


def mascarar_webhook(texto: str) -> str:
    """Remove o ID/Token do Webhook de qualquer string antes de ir para os logs."""
    if "/webhooks/" in texto:
        base, _ = texto.split("/webhooks/", 1)
        # Corta tudo depois de '/webhooks/' até o próximo espaço (se houver mais texto na mensagem)
        resto = texto.split("/webhooks/", 1)[1]
        resto_apos_token = resto.split(" ", 1)
        sufixo = f" {resto_apos_token[1]}" if len(resto_apos_token) > 1 else ""
        return f"{base}/webhooks/***MASKED***{sufixo}"
    return texto


def enviar_alerta_discord(nome, container_id, imagem, exit_code, data_hora):
    """Envia uma notificação estruturada (Embed) para o canal do Discord via Webhook."""
    # Define a cor e o título consoante o código de saída
    if exit_code == 0:
        cor = 0x2ECC71  # Verde (Sucesso)
        titulo = "🟢 Contentor Finalizado (Sucesso)"
    else:
        cor = 0xE74C3C  # Vermelho (Falha / Erro)
        titulo = "🔴 Contentor Finalizado com Erro"

    payload = {
        "embeds": [
            {
                "title": titulo,
                "color": cor,
                "fields": [
                    {
                        "name": "Nome do Contentor",
                        "value": f"`{nome}`",
                        "inline": True
                    },
                    {
                        "name": "ID",
                        "value": f"`{container_id[:12]}`",
                        "inline": True
                    },
                    {
                        "name": "Código de Saída (Exit Code)",
                        "value": f"`{exit_code}`",
                        "inline": True
                    },
                    {
                        "name": "Imagem Base",
                        "value": f"`{imagem}`",
                        "inline": True
                    },
                    {
                        "name": "Data e Hora",
                        "value": data_hora,
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Docker Event Monitor • Alerta Automático"
                }
            }
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=10)
        response.raise_for_status()
        print(f"[+] Alerta enviado para o Discord | Contentor: {nome} | Exit Code: {exit_code}")
    except requests.exceptions.RequestException as e:
        # A mensagem de erro do requests inclui a URL completa da requisição (com o
        # ID/Token do Webhook). Mascaramos antes de logar para não expor a credencial.
        print(f"[-] Erro ao enviar notificação para o Discord: {mascarar_webhook(str(e))}", file=sys.stderr)


def monitorar_eventos():
    """Conecta ao daemon do Docker e monitora eventos de término de contentores em tempo real."""
    try:
        client = docker.from_env()
        # Testa a conectividade com o daemon
        client.ping()
        print("[*] Conectado ao Docker Daemon com sucesso.")
        print("[*] Aguardando eventos de contentores (die)... Pressione Ctrl+C para encerrar.")
    except Exception as e:
        print(f"[-] Falha ao conectar ao Docker Daemon: {e}", file=sys.stderr)
        sys.exit(1)

    # Filtra apenas eventos do tipo container e ação 'die' (término do processo)
    for event in client.events(decode=True, filters={"type": "container", "event": "die"}):
        actor = event.get("Actor", {})
        attributes = actor.get("Attributes", {})

        nome = attributes.get("name", "Desconhecido")
        # O ID do contentor vem em Actor.ID (não em event["id"], que costuma vir vazio/N.A.)
        container_id = actor.get("ID", "N/A")
        imagem = attributes.get("image", "Desconhecida")
        
        try:
            exit_code = int(attributes.get("exitCode", 0))
        except (ValueError, TypeError):
            exit_code = -1

        # Formata o timestamp do evento para leitura humana
        timestamp = event.get("time", 0)
        data_hora = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y às %H:%M:%S")

        enviar_alerta_discord(nome, container_id, imagem, exit_code, data_hora)


if __name__ == "__main__":
    try:
        monitorar_eventos()
    except KeyboardInterrupt:
        print("\n[*] Monitoramento finalizado pelo utilizador.")
        sys.exit(0)
