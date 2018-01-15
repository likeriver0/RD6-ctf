# Easyre Write Up

giglf

---

很容易能找到入口

首先通过

```c
CreateMutexA(0, 0, "Far_away_from_flag");
if ( GetLastError() == ERROR_ALREADY_EXISTS )
```

进入不同的分支

分支2输入len = 32的flag然后以输入为参数又再开了一个同样的进程

```c
  memset(&v2, 0xCCu, 0x198u);
  if ( strlen(lpCommandLine) == 32 )
  {
    StartupInfo.cb = 68;
    memset(&StartupInfo.lpReserved, 0, 0x40u);
    GetModuleFileNameA(0, &Filename, 0x104u);
    result = CreateProcessA(&Filename, lpCommandLine, 0, 0, 0, 0, 0, 0, &StartupInfo, &ProcessInformation);
  }
  else
  {
    result = printf("Wrong!\n");
  }
```

这个新开的进程会进入满足了`ALREADY_EXISTS` 的条件，进入第一个分支

```c
 sub_401064((int)&v6);
    v2 = &pNumArgs;
    v0 = GetCommandLineW();
    v8 = (const wchar_t **)CommandLineToArgvW(v0, v2);
    v2 = (int *)33;
    wcstombs(&Name, *v8, 0x21u);
    CreateMutexA(0, 0, &Name);
    if ( GetLastError() == 183 )
    {
      if ( sub_40106E(&Name) )
        dword_871CA0 = 1;
      if ( dword_871CA0 )
        printf("Correct!\n");
      else
        printf("Wrong!\n");
    }
    else
    {
      sub_401050(&Name);
      Sleep(0x14u);
    }
    result = 0;
  }
  else
  {
    printf("Please input flag:");
    scanf("%32s", &CommandLine);
    sub_401050(&CommandLine);
    Sleep(0x64u);
    system("pause");
    result = 0;
  }
  return result;
```

通过sub_40106E函数的check来判断是否正确

进去的逻辑很简单，就一个异或的操作，不过跑出来显然被耍了

`This_is_not_the_flag`

---

继续看，sub_401064函数里嵌套了很多层，一个个乱点进去，会发现到某个函数直接卡住了

似乎是这有问题了，刚开始拖进ida7.0直接卡死了，后来扔进OD也跑了挺久才分析出来，扔进ida6.8也跑了有点久但跑出来了，看了ida7.0进行了更深层的分析，渣渣电脑直接卡死了

放弃f5直接看看汇编，第一个关键函数是`sub_627260`

发现有33333个分支

```asm
.text:006272A0                 cmp     [ebp+var_8], 8234h ; switch 33333 cases
.text:006272A7                 ja      loc_699177      ; jumptable 006272B0 default case
.text:006272AD                 mov     eax, [ebp+var_8]
.text:006272B0                 jmp     ds:off_699194[eax*4] ; switch jump
.text:006272B7 ; ---------------------------------------------------------------------------
.text:006272B7
.text:006272B7 loc_6272B7:                             ; CODE XREF: sub_627260+50j
.text:006272B7                                         ; DATA XREF: .text:off_699194o
.text:006272B7                 mov     ecx, [ebp+var_4] ; jumptable 006272B0 case 0
.text:006272BA                 add     ecx, 1
.text:006272BD                 mov     [ebp+var_4], ecx
.text:006272C0                 jmp     loc_699177      ; jumptable 006272B0 default case
.text:006272C5 ; ---------------------------------------------------------------------------
.text:006272C5
.text:006272C5 loc_6272C5:                             ; CODE XREF: sub_627260+50j
.text:006272C5                                         ; DATA XREF: .text:off_699194o
.text:006272C5                 mov     edx, [ebp+var_4] ; jumptable 006272B0 case 1
.text:006272C8                 add     edx, 1
.text:006272CB                 mov     [ebp+var_4], edx
.text:006272CE                 jmp     loc_699177      ; jumptable 006272B0 default case
.text:006272D3 ; ---------------------------------------------------------------------------
.text:006272D3
.text:006272D3 loc_6272D3:                             ; CODE XREF: sub_627260+50j
.text:006272D3                                         ; DATA XREF: .text:off_699194o
.text:006272D3                 mov     eax, [ebp+var_4] ; jumptable 006272B0 case 2
.text:006272D6                 add     eax, 1
.text:006272D9                 mov     [ebp+var_4], eax
.text:006272DC                 jmp     loc_699177      ; jumptable 006272B0 default case
```

