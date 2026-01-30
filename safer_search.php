<?php
echo "<h2> Search users (safer)</h2>";

$input = $_GET['user'] ?? '';

if ($input !== '') {

    $conn = new mysqli("localhost", "demo_user", "demo_pass", "demo_db");
    $statement = $conn->prepare("SELECT id, username, email FROM users WHERE username = ?");
    $statement->bind_param("s", $input);
    $statement->execute();
    $result = $statement->get_result();
    if ($result->num_rows > 0) {
        header("Location: /demo/user.php");
        $conn->close();
        exit();
    }
    $conn->close();
}
?>
<form>
    <input type="text" name="user" placeholder="username: ">
    <button type="submit">Szukaj</button>
</form>
