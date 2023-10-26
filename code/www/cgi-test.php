<?php

// Check if the REQUEST_METHOD is GET
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    echo "Request Method: GET\n";
    echo "Script Name: " . $_SERVER['SCRIPT_NAME'] . "\n";
    echo "Redirect Status: " . $_SERVER['REDIRECT_STATUS'] . "\n";

    // Get the QUERY_STRING and parse it
    parse_str($_SERVER['QUERY_STRING'], $params);
    
    // Print each parameter and its value
    echo "GET parameters:\n";
    foreach ($params as $key => $value) {
        echo "$key: $value\n";
    }
} else {
    echo "This script should be invoked with a GET request.";
}

?>
