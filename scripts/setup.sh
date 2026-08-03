#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${ROOT_DIR}/.env"
ENV_EXAMPLE="${ROOT_DIR}/.env.example"

ERRO_BG="\033[0;41m"
KAIROS="\033[0;30;42m"
BACKEND="\033[0;30;43m"
FRONTEND="\033[0;30;45m"
RESET="\033[0m"

# Variaveis que recebem um valor aleatorio ao criar o .env
SEGREDOS=(SECRET_KEY POSTGRES_PASSWORD)

OPT_ENV=0
OPT_BACKEND=0
OPT_FRONTEND=0

log_info() {
  echo -e "${KAIROS}[KAIROS]${RESET} $1"
}

log_error() {
  echo -e "${ERRO_BG}[KAIROS]${RESET} $1"
}

log_backend() {
  echo -e "${BACKEND}[BACKEND]${RESET} $1"
}

log_frontend() {
  echo -e "${FRONTEND}[FRONTEND]${RESET} $1"
}

help() {
  echo "Uso: devbox run setup [--env|--backend|--frontend|--all]"
  echo ""
  echo "Sem argumentos, executa o setup completo."
  echo ""
  echo "  --env        Cria o .env a partir do .env.example e gera os segredos"
  echo "  --backend    Instala as dependencias do backend (uv sync)"
  echo "  --frontend   Instala as dependencias do frontend (bun install)"
  echo "  --all        Executa tudo (padrao)"
  echo ""
  echo "Exemplos:"
  echo "  devbox run setup"
  echo "  devbox run setup --env"
  echo "  devbox run setup --backend --frontend"
  echo ""
}

gerar_segredo() {
  python -c "import secrets; print(secrets.token_urlsafe(32))"
}

conferir_variaveis() {
  local faltando=()
  local key

  while IFS= read -r key; do
    grep -q "^${key}=" "${ENV_FILE}" || faltando+=("${key}")
  done < <(grep -oE '^[A-Z0-9_]+=' "${ENV_EXAMPLE}" | tr -d '=')

  if [ ${#faltando[@]} -gt 0 ]; then
    log_error "O .env nao tem estas variaveis presentes no .env.example."
    printf '  %s\n' "${faltando[@]}"
    log_error "Adicione as variaveis acima antes de subir o sistema."
    return 1
  fi

  if grep -q '=changethis$' "${ENV_FILE}"; then
    log_error "Ainda existem valores 'changethis' no .env. Substitua antes de publicar."
  fi
}

criar_env() {
  if [ ! -f "${ENV_EXAMPLE}" ]; then
    log_error "Arquivo .env.example nao encontrado em ${ROOT_DIR}."
    exit 1
  fi

  if [ -f "${ENV_FILE}" ]; then
    log_info "O .env ja existe e nao sera sobrescrito."
    conferir_variaveis
    return
  fi

  cp "${ENV_EXAMPLE}" "${ENV_FILE}"

  local key valor
  for key in "${SEGREDOS[@]}"; do
    valor="$(gerar_segredo)"
    sed -i "s|^${key}=changethis$|${key}=${valor}|" "${ENV_FILE}"
  done

  log_info ".env criado a partir do .env.example, com segredos gerados."
}

instalar_backend() {
  log_backend "Instalando dependencias com uv..."
  cd "${ROOT_DIR}"
  uv sync
  log_backend "Backend pronto."
}

instalar_frontend() {
  log_frontend "Instalando dependencias com bun..."
  cd "${ROOT_DIR}"
  bun install
  log_frontend "Frontend pronto."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)      OPT_ENV=1; shift ;;
    --backend)  OPT_BACKEND=1; shift ;;
    --frontend) OPT_FRONTEND=1; shift ;;
    --all)      OPT_ENV=1; OPT_BACKEND=1; OPT_FRONTEND=1; shift ;;
    -h|--help)  help; exit 0 ;;
    *)          log_error "Opcao desconhecida: $1"; help; exit 1 ;;
  esac
done

if [[ $OPT_ENV -eq 0 && $OPT_BACKEND -eq 0 && $OPT_FRONTEND -eq 0 ]]; then
  OPT_ENV=1
  OPT_BACKEND=1
  OPT_FRONTEND=1
fi

[[ $OPT_ENV -eq 1 ]] && criar_env
[[ $OPT_BACKEND -eq 1 ]] && instalar_backend
[[ $OPT_FRONTEND -eq 1 ]] && instalar_frontend

log_info "Setup concluido. Use 'devbox run help' para ver os comandos disponiveis."
