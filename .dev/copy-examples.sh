#!/usr/bin/env bash

set -euo pipefail

usage() {
  cat <<EOF
Usage: ${BASH_SOURCE[0]} [OPTIONS]

Copies example dotenv files if they don't exist.

Options:
  --dry-run               Don't actually copy, just print what would be copied [\$DEV_DRY_RUN]
  --verbose               Verbose output
  -h, --help              Show this help message and exit

Environment Variables:
  \$DEV_DRY_RUN           Set to 1 for dry-run mode
EOF
}

# TODO: not implemented
# This script should:
# 1. Check for example dotenv files (e.g., .env.example, .envrc.example)
# 2. Copy them to their non-example versions (.env, .envrc) if they don't exist
# 3. Support --dry-run to show what would be copied
# 4. Support --verbose for detailed output

echo "ERROR: TODO: not implemented" >&2
usage >&2
exit 1
