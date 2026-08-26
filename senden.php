<?php
declare(strict_types=1);

ini_set('display_errors', '0');
error_reporting(0);

header('Content-Type: application/json; charset=utf-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'Method not allowed']);
    exit;
}

// Honeypot field — must remain empty
if (!empty($_POST['website'])) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'Spam detected']);
    exit;
}

$name    = isset($_POST['name'])    ? trim($_POST['name'])    : '';
$email   = isset($_POST['email'])   ? trim($_POST['email'])   : '';
$tel     = isset($_POST['tel'])     ? trim($_POST['tel'])     : '';
$message = isset($_POST['message']) ? trim($_POST['message']) : '';
$consent = isset($_POST['consent']);

$errors = [];
if ($name === '') {
    $errors[] = 'Name ist erforderlich.';
}
if ($email === '' || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'E-Mail ist ungültig.';
}
if ($message === '') {
    $errors[] = 'Nachricht ist erforderlich.';
}
if (!$consent) {
    $errors[] = 'Datenschutzeinwilligung ist erforderlich.';
}

if ($errors) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => implode(' ', $errors)]);
    exit;
}

$to      = 'giuliano.russo@primestructures.de';
$subject = 'Anfrage über Website von ' . $name;

$bodyText  = "Name: $name\n";
$bodyText .= "E-Mail: $email\n";
if ($tel !== '') {
    $bodyText .= "Telefon: $tel\n";
}
$bodyText .= "\nNachricht:\n$message\n";

$allowedExts = ['pdf', 'jpg', 'jpeg', 'png'];
$allowedMimes = ['application/pdf', 'image/jpeg', 'image/png'];
$maxPerFile  = 10 * 1024 * 1024; // 10 MB
$maxTotal    = 25 * 1024 * 1024; // 25 MB

$attachments = [];
$totalSize   = 0;

function processUploadedFile($error, $tmpName, $origName, $size, &$errors, &$attachments, &$totalSize)
{
    global $maxPerFile, $maxTotal, $allowedExts, $allowedMimes;

    if ($error === UPLOAD_ERR_NO_FILE) {
        return;
    }
    if ($error !== UPLOAD_ERR_OK) {
        $errors[] = 'Fehler beim Hochladen von ' . basename($origName) . '.';
        return;
    }

    $size = (int) $size;
    if ($size > $maxPerFile) {
        $errors[] = basename($origName) . ' ist zu groß (max. 10 MB).';
        return;
    }
    $totalSize += $size;
    if ($totalSize > $maxTotal) {
        $errors[] = 'Die Gesamtgröße der Anhänge überschreitet 25 MB.';
        return;
    }

    $ext = strtolower(pathinfo($origName, PATHINFO_EXTENSION));
    if (!in_array($ext, $allowedExts, true)) {
        $errors[] = basename($origName) . ' hat ein unzulässiges Dateiformat.';
        return;
    }

    $finfo = new finfo(FILEINFO_MIME_TYPE);
    $mime  = $finfo->file($tmpName);
    if (!in_array($mime, $allowedMimes, true)) {
        $errors[] = basename($origName) . ' hat einen unzulässigen Dateityp.';
        return;
    }

    $attachments[] = [
        'path' => $tmpName,
        'name' => $origName,
        'mime' => $mime,
    ];
}

if (!empty($_FILES['files'])) {
    if (is_array($_FILES['files']['name'])) {
        $fileCount = count($_FILES['files']['name']);
        for ($i = 0; $i < $fileCount; $i++) {
            processUploadedFile(
                $_FILES['files']['error'][$i],
                $_FILES['files']['tmp_name'][$i],
                $_FILES['files']['name'][$i],
                $_FILES['files']['size'][$i],
                $errors,
                $attachments,
                $totalSize
            );
        }
    } else {
        processUploadedFile(
            $_FILES['files']['error'],
            $_FILES['files']['tmp_name'],
            $_FILES['files']['name'],
            $_FILES['files']['size'],
            $errors,
            $attachments,
            $totalSize
        );
    }
}

if ($errors) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => implode(' ', $errors)]);
    exit;
}

$boundary = '----PrimeStructuresBoundary' . md5((string) time());
$headers  = "From: Prime Structures <noreply@primestructures.de>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: multipart/mixed; boundary=\"$boundary\"\r\n";

$mailBody  = "--$boundary\r\n";
$mailBody .= "Content-Type: text/plain; charset=UTF-8\r\n";
$mailBody .= "Content-Transfer-Encoding: quoted-printable\r\n\r\n";
$mailBody .= quoted_printable_encode($bodyText) . "\r\n";

foreach ($attachments as $att) {
    $content = file_get_contents($att['path']);
    if ($content === false) {
        continue;
    }
    $encoded  = chunk_split(base64_encode($content));
    $filename = sanitizeFilename($att['name']);

    $mailBody .= "--$boundary\r\n";
    $mailBody .= "Content-Type: " . $att['mime'] . "; name=\"$filename\"\r\n";
    $mailBody .= "Content-Disposition: attachment; filename=\"$filename\"\r\n";
    $mailBody .= "Content-Transfer-Encoding: base64\r\n\r\n";
    $mailBody .= $encoded . "\r\n";
}

$mailBody .= "--$boundary--\r\n";

$ok = mail($to, $subject, $mailBody, $headers);

if ($ok) {
    echo json_encode(['ok' => true]);
} else {
    http_response_code(500);
    echo json_encode(['ok' => false, 'error' => 'Die E-Mail konnte nicht versendet werden.']);
}

function sanitizeFilename(string $name): string
{
    $base = basename($name);
    $base = preg_replace('/[^a-zA-Z0-9._-]/', '_', $base);
    $base = preg_replace('/_{2,}/', '_', $base);
    return $base === '' ? 'anhang' : $base;
}
