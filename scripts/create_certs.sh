#!/bin/bash

set -euo pipefail

if (( $EUID != 0 ))
then
    echo >&2 'Expects to run with sudo.'
    exit 1
fi

if ! hash mkcert 2>/dev/null
then
    echo >&2 'mkcert: command not found'
    echo >&2 'You need to install mkcert locally.'
    echo >&2 'Try brew install mkcert.'
    exit 1
fi
MKCERT_DIR=$(mkcert -CAROOT)

if [[ -z "$MKCERT_DIR" || ! -r "$MKCERT_DIR/rootCA.pem" ]]
then
    mkcert -install
fi

mkcert \
    -cert-file nginx/local.crt \
    -key-file nginx/local.key \
    localhost 10.0.2.2 "$(hostname).local"

chown $SUDO_USER nginx/local.crt nginx/local.key
