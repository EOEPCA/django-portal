#!/usr/bin/env bash

ORIG_DIR="$(pwd)"
cd "$(dirname "$0")"
BIN_DIR="$(pwd)"

trap "cd '${ORIG_DIR}'" EXIT

function setup_venv() {
  if [ ! -d venv ]
  then
    if python3 -m venv --help >/dev/null 2>&1
    then
      echo "INFO: creating venv..."
      python3 -m venv venv
    else
      echo "ERROR: python virtualenv package is required. Please install (e.g. apt install python3-venv)"
      return 1
    fi
    echo "INFO: activate venv and update..."
    source venv/bin/activate
    python -m pip install -U pip
    pip install -U wheel
  else
    echo "INFO: activate venv..."
    source venv/bin/activate
  fi
}


function install_requirements() {
  pip install -r ./requirements.txt
}


function main() {
  setup_venv && install_requirements && python ./registerclient.py $1 $2
  STATUS=$?
  hash deactivate 2>/dev/null && deactivate
  return $STATUS
}

main "$@"

