<?php
declare(strict_types=1);

$path = parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH) ?: '';
$ext = strtolower(pathinfo($path, PATHINFO_EXTENSION));

if ($ext === 'png') {
    $file = __DIR__ . '/og-image.png';
    $type = 'image/png';
} else {
    $file = __DIR__ . '/og-image.jpg';
    $type = 'image/jpeg';
}

if (!is_file($file)) {
    http_response_code(404);
    exit;
}

$size = filesize($file);
header('HTTP/1.1 200 OK');
header('Content-Type: ' . $type);
header('Accept-Ranges: none');
header('Content-Length: ' . $size);
header('Cache-Control: public, max-age=31536000, immutable');

if (($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'HEAD') {
    exit;
}

readfile($file);
