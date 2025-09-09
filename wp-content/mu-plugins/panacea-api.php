<?php
/**
 * Plugin Name: Panacea API (MU)
 * Description: Endpoints REST básicos para integración Panacea (deploy, upload, hola) como MU-Plugin.
 * Author: Panacea Icono S.A.
 */

add_action('rest_api_init', function () {
    register_rest_route('panacea/v1', '/hola', [
        'methods'  => 'GET',
        'callback' => function () { return ['mensaje' => '¡Hola desde Panacea API!']; },
        'permission_callback' => '__return_true',
    ]);

    register_rest_route('panacea/v1', '/deploy', [
        'methods'  => 'POST',
        'callback' => 'panacea_deploy_callback',
        'permission_callback' => '__return_true',
    ]);

    register_rest_route('panacea/v1', '/upload', [
        'methods'  => 'POST',
        'callback' => 'panacea_upload_callback',
        'permission_callback' => '__return_true',
    ]);
});

function panacea_check_token($req) {
    $token = $req->get_header('X-PANACEA-TOKEN');
    $expected = defined('PANACEA_DEPLOY_TOKEN') ? PANACEA_DEPLOY_TOKEN : 'CHANGE_ME';
    return ($token && hash_equals($expected, $token));
}

function panacea_deploy_callback(\WP_REST_Request $req) {
    if (!panacea_check_token($req)) {
        return new \WP_Error('forbidden', 'Token inválido', ['status' => 403]);
    }
    $action = sanitize_text_field($req->get_param('action') ?: 'noop');
    switch ($action) {
        case 'clear_cache':
            if (function_exists('wp_cache_flush')) { wp_cache_flush(); }
            break;
        case 'sync_content':
            // Placeholder de sync (S3, Git, etc.)
            break;
        default:
            // no-op
    }
    return ['status' => 'ok', 'action' => $action, 'ts' => current_time('mysql')];
}

function panacea_upload_callback(\WP_REST_Request $req) {
    if (!panacea_check_token($req)) {
        return new \WP_Error('forbidden', 'Token inválido', ['status' => 403]);
    }
    $filename = sanitize_file_name($req->get_param('filename') ?: ('file_'.time().'.bin'));
    $data_b64 = $req->get_param('data_base64');
    if (!$data_b64) {
        return new \WP_Error('bad_request', 'Falta data_base64', ['status' => 400]);
    }
    $data = base64_decode($data_b64);
    if ($data === false) {
        return new \WP_Error('bad_request', 'Base64 inválido', ['status' => 400]);
    }
    $upload_dir = wp_upload_dir();
    if (!empty($upload_dir['error'])) {
        return new \WP_Error('server_error', $upload_dir['error'], ['status' => 500]);
    }
    $path = trailingslashit($upload_dir['path']).$filename;
    if (file_put_contents($path, $data) === false) {
        return new \WP_Error('server_error', 'No se pudo guardar el archivo', ['status' => 500]);
    }
    $filetype = wp_check_filetype(basename($path), null);
    $attachment = [
        'guid'           => $upload_dir['url'].'/'.basename($path),
        'post_mime_type' => $filetype['type'] ?: 'application/octet-stream',
        'post_title'     => sanitize_text_field(pathinfo($filename, PATHINFO_FILENAME)),
        'post_content'   => '',
        'post_status'    => 'inherit'
    ];
    $attach_id = wp_insert_attachment($attachment, $path);
    require_once ABSPATH.'wp-admin/includes/image.php';
    $attach_data = wp_generate_attachment_metadata($attach_id, $path);
    wp_update_attachment_metadata($attach_id, $attach_data);
    return ['status' => 'ok', 'attachment_id' => $attach_id, 'url' => wp_get_attachment_url($attach_id)];
}

// Cron diario ejemplo
register_activation_hook(__FILE__, function () {
    if (!wp_next_scheduled('panacea_daily_task')) {
        wp_schedule_event(time() + 3600, 'daily', 'panacea_daily_task');
    }
});
register_deactivation_hook(__FILE__, function () {
    wp_clear_scheduled_hook('panacea_daily_task');
});
add_action('panacea_daily_task', function () {
    // Placeholder: tareas diarias (limpieza, verificación, etc.)
});

/**
 * Personalización de textos y ajustes básicos para Panacea Icono S.A.
 * - Tagline, zona horaria, formatos, primer día de semana
 * - Pie del admin, pantalla de login, remitente de emails
 */
add_action('init', function () {
    if (!get_option('panacea_setup_done')) {
        // Nombre del sitio y tagline
        if (get_option('blogname') !== 'Panacea Icono S.A.') {
            update_option('blogname', 'Panacea Icono S.A.');
        }
        if (get_option('blogdescription') !== 'Medicina Estética · Cirugía Plástica · IA · Web3') {
            update_option('blogdescription', 'Medicina Estética · Cirugía Plástica · IA · Web3');
        }

        // Zona horaria y formatos
        if (get_option('timezone_string') !== 'America/La_Paz') {
            update_option('timezone_string', 'America/La_Paz');
        }
        if (get_option('date_format') !== 'd/m/Y') {
            update_option('date_format', 'd/m/Y');
        }
        if (get_option('time_format') !== 'H:i') {
            update_option('time_format', 'H:i');
        }
        if ((int) get_option('start_of_week') !== 1) {
            update_option('start_of_week', 1);
        }

        update_option('panacea_setup_done', 1, true);
    }
});

// Pie del administrador
add_filter('admin_footer_text', function () {
    return 'Panacea Icono S.A. — Ecosistema Médico (Santa Cruz de la Sierra, Bolivia) · ☎ +591 69674560 · ✉ repositorios.panacea@gmail.com · 🌐 panacea-icono.org';
});

// Pantalla de login
add_filter('login_headertext', function () { return 'Panacea Icono S.A.'; });
add_filter('login_headerurl', function () { return home_url('/'); });
add_action('login_message', function () {
    echo '<p style="text-align:center;margin:8px 0;color:#226;">🏥 Panacea Icono S.A. — Medicina Estética · Cirugía Plástica · IA · Web3</p>';
});

// Remitente de emails
add_filter('wp_mail_from', function ($email) {
    $domain = isset($_SERVER['SERVER_NAME']) ? $_SERVER['SERVER_NAME'] : 'panacea-icono.org';
    $default = 'wordpress@' . $domain;
    if ($email && $email !== $default) { return $email; }
    return 'no-reply@panacea-icono.org';
});
add_filter('wp_mail_from_name', function () { return 'Panacea Icono S.A.'; });
