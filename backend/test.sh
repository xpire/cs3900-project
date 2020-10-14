set -e
set -x

# bash scripts/test.sh --cov-report=html "${@}"
pytest --cov=app --cov-report=term-missing app/tests "${@}"