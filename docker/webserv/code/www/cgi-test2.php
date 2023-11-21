<?php
    echo "Method: " . $_SERVER['REQUEST_METHOD'] . "\n";
    echo "Script Name: " . $_SERVER['SCRIPT_FILENAME'] . "\n";
    echo "Redirect Status: " . $_SERVER['REDIRECT_STATUS'] . "\n";

    if ($_SERVER['REQUEST_METHOD'] === 'GET') {
        echo  "GET Parameters: \n";
        var_dump($_GET);
    } elseif ($_SERVER['REQUEST_METHOD'] === 'POST') {
        echo "POST Parameters: \n";
        var_dump($_POST);
    } else {
        echo "Unknown Request Method.";
    }
?>



