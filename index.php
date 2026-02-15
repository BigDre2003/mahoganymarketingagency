<?php
    use PHPMailer\PHPMailer\PHPMailer;
    use PHPMailer\PHPMailer\Exception;
    use PHPMailer\PHPMailer\SMTP;

    include('vendor/autoload.php');
    include('PHPMailer.php');
    include("SMTP.php");
    include('Exception.php');



    if($_SERVER["REQUEST_METHOD"] == "POST") {
        $name = htmlspecialchars($_POST['name']);
        $email = htmlspecialchars($_POST['email']);
        $company = htmlspecialchars($_POST['company']);
        $phone = htmlspecialchars($_POST['phone']);
        $subject = htmlspecialchars($_POST['subject']);
        $message = htmlspecialchars($_POST['message']);

        $mail = new PHPMailer(true);

        $mail->isSMTP();
            $mail->Host = 'smtpout.secureserver.net';
            $mail->SMTPAuth = true;
            $mail->Username = 'mahogany@mahoganymarketingagency.com';
            $mail->Password = 'M@hoganyMarketingfocused2024';
            $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
            $mail->Port = 587;


            $mail->setFrom("mahogany@mahoganymarketingagency.com");
            $mail->addAddress('mahogany@mahoganymarketingagency.com');
            $mail->isHTML(true);
            $mail->Subject = $subject;
            $mail->Body = "Name: " . "$name" . "<br>" . "Email: " . "$email" . "<br>" . "Company: " . "$company" .  "<br>" . 
            "Phone: " . "$phone" .  "<br>"
            . "Message: " . "$message" .  "<br>";
            $mail->send();
            echo '<script type="text/javascript">
            window.onload = function () { alert("Your email was sent!!!"); }
            </script>';

            header("Location: http://localhost/hoogyPhp/index.html");
            exit;

    }

?>