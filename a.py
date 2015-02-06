# -*- coding: cp936 -*-

import re
import os
import traceback

def refind(reg, s):
    r = re.findall(reg, s)
    if r:
        return r[0].strip()
    else:
        return ""
    

raw_input("请将需要处理的 txt 文件放置于input目录中, 按下回车键开始自动处理..")
print "注意:测试版本入账日期最后一位以 * 号隐藏"
open("error.txt", "w").write("")

s = ""
for n in os.listdir("./input/"):
    fn = "./input/" + n
    t = open(fn).read()
    try:
        t = t.decode("utf8")[1:].encode("gbk", "replace")
    except:
        pass
    s += t + "\n"

snum = 0
enum = 0
outstr = ""
ss = s.split("记账回执")
for s in ss:
    if len(s) < 100:
        continue
    s0 = s
    try:
        s = s.replace("\n", " ").replace("\r", " ").replace(":", "：").replace(" ", "")
        s = s.replace(".?", "：").replace("=", "：")
        a1 = re.findall(r"入账日期：(.*?)会计流水", s)[0].strip()
        a2 = refind(r"发报行号：(.*?)收款人账号", s)
        if not a2:
            a2 = re.findall(r"发报行号：(.*?)销账编号", s)[0].strip()
            a3 = re.findall(r"发报行名：(.*?)收款人账号", s)[0].strip()
            a4 = re.findall(r"付款人名称：(.*?)发报行名", s)[0].strip()
        else:
            a3 = re.findall(r"发报行名：(.*?)发报行号", s)[0].strip()
            a4 = re.findall(r"付款人名称：(.*?)报文编号", s)[0].strip()
        a5 = re.findall(r"付款人账号：(.*?)付款人地址", s)[0].strip()
        a6 = re.findall(r"收款人名称：(.*?)币种", s)[0].strip()
        a7 = re.findall(r"收款人账号：(.*?)收款人", s)[0].strip()
        a8 = refind(r"摘要：(.*?)票据日期", s) + refind(r"附言：(.*?)摘要", s)
        a9 = re.findall(r"金额：(.*?)金额大写", s)[0].replace(",", "").replace("，", "").replace("一", "").replace("—", "").replace("_", ".").strip()
        a1 = a1.replace("年", ",").replace("月", ",").replace("日", ",")
        a1 = a1.split(",")
        a10 = a1[0].strip()
        a11 = a1[1].strip()
        a12 = a1[2].strip()
        a1 = a10 + a11.zfill(2) + a12.zfill(2)
        a1 = a1[:-1] + "*"
        a = "%s ~ %s ~ 00000000 ~ %s ~ %s ~ %s ~ %s ~ %s ~ %s ~ %s ~ %s ~ 00" % (
            a1, a1, a2, a3, a4, a5, a6, a7, a8, a9
            )
        print a
        outstr += a + "\n"
        snum += 1
    except:
        traceback.print_exc()
        print "============== error ================="
        print s0
        print "======================================"
        open("error.txt", "a").write("记账回执\n" + s0 + "\n\n")
        enum += 1

open("output.txt", "w").write(outstr)

print "成功处理 %d 组数据, 失败 %d 组." % (snum, enum)
raw_input("完成!结果保存于 output.txt 文件中, 按下回车键退出...")



