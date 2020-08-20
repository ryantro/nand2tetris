# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 16:28:17 2020

@author: Ryan

Course: Nand2Tetris II
Converts from virtual machine language to hax language

"""
import sys
import os

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
        commands = ["pop","add","sub","push","neg","eq","gt","lt","and","or","not","label","if-goto","goto","function","return","call"]
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
                "not" : "C_ARITHMETIC",
                "label" : "C_LABEL",
                "if-goto" : "C_IF",
                "goto" : "C_GOTO",
                "function" : "C_FUNCTION",
                "return" : "C_RETURN",
                "call" : "C_CALL"
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
        self.labels = []
    
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
            return None
        
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
                return None
            elif(command=="C_POP"):
                # SP--
                self.outfile.write("@SP\n")
                self.outfile.write("M=M-1\n")
                # THIS/THAT = *SP
                self.outfile.write("A=M\n") # M = SP and goto A
                self.outfile.write("D=M\n") # D = *SP
                self.outfile.write("@R"+str(m)+"\n")# @R3/R4
                self.outfile.write("M=D\n") # THIS/THAT = D
                return None
                
        # PUSH/POP TEMP
        elif(segment=="temp"):
            if(command=="C_PUSH"):
                 self.outfile.write("@"+str(5+int(index))+"\n")
                 self.outfile.write("D=M\n")
                 self.outfile.write("@SP\n")
                 self.outfile.write("M=M+1\n")
                 self.outfile.write("A=M-1\n")
                 self.outfile.write("M=D\n")
            elif(command=="C_POP"):
                 self.outfile.write("@SP\n")
                 self.outfile.write("AM=M-1\n")
                 self.outfile.write("D=M\n")
                 self.outfile.write("@"+str(5+int(index))+"\n")
                 self.outfile.write("M=D\n")
        
        # PUSH/POP STATIC         
        elif(segment=="static"):   
            if(command=="C_PUSH"):
                 self.outfile.write("@"+self.fileName+str(index)+"\n")
                 self.outfile.write("D=M\n")
                 self.outfile.write("@SP\n")
                 self.outfile.write("M=M+1\n")
                 self.outfile.write("A=M-1\n")
                 self.outfile.write("M=D\n")
            elif(command=="C_POP"):
                 self.outfile.write("@SP\n")
                 self.outfile.write("AM=M-1\n")
                 self.outfile.write("D=M\n")
                 self.outfile.write("@"+self.fileName+str(index)+"\n")
                 self.outfile.write("M=D\n")
        return None
    
    def setFileName(self,fileName):
        self.fileName = fileName
        return None
    
    def writeInit(self):
        '''Writes assembly instructions that effect the bootstrap code. Must be placed at beginning of *.asm'''
#        self.outfile.write("@Sys.init\n")
#        self.outfile.write("0;JMP\n")
        self.outfile.write("@256\n")
        self.outfile.write("D=A\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=D\n")
        self.writeCall("Sys.init",0)
        return None
    
    def writeLabel(self,label):
        '''effects the label command'''
        if label not in self.labels:
            self.labels.append(label)
        self.outfile.write("("+label+")\n")
        return None
    
    def writeGoto(self,label):
        '''effects the goto command'''
        self.outfile.write("@"+label+"\n")
        self.outfile.write("0;JMP\n")
        return None
    
    def writeIf(self,label):
        '''effects the if-goto command'''
        self.outfile.write("@SP\n")
        self.outfile.write("AM=M-1\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@"+label+"\n")
        self.outfile.write("D;JNE\n")
        return None
    
    def writeCall(self,functionName,numArgs):
        '''Writes assembly code that effects the call command'''
        # PUSH ALL NEEDED ARGS
        #for i in range(0,int(numArgs)):
        #    self.writePushPop("C_PUSH","argument",i)
        
        # SAVE THE FRAME OF THE CALLER
        cJump = self.getJump()
        self.outfile.write("@"+cJump+"\n")
        self.outfile.write("D=A\n")
        # PUSH D TO THE STACK
        self.outfile.write("@SP\n")
        self.outfile.write("AM=M+1\n")
        self.outfile.write("A=A-1\n")
        self.outfile.write("M=D\n")
        
        # POINTER PUSHES
        self.writePointerPush("LCL")
        self.writePointerPush("ARG")
        self.writePointerPush("THIS")
        self.writePointerPush("THAT")
        
        # SET ARG ADDRESS
        self.writePointerPush("SP")
        self.writePushPop("C_PUSH","constant",numArgs)
        self.writeArithmetic("sub")
        self.writePushPop("C_PUSH","constant",5)
        self.writeArithmetic("sub")
        self.writePointerPop("ARG")
        
        # WRITE THE FUNCTION?
        self.outfile.write("@"+functionName+"\n")
        self.outfile.write("0;JMP\n")
        
        # RETURN ADDRESS
        self.outfile.write("("+cJump+")\n")
        return None
    
    def writeFunction(self,functionName,numVars):
        '''Writes assembly code that effects the function command'''
        # JUMP ADDRESS
        self.outfile.write("("+functionName+")\n")
        
        # SET LCL TO SP
        self.writePointerPush("SP")
        self.writePointerPop("LCL")
        
        # INITIALIZE LOCAL VARIABLES TO 0
        for i in range(0,int(numVars)):
            self.writePushPop("C_PUSH","constant",0)
        return None    
    
    def writePointerPop(self,pointer):
        '''Pushes stack to pointer'''
        self.outfile.write("@SP\n")
        self.outfile.write("AM=M-1\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@"+str(pointer)+"\n")
        self.outfile.write("M=D\n")
        return None
    
    def writePointerPush(self,pointer):
        '''Push pointer address to the stack'''
        self.outfile.write("@"+str(pointer)+"\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=M+1\n")
        self.outfile.write("A=M-1\n")
        self.outfile.write("M=D\n")
        return None
        
    def writeReturn(self):
        '''writes assembly code that effects the return command'''
        # SAVE THE RETURN VALUE IN R13
        self.outfile.write("@SP\n")
        self.outfile.write("A=M-1\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@R13\n")
        self.outfile.write("M=D\n")
        
        # SAVE THE RETURN VALUE LOCATION IN R14
        self.outfile.write("@ARG\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@R14\n")
        self.outfile.write("M=D\n")
        
        # POSITION THE POINTER AT THE END OF THE SAVED FRAME
        self.outfile.write("@LCL\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=D\n")
        
        # RESTORE POINTERS
        self.writePointerPop("THAT")
        self.writePointerPop("THIS")
        self.writePointerPop("ARG")
        self.writePointerPop("LCL")
        
        # SAVE THE RETURN ADDRESS IN R15
        self.outfile.write("@SP\n")
        self.outfile.write("A=M-1\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@R15\n")
        self.outfile.write("M=D\n")
        
        # PLACE RETURN VALUE
        self.outfile.write("@R13\n")
        self.outfile.write("D=M\n")
        self.outfile.write("@R14\n")
        self.outfile.write("A=M\n")
        self.outfile.write("M=D\n")
        
        # POSITION THE POINTER
        self.outfile.write("D=A+1\n")
        self.outfile.write("@SP\n")
        self.outfile.write("M=D\n")
    
        # GO TO RETURN ADDRESS
        self.outfile.write("@R15\n")
        self.outfile.write("A=M\n")
        self.outfile.write("0;JMP\n")
        return None
    
    def close(self):
        """Closes the outfile."""
        self.outfile.close()
        return None

def getFiles(filename):
    if(".vm" in filename):
        print("EASY CASE")
    else:
        print("HARD CASE")

def main():
    d = "/"
    # FILE OR DIRECTORY NAME
    programinput = sys.argv[1]
    #programinput = "07\\MemoryAccess\\StaticTest\\StaticTest.vm"
    #filename = "08\\ProgramFlow\\BasicLoop\\BasicLoop.vm"
    #filename = "08\\ProgramFlow\\FibonacciSeries\\FibonacciSeries.vm"
    #filename = "08\\FunctionCalls\\SimpleFunction\\SimpleFunction.vm"
    #programinput = "08\\FunctionCalls\\NestedCall"
    #programinput = "08\\FunctionCalls\\FibonacciElement"
    #programinput = "08/FunctionCalls/StaticsTest"
    
    # GENERATE FILENAMES AND OUTFILENAME
    if(".vm" in programinput):
        filenames = [programinput]
        outfilename = programinput.replace('.vm','.asm')
        initneeded = False
    else:
        programdir = os.listdir(programinput)
        filenames = [programinput+d+f for f in programdir if '.vm' in f]
        outfilename = programinput+d+programinput.split(d)[-1]+".asm"
        initneeded = True
    outfile = CodeWriter(outfilename)

    
    
    # VERIFICATION
    print("In File(s): ", end = "")
    print(filenames)
    print("Out File: "+outfilename)
    
    # DOES THE PROGRAM NEED TO BE INITATIED
    if(initneeded):
        outfile.writeInit()
        
    # GO THROUGH ALL NEEDED FILES
    for filename in filenames:
        
        # CREATE FILE OBJECT
        file = Parser(filename)
        
        outfile.setFileName(filename.split(d)[-1].strip(".vm"))
        
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
            
            # MAIN PROGRAM
            if("C_ARITHMETIC"==file.commandType()):
                outfile.writeArithmetic(file.arg1())
            if("C_PUSH"==file.commandType() or "C_POP"==file.commandType()):
                outfile.writePushPop(file.commandType(), file.arg1(), file.arg2())
            if("C_LABEL"==file.commandType()):
                outfile.writeLabel(file.arg1())
            if("C_IF"==file.commandType()):
                outfile.writeIf(file.arg1())
            if("C_GOTO"==file.commandType()):
                outfile.writeGoto(file.arg1())
            if("C_FUNCTION"==file.commandType()):
                outfile.writeFunction(file.arg1(),file.arg2())
            if("C_RETURN"==file.commandType()):
                outfile.writeReturn()
            if("C_CALL"==file.commandType()):
                outfile.writeCall(file.arg1(),file.arg2())
    outfile.close()
    
    # PRINT THE FILE JUST CREATED
    #test_outfile = open(outfilename)
    #print(test_outfile.read())
    
    return None

if __name__=="__main__":
    main()