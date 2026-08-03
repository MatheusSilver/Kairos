#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"

ERRO_BG="\033[0;41m"
KAIROS="\033[0;30;42m"
BACKEND="\033[0;30;43m"
FRONTEND="\033[0;30;45m"
RESET="\033[0m"

OPT_BACKEND=0
OPT_FRONTEND=0
OPT_FIX=0

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
  echo "Uso: devbox run lint [--backend|--frontend|--all] [--fix]"
  echo ""
  echo "Sem argumentos, verifica backend e frontend."
  echo ""
  echo "  --backend    ruff, pylint e bandit"
  echo "  --frontend   biome"
  echo "  --all        Ambos (padrao)"
  echo "  --fix        Corrige o que for corrigivel automaticamente"
  echo ""
  echo "Exemplos:"
  echo "  devbox run lint"
  echo "  devbox run lint --backend"
  echo "  devbox run lint --fix"
  echo ""
}

run_backend() {
  cd "${BACKEND_DIR}"

  if [[ $OPT_FIX -eq 1 ]]; then
    log_backend "ruff check --fix"
    uv run ruff check --fix app tests
    log_backend "ruff format"
    uv run ruff format app tests
  else
    log_backend "ruff check"
    uv run ruff check app tests
    log_backend "ruff format --check"
    uv run ruff format --check app tests
  fi

  log_backend "pylint"
  uv run pylint app

  log_backend "bandit"
  uv run bandit -r app -ll -q

  log_backend "Backend sem pendencias."
}

run_frontend() {
  cd "${ROOT_DIR}"
  log_frontend "biome"
  if [[ $OPT_FIX -eq 1 ]]; then
    bun run lint
  else
    bun run --filter frontend lint:check
  fi
  log_frontend "Frontend sem pendencias."
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --backend)  OPT_BACKEND=1; shift ;;
    --frontend) OPT_FRONTEND=1; shift ;;
    --all)      OPT_BACKEND=1; OPT_FRONTEND=1; shift ;;
    --fix)      OPT_FIX=1; shift ;;
    -h|--help)  help; exit 0 ;;
    *)          log_error "Opcao desconhecida: $1"; help; exit 1 ;;
  esac
done

if [[ $OPT_BACKEND -eq 0 && $OPT_FRONTEND -eq 0 ]]; then
  OPT_BACKEND=1
  OPT_FRONTEND=1
fi

[[ $OPT_BACKEND -eq 1 ]] && run_backend
[[ $OPT_FRONTEND -eq 1 ]] && run_frontend

log_info "Lint concluido."
