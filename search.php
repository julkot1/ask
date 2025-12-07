<?php
echo "<h2> Search users (unsafe)</h2>";

$input = $_GET['user'] ?? '';

if ($input !== '') {

    $conn = new mysqli("localhost", "demo_user", "demo_pass", "demo_db");

    if ($conn->connect_error) {
        die("Błąd połączenia: " . $conn->connect_error);
    }
 

    $result  = $conn->query("
        SELECT id, username, email 
        FROM users 
        WHERE username = '$input'
    ");

    if ($result->num_rows > 0) {
        header("Location: /demo/user.php");
        exit();
    }

    $conn->close();
}

?>

<form>
    <input type="text" name="user" placeholder="username: ">
    <button type="submit">Szukaj</button>
</form>
