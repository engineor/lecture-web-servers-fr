#!/usr/bin/php-cgi

<?php 
    header('Content-Type: text/html;charset=utf-8');
    $currentTime = new DateTimeImmutable;
?>
<!Doctype html>
<html>
    <head>
        <title>CGI Apache httpd demo PHP</title>
    </head>
    <body>
        <h1>CGI Apache httpd demo PHP</h1>
        <p>We are the <?= $currentTime->format("d, M Y h:i:s A") ?></p>
    </body>
</html>
