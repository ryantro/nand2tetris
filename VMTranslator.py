# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:28:17 2020

@author: Ryan

Course: Nand2Tetris II
Converts from virtual machine language to hax language

"""
import sys

class Parser:
    """Parses the infile which contains the VM code."""
    
    def __init__(self,filename):
        """Initiate the file and strip out comments."""
        self.infile = open(filename,"r")    # file pointer
        lines = self.infile.readlines()     # non-formatted lines
        self.index = 0                      # line number
        self.flines = []                    # formatted lines
        self.command = None
        
        # COMMENT STRIPPER
        commands = ["pop","add","sub","push","neg","eq","gt","lt","and","or","not"]
        for line in lines:
            line = line.split("//")
            line = line[0]
            p = any(command in line for command in commands)
            if p:
                self.flines.append(line)
        
    def hasMoreCommands(self):
        """Check if more commands exist in the object."""
        if self.index >= len(self.flines):
            return False
        else:
            return True
         
    def advance(self):
        """Advance to the next command in the object."""
        self.command = self.flines[self.index].split()
        self.index = self.index + 1
        
    def commandType(self):
        """Determine the type of command is curretnly in the command varable."""
        # All Commands will be used later
        allcommands = {
                0: "C_ARITHMETIC",
                1: "C_PUSH",
                2: "C_POP",
                3: "C_LABEL",
                4: "C_GOTO",
                5: "C_IF",
                6: "C_FUNCTION",
                7: "C_RETURN",
                8: "C_CALL",
                }
        # We use this for now
        commands = {
                "push" : "C_PUSH",
                "pop" : "C_POP",
                "add" : "C_ARITHMETIC",
                "sub" : "C_ARITHMETIC",
                "neg" : "C_ARITHMETIC",
                "eq" : "C_ARITHMETIC",
                "gt" : "C_ARITHMETIC",
                "lt" : "C_ARITHMETIC",
                "and" : "C_ARITHMETIC",
                "or" : "C_ARITHMETIC",
                "not" : "C_ARITHMETIC"
                }
        
        return commands.get(self.command[0],"Error")
        
    def arg1(self):
        """Returns the first arguement of the current command."""
        if self.commandType() == "C_ARITHMETIC":
            return self.command[0]
        else:
            return self.command[1]
    
    def arg2(self):
        """Return the second arguement of the current command."""
        return self.command[2]

class CodeWriter:
    def __init__(self,filename):
        """Initiates the code writer object."""
        self.outfile = open(filename,"w")
        self.jn = 0
    
    def getJump(self):
        jumpname = "JUMP"+str(self.jn)
        self.jn = self.jn+1
        return jumpname
    
    def writeArithmetic(self,command):
        """Writes arithmetic command."""

        if(command=="add"):
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("M=M+D\n")
        if(command=="sub"):
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("M=M-D\n")
        elif(command == "neg"):
            self.outfile.write("@SP\n")
            self.outfile.write("A=M-1\n")
            self.outfile.write("M=-M\n")
        elif(command =="eq"):
            dest1 = self.getJump()
            dest2 = self.getJump()
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("D=M-D\n")
            self.outfile.write("@"+dest1+"\n")
            self.outfile.write("D;JEQ\n")
            self.outfile.write("D=0\n")
            self.outfile.write("@"+dest2+"\n")
            self.outfile.write("0;JMP\n")
            self.outfile.write("("+dest1+")\n")
            self.outfile.write("D=-1\n")
            self.outfile.write("("+dest2+")\n")
            self.outfile.write("@SP\n")
            self.outfile.write("A=M-1\n")
            self.outfile.write("M=D\n")
        elif(command=="gt"):
            dest1 = self.getJump()
            dest2 = self.getJump()
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("D=M-D\n")
            self.outfile.write("@"+dest1+"\n")
            self.outfile.write("D;JGT\n")
            self.outfile.write("D=0\n")
            self.outfile.write("@"+dest2+"\n")
            self.outfile.write("0;JMP\n")
            self.outfile.write("("+dest1+")\n")
            self.outfile.write("D=-1\n")
            self.outfile.write("("+dest2+")\n")
            self.outfile.write("@SP\n")
            self.outfile.write("A=M-1\n")
            self.outfile.write("M=D\n")
        elif(command=="lt"):
            dest1 = self.getJump()
            dest2 = self.getJump()
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("D=M-D\n")
            self.outfile.write("@"+dest1+"\n")
            self.outfile.write("D;JLT\n")
            self.outfile.write("D=0\n")
            self.outfile.write("@"+dest2+"\n")
            self.outfile.write("0;JMP\n")
            self.outfile.write("("+dest1+")\n")
            self.outfile.write("D=-1\n")
            self.outfile.write("("+dest2+")\n")
            self.outfile.write("@SP\n")
            self.outfile.write("A=M-1\n")
            self.outfile.write("M=D\n")
        elif(command =="and"):
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("M=D&M\n")    
        elif(command=="or"):   
            self.outfile.write("@SP\n")
            self.outfile.write("AM=M-1\n")
            self.outfile.write("D=M\n")
            self.outfile.write("A=A-1\n")
            self.outfile.write("M=D|M\n")   
        elif(command == "not"):
            self.outfile.write("@SP\n")
            self.outfile.write("A=M-1\n")
            self.outfile.write("M=!M\n")  
        
    def writePushPop(self, command, segment, index):
        """Writes push pop in assembly."""
        segmentList = ['local','argument','this','that']
        
        if(segment in segmentList):
            segments = {
                    "local" : "@LCL\n",
                    "argument" : "@ARG\n",
                    "this" : "@THIS\n",
                    "that" : "@THAT\n"
                        }
            seg = segments.get(segment)
            
            if(command=="C_PUSH"):
                self.outfile.write(seg) 
                self.outfile.write("D=M\n")
                self.outfile.write("@"+str(index)+"\n")
                self.outfile.write("A=D+A\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")
                self.outfile.write("A=M-1\n")
                self.outfile.write("M=D\n")
            elif(command=="C_POP"):
                self.outfile.write("@SP\n") 
                self.outfile.write("AM=M-1\n") 
                self.outfile.write("D=M\n") 
                self.outfile.write(seg)
                self.outfile.write("A=M\n")
                for i in range(0,int(index)):
                    self.outfile.write("A=A+1\n")
                self.outfile.write("M=D\n")
        
        # PUSH CONSTANT i
        elif(segment=="constant"):
            self.outfile.write("@"+str(index)+"\nD=A\n")
            self.outfile.write("@SP\nM=M+1\nA=M-1\nM=D\n")
            return
        
        # PUSH/POP POINTER
        elif(segment=="pointer"):
            # 0: THIS Ram(3); 1: THAT Ram(4)
            if(index=="0"):
                m = "3"
            elif(index=="1"):
                m = "4"
            if(command=="C_PUSH"):
                # *SP = THIS/THAT
                self.outfile.write("@R"+m+"\n")
                self.outfile.write("D=M\n")
                self.outfile.write("@SP\n")
                self.outfile.write("A=M\n")
                self.outfile.write("M=D\n")
                # SP++
                self.outfile.write("@SP\n")
                self.outfile.write("M=M+1\n")
                return
            elif(command=="C_POP"):
                # SP--
                self.outfile.write("@SP\n")
                self.outfile.write("M=M-1\n")
                # THIS/THAT = *SP
                self.outfile.write("A=M\n") # M = SP and goto A
                self.outfile.write("D=M\n") # D = *SP
                self.outfile.write("@R"+str(m)+"\n")# @R3/R4
                self.outfile.write("M=D\n") # THIS/THAT = D
                return
                
        # PUSH/POP TEMP
        elif(segment=="temp" or segment=="static"):
            if(segment=="temp"):
                os = 5
            elif(segment=="static"):
                os = 16    
            if(command=="C_PUSH"):
                 self.outfile.write("@"+str(os+int(index))+"\n")
                 self.outfile.write("D=M\n")
                 self.outfile.write("@SP\n")
                 self.outfile.write("M=M+1\n")
                 self.outfile.write("A=M-1\n")
                 self.outfile.write("M=D\n")
            elif(command=="C_POP"):
                 self.outfile.write("@SP\n")
                 self.outfile.write("AM=M-1\n")
                 self.outfile.write("D=M\n")
                 self.outfile.write("@"+str(os+int(index))+"\n")
                 self.outfile.write("M=D\n")
        
        
    def close(self):
        """Closes the outfile."""
        self.outfile.close()


def main():  
    filename = sys.argv[1]
    #filename = "StackArithmetic\\SimpleAdd\\SimpleAdd.vm"
    #filename = "StackArithmetic\\StackTest\\StackTest.vm"
    #filename = "MemoryAccess\\BasicTest\\BasicTest.vm"
    #filename = "MemoryAccess\\PointerTest\\PointerTest.vm"
    #filename = "MemoryAccess\\StaticTest\\StaticTest.vm"    
    file = Parser(filename) # create object
    
    outfilename = filename.replace('.vm','.asm')
    print("Out File: "+outfilename)
    outfile = CodeWriter(outfilename)
    
    
    while(file.hasMoreCommands()):
        file.advance()
        
        # TEST SCRIPT
        print("commandType(): "+file.commandType(), end = " ")
        if file.commandType() != "C_RETURN":
            print("arg1(): "+file.arg1(), end = " ")
        tsts = ["C_PUSH","C_POP","C_FUNCTION","C_CALL"]
        p = any(tst in file.commandType() for tst in tsts)
        if p:
            print("arg2(): "+file.arg2(), end = " ")
        print(file.command)
        
        if("C_ARITHMETIC"==file.commandType()):
            outfile.writeArithmetic(file.arg1())
        if("C_PUSH"==file.commandType() or "C_POP"==file.commandType()):
            outfile.writePushPop(file.commandType(), file.arg1(), file.arg2())
       
    outfile.close()
    
    # TEST SCRIPT
    test_outfile = open(outfilename)
    print(test_outfile.read())

if __name__=="__main__":
    main()