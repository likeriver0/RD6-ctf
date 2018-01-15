# HexIt Write Up

giglf

---

打开发现这东西没见过啊

格式怎么这么有趣

不过看前面的内容感觉像地址

然后发现010Editor关联了这个后缀，`.hex` 可以直接打开，然后google也能找到这种格式的说明

直接打开后就正常多了，不过提示checksum不对，但在最底下能看到这样的字样

`Success Pin Value: PurpleCTF2018 Arduino Play Ground Pin Value:`

Arduino，然后查相关的东西，直接扔进ida打开时乱的，但后来从arduino的社区看到说用的是AVR指令

手动改了ida使用的处理器就正常识别出来了

然后AVR看着不懂，就上网找手册

ida也没识别出什么特殊的函数，就一个`RESET` ，不过联想到单片机也没说什么入口函数，但正常都是有个RESET的操作，那么就可以从那开始跟进

因为指令集的原因，这个没法用F5，只能跟着汇编走

google了一个AVR指令的手册

http://www.microchip.com/webdoc/avrassembler/avrassembler.wb_instruction_list.html

同时我还想能不能找到类似的WP做参考，然后就还真被我搜到了Flare-on2017的Wp

https://www.fireeye.com/content/dam/fireeye-www/global/en/blog/threat-research/Flare-On%202017/Challenge9.pdf

http://vulnerablespace.blogspot.com/2017/11/ctf-writeup-flare-on-2017-09.html

看了一遍他的思路，然后AVR中一些寄存器使用，然后自己在HexIt中跟了一段

跟到`sub_536` 后，突然发现这段代码结构怎么跟上面WP的那么像

仔细看下简直就是一毛一样2333333

最后也就这段数据不一样

```assembly
ldi     r25, 0xCD
std     Y+1, r25
std     Y+3, r25
ldi     r25, 0xC9
std     Y+2, r25
ldi     r25, 0xD0
std     Y+4, r25
ldi     r25, 0xD9
std     Y+9, r25
ldi     r25, 0xC8
std     Y+7, r25
ldi     r25, 0xD5
std     Y+5, r25
ldi     r18, 0xDD
std     Y+6, r18
std     Y+0x10, r18
std     Y+0xC, r25
ldi     r25, 0xF4
std     Y+8, r25
ldi     r25, 0xE1
std     Y+0xA, r25
ldi     r25, 0x8B
std     Y+0xB, r25
ldi     r25, 0xE4
std     Y+0xD, r25
ldi     r25, 0xEF
std     Y+0xE, r25
ldi     r25, 0xEA
std     Y+0xF, r25
ldi     r25, 0xDF
std     Y+0x11, r25
ldi     r25, 0xF3
std     Y+0x12, r25
ldi     r25, 0xDF
std     Y+0x13, r25
ldi     r25, 0xE8
std     Y+0x14, r25
ldi     r25, 0xEC
std     Y+0x15, r25
ldi     r25, 0xE5
std     Y+0x16, r25
ldi     r25, 0xDA
std     Y+0x17, r25
ldi     r26, 0x6C ; 'l'
ldi     r27, 5
ldi     r18, 0
```

修改一下Wp里的代码就跑出来了

```python
#http://vulnerablespace.blogspot.com/2017/11/ctf-writeup-flare-on-2017-09.html
#http://www.microchip.com/webdoc/avrassembler/avrassembler.wb_instruction_list.html
#https://www.fireeye.com/content/dam/fireeye-www/global/en/blog/threat-research/Flare-On%202017/Challenge9.pdf
encrypted = [0]*23

encrypted[0] = encrypted[2] = 0xcd
encrypted[1] = 0xc9
encrypted[3] = 0xd0
encrypted[8] = 0xd9
encrypted[6] = 0xc8
encrypted[4] = encrypted[0xB] = 0xd5
encrypted[5] = encrypted[0xF] = 0xdd
encrypted[7] = 0xF4
encrypted[9] = 0xe1
encrypted[0xA] = 0x8b
encrypted[0xC] = 0xe4
encrypted[0xD] = 0xef
encrypted[0xE] = 0xea
encrypted[0x10] = 0xdf
encrypted[0x11] = 0xf3
encrypted[0x12] = 0xdf
encrypted[0x13] = 0xe8
encrypted[0x14] = 0xec
encrypted[0x15] = 0xe5
encrypted[0x16] = 0xda


for y in range (255):
    answer = ''
    for x in range(len(encrypted)):
        answer += chr(((encrypted[x] ^ y) + x) % 256)
        
    if answer[10] == '@':
        print answer
        break
```

难怪提示checksum不对，因为是直接在原题上面改的数据

其实恢复checksum也很简单，刚开始就写了个脚本修复了

```python
fd = open('HexIt.hex', 'r')
out = open('HexIt_copy.hex', 'w')

for line in fd:
	s = line[1:-3]

	checksum = 0
	for i in range(len(s)/2):
		num = s[2*i:2*i+2]
		checksum += int(num, 16)
	checksum &= 0xFF
	checksum = ~checksum
	checksum += 1
	checksum &= 0xFF
	s += '{:02X}'.format(checksum)
	s = ':' + s + '\n'

	out.write(s)

fd.close()
out.close()
```



flag是purple{Ple@se_eor_them}

eor是avr中的指令，其实跟xor是一个意思