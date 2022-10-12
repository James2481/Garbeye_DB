<?php

class DatabaseConfig {

    public $host;
    public $username;
    public $password;
    public $dbName;

    public function __construct() {
        $this->host = 'localhost';
        $this->username = 'bamavave';
        $this->password = 'Bamavave123';
        $this->dbName = 'garbage_location';
    }

}

?>