<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (isset($_POST['visitor_name'], $_POST['number1'], $_POST['operation'], $_POST['number2'])) {
        $visitor_name = $_POST['visitor_name'];
        $number1 = $_POST['number1'];
        $operation = $_POST['operation'];
        $number2 = $_POST['number2'];

        // calc string
        $calculation = $number1 . ' ' . $operation . ' ' . $number2;
        eval("\$result = $calculation;");

    } else {
        echo "Invalid input.";
    }
} else {
    echo "Please use the form to submit a calculation.";
}
?>

<h1>Welcome <?php echo $visitor_name;?> </h1>
<h2>Thanks for calculating with us! Your results can be found below. Please come again!</h2>
<p>Result: <?php echo $result?> </p>