难怪直接卡死

底下的汇编代码结构全都一样的，好花哇

刚开始还想着有没有什么插件直接去掉，可以让我F5，不用看汇编，试了一段时间，发现其实有很简单的方法

每个分支的效果都只是对var_4加1，效果都是一样的，那我直接把jmp那段patch成nop，直接只进入第一个分支，效果都是一样的

这样结构的汇编有4段，刚好对应了ida内存段上4段蓝色的，都该了后再继续跟进去，然后就看到比较有趣的代码了

```c
void __cdecl sub_401930(_DWORD *a1)
{
  char v1; // [sp+Ch] [bp-64h]@1
  int v2; // [sp+4Ch] [bp-24h]@1
  DWORD dwProcessId; // [sp+50h] [bp-20h]@1
  int i; // [sp+54h] [bp-1Ch]@1
  char v5; // [sp+58h] [bp-18h]@1
  char v6; // [sp+59h] [bp-17h]@1
  char v7; // [sp+5Ah] [bp-16h]@1
  char v8; // [sp+5Bh] [bp-15h]@1
  char v9; // [sp+5Ch] [bp-14h]@1
  char v10; // [sp+5Dh] [bp-13h]@1
  char v11; // [sp+5Eh] [bp-12h]@1
  char v12; // [sp+5Fh] [bp-11h]@1
  char v13; // [sp+60h] [bp-10h]@1
  char v14; // [sp+61h] [bp-Fh]@1
  char v15; // [sp+62h] [bp-Eh]@1
  DWORD flOldProtect; // [sp+64h] [bp-Ch]@1
  DWORD v17; // [sp+68h] [bp-8h]@1
  int v18; // [sp+6Ch] [bp-4h]@1

  memset(&v1, 0xCCu, 0x64u);
  v2 = ++v18;
  ++v18;
  v17 = 0;
  v5 = 0;
  v6 = 0;
  v7 = 0;
  v8 = 0;
  v9 = 0;
  v10 = 0;
  v11 = 0;
  v12 = 0;
  v13 = 0;
  v14 = 0;
  v15 = 0;
  *a1 ^= 0xC1315u;
  dwProcessId = GetCurrentProcessId();
  hProcess = OpenProcess(PROCESS_ALL_ACCESS, 0, dwProcessId);
  VirtualProtectEx(hProcess, &loc_401600, 0xB2u, PROCESS_SET_SESSIONID, &flOldProtect);
  for ( i = 0; i < 178; ++i )
    *((_BYTE *)&loc_401600 + i) ^= *((_BYTE *)a1 + i % 4);
  VirtualProtectEx(hProcess, &loc_401600, 0xB2u, flOldProtect, &v17);
  VirtualProtectEx(hProcess, sub_401290, 0x117u, PROCESS_SET_SESSIONID, &flOldProtect);
  for ( i = 0; i < 279; ++i )
    *((_BYTE *)sub_401290 + i) ^= *((_BYTE *)a1 + i % 4);
  VirtualProtectEx(hProcess, sub_401290, 0x117u, flOldProtect, &v17);
  sub_401069();
}
```

更改了段的保护属性，对text的代码进行了异或，然后后面调用了那一块的函数

动态调直接跟过去，就发现关键函数了

