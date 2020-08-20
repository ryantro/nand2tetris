# -*- coding: utf-8 -*-
"""'
Created on Sun Dec  1 03:07:37 2019

@author: Ryan
"""

jumparr = ["SCREEN", "KEYBOARD", "SP", "LCL", "ARG", "THIS", "THAT"]
njumparr = [16384, 24576, 0, 1, 2, 3, 4]
offset = 16
linenum = 0  


def main():
    filenames = ['add\\Add.asm','pong\\Pong.asm','max\\Max.asm','rect\\Rect.asm']
    writefiles = ['project6\\Add.hack','project6\\Pong.hack','project6\\Max.hack','project6\\Rect.hack']
    
    for i in range(0,16):
        jumparr.append("R"+str(i))
        njumparr.append(i)
        
    print(jumparr)
    print(njumparr)
    
# =============================================================================
#     for i in range(0,len(filenames)):
#         global jumparr
#         global njumparr
#         jumparr.clear()
#         njumparr.clear()
#         hackcompile(filenames[i],writefiles[i])
# =============================================================================
        
    hackcompile(filenames[0],writefiles[0])

def hackcompile(filename,writefile):

    
    ## Find all jump points
    ln = 0;
    with open(filename) as fp:
        for line in fp:
            line = line.replace(' ','')
            if(line != '' and line != '\n'):
                if(line[0] == '('):
                    jstr = line[1:(len(line)-2)]
                    #print(jstr)
                    jumparr.append(jstr)
                    njumparr.append(ln)
                elif(line[0] != '/'):
                    print(str(ln)+": "+rmCommentSpaces(line))
                    ln += 1
    
    ## Translate
    wf = open(writefile, "w")
    with open(filename) as fp:
        for line in fp:
            #print("XX    "+translate(line.strip()))
            tstr=str(translate(line.strip()))
            if(tstr!=''):
                wf.write(tstr+'\n')
    wf.close()

        
def rmCommentSpaces(line):
    line = line.replace(' ','')
    line = line.replace('\n','')
    if('//' in line):
        pline = line.split('//')
        line = pline[0]
    return line
        

def translate(line):
    if('' == line):
        return ''
    if('//' in line):
        pline = line.split('//')
        if(pline[0]==''):
            return ''
        line = pline[0].replace(' ','')
    # A Instruction
    if(line[0]=="@"):
        hex = "0"
        num = line[1:]
        # Non-Symbol
        if(str.isdigit(num)):
            binnum = "{0:b}".format(int(num))
        # Symbol
        else:
            binnum = "{0:b}".format(checksymbol(num))
        k = 15 - len(binnum)
        for m in range(0,k):
            hex = hex + "0"
        hex = hex + binnum
        global linenum
        print("{}: ".format(linenum)+"0x"+hex)
        linenum += 1
        return hex
    # Jump Point    
# =============================================================================
#     elif(line[0]=="("):
#         num = line[1:(len(line)-1)]
#         for i in range(0,len(jumparr)):
#             if(jumparr[i]==num):
#                 njumparr[i]=linenum
#                 return ''
#         jumparr.append(num)
#         njumparr.append(linenum)
#         return ''
#         #print(num+"= line "+str(linenum))
#     # C Instruction
# =============================================================================
    elif("=" in line):
        cinst = line.split('=')
        left = cinst[0]
        right = cinst[1]
        binnum = "111"
        
        if('M' in right):
            binnum += "1"
        else:
            binnum += "0"
        binnum += switch_c(right.replace('M','A'))
        binnum += switch_d(left)
        binnum += '000'
        
        hex = binnum
        print("{}: ".format(linenum)+"0x"+hex)
        linenum += 1
        return binnum
    # C Instruction (JUMP)
    elif(";" in line):
        cinst = line.split(';')
        right = cinst[0]
        jstr = cinst[1]
        binnum = "111"        
        if('M' in right):
            binnum += "1"
        else:
            binnum += "0"
        binnum += switch_c(right.replace('M','A'))
        binnum += "000"
        binnum += switch_j(jstr)
        print("{}: ".format(linenum)+"0x"+binnum)
        linenum += 1
        return binnum
    else:
        return ''
        
        
        
        
def switch_j(jstr):
    jhex = {
            '' : '000',
            'JGT' : '001',
            'JEQ' : '010',
            'JGE' : '011',
            'JLT' : '100',
            'JNE' : '101',
            'JLE' : '110',
            'JMP' : '111'
            }
    return jhex[jstr]
        
        
def switch_c(cstr):
    chex = {
            '0' : '101010',
            '1' : '111111',
            '-1' : '111010',
            'D' : '001100',
            'A' : '110000',
            '!D' : '001101',
            '!A' : '110001',
            '-D' : '001111',
            '-A' : '110011',
            'D+1' : '011111',
            'A+1' : '110111',
            'D-1' : '001110',
            'A-1' : '110010',
            'D+A' : '000010',
            'D-A' : '010011',
            'A-D' : '000111',
            'D&A' : '000000',
            'D|A' : '010101'
            }
    
    return chex[cstr]
        
def switch_d(dstr):
    dhex = {
            '' : '000',
            'M' : '001',
            'D' : '010',
            'MD' : '011',
            'A' : '100',
            'AM' : '101',
            'AD' : '110',
            'AMD' : '111'
            }
    return dhex[dstr]
        
  
def checksymbol(num):
    global offset
    for i in range(0,len(jumparr)):
        if (jumparr[i]==num):
            #print(num+" = {}".format(njumparr[i]))
            return njumparr[i]
    jumparr.append(num)
    njumparr.append(offset)
    #print(num+"= {}".format(njumparr))
    offset += 1
    return offset - 1

        
        
if __name__=="__main__":
    main()