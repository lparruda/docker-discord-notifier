# 🐳 Docker Event Discord Notifier

Aplicação em Python concebida para monitorizar o ciclo de vida de contentores Docker em tempo real através da Docker Socket API. A ferramenta interceta eventos de paragem/término de contentores e envia notificações formatadas (Discord Rich Embeds) diretamente para um canal através de Webhook.

---

## 🚀 Funcionalidades

- **Monitorização em Tempo Real:** Captura eventos de encerramento (`die`) emitidos pelo Docker Daemon.
- **Alertas Estruturados (Discord Rich Embeds):**
  - 🟢 **Verde (`Exit Code 0`):** Contentor finalizado com sucesso.
  - 🔴 **Vermelho (`Exit Code != 0`):** Contentor finalizado com erro ou falha.
- **Metadados Detalhados:** Exibe Nome do Contentor, ID Curto (12 carateres), Imagem Base utilizada, Código de Saída e Data/Hora da ocorrência.
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

Clone o código-fonte para a sua máquina e aceda à pasta do projeto:

```bash
git clone https://github.com/lparruda/docker-discord-notifier.git
cd docker-discord-notifier
```

### 2. Criar e ativar o ambiente virtual (venv)

Isole as dependências da aplicação para evitar conflitos com o sistema operativo:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

(No Windows/PowerShell, execute: `.venv\Scripts\Activate.ps1`)

### 3. Instalar as dependências

Com o ambiente virtual ativado (indicado pelo prefixo `(.venv)` no terminal), instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### 4. Configurar a variável de ambiente do Webhook

⚠️ **Importante:** Substitua a URL abaixo pela URL real gerada no seu canal do Discord. Se mantiver os valores de exemplo literais (`SEU_ID_REAL/SEU_TOKEN_REAL`), a API do Discord responderá com o erro `400 Bad Request`.

**Linux / WSL / macOS:**

```bash
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/SEU_ID_REAL/SEU_TOKEN_REAL"
```

**Windows (PowerShell):**

```powershell
$env:DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/SEU_ID_REAL/SEU_TOKEN_REAL"
```

### 5. Iniciar o monitorizador

No mesmo terminal onde a variável foi definida, execute a aplicação:

```bash
python events.py
```

Quando a ligação for estabelecida com sucesso, o terminal apresentará:

```
[*] Conectado ao Docker Daemon com sucesso.
[*] Aguardando eventos de contentores (die)... Pressione Ctrl+C para encerrar.
```

---

## 🧪 Como Testar

Com o `events.py` em execução, abra um segundo terminal (mantendo o primeiro aberto) e execute os testes seguintes para simular o encerramento de contentores:

**Teste de Falha (Exit Code 1 → Alerta Vermelho):**

```bash
docker run --rm busybox sh -c "exit 1"
```

**Teste de Sucesso (Exit Code 0 → Alerta Verde):**

```bash
docker run --rm busybox sh -c "exit 0"
```

---

## ⚠️ Resolução de Problemas (Troubleshooting)

**`400 Client Error: Bad Request for url: .../SEU_ID/SEU_TOKEN`**
A variável `DISCORD_WEBHOOK_URL` foi exportada com os dados de exemplo. Encerre o script (`Ctrl + C`), exporte a URL completa obtida no Discord e volte a executar `python events.py`.

**`-bash: syntax error near unexpected token '('`**
O comando `git clone` foi colado com a sintaxe de link Markdown (`[url](url)`). Execute apenas o comando com o endereço limpo:
`git clone https://github.com/lparruda/docker-discord-notifier.git`

**`Permission denied: '/var/run/docker.sock'`**
O utilizador atual não tem privilégios para aceder à socket do Docker. Para corrigir em distribuições Linux/WSL:

```bash
sudo usermod -aG docker $USER
newgrp docker
```

**`ERRO: A variável de ambiente DISCORD_WEBHOOK_URL não está configurada!`**
A variável não foi exportada no terminal ativo. Certifique-se de executar o comando `export DISCORD_WEBHOOK_URL="..."` na mesma sessão onde executa o script Python.

---

## 📄 Licença

Distribuído sob a licença MIT. Consulte o ficheiro `LICENSE` para mais detalhes.
