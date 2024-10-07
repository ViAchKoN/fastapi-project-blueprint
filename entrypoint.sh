#! /usr/bin/env bash

alembic upgrade head

exec "$@"
