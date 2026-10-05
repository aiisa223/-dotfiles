#!/usr/bin/env bash
set -u

polybar-msg cmd quit >/dev/null 2>&1 || true
pkill -x polybar >/dev/null 2>&1 || true

for _ in $(seq 1 50); do
    pgrep -x polybar >/dev/null || break
    sleep 0.05
done

exec polybar \
    -q \
    -c "$HOME/.config/polybar/config.ini" \
    main
