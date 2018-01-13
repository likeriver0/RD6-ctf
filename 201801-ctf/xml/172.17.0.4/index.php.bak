<?php
	error_reporting(0);
	$file=$_GET['file'];
	if(strstr($file,"../")||stristr($file, "tp")||stristr($file,"input")||stristr($file,"data"))
	{
		echo "Oh no!";
		exit();
	}
	include($file); 
?>