# 🐳 Docker Event Discord Notifier

Uma aplicação leve em Python criada para monitorar o ciclo de vida de contêineres Docker em tempo real via Docker Socket API e disparar alertas estruturados (Discord Embeds) diretamente para um canal de notificações.

---

## 🚀 Funcionalidades

- **Monitoramento em Tempo Real:** Captura eventos de término de contêineres (`die` / `stop`) diretamente do Docker Daemon.
- **Alertas Estruturados (Discord Rich Embeds):**
  - 🟢 **Verde (`Exit Code 0`):** Contêiner finalizado com sucesso.
  - 🔴 **Vermelho (`Exit Code != 0`):** Contêiner finalizado com falha ou erro.
- **Metadados Detalhados:** Exibe Nome do Contêiner, Container ID (curto), Imagem utilizada, Exit Code e Data/Hora da ocorrência.
- **Tratamento de Exceções:** Parsing resiliente de atributos e requisições HTTP seguras com fallback.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Docker SDK for Python (`docker`)**
- **Requests**
- **Discord Webhooks API**

---

## 📋 Pré-requisitos

- Docker instalado e o serviço rodando (`docker ps` acessível pelo usuário).
- Python 3.12 instalado.
- Um Webhook criado no seu servidor do Discord.

---

## 🔧 Instalação e Execução

### 1. Clonar o repositório
```bash
git clone https://github.com/lparruda/docker-discord-notifier.git
cd docker-discord-notifier