```c
int __cdecl sub_401180(int a1, int a2)
{
  int result; // eax@1
  char v3; // [sp+Ch] [bp-64h]@1
  int i; // [sp+4Ch] [bp-24h]@1
  char v5; // [sp+50h] [bp-20h]@1
  char v6; // [sp+51h] [bp-1Fh]@1
  char v7; // [sp+52h] [bp-1Eh]@1
  char v8; // [sp+53h] [bp-1Dh]@1
  char v9; // [sp+54h] [bp-1Ch]@1
  char v10; // [sp+55h] [bp-1Bh]@1
  char v11; // [sp+56h] [bp-1Ah]@1
  char v12; // [sp+57h] [bp-19h]@1
  char v13; // [sp+58h] [bp-18h]@1
  char v14; // [sp+59h] [bp-17h]@1
  char v15; // [sp+5Ah] [bp-16h]@1
  char v16; // [sp+5Bh] [bp-15h]@1
  char v17; // [sp+5Ch] [bp-14h]@1
  char v18; // [sp+5Dh] [bp-13h]@1
  char v19; // [sp+5Eh] [bp-12h]@1
  char v20; // [sp+5Fh] [bp-11h]@1
  char v21; // [sp+60h] [bp-10h]@1
  char v22; // [sp+61h] [bp-Fh]@1
  char v23; // [sp+62h] [bp-Eh]@1
  char v24; // [sp+63h] [bp-Dh]@1
  char v25; // [sp+64h] [bp-Ch]@1
  char v26; // [sp+65h] [bp-Bh]@1
  char v27; // [sp+66h] [bp-Ah]@1
  char v28; // [sp+67h] [bp-9h]@1
  char v29; // [sp+68h] [bp-8h]@1
  char v30; // [sp+69h] [bp-7h]@1
  char v31; // [sp+6Ah] [bp-6h]@1
  char v32; // [sp+6Bh] [bp-5h]@1
  char v33; // [sp+6Ch] [bp-4h]@1
  char v34; // [sp+6Dh] [bp-3h]@1
  char v35; // [sp+6Eh] [bp-2h]@1
  char v36; // [sp+6Fh] [bp-1h]@1

  result = -858993460;
  memset(&v3, 0xCCu, 0x64u);
  v5 = 10;
  v6 = 11;
  v7 = 23;
  v8 = 15;
  v9 = 17;
  v10 = 19;
  v11 = 3;
  v12 = 9;
  v13 = 8;
  v14 = 25;
  v15 = 18;
  v16 = 20;
  v17 = 13;
  v18 = 21;
  v19 = 16;
  v20 = 2;
  v21 = 14;
  v22 = 27;
  v23 = 29;
  v24 = 28;
  v25 = 5;
  v26 = 31;
  v27 = 22;
  v28 = 7;
  v29 = 24;
  v30 = 30;
  v31 = 12;
  v32 = 4;
  v33 = 26;
  v34 = 0;
  v35 = 1;
  v36 = 6;
  for ( i = 0; i < 32; ++i )
  {
    *(_BYTE *)(i + a1) = *(_BYTE *)(a2 + *(&v5 + i));
    result = i + 1;
  }
  return result;
}
```

