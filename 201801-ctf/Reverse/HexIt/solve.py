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