<?php

require 'dbHandler.php';
$db = new DatabaseHandler();

$response = array(
    'state'=>false,
    'status'=>false
);

if (isset($_POST['timestamp']) && isset($_POST['location']) && isset($_POST['garbage_long']) && isset($_POST['garbage_lat'])) {
    if ($db->dbConnect()) {
        if ($db->appendLocation($_POST['timestamp'], $_POST['location'], $_POST['garbage_long'], $_POST['garbage_lat'])) {
            $response['state'] = true;
            $response['status'] = true;
        } else {
            $response['state'] = true;
            $response['status'] = false;
        };
    } else {
        $response['state'] = true;
        $response['status'] = false;
    };
} else  {
    $response['state'] = false;
    $response['status'] = false;
};

echo json_encode($response);

?>