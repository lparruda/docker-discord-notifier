from datetime import datetime
import docker
import requests

# URL do Webhook obtido no Discord
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1552349788635136020/hx0hRuu11BbJfhmqsbmk-kO8MSGnqiNTOkYS5aLB2NTDJGvFMmTpkFkCyLLuUyTROfPi'  #[cite: 19]


def enviar_alerta_discord(nome, container_id, imagem, exit_code, data_hora):
    """Envia um cartão formatado (Embed) para o canal do Discord."""

    # Cor vermelha (0xE74C3C) para erros (exit_code != 0) e laranja/verde se for saída limpa
    cor_alerta = 0xE74C3C if exit_code != '0' else 0x2ECC71
    status_titulo = (
        'Contentor Parou com Erro'
        if exit_code != '0'
        else 'Contentor Finalizado (Sucesso)'
    )

    embed = {
        'title': status_titulo,
        'color': cor_alerta,
        'fields': [
            {'name': 'Nome do Contentor', 'value': f'`{nome}`', 'inline': True},
            {
                'name': 'ID',
                'value': f'`{container_id}`',
                'inline': True,
            },
            {
                'name': 'Código de Saída (Exit Code)',
                'value': f'**{exit_code}**',
                'inline': True,
            },
            {
                'name': 'Imagem Base',
                'value': f'`{imagem}`',
                'inline': True,
            },
            {
                'name': 'Data e Hora',
                'value': data_hora,
                'inline': True,
            },
        ],
        'footer': {'text': 'Docker Event Monitor • Alerta Automático'},
        'timestamp': datetime.utcnow().isoformat(),
    }

    payload = {'embeds': [embed]}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
        response.raise_for_status()
        print(f'[OK] Alerta do contentor {nome} enviado com sucesso ao Discord.')
    except requests.exceptions.RequestException as erro:
        print(f'[ERRO] Falha ao comunicar com o Discord: {erro}')


def iniciar_monitorizacao():
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    print('Monitorização ativa. A escutar eventos "die" do Docker...')

    for event in client.events(decode=True, filters={'event': 'die'}):
        actor_attrs = event.get('Actor', {}).get('Attributes', {})

        container_id = event['Actor']['ID'][:12]
        container_name = actor_attrs.get('name', 'desconhecido')
        imagem = actor_attrs.get('image', 'desconhecida')
        exit_code = actor_attrs.get('exitCode', '1')

        # Formatação do timestamp para formato legível
        data_formatada = datetime.fromtimestamp(event['time']).strftime(
            '%d/%m/%Y às %H:%M:%S'
        )

        enviar_alerta_discord(
            nome=container_name,
            container_id=container_id,
            imagem=imagem,
            exit_code=exit_code,
            data_hora=data_formatada,
        )


if __name__ == '__main__':
    iniciar_monitorizacao()