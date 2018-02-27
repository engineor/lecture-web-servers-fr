<?php

session_start();

if (!isset($_SESSION['nb'])) {
    $_SESSION['nb'] = 0;
}

$_SESSION['nb']++;

var_dump($_SESSION['nb']);
