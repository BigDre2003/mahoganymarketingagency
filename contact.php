<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Load environment variables
$envPath = __DIR__ . '/.env';
if (!is_readable($envPath)) { exit('ENV NOT READABLE'); }
$env = parse_ini_file($envPath, false, INI_SCANNER_RAW);
if ($env === false) { exit('ENV PARSE FAILED'); }

// Only allow POST requests
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    die('<p>Invalid request.</p>');
}

// Collect form data safely
$name     = trim(htmlspecialchars($_POST['name'] ?? 'No Name Provided'));
$email    = trim(htmlspecialchars($_POST['email'] ?? ''));
$company  = trim(htmlspecialchars($_POST['company'] ?? 'N/A'));
$phone    = trim(htmlspecialchars($_POST['phone'] ?? 'N/A'));
$subject = trim(htmlspecialchars($_POST['subject'] ?? 'N/A'));
$message  = trim(htmlspecialchars($_POST['message'] ?? 'No message'));


// Ensure Reply-To is valid, otherwise fallback to domain email
$replyTo = $env['MAIL_FROM'];

// Build email
$to      = $env['MAIL_FROM'];
$subject = $subject;
$body = "
<strong>Name:</strong> $name <br>
<strong>Email:</strong> $email <br>
<strong>Company:</strong> $company <br>
<strong>Phone:</strong> $phone <br>
<strong>Message:</strong> $message
";

// Headers
$headers = "From: {$env['MAIL_FROM_NAME']} <{$env['MAIL_FROM']}>\r\n";
$headers .= "Reply-To: $replyTo\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/html; charset=UTF-8\r\n";

// Function to send mail with one retry
function sendMailWithRetry($to, $subject, $body, $headers, $retries = 1) {
    for ($i = 0; $i <= $retries; $i++) {
        if(mail($to, $subject, $body, $headers)) {
            return true;
        }
        sleep(2);
    }
    return false;
}

// Send the email
$sent = sendMailWithRetry($to, $subject, $body, $headers, 1);

// Display message directly
if ($sent) {
    header("Location: /contact?status=success");
    exit;
} else {
    header("Location: /contact?status=error");
    exit;
}
?>