# Guia de Contribuição - Kairos

Obrigado por se interessar em contribuir com o Kairos! Este guia cobre as melhores práticas para cada tipo de contribuição.

## Índice

- [Guia de Contribuição - Kairos](#guia-de-contribuição---kairos)
  - [Índice](#índice)
  - [Parte 1. Boas Práticas](#parte-1-boas-práticas)
    - [Etiqueta](#etiqueta)
    - [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
  - [Parte 2. Trabalhando com Issues](#parte-2-trabalhando-com-issues)
    - [Como Abrir uma Issue](#como-abrir-uma-issue)
    - [Antes de Submeter](#antes-de-submeter)
    - [Para Mais Informações](#para-mais-informações)
  - [Parte 3. Contribuindo com Código](#parte-3-contribuindo-com-código)
    - [Quando Modificar o Código](#quando-modificar-o-código)
    - [Nunca modifique o código para](#nunca-modifique-o-código-para)
    - [Processo de Contribuição](#processo-de-contribuição)
    - [Estrutura do Projeto](#estrutura-do-projeto)
    - [Comentários no Código](#comentários-no-código)
      - [Commits](#commits)
      - [Executando Testes e Linters](#executando-testes-e-linters)
  - [Dúvidas?](#dúvidas)

## Parte 1. Boas Práticas

### Etiqueta

Ao contribuir para o Kairos, lembre-se dos pontos abaixo.

- Escreva títulos claros e concisos para as Issues
  - Não coloque a descrição inteira no título da issue
- Evite duplicações
  - Verifique se a issue ou PR que você quer abrir já existe
- Uma coisa por vez
  - Uma issue ou PR por problema/feature
- Qualidade primeiro
  - Priorize código bem escrito e testado

> [!TIP]
> Use a barra de busca antes de abrir uma nova issue. Muitas vezes, alguém já reportou o mesmo problema!

### Ambiente de Desenvolvimento

Antes de qualquer contribuição em código, configure o ambiente seguindo [docs/SETUP.MD](SETUP.MD).

## Parte 2. Trabalhando com Issues

### Como Abrir uma Issue

1. Acesse a aba [Issues](https://github.com/MatheusSilver/Kairos/issues) do repositório
2. Clique em **New Issue**
3. Escolha o template apropriado que melhor descreve sua necessidade
4. Preencha todos os campos obrigatórios com o máximo de detalhes
5. Submeta a issue

> [!IMPORTANT]
> Todos os campos marcados como obrigatórios no template devem ser preenchidos. Issues incompletas podem ser fechadas.

### Antes de Submeter

- Procure duplicatas
    - Use a barra de busca para verificar se a issue já foi reportada
- Complete o checklist
    - Preencha todos os campos solicitados no template
- Seja específico
    - Quanto mais detalhes, melhor poderemos ajudar

### Para Mais Informações

Para uma descrição detalhada de cada tipo de issue disponível, consulte [docs/ISSUES.MD](ISSUES.MD).

## Parte 3. Contribuindo com Código

### Quando Modificar o Código

Você deve modificar o código nas situações abaixo.

- Corrigir um bug reportado e confirmado
- Implementar uma feature que foi solicitada e aprovada em uma issue
- Melhorar a qualidade do código existente (refatoração, otimização)
- Atualizar documentação que está desatualizada ou incompleta

> [!TIP]
> Sempre abra uma issue antes de começar a trabalhar. Assim, a discussão pode acontecer antes do trabalho ser feito!

### Nunca modifique o código para

- Adicionar funcionalidades não solicitadas
- Mudar estilos visuais sem discussão prévia
- Refatorar código sem abrir uma issue de manutenção
- Mergear grandes mudanças sem review

> [!CAUTION]
> PRs que violarem essas regras podem ser rejeitadas sem revisão. Sempre discuta antes de implementar!

### Processo de Contribuição

1. Crie uma issue primeiro - Descreva o que você pretende fazer
2. Aguarde feedback
3. Faça um fork do repositório
4. Clone seu fork localmente com `git clone seu-fork-url`
5. Crie uma branch descritiva
   - `fix/nome-do-bug` para correções
   - `feature/nome-da-funcionalidade` para novas features
   - `docs/descricao` para documentação
6. Implemente suas mudanças com commits bem descritos
7. Execute as validações locais (lint e testes)
8. Push para seu fork
9. Abra um Pull Request (PR) referenciando a issue original

### Estrutura do Projeto

O backend segue uma separação por camadas.

```
backend/app/
├── api/        Dependências e agregação das rotas
├── routers/    Endpoints
├── core/       Configuração, segurança e Senha Única
├── db/         Sessão e inicialização do banco
├── models/     Tabelas SQLModel
└── schemas/    Entrada e saída da API
```

Duas regras merecem atenção.

- Todo novo modelo de tabela deve ser importado em `models/__init__.py`, senão o Alembic não o enxerga
- As classes base compartilhadas ficam em `schemas/`, e a dependência corre em uma direção só, de `models` para `schemas`

Ao alterar rotas ou schemas, regenere o client do frontend com `devbox run client`.

### Comentários no Código

Escreva comentários úteis, não óbvios.

Evite o estilo abaixo.

```python
# Incrementa contador
contador += 1

# Verifica se o usuário é nulo
if user is not None: ...
```

Prefira o estilo abaixo.

```python
# Conta apenas as sugestões aceitas, para calcular o impacto final
contador += 1

# O usuário pode ser nulo se o token expirou entre duas requisições
if user is not None: ...
```

> [!TIP]
> Comentários devem explicar o "por quê", não o "o quê". O código já diz o que está fazendo!

#### Commits

Escreva mensagens de commit claras e descritivas.

```bash
fix: corrigir contagem de conflitos na grade de horários
feature: adicionar filtro por semestre na tela de horários
docs: atualizar instruções de instalação
test: adicionar testes para o login simulado da USP
```

> [!IMPORTANT]
> Commits devem ser atômicos - cada commit deve representar uma mudança lógica única.

#### Executando Testes e Linters

Sempre execute as validações antes de criar uma PR.

```bash
devbox run lint
devbox run test
```

Seu código deve atender aos pontos abaixo.

- Passar em todos os testes existentes
- Incluir novos testes para funcionalidades novas
- Manter a cobertura de testes consistente

> [!CAUTION]
> A CI exige **90% de cobertura** no backend e reprova a PR abaixo disso. Nenhuma PR será aceita se os testes ou os linters não passarem.

Os workflows de testes e de linters rodam a cada push em qualquer branch, então você não precisa abrir uma PR para ver o resultado. O SonarQube roda apenas em `master` e nas PRs que apontam para ela.

## Dúvidas?

Se tiver dúvidas sobre como contribuir, use um dos caminhos abaixo.

- Abra uma issue perguntando
- Consulte a documentação do projeto
- Converse com algum dos membros da equipe
