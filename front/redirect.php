<?php
// 데이터베이스 연결 설정
$db = new PDO('mysql:host=event-price.com;dbname=links;port=3306;charset=utf8', 'dbuser', 'asdfqwerty@1234*');

// GET 요청으로부터 짧은 URL key를 얻습니다.
$short = $_GET['short'];

// 데이터베이스에서 짧은 URL key에 해당하는 긴 URL을 검색합니다.
$stmt = $db->prepare('SELECT name FROM links WHERE url = :short');
$stmt->execute(['short' => $short]);

// 데이터베이스에서 긴 URL을 가져옵니다.
$row = $stmt->fetch(PDO::FETCH_ASSOC);
$long_url = $row['name'];

echo $short;

// 긴 URL로 301 리다이렉트합니다.
header("HTTP/1.1 301 Moved Permanently"); 
header("Location: $long_url");
?>