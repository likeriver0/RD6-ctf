<!DOCTYPE html>
<html>
<head>
    <title>你离gakki只差一点点套路了</title>
</head>
<body>
<form action="a1d63bb3ed1f9df89b72375f1ed79e5d.php" method="post" enctype="multipart/form-data"> 
            <input type="file" name="filename">                  
            <input type="submit" name="submit" value="upload"> 
            </form>
</body>
</html>
<?php 
if(isset($_POST["submit"])){
            $name=explode(".", $_FILES["filename"]["name"]);
            $suffix=$name[count($name)-1];
            if($suffix!=="jpg"&&$suffix!=="png"&&$suffix!=="gif"&&$suffix!=="phps")
            {
                die('Hello hacker');
            }
            $file=@file_get_contents($_FILES["filename"]["tmp_name"]); 
            if(empty($file)) 
            { 
                die('do you upload a file?'); 
            } 
            else if($suffix==="phps")
            { 
                if((strpos($file,'<?')>-1)) 
                {
                    die('flagfl3g.php');
                } 
            }
            else
            {
                die('上传成功，但我要一个能执行的');
            } 
        }