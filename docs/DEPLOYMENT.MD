# Deploy

Este documento descreve como colocar o Kairos no ar. O sistema é publicado com **Docker Compose** e usa o **Traefik** como proxy reverso, que também cuida da emissão automática dos certificados HTTPS pelo Let's Encrypt.

O guia assume um servidor Linux com acesso administrativo e um domínio já registrado.

## Dependências

- Um servidor Linux com IP público
- Um domínio com acesso ao painel de DNS
- Docker e Docker Compose instalados no servidor
- Um runner self-hosted do GitHub Actions configurado no servidor

## Preparação do Servidor

### 1. Configurar o DNS

O Kairos publica cada parte do sistema em um subdomínio diferente. Crie registros do tipo A apontando para o IP do servidor.

| Subdomínio | Serviço |
| --- | --- |
| `dashboard.seudominio.com` | Frontend |
| `api.seudominio.com` | Backend |
| `adminer.seudominio.com` | Adminer |
| `traefik.seudominio.com` | Painel do Traefik |

O caminho mais simples é criar um registro curinga `*.seudominio.com`, que cobre os quatro de uma vez e ainda atende os subdomínios de staging.

> [!TIP]
> Se você pretende manter staging e produção no mesmo domínio, use um prefixo para separar, como `dashboard.staging.seudominio.com`.

### 2. Criar a rede pública do Docker

O Traefik e os serviços do Kairos se comunicam por uma rede externa compartilhada. Ela precisa existir antes de qualquer container subir.

```bash
docker network create traefik-public
```

### 3. Subir o Traefik

O Traefik roda em uma stack separada, definida em `compose.traefik.yml`. Ele é iniciado uma única vez no servidor e passa a atender todas as stacks do Kairos.

Primeiro exporte as variáveis que ele exige.

```bash
export DOMAIN=seudominio.com
export EMAIL=seu@email.com
export USERNAME=admin
```

O painel do Traefik é protegido por autenticação básica, então é preciso gerar o hash da senha. Gere com o comando abaixo e copie o resultado.

```bash
export HASHED_PASSWORD=$(openssl passwd -apr1)
```

Com as variáveis definidas, suba a stack.

```bash
docker compose -f compose.traefik.yml up -d
```

> [!CAUTION]
> Não use um endereço de e-mail inválido em `EMAIL`. O Let's Encrypt recusa a emissão de certificados quando o endereço não é aceito.

## Configuração do GitHub

O deploy é feito pelos workflows em `.github/workflows`. Eles rodam em runners self-hosted, ou seja, no próprio servidor.

### 1. Registrar os runners

Cada ambiente usa um runner identificado por uma etiqueta. Em Settings, Actions, Runners, adicione um novo runner self-hosted e atribua a etiqueta correspondente.

| Ambiente | Etiquetas exigidas |
| --- | --- |
| Staging | `self-hosted`, `staging` |
| Produção | `self-hosted`, `production` |

### 2. Cadastrar os secrets

Em Settings, Secrets and variables, Actions, cadastre os valores abaixo.

| Secret | Descrição |
| --- | --- |
| `DOMAIN_STAGING` | Domínio usado em staging |
| `DOMAIN_PRODUCTION` | Domínio usado em produção |
| `STACK_NAME_STAGING` | Nome da stack de staging, sem espaços |
| `STACK_NAME_PRODUCTION` | Nome da stack de produção, sem espaços |
| `SECRET_KEY` | Chave usada para assinar os tokens |
| `FIRST_APOIO_CODPES` | Número USP do primeiro membro do Apoio BCC |
| `POSTGRES_PASSWORD` | Senha do banco de dados |
| `SMTP_HOST` | Servidor de e-mail |
| `SMTP_USER` | Usuário do servidor de e-mail |
| `SMTP_PASSWORD` | Senha do servidor de e-mail |
| `EMAILS_FROM_EMAIL` | Endereço remetente |
| `SENTRY_DSN` | DSN do Sentry, se for usado |

Gere as chaves com o comando abaixo.

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

> [!CAUTION]
> O arquivo `.env` não é versionado. Em produção nada é lido dele, todas as variáveis vêm dos secrets declarados nos workflows. Se você adicionar uma variável obrigatória nova ao `compose.yml`, precisa declará-la também nos dois workflows de deploy, senão o deploy falha com a mensagem `Variable not set`.

## Executando o Deploy

### Staging

O deploy de staging acontece automaticamente a cada push na branch `master`. Também é possível disparar manualmente pela aba Actions, escolhendo o workflow e clicando em Run workflow.

### Produção

O deploy de produção acontece quando uma release é publicada no GitHub. Vá em Releases, crie uma nova tag e publique.

> [!IMPORTANT]
> Publicar a release é o gatilho. Salvar como rascunho não dispara o deploy.

### Deploy manual

Também é possível subir a stack diretamente no servidor, sem passar pelo GitHub Actions. Exporte as mesmas variáveis usadas pelos workflows e execute os comandos abaixo.

```bash
docker compose -f compose.yml --project-name kairos build
docker compose -f compose.yml --project-name kairos up -d
```

O `--project-name` isola as stacks entre si. Use nomes diferentes para staging e produção no mesmo servidor.

## Endereços após o Deploy

| Serviço | Endereço |
| --- | --- |
| Frontend | `https://dashboard.seudominio.com` |
| Documentação da API | `https://api.seudominio.com/docs` |
| API | `https://api.seudominio.com` |
| Adminer | `https://adminer.seudominio.com` |
| Painel do Traefik | `https://traefik.seudominio.com` |

## Migrations

As migrations rodam sozinhas a cada deploy. O serviço `prestart` sobe antes do backend, espera o banco responder, aplica `alembic upgrade head` e cria o primeiro usuário do Apoio BCC a partir de `FIRST_APOIO_CODPES`.

Isso significa que uma migration quebrada impede a subida do backend, o que é intencional. O banco nunca fica em um estado que o código não espera.

## Login em Produção

O login simulado da Senha Única USP existe apenas quando `ENVIRONMENT=local`. Em staging e produção essas rotas não são registradas.

Enquanto as credenciais da Senha Única não forem liberadas pela USP, não há como autenticar em um ambiente publicado. Consulte [SETUP.MD](SETUP.MD) para entender como o login simulado funciona no ambiente de desenvolvimento.