```c
signed int __cdecl sub_401290(int a1)
{
  char v2; // [sp+Ch] [bp-88h]@1
  int i; // [sp+4Ch] [bp-48h]@1
  char v4[33]; // [sp+50h] [bp-44h]@1
  char v5; // [sp+71h] [bp-23h]@1
  char v6; // [sp+74h] [bp-20h]@1
  char v7; // [sp+75h] [bp-1Fh]@1
  char v8; // [sp+76h] [bp-1Eh]@1
  char v9; // [sp+77h] [bp-1Dh]@1
  char v10; // [sp+78h] [bp-1Ch]@1
  char v11; // [sp+79h] [bp-1Bh]@1
  char v12; // [sp+7Ah] [bp-1Ah]@1
  char v13; // [sp+7Bh] [bp-19h]@1
  char v14; // [sp+7Ch] [bp-18h]@1
  char v15; // [sp+7Dh] [bp-17h]@1
  char v16; // [sp+7Eh] [bp-16h]@1
  char v17; // [sp+7Fh] [bp-15h]@1
  char v18; // [sp+80h] [bp-14h]@1
  char v19; // [sp+81h] [bp-13h]@1
  char v20; // [sp+82h] [bp-12h]@1
  char v21; // [sp+83h] [bp-11h]@1
  char v22; // [sp+84h] [bp-10h]@1
  char v23; // [sp+85h] [bp-Fh]@1
  char v24; // [sp+86h] [bp-Eh]@1
  char v25; // [sp+87h] [bp-Dh]@1
  char v26; // [sp+88h] [bp-Ch]@1
  char v27; // [sp+89h] [bp-Bh]@1
  char v28; // [sp+8Ah] [bp-Ah]@1
  char v29; // [sp+8Bh] [bp-9h]@1
  char v30; // [sp+8Ch] [bp-8h]@1
  char v31; // [sp+8Dh] [bp-7h]@1
  char v32; // [sp+8Eh] [bp-6h]@1
  char v33; // [sp+8Fh] [bp-5h]@1
  char v34; // [sp+90h] [bp-4h]@1
  char v35; // [sp+91h] [bp-3h]@1
  char v36; // [sp+92h] [bp-2h]@1
  char v37; // [sp+93h] [bp-1h]@1

  memset(&v2, 0xCCu, 0x88u);
  v6 = 95;
  v7 = 23;
  v8 = -87;
  v9 = -32;
  v10 = -56;
  v11 = 97;
  v12 = -35;
  v13 = 66;
  v14 = -25;
  v15 = -92;
  v16 = -20;
  v17 = -101;
  v18 = 41;
  v19 = 40;
  v20 = 92;
  v21 = 67;
  v22 = -94;
  v23 = -24;
  v24 = -58;
  v25 = 108;
  v26 = -107;
  v27 = -18;
  v28 = -94;
  v29 = 115;
  v30 = 106;
  v31 = 82;
  v32 = -92;
  v33 = -84;
  v34 = -94;
  v35 = 102;
  v36 = -5;
  v37 = 53;
  v5 = 0;
  sub_401046(v4, a1);
  sub_40103C(v4, v4);
  for ( i = 0; i < 32; ++i )
  {
    if ( *(&v6 + i) != v4[i] )
      return 0;
  }
  dword_871CA0 = 1;
  return 1;
}


int __cdecl sub_4010F0(int a1, int a2)
{
  int result; // eax@1
  char v3; // bl@3
  char v4; // al@3
  char v5; // [sp+Ch] [bp-44h]@1
  int i; // [sp+4Ch] [bp-4h]@1

  memset(&v5, 0xCCu, 0x44u);
  result = sub_6DE7E0(0);
  for ( i = 0; i < 32; ++i )
  {
    v3 = *(_BYTE *)(i + a2);
    v4 = rand();
    *(_BYTE *)(i + a1) = v4 ^ v3;
    result = i + 1;
  }
  return result;
}
```

---

把输入跟srand(0)的rand()异或，还有根据一个表的移位

很容易就能恢复

```python


# v4 = [84,105,107,112,91,108,117,88,102,102,126,84,120,101,107,80,118,125,115,116,20]

# for i in range(len(v4)):
# 	v4[i] = i^v4[i]

# print ''.join(map(chr,v4))

result = [95,23,-87,-32,-56,97,-35,66,-25,-92,-20,-101,41,40,92,67,-94,-24,-58,108,-107,-18,-94,115,106,82,-92,-84,-94,102,-5,53]
flag = [0]*32

v5 = [10,11,23,15,17,19,3,9,8,25,18,20,13,21,16,2,14,27,29,28,5,31,22,7,24,30,12,4,26,0,1,6]

rand = [38, 7719, 21238, 2437, 8855, 11797, 8365, 32285, 10450, 30612, 5853, 28100, 1142, 281, 20537, 15921, 8945, 26285, 2997, 14680, 20976, 31891, 21655, 25906, 18457, 1323, 28881, 2240, 9725, 32278, 2446, 590]

for i in range(len(result)):
	result[i] = (result[i] ^ rand[i]) & 0xFF
	flag[v5[i]] = result[i]

print flag
print ''.join(map(chr, flag))
```

purple{A5_y0u_See_1t_15_s0_E4sy}