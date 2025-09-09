# Scripts Panacea Icono — Hostinger + WordPress

## Rutas locales y remotas
- Local (este repo): /Users/kuchimac/Desktop/panacea-icono
- WordPress local opcional: /Users/kuchimac/Desktop/panacea-icono/public_html
- Remoto Hostinger (docroot): /home/u485132360/public_html

## Despliegue SFTP (GitHub Actions)
Variables (GitHub Secrets):
- HOSTINGER_HOST = fibonacci.boliviachic.com
- HOSTINGER_USER = u485132360
- HOSTINGER_PASSWORD = ********
- HOSTINGER_PATH = /home/u485132360/public_html
- HOSTINGER_PORT = 65002 (o 22)

Workflow: .github/workflows/wp_deploy.yml
Sincroniza: public/ y wp-content/* (plugins, themes, mu-plugins, uploads)

## Scripts locales
- scripts/wp_deploy_sftp.sh: despliegue incremental por SFTP (usa lftp)
- scripts/wp_backup.sh: backup de archivos y base de datos (ejecutar en servidor o cron)

## Preparación en Hostinger (SSH)
```
mkdir -p /home/u485132360/public_html/_backups
chmod 750 /home/u485132360/public_html/_backups
```

En wp-config.php:
```
define('PANACEA_DEPLOY_TOKEN', 'tu_token_secreto');
define('DISALLOW_FILE_EDIT', true);
```

## Cron Jobs (hPanel)
- Backup diario (03:00):
```
0 3 * * * bash /home/u485132360/public_html/scripts/wp_backup.sh
```
- Rotación (7 días):
```
find /home/u485132360/public_html/_backups -type f -mtime +7 -delete
```
- Limpieza caché (cada 6h, si WP-CLI):
```
0 */6 * * * wp cache flush --path=/home/u485132360/public_html
```

## Endpoints MU-plugin
- GET /wp-json/panacea/v1/hola
- POST /wp-json/panacea/v1/deploy  (Header: X-PANACEA-TOKEN)
- POST /wp-json/panacea/v1/upload  (Header: X-PANACEA-TOKEN, body base64)

## Recomendación sobre public_html en el repositorio
- No subas el core de WordPress al repositorio (pesado y no necesario).
- Mantén versionado únicamente wp-content/* y scripts.
- Si necesitas trabajar con una copia local, usa /public_html solo como staging local y despliega con el workflow.
