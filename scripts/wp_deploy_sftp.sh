#!/bin/bash
# Despliegue incremental de wp-content (temas/plugins/uploads) vía SFTP usando lftp
# Requiere: lftp instalado en runner o máquina local
set -e

if ! command -v lftp >/dev/null 2>&1; then
  echo "lftp no está instalado" >&2
  exit 1
fi

HOST="${HOSTINGER_HOST:?set HOSTINGER_HOST}"
USER="${HOSTINGER_USER:?set HOSTINGER_USER}"
PASS="${HOSTINGER_PASSWORD:?set HOSTINGER_PASSWORD}"
REMOTE_PATH="${HOSTINGER_PATH:-/public_html}"

# Rutas locales a sincronizar (evitar subir core de WP)
SYNC_DIRS=(
  "public/" # opcional si usas contenido estático
  "wp-content/plugins/"
  "wp-content/themes/"
  "wp-content/mu-plugins/"
  "wp-content/uploads/"
)

for DIR in "${SYNC_DIRS[@]}"; do
  if [ -d "$DIR" ]; then
    echo "Sincronizando $DIR -> $REMOTE_PATH/$DIR"
    lftp -u "$USER","$PASS" sftp://"$HOST" <<EOF2
set sftp:auto-confirm yes
mirror -R --only-newer --parallel=4 --verbose=1 --exclude-glob .git* --exclude-glob node_modules --exclude-glob *.map "$DIR" "$REMOTE_PATH/$DIR"
quit
EOF2
  fi
done

echo "Despliegue SFTP finalizado"
