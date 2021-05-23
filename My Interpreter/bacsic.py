from sys import *

tokens = []
num_stack = []
symbols = {}

def open_file(filename):
    data = open(filename, "r").read()
    data += "<EOF>" 
    return data

def lex(filecontents):
    tok = ""
    state = 0
    isexpr = 0
    varStated = 0
    var = ""
    string = ""
    tukhoa =""
    expr = ""
    n = ""
    filecontents = list(filecontents)
    for char in filecontents :
        tok += char 
        if tok == " " :
            if state == 0 :
                tok = ""
            else:
                tok = " " 

        elif tok == "\n" or tok == "<EOF>":
            if expr != "" and isexpr == 1:
               # print(expr + ": EXPR") 
                tokens.append("EXPR:" + expr) 
                expr = ""
            elif expr != "" and isexpr == 0 :
              # print(expr + ": NUM")
                tokens.append("NUM:" + expr) 
                expr = ""
            elif var != "" :
                tokens.append("VAR:" + var)
                var = "" 
                varStated = 0
            elif string != "":
                tokens.append("STRING:" + string)
                string =""

            tok = ""
        
        elif tok == "=" and state == 0 :
            if expr != "" and isexpr == 0 :
                tokens.append("NUM:" + expr) 
                expr = ""
            if var != "" :
                tokens.append("VAR:" + var)
                var = "" 
                varStated = 0
            if tokens[-1] == "EQUALS":
                tokens[-1] = "EQEQ"
            else:
                tokens.append("EQUALS")
            tok = ""

        elif tok == "(" and state == 0:
            if string != "" and state == 0:
                tokens.append("STRING" + string)
                string = ""
            tokens.append("NGOACTRAI")
            tok = ""

        elif tok == ")" and state == 0:
            tokens.append("NGOACPHAI")
            tok = ""

        elif tok == "$" and state == 0 :
            varStated = 1
            var += tok
            tok = ""
        
        elif varStated == 1 :
            if tok == "<" or tok == ">" :
                if var != "" :
                    tokens.append("VAR:" + var)
                    var = "" 
                    varStated = 0
            var += tok
            tok = ""

        elif tok == "IN" or  tok == "in":
           # print("Thay Ham In")
            tokens.append("IN")
            tok = ""
        
        
        elif tok == "NEU" or  tok == "neu" or tok == "Neu":
               # print("Thay Ham In")
            tokens.append("NEU")
            tok = ""

        elif tok == "KTNEU" or  tok == "ktneu" or tok == "KTneu":
               # print("Thay Ham In")
            tokens.append("KTNEU")
            tok = ""
        
        elif tok == "THI" or  tok == "thi" or tok == "Thi":
            if expr != "" and isexpr == 0 :
                tokens.append("NUM:" + expr) 
                expr = ""
            tokens.append("THI")
            tok = ""

        elif tok == "mota" :
            tokens.append("MOTA")
            tok = ""

        elif tok == "DAUVAO" or  tok == "dauvao":
            tokens.append("DAUVAO")
            tok = ""
            
        elif tok == "0" or tok == "1" or tok == "2" or tok == "3" or tok == "4" or tok == "5" or tok == "6" or tok == "7" or tok == "8" or tok == "9" :
            expr += tok
            tok =""

        elif tok == "+" or tok == "-" or tok == "/" or tok == "*" or tok == "(" or tok == ")":
            isexpr = 1
            string += tok
            expr += tok
            tok = ""

        elif tok == "\t" :
            tok = ""

        elif tok == "\"" or tok ==" \"" :
            if state == 0:
                
                state = 1 
            elif state == 1:
               # print("Tim thay chuoi String")
                tokens.append("STRING:" + string + "\"") 
                string = ""
                state = 0
                tok = ""
                
            

        elif state == 1 :
            string += tok
            tok = ""
        
    #print(tokens) # viet ham Parse
    #return ''
    return tokens

