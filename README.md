# 🐳 Docker Event Discord Notifier

Aplicação em Python para monitoramento de eventos do Docker Daemon em tempo real via Docker Socket API. A aplicação captura o término de execução de contêineres e dispara notificações formatadas (Discord Rich Embeds) diretamente para um canal via Webhook.

---

## 📌 Funcionalidades

- **Monitoramento em Tempo Real:** Captura eventos de encerramento (`die`) emitidos pelo Docker Daemon.
- **Alertas Visuais Estruturados:**
  - 🟢 **Verde (`Exit Code 0`):** Contêiner finalizado com sucesso.
  - 🔴 **Vermelho (`Exit Code != 0`):** Contêiner finalizado com erro ou falha.
- **Detalhamento do Evento:** Nome do contêiner, ID curto (12 caracteres), imagem base utilizada, código de saída e data/hora do evento.
- **Segurança:** Configuração da URL do Webhook desacoplada do código fonte via variável de ambiente.

---

## 📋 Pré-requisitos

Antes de iniciar, certifique-se de ter instalado no sistema:

- **Docker:** Serviço em execução e usuário atual com permissão para executar comandos Docker sem `sudo` (pertencente ao grupo `docker`).
- **Python 3.10 ou superior:** Com o módulo `venv` e o gerenciador `pip`.
- **Canal no Discord:** Com um Webhook criado e URL copiada.

---

## 🚀 Instalação e Execução

### 1. Clonar o repositório
```bash
git clone [https://github.com/lparruda/docker-discord-notifier.git](https://github.com/lparruda/docker-discord-notifier.git)
cd docker-discord-notifier
