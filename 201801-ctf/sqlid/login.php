<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>gakki 最美</title>
        <link rel="stylesheet" href="assets/css/fonts.css">
        <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
        <link rel="stylesheet" href="assets/font-awesome/css/font-awesome.min.css">
		<link rel="stylesheet" href="assets/css/form-elements.css">
        <link rel="stylesheet" href="assets/css/style.css">
        <link rel="shortcut icon" href="assets/ico/favicon.png">
        <link rel="apple-touch-icon-precomposed" sizes="144x144" href="assets/ico/apple-touch-icon-144-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="114x114" href="assets/ico/apple-touch-icon-114-precomposed.png">
        <link rel="apple-touch-icon-precomposed" sizes="72x72" href="assets/ico/apple-touch-icon-72-precomposed.png">
        <link rel="apple-touch-icon-precomposed" href="assets/ico/apple-touch-icon-57-precomposed.png">
        <script src="assets/js/jquery-1.11.1.min.js"></script>
        <script src="assets/bootstrap/js/bootstrap.min.js"></script>
        <script src="assets/js/jquery.backstretch.min.js"></script>
        <script src="assets/js/scripts.js"></script>
        <style type="text/css">
        #error{
            color: red;
        }
    </style>

    </head>

    <body>
        <div class="top-content">
        <div class="inner-bg">
        <div class="container">
        <div class="row">
        <div class="col-sm-8 col-sm-offset-2 text">
            <h1><strong>Welcome to a simple login</strong></h1>
        </div>
        </div>
        <div class="row">
            <div class="col-sm-6 col-sm-offset-3 form-box">
            <div class="form-top">
            <div class="form-top-left">
                <h3>purple purple purple!</h3>
            <p>Enter your username and password to login XD</p>
            </div>
            <div class="form-top-right">
            <i class="fa fa-key"></i>
            </div>
            </div>
            <div class="form-bottom">
			<form role="form" action="login.php" method="post" class="login-form">
			     <div class="form-group">
			     <input type="text" name="username" class="form-username form-control" id="username">
			     </div>
			     <div class="form-group">
			     <input type="password" name="password" class="form-password form-control" id="password">
			     </div>
			     <input name="submit" type="submit" value="submit"></input>
                 <a href="./hint.php?id=1"><strong class="text-muted pull-right">点我看gakki</strong></a>
            </form>
            </div>
            <p id="error">
<?php
    if(isset($_POST['submit'])){
        function error_die($msg){
            echo $msg;
            die();
        }
        $con=mysqli_connect("localhost","rebirth","root_1234","sqlid");
        if (mysqli_connect_errno()) 
        {
            printf("Connect failed: %s\n", mysqli_connect_error());
            exit();
        }
        if(isset($_POST['username'])===false||isset($_POST['password'])===false)
        {
            error_die("用户名和密码不能为空");
        }
        $username = $_POST['username'];
        $password = $_POST['password'];
        $pass_pattern="/^[0-9a-zA-Z]*$/";
        $user_pattern="/^[0-9a-zA-Z]*$/";
        if(preg_match($pass_pattern,$password)===0)
        {
            error_die("检测到攻击");
        }
        if(preg_match($user_pattern,$username)===0)
        {
            error_die("检测到攻击");
        }
        $password=substr(md5($password),5,20);//awedc123Z
        $sql = "SELECT * from admin where username = '".$username."' and password = '".$password."'";
        $r = mysqli_query($con,$sql);
        if(!$r)
            error_die("sql语句炸了");
        $result = mysqli_fetch_array($r, MYSQLI_ASSOC);
        if($result === NULL){
            error_die("用户名或密码错误");
        }else{
            header('Location:a1d63bb3ed1f9df89b72375f1ed79e5d.php');
        }
    }
?>
</p>
        </div>
        </div>
        </div>
        </div>   
        </div>
    </body>

</html>