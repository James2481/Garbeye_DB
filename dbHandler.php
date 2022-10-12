<?php

require_once 'DatabaseConfig.php';

class DatabaseHandler {

    public $connection;
    private $host;
    private $username;
    private $password;
    private $dbName;
    private $table_name;
    private $db;
    
    public function __construct() {
        $dbConfig = new DatabaseConfig();
        $this->host = $dbConfig->host;
        $this->username = $dbConfig->username;
        $this->password = $dbConfig->password;
        $this->dbName = $dbConfig->dbName;
        $this->table_name = "garbage_table";
    }

    public function dbConnect() {
        $this->connection = mysqli_connect($this->host, $this->username, $this->password, $this->dbName);
        return $this->connection;
    }

    private function prepareData($data) {
        return mysqli_real_escape_string($this->connection, stripslashes(htmlspecialchars($data)));
    }

    public function appendLocation($timestamp, $location, $garbage_long, $garbage_lat) {
        $timestamp = $this->prepareData($timestamp);
        $location = $this->prepareData($location);
        $garbage_long = $this->prepareData($garbage_long);
        $garbage_lat = $this->prepareData($garbage_lat);

        $query = "INSERT INTO " . $this->table_name . "(timestamp, location, garbage_long, garbage_lat) VALUES ('" . $timestamp . "', '" . $location . "', '" . $garbage_long . "', '" . $garbage_lat . "');";

        if(mysqli_query($this->connection, $query)) {
            return true;
        } else return false;
    }
}

?>