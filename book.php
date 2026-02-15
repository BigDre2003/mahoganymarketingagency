<?php
    use PHPMailer\PHPMailer\PHPMailer;
    use PHPMailer\PHPMailer\Exception;
    use PHPMailer\PHPMailer\SMTP;

    include('PHPMailer.php');
    include("SMTP.php");
    include('Exception.php');

    if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $name = htmlspecialchars($_POST['name']);
    $email = htmlspecialchars($_POST['email']);
    $company = htmlspecialchars($_POST['company']);
    $phone = htmlspecialchars($_POST['phone']);
    $services = $_POST['services'] ?? [];
    $message = htmlspecialchars($_POST['message']);

    $cleanServices = array_map('htmlspecialchars', $services);
    $servicesList = implode(", ", $cleanServices);

    try {
        $mail = new PHPMailer(true);
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;
        $mail->Username = 'deandrearcher2003@gmail.com';
        $mail->Password = 'mqkd jyof vxtu pdzc';
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;
        $mail->Port = 465;

        $mail->setFrom('deandrearcher2003@gmail.com', 'Mahogany Marketing Agency');
        $mail->addAddress($email);

        $mail->isHTML(true);
        $mail->Subject = "New service request from $name";
        $mail->Body = "
            <strong>Name:</strong> $name <br>
            <strong>Email:</strong> $email <br>
            <strong>Company:</strong> $company <br>
            <strong>Phone:</strong> $phone <br>
            <strong>Services:</strong> $servicesList <br>
            <strong>Message:</strong> $message
        ";

        $mail->send();

        // ✅ Redirect with success flag
        header("Location: http://localhost/hoogyPhp/book.html?status=success");
        exit;

    } catch (Exception $e) {
        header("Location: http://localhost/hoogyPhp/book.html?status=success");
        exit;
    }
}



    // if($_SERVER["REQUEST_METHOD"] == "POST") {
    //     $name = htmlspecialchars($_POST['name']);
    //     $email = htmlspecialchars($_POST['email']);
    //     $company = htmlspecialchars($_POST['company']);
    //     $phone = htmlspecialchars($_POST['phone']);
    //     $services = $_POST['services'];
    //     $message = htmlspecialchars($_POST['message']);

    //     $cleanServices = array_map('htmlspecialchars', $services);

    //     // Convert array to string (comma-separated)
    //     $servicesList = implode(", ", $cleanServices);

        

        
    //     $mail = new PHPMailer(true);
    //     $mail->isSMTP();
    //         $mail->Host = 'smtp.gmail.com';
    //         $mail->SMTPAuth = true;
    //         $mail->Username = 'deandrearcher2003@gmail.com';
    //         $mail->Password = 'mqkd jyof vxtu pdzc';
    //         $mail->SMTPSecure = 'ssl';
    //         $mail->Port = 465;
    //         $mail->setFrom('deandrearcher2003@gmail.com');
    //         $mail->addAddress($email);
    //         $mail->isHTML(true);
    //         $mail->Subject = "New service request from $name";
    //         $mail->Body = "Name: " . "$name" . "<br>" . "Email: " . "$email" . "<br>" . "Company: " . "$company" .  "<br>" . 
    //         "Phone: " . "$phone" .  "<br>" . "Services: " . "$servicesList" .  "<br>" . "Message: " . "$message" .  "<br>";
    //         $mail->send();
    //         echo '<script type="text/javascript">
    //         window.onload = function () { alert("Your email was sent!!!"); }
    //         </script>';
    //         header("Location: http://localhost/hoogyPhp/index.html");
    //         exit;
       

?>