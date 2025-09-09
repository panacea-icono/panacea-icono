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
