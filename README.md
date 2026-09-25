# 🐳 Docker Event Discord Notifier

Aplicação em Python concebida para monitorizar o ciclo de vida de contentores Docker em tempo real através da Docker Socket API. A ferramenta interceta eventos de paragem/término de contentores e envia notificações formatadas (Discord Rich Embeds) diretamente para um canal através de Webhook.

---

## 🚀 Funcionalidades

- **Monitorização em Tempo Real:** Captura eventos de encerramento (`die`) emitidos pelo Docker Daemon.
- **Alertas Estruturados (Discord Rich Embeds):**
  - 🟢 **Verde (`Exit Code 0`):** Contentor finalizado com sucesso.
  - 🔴 **Vermelho (`Exit Code != 0`):** Contentor finalizado com erro ou falha.
- **Metadados Detalhados:** Exibe o Nome do Contentor, ID Curto (12 carateres), Imagem Base utilizada, Código de Saída e Data/Hora da ocorrência.
- **Segurança de Credenciais:** Configuração do Webhook desacoplada do código fonte via variável de ambiente.

---

## 📋 Pré-requisitos

Antes de iniciar a instalação, certifique-se de que o ambiente cumpre os seguintes requisitos:

- **Docker:** Serviço em execução e o utilizador atual com permissões para interagir com o daemon (membro do grupo `docker`).
- **Python 3.10 ou superior:** Com os módulos `venv` e `pip` disponíveis.
- **Servidor Discord:** Um canal de texto com um Webhook configurado e a respetiva URL copiada (**Definições do Canal > Integrações > Webhooks**).

---

## 🔧 Instalação e Execução

### 1. Clonar o repositório
Clone o código-fonte limpo para a sua máquina e entre na pasta:
```bash
git clone https://github.com/lparruda/docker-discord-notifier.git
cd docker-discord-notifier
