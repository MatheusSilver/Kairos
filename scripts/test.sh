#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ERRO_BG="\033[0;41m"
KAIROS="\033[0;30;42m"
BACKEND="\033[0;30;43m"
FRONTEND="\033[0;30;45m"
RESET="\033[0m"

OPT_BACKEND=0
OPT_E2E=0

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
  echo "Uso: devbox run test [--backend|--e2e|--all]"
  echo ""
  echo "Sem argumentos, executa os testes do backend."
  echo ""
  echo "  --backend   Testes do backend (pytest) com relatorio de cobertura"
  echo "  --e2e       Testes ponta a ponta do frontend (Playwright)"
  echo "  --all       Executa backend e e2e"
  echo ""
  echo "Exemplos:"
  echo "  devbox run test"
  echo "  devbox run test --all"
  echo "  devbox run test --e2e"
  echo ""
}

ensure_env() {
  if [ ! -f "${ROOT_DIR}/.env" ]; then
    log_error "Arquivo .env nao encontrado. Execute 'devbox run setup' primeiro."
    exit 1
  fi
}

ensure_db() {
  log_info "Subindo db e mailcatcher..."
  docker compose up -d db mailcatcher >/dev/null
  log_info "Aplicando migrations..."
  (cd "${ROOT_DIR}/backend" && uv run bash scripts/prestart.sh >/dev/null 2>&1)
}

run_backend() {
  ensure_env
  ensure_db
  log_backend "Executando pytest..."
  cd "${ROOT_DIR}/backend"
  uv run coverage run -m pytest tests/
  uv run coverage report
  log_backend "Testes do backend concluidos."
}

run_e2e() {
  ensure_env
  cd "${ROOT_DIR}"
  log_frontend "Preparando a stack para os testes ponta a ponta..."
  docker compose build >/dev/null
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
  log_frontend "Executando Playwright..."
  docker compose run --rm playwright bunx playwright test
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
  log_frontend "Testes ponta a ponta concluidos."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend) OPT_BACKEND=1; shift ;;
    --e2e)     OPT_E2E=1; shift ;;
    --all)     OPT_BACKEND=1; OPT_E2E=1; shift ;;
    -h|--help) help; exit 0 ;;
    *)         log_error "Opcao desconhecida: $1"; help; exit 1 ;;
  esac
done

if [[ $OPT_BACKEND -eq 0 && $OPT_E2E -eq 0 ]]; then
  OPT_BACKEND=1
fi

[[ $OPT_BACKEND -eq 1 ]] && run_backend
[[ $OPT_E2E -eq 1 ]] && run_e2e

log_info "Tudo pronto."
