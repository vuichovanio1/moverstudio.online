<?php
declare(strict_types=1);

/**
 * Lead capture endpoint for moverstudio.online
 * POST application/x-www-form-urlencoded or application/json → mail() → JSON
 */

header('X-Content-Type-Options: nosniff');
header('Cache-Control: no-store');

if (($_SERVER['REQUEST_METHOD'] ?? '') === 'OPTIONS') {
    header('Allow: POST, OPTIONS');
    http_response_code(204);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    header('Content-Type: application/json; charset=utf-8');
    header('Allow: POST, OPTIONS');
    echo json_encode(['ok' => false, 'error' => 'method_not_allowed'], JSON_UNESCAPED_UNICODE);
    exit;
}

$ctype = $_SERVER['CONTENT_TYPE'] ?? '';
$data = [];
if (stripos($ctype, 'application/json') !== false) {
    $raw = file_get_contents('php://input') ?: '';
    $decoded = json_decode($raw, true);
    if (is_array($decoded)) {
        $data = $decoded;
    }
} else {
    $data = $_POST;
}

function field(array $data, string $key): string
{
    $v = $data[$key] ?? '';
    if (!is_string($v)) {
        return '';
    }
    return trim($v);
}

// Honeypot — bots fill this; humans never see it
$honeypot = field($data, 'company_url');
if ($honeypot !== '') {
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['ok' => true, 'deduped' => true], JSON_UNESCAPED_UNICODE);
    exit;
}

$name = field($data, 'name');
$phone = field($data, 'phone');
$body = field($data, 'body');
if ($body === '') {
    $body = field($data, 'message');
}
$subject = field($data, 'subject');
if ($subject === '') {
    $subject = 'Запитване от сайта';
}

$errors = [];
if ($name === '' || mb_strlen($name) > 120) {
    $errors[] = 'name';
}
if ($phone === '' || mb_strlen($phone) > 40) {
    $errors[] = 'phone';
}
if ($body === '' || mb_strlen($body) > 4000) {
    $errors[] = 'body';
}
if (mb_strlen($subject) > 160) {
    $errors[] = 'subject';
}

header('Content-Type: application/json; charset=utf-8');

if ($errors) {
    http_response_code(422);
    echo json_encode(['ok' => false, 'error' => 'validation', 'fields' => $errors], JSON_UNESCAPED_UNICODE);
    exit;
}

$ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$ua = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 240);
$page = field($data, 'page');
if ($page === '') {
    $page = $_SERVER['HTTP_REFERER'] ?? '';
}

$mailBody = "Ново запитване от moverstudio.online\n\n"
    . "Име/фирма: {$name}\n"
    . "Телефон: {$phone}\n"
    . "Тема: {$subject}\n"
    . "Страница: {$page}\n"
    . "IP: {$ip}\n"
    . "UA: {$ua}\n\n"
    . "Съобщение:\n{$body}\n";

$to = 'admin@moverstudio.online';
$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'From: MOVER Studio Lead <noreply@moverstudio.online>',
    'Reply-To: ' . $to,
    'X-Mailer: moverstudio-lead/1.0',
];

$sent = @mail($to, $encodedSubject, $mailBody, implode("\r\n", $headers));

if (!$sent) {
    http_response_code(502);
    echo json_encode(['ok' => false, 'error' => 'mail_failed'], JSON_UNESCAPED_UNICODE);
    exit;
}

echo json_encode(['ok' => true], JSON_UNESCAPED_UNICODE);
