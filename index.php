<?php
echo "<h2> Search users (very unsafe)</h2>";
$input = $_GET['user'] ?? '';
if ($input !== '') {
    echo "<p>User given: <b>$input</b></p>";
    $conn = new mysqli("localhost", "demo_user", "demo_pass", "demo_db");
    $result  = $conn->query("
        SELECT id, username, email 
        FROM users 
        WHERE username = '$input'
    ");
    echo "<h3>Results:</h3>";
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            echo "<p>
                   ID: {$row['id']}<br>
                   User: {$row['username']}<br>
                   Email: {$row['email']}
                  </p><hr>";
        }
    } else {
        echo "<p>Non Users</p>";
    }
    $conn->close();
}
?>
<form>
    <input type="text" name="user" placeholder="username: ">
    <button type="submit">Szukaj</button>
</form>
