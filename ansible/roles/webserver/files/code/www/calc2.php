// This is functionally the same as calc.php but with GET instead of POST
<?php
// Set a custom error handler
set_error_handler(function($severity, $message, $file, $line) {
    throw new ErrorException($message, 0, $severity, $file, $line);
});

register_shutdown_function(function(){
    $error = error_get_last();
    if ($error !== NULL) {
        echo '<h1>500 Error: Internal Server Error</h1>';
    }
});

$result = null;
$visitor_name = null;

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (isset($_GET['visitor_name'], $_GET['number1'], $_GET['operation'], $_GET['number2'])) {
        $visitor_name = $_GET['visitor_name'];
        $number1 = $_GET['number1'];
        $operation = $_GET['operation'];
        $number2 = $_GET['number2'];

        // calc string
        $calculation = $number1 . ' ' . $operation . ' ' . $number2;
        // Handle eval in a try-catch block
        try {
            eval("\$result = $calculation;");
        } catch (Throwable $e) { // Catch any errors or exceptions
            echo '<h1>500 Error: Internal Server Error</h1>';
            exit; // Stop script execution after an error
        }
    } else {
        echo '<h1>500 Error: Invalid Input</h1>';
        exit; // Stop script execution if input is invalid
    }
} else {
    echo '<h1>500 Error: Please use the form to submit a calculation.</h1>';
    exit; // Stop script execution if the method is not GET
}
?>

<h1>Welcome <?php echo $visitor_name; ?></h1>
<h2>Thanks for calculating with us! Your results can be found below. Please come again!</h2>
<p>Result: <?php echo $result; ?></p>
