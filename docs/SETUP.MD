# Configuração do Ambiente de Desenvolvimento

Este projeto usa **DevBox** para criar um ambiente de desenvolvimento isolado com todas as ferramentas necessárias.

O guia a partir daqui assume que você está usando um Sistema Operacional Linux.

## Dependências

- Docker e Docker Compose
- DevBox
- Python 3.14 - (Instalado pelo DevBox)
- uv - (Instalado pelo DevBox)
- Bun - (Instalado pelo DevBox)
- PostgreSQL client - (Instalado pelo DevBox)

As dependências de Python e do frontend são instaladas pelo comando de setup do DevBox.

Das quais, apenas o Docker e o DevBox devem ser instalados primeiro, de forma manual.

# Instalação de Dependências

Caso tenha qualquer problema na instalação de qualquer componente, refira-se a [página de troubleshooting](TROUBLESHOOTING.MD) para os problemas mais comuns.

## 1. Docker

O Docker é usado para subir o banco de dados PostgreSQL, o Adminer e o Mailcatcher, além de permitir executar a stack completa.

### 1. Instalação

Siga o guia oficial do [Docker Engine](https://docs.docker.com/engine/install/) para a sua distribuição.

### 2. Configuração

Adicione seu usuário ao grupo `docker` para não precisar de `sudo`.

```bash
sudo usermod -aG docker $USER
```

Faça logout e login novamente para que a mudança tenha efeito.

## 2. DevBox

O DevBox é um gerenciador de ambientes de desenvolvimento que permite que as instalações feitas para este projeto não interfiram com o restante do seu sistema.

### 1. Instalação

Baixe o DevBox com o comando abaixo.

```bash
curl -fsSL https://get.jetify.com/devbox | bash
```

## Setup do Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/MatheusSilver/Kairos.git
cd Kairos
```

### 2. Iniciar o DevBox

Dentro da pasta raiz do projeto, execute o comando abaixo.

```bash
devbox shell
```

Na primeira execução o DevBox irá baixar Python, uv, Bun e o cliente do PostgreSQL. É normal demorar.

### 3. Executar o setup

```bash
devbox run setup
```

Este comando faz o seguinte.

- Cria o `.env` a partir do `.env.example`, se ele ainda não existir
- Gera valores aleatórios para `SECRET_KEY` e `POSTGRES_PASSWORD`
- Instala as dependências do backend (`uv sync`) e do frontend (`bun install`)

Um `.env` que já exista nunca é sobrescrito. Nesse caso o comando apenas confere se todas as variáveis do `.env.example` estão presentes e avisa quais faltam.

Também é possível executar apenas uma parte do setup.

```bash
devbox run setup --env        # Apenas o .env
devbox run setup --backend    # Apenas as dependências do backend
devbox run setup --frontend   # Apenas as dependências do frontend
```

> [!CAUTION]
> **NUNCA** sob hipótese alguma faça commit do `.env`. Ele está no `.gitignore` justamente por conter credenciais reais. O arquivo versionado é o `.env.example`, que deve conter apenas valores de exemplo.

### 4. Ajustar o `.env` (se necessário)

Se você já tiver um PostgreSQL rodando na porta 5432 da sua máquina, altere a porta publicada no `.env`.

```bash
POSTGRES_PORT=5433
```

Essa variável controla apenas a porta exposta no host. Os containers continuam conversando entre si pela porta interna padrão.

### 5. Subir o sistema

```bash
devbox run up
```

O comando sobe a stack completa em Docker com recarregamento automático.

| Serviço | Endereço |
| --- | --- |
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Documentação da API | http://localhost:8000/docs |
| Adminer | http://localhost:8080 |
| Mailcatcher | http://localhost:1080 |

### 6. Entrar no sistema

A autenticação definitiva será feita pela **Senha Única USP**, mas ela depende de credenciais institucionais que ainda não foram liberadas. Enquanto isso, o ambiente local expõe um login simulado.

Na tela de login você verá uma lista de usuários USP fictícios. Basta clicar em um deles. O usuário cujo nº USP corresponde a `FIRST_APOIO_CODPES` no `.env` entra com permissão de Apoio BCC.

> [!NOTE]
> As rotas do login simulado só são registradas quando `ENVIRONMENT=local`. Elas não existem em staging nem em produção.

## Comandos do DevBox

Para ver a lista completa, execute o comando abaixo.

```bash
devbox run help
```

### Execução

```bash
devbox run up        # Stack completa em Docker, com watch
devbox run down      # Para a stack
devbox run reset     # Para a stack e apaga o banco
devbox run logs      # Acompanha os logs
```

Para desenvolver com recarregamento mais rápido, é possível rodar backend e frontend fora do Docker.

```bash
devbox run infra     # Sobe apenas db, adminer e mailcatcher
devbox run api       # Backend em :8000
devbox run web       # Frontend em :5173
```

### Banco de dados

```bash
devbox run migrate                     # Aplica as migrations
devbox run revision "mensagem"         # Gera uma migration automática
devbox run prestart                    # Espera o banco, migra e popula
devbox run psql                        # Abre um shell psql
```

> [!IMPORTANT]
> Todo novo modelo de tabela precisa ser importado em `backend/app/models/__init__.py`. O Alembic descobre as tabelas a partir desse arquivo, e se você esquecer, a migration gerada virá vazia.

### Testes

```bash
devbox run test              # Testes do backend, com relatório de cobertura
devbox run test --e2e        # Testes ponta a ponta (Playwright)
devbox run test --all        # Ambos
```

O comando sobe o banco e aplica as migrations sozinho antes de executar.

### Linters

```bash
devbox run lint              # ruff, pylint, bandit e biome
devbox run lint --backend    # Apenas o backend
devbox run lint --frontend   # Apenas o frontend
devbox run lint --fix        # Corrige o que for corrigível automaticamente
```

### Client do frontend

O frontend consome uma camada de acesso à API gerada a partir do OpenAPI do backend. Sempre que você alterar rotas ou schemas, regenere com o comando abaixo.

```bash
devbox run client
```

## Fluxo recomendado para desenvolvimento

```bash
devbox shell
devbox run infra
devbox run api      # em um terminal
devbox run web      # em outro terminal
```

Antes de abrir uma Pull Request, execute as validações abaixo.

```bash
devbox run lint
devbox run test
```
