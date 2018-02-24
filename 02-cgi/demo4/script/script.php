#!/usr/bin/php-cgi

<?php header('Content-Type: text/html;charset=utf-8') ?>
<!Doctype html>
<html>
    <head>
        <title>CGI Apache httpd demo PHP</title>
    </head>
    <body>
        <h1>CGI Apache httpd demo PHP</h1>
        <p>Welcome <?= get_current_user() ?>!</p>
    </body>
</html>
