#!/bin/bash
# Backup WordPress files + DB en Hostinger vía SSH/SFTP (ejecutar en servidor si hay SSH; si no, usar cron/Panel)
# Variables
WP_PATH="${WP_PATH:-/home/USER/public_html}"
BACKUP_DIR="${BACKUP_DIR:-$WP_PATH/_backups}"
DB_NAME="${DB_NAME:-CHANGE_ME}"
DB_USER="${DB_USER:-CHANGE_ME}"
DB_PASS="${DB_PASS:-CHANGE_ME}"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Backup base de datos
if command -v mysqldump >/dev/null 2>&1; then
  mysqldump -u"$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_DIR/db_${DB_NAME}_${DATE}.sql" 2>/dev/null || true
fi

# Backup archivos (excluye cachés y backups previos)
cd "$WP_PATH" || exit 0
zip -r "$BACKUP_DIR/wp_files_${DATE}.zip" . -x "wp-content/cache/*" -x "_backups/*" >/dev/null 2>&1 || true

echo "Backup completado en $BACKUP_DIR"
