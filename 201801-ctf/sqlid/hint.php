<?php  
if(isset($_GET['id'])) 
{
    $id=$_GET['id'];
    $con=mysqli_connect("localhost","rebirth","root_1234","sqlid");
    if (mysqli_connect_errno()) 
    {
        printf("Connect failed: %s\n", mysqli_connect_error());
        exit();
    }
    $id_pattern="/load|data|local|infile|extractvalue|sleep|floor|updatexml|benchmark|column|table|schema|database|like|reg|into|union|sub|select|insert|outfile|from/i";
    if(preg_match($id_pattern,$id)===1)
    {
        die("检测到攻击");
    }
    $sql = "SELECT * from hint,admin where hint.id = \"".$id."\"";
    $r = mysqli_query($con,$sql);
    if(!$r)
        die("sql语句炸了");
    $result = mysqli_fetch_array($r, MYSQLI_ASSOC);
    if($result === NULL){
        die("想啥呢，密码都不知道还想要gakki");
    }else{
        die("想啥呢，密码都不知道还想要gakki");
    }
}
?>