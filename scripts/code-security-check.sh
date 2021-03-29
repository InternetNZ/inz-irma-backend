#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit

bandit -r ./inz_irma_backend
