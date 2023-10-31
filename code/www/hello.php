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
        echo "Please provide a name\n\n";
    }


    $filename = "No filename";
    $content = "No content";
    // convert input to lowercase
    if(isset($_GET['filename']) && isset($_GET['content']) ){
        $filename = $_GET['filename'] . ".txt";
        $content= $_GET['content'];

        // create file and populate it with content
        shell_exec("echo $content >> $filename");
        echo "$filename created";
    }
?>

<h1>Filename: <?php echo $filename;?> </h1>
<h1>File Content:</h1>
<p> <?php echo $content?> </p>