## Ham danh gia EXPR
def evalExpresstion(expr):
    # expr = "," + expr
    # i = len(expr) - 1
    # num = ""
    # while i >= 0 :
    #     if (expr[i] == "+" or expr[i] == "-" or expr[i] == "*" or expr[i] == "/" or expr[i] == "%" ):
    #         num = num[::-1]
    #         num_stack.append(num)
    #         num_stack.append(expr[i])
    #         num = ""
    #     elif (expr[i] == ","):
    #         num = num[::-1]
    #         num_stack.append(num)
    #         num = ""
    #     else:
    #         num += expr[i]
    #     i -= 1
    # print(num_stack) 
    
    return eval(expr)
    

def doIN(toIN):
    if (toIN[0:6] == "STRING"):
        toIN = toIN[8:]
        toIN = toIN[:-1]
    elif (toIN[0:3] == "NUM"):
        toIN = toIN[4:]
    elif (toIN[0:4] == "EXPR"):
        toIN = evalExpresstion(toIN[5:])
    print(toIN)

def doASSIGN(varname, varalue):
    symbols[varname[4:]] = varalue

def getVARIABLE(varname):
    varname = varname[4:]
    if varname in symbols :
        return symbols[varname]
    else:
        return"VARIABLE ERROR : UNFIND VARIABLE" 
        exit()

def getDAUVAO(string , varname):
    i = input(string[2:-1] + " ")
    symbols[varname] = "STRING:\"" + i + "\""

def parse(toks):
    # print(toks)
    i = 0
    while  (i < len(toks)) :
        if toks[i] == "KTNEU" :
            i += 1
        elif toks[i] + " " + toks[i + 1][0 : 6] == "IN STRING" or toks[i] + " " + toks[i + 1][0 : 3] == "IN NUM" or toks[i] + " " + toks[i + 1][0 : 4] == "IN EXPR" or toks[i] + " " + toks[i + 1][0 : 3] == "IN VAR":
            if toks[i + 1][0:6] == "STRING":
                doIN(toks[i + 1])
            elif  toks[i+1][0:3] == "NUM":
                doIN(toks[i + 1])
            elif  toks[i+1][0:4] == "EXPR":
                doIN(toks[i + 1])
            elif  toks[i+1][0:3] == "VAR":
                doIN(getVARIABLE(toks[i+1]))       
            i += 2
 
        elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
            if toks[i + 2][0:6] == "STRING":
                doASSIGN(toks[i] ,toks[i+2])
            elif  toks[i+2][0:3] == "NUM":
                doASSIGN(toks[i] ,toks[i+2])
            elif  toks[i+2][0:3] == "VAR":
                doASSIGN(toks[i] ,getVARIABLE(toks[i+2]))
            elif  toks[i+2][0:4] == "EXPR":
                doASSIGN(toks[i] ,"NUM:" + str(evalExpresstion(toks[i+2][5:]))) ## Chuyen ve dang STRING
            i += 3
        elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "DAUVAO STRING VAR" :
            getDAUVAO(toks[i+1][6:],toks[i+2][4:])
            i+=3
        elif toks[i] + " " + toks[i+1][0:9]+ " " + toks[i+2] + " " + toks[i+3][0:9] == "MOTA NGOACTRAI IN NGOACPHAI":
            print("Hàm in : in (chuỗi , số , phương thức , biến ) ")
            print("vd : in \"Helloword\" , in 3 , in $biến")
            print("in các giá trí vào một luồng")
            i+=4
        elif toks[i] + " " + toks[i+1][0:9]+ " " + toks[i+2] + " " + toks[i+3][0:9] == "MOTA NGOACTRAI DAUVAO NGOACPHAI":
            print("Hàm đầu vào (INPUT): dauvao \"Chuỗi muốn nhập\" $có thể gán biến" )
            print("Ví dụ : dauvao \"Nhập Tên bạn vô \" $name ")
            print("Ví dụ : in $name")
            i+=4
        elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2] + " " + toks[i+3][0:3] + " " + toks[i+4] == "NEU NUM EQEQ NUM THI" :
            if toks[i+1][4:] == toks[i+3][4:] :
                print("Found True Math")
            else :
                print("False")
            i+=5
        
          
        
       
       
    # In cac directory
    #print(symbols)
        
def run():
    data =  open_file(argv[1])
    toks =  lex(data)
    parse(toks)

run()