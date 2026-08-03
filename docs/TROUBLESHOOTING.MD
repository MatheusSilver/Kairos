# Troubleshooting

Este documento reúne os problemas mais comuns durante a configuração e execução do projeto, junto com a solução recomendada.

Caso encontre um problema novo e que não esteja coberto nesta página, por favor nos informe abrindo uma Issue para que possamos te ajudar.

## 1. Porta 5432 já está em uso

### Descrição

Ao executar `devbox run up`, `devbox run infra` ou `devbox run test`, aparece a mensagem abaixo.

```bash
failed to bind host port 0.0.0.0:5432/tcp: address already in use
```

Isso acontece quando já existe um PostgreSQL instalado e rodando na sua máquina, ocupando a porta padrão.

### Solução

A forma recomendada é trocar a porta publicada pelo container, alterando no `.env`.

```bash
POSTGRES_PORT=5433
```

Essa variável controla apenas a porta exposta no host. Os containers continuam se comunicando pela porta interna padrão, então nada mais precisa ser ajustado.

Alternativamente, você pode parar o PostgreSQL do sistema.

```bash
sudo systemctl stop postgresql
```

> [!NOTE]
> Se você usa o PostgreSQL local para outros projetos, prefira a primeira opção.

## 2. Variável obrigatória não definida

### Descrição

Ao rodar qualquer comando que use o Docker Compose, aparece a mensagem abaixo.

```bash
required variable POSTGRES_PASSWORD is missing a value: Variable not set
```

### Solução

O arquivo `.env` não existe ou está incompleto. Ele não é versionado por conter credenciais reais.

```bash
devbox run setup
```

O comando cria o `.env` a partir do `.env.example` e gera os valores aleatórios necessários. Se o `.env` já existir, ele não é sobrescrito, e o comando lista quais variáveis do `.env.example` estão faltando para você completar.

## 3. Migration gerada vem vazia

### Descrição

Após criar um novo modelo de tabela, `devbox run revision "mensagem"` gera uma migration com `pass` no `upgrade()`.

### Solução

O Alembic descobre as tabelas a partir de `backend/app/models/__init__.py`. Se o modelo novo não estiver importado ali, ele não é registrado no metadata e a autogeração não vê nada.

```python
from app.models.seu_modelo import SeuModelo

__all__ = ["SeuModelo", ...]
```

Apague a migration vazia, corrija o `__init__.py` e gere novamente.

## 4. Erro do Alembic sobre revisão inexistente

### Descrição

```bash
Can't locate revision identified by '<hash>'
```

### Solução

O banco guarda, na tabela `alembic_version`, qual foi a última migration aplicada. Se essa migration foi removida ou reescrita, o Alembic não consegue mais localizá-la.

Como o projeto ainda não tem dados de produção, o caminho mais simples é recriar o banco do zero.

```bash
devbox run reset
devbox run prestart
```

> [!CAUTION]
> `devbox run reset` apaga o volume do banco e todos os dados locais.

## 5. O frontend não enxerga uma rota nova da API

### Descrição

Você criou ou alterou um endpoint no backend, mas o frontend não reconhece o método correspondente e o TypeScript acusa erro.

### Solução

A camada de acesso à API do frontend é gerada a partir do OpenAPI do backend. Regenere com o comando abaixo.

```bash
devbox run client
```

O backend precisa estar importável no momento da geração. Note também que as rotas do login simulado só aparecem quando `ENVIRONMENT=local`.

## 6. O login simulado não aparece

### Descrição

A tela de login abre sem nenhum usuário USP listado.

### Solução

As rotas do login simulado só são registradas quando `ENVIRONMENT=local` no `.env`. Confira o valor e reinicie o backend.

Se a variável estiver correta, verifique se o backend está no ar em `http://localhost:8000/docs` e se a seção `auth` aparece na documentação.

## 7. Nix ou DevBox travando na primeira execução

### Descrição

Ao executar `devbox shell` pela primeira vez, o processo parece parado em uma mensagem como `evaluating derivation 'github:NixOS...`.

### Solução

1. Pressione `Enter` algumas vezes.
2. Aguarde a instalação terminar. É normal demorar bastante na primeira vez, pois o DevBox baixa Python, uv, Bun e o cliente do PostgreSQL.
3. Se o prompt final ficar parecido com `(devbox) <seu usuario>@<path>`, deu certo.

> [!NOTE]
> Esse procedimento pode demorar um pouco mais se estiver usando o WSL.
