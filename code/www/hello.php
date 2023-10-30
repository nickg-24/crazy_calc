<?php
    if(isset($_GET['name'])){
        $name = $_GET['name'];
    
        echo "GET Hello, $name";
    }
    elseif(isset($_POST['name'])){
        $name = $_POST['name'];
    
        echo "POST Hello, $name";
    } 
    else{
        echo "Please provide a name";
    }
?>