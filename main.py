import sys
scopeVariable = []
scopeVariable.append({})
scope_count = 0
errorcode = 0
operators = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "STAR",
    "/": "SLASH",
    "(": "LEFT_PAREN",
    ")": "RIGHT_PAREN",
    "{": "LEFT_BRACE",
    "}": "RIGHT_BRACE",
    ",": "COMMA",
    ";": "SEMICOLON",
    ".": "DOT",
    "=": "EQUAL",
    "!": "BANG",
    ">": "GREATER",
    "<": "LESS",
    '"':"STRING"
}
reserved_word = {
    "and": "AND",
    "class":"CLASS",
    "else":"ELSE",
    "false":"FALSE",
    "for" : "FOR",
    "fun" : "FUN",
    "if": "IF",
    "nil" :"NIL",
    "or" : "OR",
    "print" : "PRINT",
    "return" : "RETURN",
    "super" : "SUPER",
    "this" : "THIS",
    "true" : "TRUE",
    "var" : "VAR",
    "while" : "WHILE"
}
alp = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
num = "1234567890"
cmnd = ['tokenize','parse',"evaluate","run"]
def getVariable(b):
    i = len(scopeVariable)-1
    while(i >= 0 ):
        if(b in scopeVariable[i]):
            return scopeVariable[i][b]
        i-=1
    return None
    
def removeSpcTb(s):
    temp = ""
    itr = 0 
    while itr < len(s):
        if s[itr] == '"':
            temp+='"'
            itr += 1
            while itr < len(s) and s[itr]!='"':
                temp += s[itr]
                itr+=1
            temp+='"'
            itr+=1
        elif s[itr] == " " or s[itr] == '\t':
            itr+=1
            continue
        else: 
            temp+=s[itr]
            itr+=1
    return temp

def arithmeticCalculation (v2,v1,operator):
    # print(v1," ",v2," ",operator)
    v1 = getVariable(v1) if(getVariable(v1) != None) else v1
    v2 = getVariable(v2) if (getVariable(v2) != None) else v2
    # if( v2 in scopeVariable[-1] and scopeVariable[-1][v2] != 'nil'):
    #     v2 = scopeVariable[-1][v2]
    if(operator == "*"):  return v1*v2
    if(operator == "+"):  return v1+v2
    if(operator == "/"):  return v1/v2
    if(operator == "-"):  return v1-v2
    if(operator == ">"): return v1>v2
    if(operator == "<"): return v1<v2
    if(operator == ">="): return v1>=v2
    if(operator == "<="): return v1<=v2
    if(operator == "=="): return v1==v2
    if(operator == "!="): return v1!=v2
    
def variableS( a , b  ):
    # print( a , "--" , b)
    if getVariable(a) != None:
        a = getVariable(a)
    scopeVariable[-1][b] = a  
    # print(scopeVariable)
    return a 
   
def variableT( a , b  ):
    # print( a , "--" , b)
    i = 0
    while i < len(scopeVariable):
        if a in scopeVariable[i]:
            scopeVariable[i][a] = b
            # print(scopeVariable)
            return a
        i+=1        
    if getVariable(a) != None:
        a = getVariable(a)
    scopeVariable[-1][b] = a  
    # print(scopeVariable)
    return a   
def parenthesis(s,itr,error_message,line_number):
    global errorcode
    opn = 1
    close =0
    temp = ""
    itr+=1
    while(itr < len(s) and (s[itr] != ')' or close != opn-1)):
        temp += s[itr]
        if(s[itr] == ')'): close +=1
        if(s[itr] == '('): opn +=1
        itr+=1
    if(itr < len(s) and s[itr]!=')' or itr>= len(s)):
        errorcode = 65
        error_message.append(f"[line {line_number + 1}] Error at ')': Unterminated string.")
        return "" , -1
    if(itr < len(s) and s[itr]==')'):itr+=1
    return temp , itr

def alphabet(s,count):
    temp=""
    while count < len(s) and ( s[count] in alp):
        temp+=s[count]
        count+=1
    return temp,count

def calculate(s,error_message,line_number):
    global errorcode
    s= removeSpcTb(s)
    count = 0 
    result = []
    operator = []
    while count < len(s):
        if s[count] == '!':
            itr = count +1
            temp1 = ""
            if(itr<len(s) and s[itr]=="="):
                operator.append("!=")
                count = itr+1
                continue
            if s[itr] == "(":
                p , itr = parenthesis(s,itr,error_message,line_number)
                if(itr == -1) : return ""
                getString = calculate(temp1,line_number,error_message)
                if(getString == "true"):
                    result.append("false")
                elif(getString == "false" or getString == "nil" ):
                    result.append("true")
                # elif(getString == 0): result.append("true")
                else: result.append("false")
                count=itr
                continue
            while itr < len(s) and (s[itr] in alp or s[itr] in num or s[itr] in operators ):
                temp1+=s[itr]
                itr+=1
            # print(temp1)
            if len(temp1) >0:
                getString = calculate(temp1,line_number,error_message)
                if(getString == "true"):
                    result.append("false")
                elif(getString == "false" or getString == "nil" ):
                    result.append("true")
                # elif(getString == 0): result.append("true")
                else: result.append("false")
                count=itr
                continue
            else :
                result.append("!")
                continue
        if(s[count]=='"'):
            # print(s,"++",s[count])
            temp=""
            while(count+1 < len(s) and s[count+1]!='"'):
                temp+= s[count+1]
                count+=1
            # print(temp,"===")
            if count+1 < len(s) and s[count+1] != '"' or count+1 >= len(s):
                # print(temp,"--")
                error_message.append(f'[line {line_number + 1}] Error at ": Expect expression')
                flag = 1
                errorcode = 65
                break
            # print(temp)
            result.append(temp)
            count+=2
            continue
        if s[count] in alp :
            temp , count = alphabet(s,count)
            result.append(temp)
            continue
        if s[count] == "(":
            p , itr = parenthesis(s,count,error_message,line_number)
            if(itr == -1) : return ""
            getString = calculate(p,error_message,line_number)
            if(getString==""): return ""
            result.append(getString)
            count = itr
            continue
        if s[count] == 'g' and count + 4 < len(s) and s[count:count+5] == "group":
            count +=5
            continue
        if s[count] in ["*" , "/" , "+" , "-","<",">","<=",">=","==","!=","=" ] and len(result)>0:
            if s[count] in ["=","<",">","!"] and count+1 < len(s) and s[count+1]=="=":
                operator.append(s[count]+"=")
                count+=1
            else :operator.append(s[count])
            count+=1
        if s[count] in num or s[count] == '.' or s[count] in ["+","-","*","/"]:
            t = ""
            if s[count] in ["+","-","*","/"]:
                t = ""+s[count]
                count+=1
            if s[count] == "(":
                p , itr = parenthesis(s,count,error_message,line_number)
                # if(itr == -1) : return ""
                getString = calculate(p,error_message,line_number)
                # if(getString==""): return ""
                result.append(-getString)
                count = itr
                continue
            while count < len(s) and ( s[count] in num or s[count] == '.'):
                t+=s[count]
                count+=1
            # print(t)
            value1 = float(t)
            # print(value1)
            if len(operator) > 0 :
                value2 = result.pop()
                op = operator.pop()
                if op in ["*","/"] and (isinstance(value1,str) or isinstance(value2,str)):
                    error_message.append(f"Operand must be a number.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                if op in ['+',">","<","<=",">="] and ((value1 in ["true","false"] or value2 in ["true","false"]) or (type(value1) != type(value2))):
                    error_message.append(f"Operand must be a number.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                if op == '-' and ((value1 in ["true","false"] or value2 in ["true","false"]) or (isinstance(value1,str) or isinstance(value2,str))):
                    error_message.append(f"Operand must be a number.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                result.append(arithmeticCalculation(value1,value2,op))
            else : result.append(value1)
    while len(operator)>0 :
        v2 = result.pop()
        v1 = result.pop()
        op = operator.pop()
        # print(v1 ," ",v2)
        if op in ["*","/"] and (isinstance(v2,str) or isinstance(v1,str)):
            error_message.append(f"Operand must be a number.")
            error_message.append(f"[line {line_number + 1}]")
            errorcode = 70
            return ""
        if op in ['+',">","<","<=",">="] and ((v1 in ["true","false"] or v2 in ["true","false"]) or (type(v1) != type(v2))):
            error_message.append(f"Operand must be a number.")
            error_message.append(f"[line {line_number + 1}]")
            errorcode = 70
            return ""
        if op == '-' and ((v1 in ["true","false"] or v2 in ["true","false"]) or (isinstance(v1,str) or isinstance(v2,str))):
            error_message.append(f"Operand must be a number.")
            error_message.append(f"[line {line_number + 1}]")
            errorcode = 70
            return ""
        result.append(arithmeticCalculation(v2,v1,op))
    # print(result)
    if result[0] == True and not isinstance(result[0],float):return "true"
    if result[0] == False and not isinstance(result[0],float):return "false"
    return result[0]

def create_stack(s,line_number ,error_message):
    # print(s)
    global errorcode
    s = removeSpcTb(s)
    stack = []
    count = 0 
    while count < len(s): 
        if s[count] in alp :
            temp , count = alphabet(s,count)
            stack.append(temp)
            continue
        if s[count] == '!':
            itr = count +1
            temp1 = ""
            if(itr<len(s) and s[itr]=="="):
                stack.append("!=")
                count = itr+1
                continue
            if s[itr] == "(":
                p , itr = parenthesis(s,itr,error_message,line_number)
                if(itr == -1) : return ""

                getString = create_stack(temp1,line_number,error_message)
                if(getString == "true"):
                    stack.append("false")
                elif(getString == "false" or getString == "nil" ):
                    stack.append("true")
                elif(getString == 0): stack.append("true")
                else: stack.append("false")
                count=itr
                continue
            while itr < len(s) and (s[itr] in alp or s[itr] in num or s[itr] in operators ):
                temp1+=s[itr]
                itr+=1
            # print(temp1)
            if len(temp1) >0:
                getString = create_stack(temp1,line_number,error_message)
                if(getString == "true"):
                    stack.append("false")
                elif(getString == "false" or getString == "nil" ):
                    stack.append("true")
                elif(getString == 0): stack.append("true")
                else: stack.append("false")
                count=itr
                continue
            else :
                stack.append("!")
                continue
        if s[count] == '(':
            p , count = parenthesis(s,count,error_message,line_number)
            if(count == -1) : return ""
            
            getString = calculate(p,line_number,error_message)
            # print(getString,"...")
            if(getString == "") : return ""
            if(not isinstance(getString, float) and " " in getString):
                stack.append(f'"{getString}"')
            else: 
                stack.append(f"{getString}")
            continue
        if s[count] == '-' and ( s[count-1] in ["-","/","+","*","<",">",">=","<=","=","("] or count == 0 ):
            temp = ""
            count += 1
            dot = 0 
            if s[count] == "(":
                p , count = parenthesis(s,count,error_message,line_number)
                
                if(count == -1) : return ""
                getString = create_stack(p,line_number,error_message)
                
                if  isinstance(getString,bool) or (isinstance(getString,str) and any(char in '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for char in getString))  : 
                    error_message.append(f"Operand must be a number.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                stack.append(f"-{getString}")
                continue
               
            while count < len(s) and (s[count] in num or s[count] == "."):
                if s[count] == ".": dot+=1
                temp+=s[count]
                count+=1
            if count < len(s) and (s[count] in alp or s[count] == '"'):
                error_message.append(f"Operand must be a number.")
                error_message.append(f"[line {line_number + 1}]")
                errorcode = 70
                return ""
            temp = "-"+nums(temp,dot)+""
            stack.append(temp)
            continue
        if s[count]  == '"':
            temp=""
            while(count+1 < len(s) and s[count+1]!='"'):
                temp+= s[count+1]
                count+=1
            
            stack.append('"'+temp+'"')
            count+=2
            continue  
        unprocessed = ""
        dot = 0
        while count < len(s) and (s[count] in num or s[count] == '.'):
            if(s[count] == '.'):
                dot+=1
            unprocessed += s[count]
            count+=1
        if(unprocessed != ""):
            stack.append(nums(unprocessed,dot))
        else: 
            if( count + 1 < len(s) and s[count] in ["<",">","="] and s[count+1] == "="):
                stack.append(s[count]+s[count+1])
                count+=1
            else :stack.append(s[count])
            count+=1
    # print(stack)
    ans = (calculate("".join(stack),error_message,line_number))
    # print(ans)
    if isinstance(ans, float) and  int(ans) == ans :
        return str(int(ans)) 
    return str(ans)
def nums(s, dot):
    fullString = ""
    if(dot>0):
        t = s.rstrip("0")
    else : t=s
    if dot > 1:
        while dot > 1 and len(t) > 0 and t[-1] == ".":
            t = t[:-1]
            t = t.rstrip("0")
            dot -= 1
    if(dot>0):
        t = t.rstrip("0")
    if dot == 0:
        if t[-1] == ".":
            t += "0"
        else:
            t = t + ".0"
        fullString += "" + t
    else:
        if t[-1] == ".":
            t += "0"
        fullString += "" + t
    return fullString

def preFix(s,line_number,error_message):
    global errorcode
    s = removeSpcTb(s)
    stack = []
    count = 0 
    # print(s)
    while count < len(s):    
        if s[count] == '!':
            itr = count +1
            temp1 = ""
            if(itr<len(s) and s[itr]=="="):
                stack.append("!=")
                count = itr+1
                continue
            if s[itr] == "(":
                opn = 1
                close =0
                temp = ""
                itr+=1
                while(itr < len(s) and (s[itr] != ')' or close != opn-1)):
                    temp += s[itr]
                    if(s[itr] == ')'): close +=1
                    if(s[itr] == '('): opn +=1
                    itr+=1
                fullString = f"(! (group {parse(temp,line_number,error_message)}))"
                stack.append(fullString)
                if(itr < len(s) and s[itr]!=')' or itr>= len(s)):
                    error_message.append(f"[line {line_number + 1}] Error at ')': Unterminated string.")
                    errorcode = 65
                    return ""
                if(itr < len(s) and s[itr]==')'):itr+=1
                count = itr
                continue
            while itr < len(s) and (s[itr] in alp or s[itr] in num or s[itr] in operators ):
                temp1+=s[itr]
                itr+=1
            if len(temp1) >0:
                stack.append (f"(! {parse(temp1,line_number,error_message)})")
                count=itr
                continue
            else :
                stack.append("!")
                continue
        if s[count] == '(':
            opn = 1
            close =0
            temp = ""
            count+=1
            while(count < len(s) and (s[count] != ')' or close != opn-1)):
                temp += s[count]
                if(s[count] == ')'): close +=1
                if(s[count] == '('): opn +=1
                count+=1
            if(count < len(s) and s[count]!=')' or count>= len(s)):
                    error_message.append(f"[line {line_number + 1}] Error at ')': Expect expression.")
                    errorcode = 65
                    return ""
            getString = preFix(temp,line_number,error_message)
            if(getString == "") : return ""
            stack.append(f"(group {getString})")
            if(count < len(s) and s[count]==')'):count+=1
            continue
        if s[count] == '-' and ( s[count-1] in ["-","/","+","*","<",">",">=","<=","="] or count == 0 ):
            temp = ""
            count += 1
            dot = 0 
            if s[count] == "(":
                opn = 1
                close =0
                temp = ""
                count+=1
                while(count < len(s) and (s[count] != ')' or close != opn-1)):
                    temp += s[count]
                    if(s[count] == ')'): close +=1
                    if(s[count] == '('): opn +=1
                    count+=1
                if(count < len(s) and s[count]!=')' or count>= len(s)):
                    error_message.append(f"[line {line_number + 1}] Error at ')': Expect expression.")
                    errorcode = 65
                    return ""
                getString = preFix(temp,line_number,error_message)
                if(getString == "" ):return ""
                stack.append(f"(- (group {getString}))")
                if(count < len(s) and s[count]==')'):count+=1
                continue
            while count < len(s) and (s[count] in num or s[count] == "."):
                if s[count] == ".": dot+=1
                temp+=s[count]
                count+=1
            temp = "(- "+nums(temp,dot)+")"
            stack.append(temp)
            continue
        if s[count]  == '"':
            temp=""
            while(count+1 < len(s) and s[count+1]!='"'):
                temp+= s[count+1]
                count+=1
            stack.append(temp)
            count+=2
            continue
        unprocessed = ""
        dot = 0
        while count < len(s) and (s[count] in num or s[count] == '.'):
            if(s[count] == '.'):
                dot+=1
            unprocessed += s[count]
            count+=1
        if(unprocessed != ""):
            stack.append(nums(unprocessed,dot))
        else: 
            if( count + 1 < len(s) and s[count] in ["<",">","="] and s[count+1] == "="):
                stack.append(s[count]+s[count+1])
                count+=1
            else :stack.append(s[count])
            count+=1
    # print(stack)
    operator = [] 
    result = []
    count = 0
    while count < len(stack) :
        if stack[count]  in ["(" , "*" , "/" , "+" , "-","<",">","<=",">=","==","!="]:
            operator.append(stack[count])
            count+=1
        elif stack[count] == ')':
            s1 = result.pop()
            result.append(f"(group {s1})")
            operator.pop()
            count+=1
        else:
            result.append(stack[count])
            if len(operator) > 0 and  operator[-1] in ['*','/',"+","-"]:
                if len(result)<2 :
                    errorcode = 65
                    error_message.append(f"[line {line_number + 1}] Error at '{operator[-1]}': Unterminated string.")
                    return ""
                s3 = operator.pop()
                s1 = result.pop()
                s2 = result.pop() 
                result.append(f"({s3} {s2} {s1})")
            count+=1
    while len(operator)>0:
        if operator[-1] in ["<",">","<=",">="]:
            revop = []
            revres = []
            while len(operator) > 0  and  operator[-1] in ["<",">","<=",">=","==","!="] :
                revop.append(operator.pop())
            for i in range(1+len(revop)):
                revres.append(result.pop())
            while(len(revop)>0):
                s1 = revres.pop()
                s2 = revres.pop()
                s3 = revop.pop()
                revres.append(f"({s3} {s1} {s2})")
            result.append("".join(revres))
            continue
        if len(result)<2 :
            errorcode = 65
            error_message.append(f"[line {line_number + 1}] Error at ')': Unterminated string.")
            return ""
        s1 = result.pop()
        s2 = result.pop()
        s3 = operator.pop()
        result.append(f"({s3} {s2} {s1})")
    return "".join(result)
             
def parse(string,line_number,error_message):
    # print(string,"--")
    global errorcode
    count = 0
    token = []
    fullString  = ""
    while count < len(string) : 
        if string[count] in alp :
            s=""
            while count < len(string) and ( string[count] in alp or string[count] in num):
                s+=string[count]
                count+=1
            if s in reserved_word:
                fullString += ""+s
        elif string[count] in num or string[count] in operators :
            flag = 0
            s=""
            while(count <len(string)  
                  and ((string[count] in num ) or  string[count] in operators or string[count] in alp or string[count] in [" ","\t"])):
                if(string[count]=='"'):
                    temp=""
                    while(count+1 < len(string) and string[count+1]!='"'):
                        temp+= string[count+1]
                        count+=1
                    if count+1 < len(string) and string[count+1] != '"' or count+1 >= len(string):
                        error_message.append(f'[line {line_number + 1}] Error at ": Expect expression')
                        flag = 1
                        errorcode = 65
                        break
                    s += '"'+temp+'"'
                    count+=1
                else: s+=""+string[count]
                count+=1
            # print(s,"....")
            if(flag==1) :  return ""
            postfix = preFix(s,line_number,error_message)
            if(postfix == ""): return ""
            fullString += postfix
            continue    
        else: count+=1
    return fullString

def evaluate(string , line_number , error_message):
    count = 0
    token = []
    fullString  = ""
    return create_stack(string,line_number,error_message)
    
def infix_to_postfix(expression,line_number , error_message):
    expression = removeSpcTb(expression)
    global errorcode
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '<': 0, '>': 0, '<=': 0, '>=': 0, '==': 0,'=':-1, '!=': 0, '!': 4, '||': -1, '&&': -1, '(': -1, ')': -1}
    associativity = {'+': 'L', '-': 'L', '*': 'L', '/': 'L', '^': 'R', '!': 'R', '||': 'L', '&&': 'L'}
    stack = []
    output = []
    i = 0
    global num
    # print(expression)
    while i < len(expression):
        token = expression[i]

        if token.isdigit() or (token == '-' and i>0 and expression[i-1] in ["+","*","/",">","<","="]):  # Operand
            num = token
            while i + 1 < len(expression) and expression[i + 1].isdigit():
                i += 1
                num += expression[i]
            output.append(num)
        elif token in alp:
            word = token
            while i+1 < len(expression) and (expression[i+1] in alp or expression[i+1] in num):
                i += 1
                word += expression[i]
            if getVariable(word) != None:
                output.append(word)
            elif word in ["false",'true']:
                output.append(word)
            else :
                error_message.append(f"Undefined variable '{word}'")
                error_message.append(f"[line {line_number + 1}]")
                errorcode = 70
                return []
        elif token == "=" and i + 1 < len(expression) and expression[i+1] != '=':
            i += 1
            output.append((evaluateRun(expression[i:],line_number,error_message)))
            variableT(output[-2],output[-1])
            i = len(expression)
            output.pop()
            # print(scopeVariable)
            break
        elif token == '"':  # String literal
            string_literal = ''
            i += 1
            while i < len(expression) and expression[i] != '"':
                string_literal += expression[i]
                i += 1
            output.append(f'"{string_literal}"')
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '(' from stack
        else:  # Operator
            if i + 1 < len(expression) and expression[i:i+2] in precedence:
                token = expression[i:i+2]
                i += 1
            while (stack and precedence[stack[-1]] > precedence[token]) or \
                  (stack and precedence[stack[-1]] == precedence[token] and associativity.get(token, 'L') == 'L'):
                output.append(stack.pop())
            stack.append(token)
        i += 1

    while stack:
        output.append(stack.pop())

    return output

def evaluate_postfix(expression,line_number,error_message):
    stack = []
    global num
    global errorcode
    # print(expression)
    for token in expression:
        if isinstance(token , float) or isinstance(token , int) or token.isdigit() or token.lstrip('-').isdigit():
            stack.append(int(token))
        elif getVariable(token) != None:
            stack.append(getVariable(token))
        elif token in 'nil':
            stack.append('nil')
        elif token == 'true':
            stack.append(True)
        elif token == 'false':
            stack.append(False)
        elif token.startswith('"') and token.endswith('"'):  # String literal
            stack.append(token.strip('"'))
        elif token == "=":
            a = stack.pop()
            b = stack.pop()
            stack.append(variableT(a,b))
        else:
            if token == '!':
                a = stack.pop()
                stack.append(not a)
            else:
                
                b = stack.pop()
                a = stack.pop()
                if getVariable(b) != None : b = getVariable(b)
                if getVariable(a) != None : b = getVariable(a)
                if (isinstance(a,bool) and not isinstance(b,bool)) or (isinstance(b,bool) and not isinstance(a,bool)):
                    # print("error ",a," ",b)
                    error_message.append(f"Operands must be two numbers or two strings.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                if(type(b) != type(a) and not ((isinstance(b,int) or isinstance(b,float)) and (isinstance(a,int) or isinstance(a,float)))):
                    # print("error ",a," ",b)
                    error_message.append(f"Operands must be two numbers or two strings.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                if isinstance(b,str) and isinstance(a,str) and token in ["-",'*',"/",">","<"] :
                    # print("error ",a," ",b)
                    error_message.append(f"Operand must be a number.")
                    error_message.append(f"[line {line_number + 1}]")
                    errorcode = 70
                    return ""
                stack.append(arithmeticCalculation(b,a,token))
    # print(stack[0])
    if(getVariable(stack[0]) != None) :
        token = getVariable(stack[0])
        if isinstance(token,str) and token.startswith('"') and token.endswith('"'):  # String literal
            return token.strip('"')
        return token
    return stack[0]

def evaluateRun(string , line_number , error_message):
    postfix_expression = infix_to_postfix(string,line_number , error_message)
    # print("Postfix Expression:", ' '.join(postfix_expression))
    if(len(postfix_expression)==0):  return ""
    result = evaluate_postfix(postfix_expression,line_number,error_message)
    # print("Result:", result)
    return result

def variable(string , line_number , error_message):
    string = removeSpcTb(string)
    # print(string,"--")
    ar = string.split('=')
    # print(ar)
    if(len(ar) == 1 ) : 
        scopeVariable[-1][ar[0]] = 'nil'
    while(len(ar) > 1):
        global errorcode
        a = evaluateRun(ar.pop(),line_number,error_message)
        # print(a)
        b = ar.pop()
        # print( a , " = " , b)
        if( (isinstance(a,str) and a not in scopeVariable[-1]) or (isinstance(a,str) and a.startswith('"') and a.endswith('"')) or (isinstance(a,str) and a.isdigit()) or  isinstance(a,int) or isinstance(a,float)):
            if(isinstance(a,str) and a.isdigit()):
                a = int(a)
            scopeVariable[-1][b] = a
            ar.append(scopeVariable[-1][b])
        elif( a in scopeVariable[-1] ):
            scopeVariable[-1][b] =scopeVariable[-1][a]
            ar.append(scopeVariable[-1][a])
        else : 
            errorcode = 70
        
        
def runIt(s,line_number,error_message):
    # print(s)
    global errorcode
    global scope_count
    global num
    count = 0 
    fullString = ""
    while count<len(s):
        if s[count] in [' ',"\t","\n"] : 
            count+=1 
            continue
        elif s[count] in alp :
            temp=""
            while count < len(s) and ( s[count] in alp or s[count] in num):
                temp+=s[count]
                count+=1
            if temp == "print":
                temp1 = s[count:]
                if(len(temp1) == 0):
                    errorcode = 65
                    return ""
                getString  = (evaluateRun(temp1,line_number,error_message))
                if(getString == "") : break
                if( getString == False and isinstance(getString , bool)) : fullString += "false"
                elif ( getString == True and isinstance(getString , bool)): fullString += "true"
                else :
                    if( isinstance(getString,float) and getString == int(getString) ):
                        getString = int(getString)
                    fullString+=str(getString)
                if count < len(s) and s[count] == ';': count+=1
            elif temp == "var":
                # if count < len(s) and s[count] in [' ',"\t","\n"] : count +=1
                # var = ""
                # while count < len(s) and s[count] in alp:
                #     var += s[count]
                #     count+=1
                # if count < len(s) and s[count] in [' ',"\t","\n"] : count +=1
                # if(count >= len(s)):
                #     # print("nil ->" , var )
                #     scopeVariable[-1][var] = 'nil'
                #     break
                # if(s[count] == "="):
                #     count+=1
                # # print(var)
                # assign  = evaluateRun(s[count:],line_number,error_message)
                # scopeVariable[-1][var] = assign
                variable(s[count:],line_number,error_message)
                break
            else:
                while count < len(s):
                    temp+=s[count]
                    count+=1
                getString = evaluateRun(temp,line_number,error_message)
                if(getString == "") :
                    # errorcode = 70
                    return ""
        elif s[count] == "{":
            scope_count +=1
            scopeVariable.append({})
            count+=1
        elif s[count] == "}":
            scope_count -=1
            scopeVariable.pop()
            count +=1
        else : 
            # print(s[count:])
            getString = evaluateRun(s[count:],line_number,error_message)
            if(getString == "") : 
                return ""
            break
    return fullString

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command not in cmnd:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)
    with open(filename) as file:
            file_contents = file.read() 
    global errorcode 
    error_message = []
    token = []
    line_count = 0
    if command == "tokenize":
        for line_number, string in enumerate(file_contents.split("\n")):
            count_chr = 0
            while count_chr < len(string):
                if string[count_chr] in operators:
                    match (string[count_chr]):
                        case "=":
                            if count_chr + 1 < len(string) and string[count_chr + 1] == "=":
                                token.append(f"EQUAL_EQUAL == null")
                                count_chr += 1
                            else:
                                token.append(
                                    f"{operators[string[count_chr]]} {string[count_chr]} null"
                                )
                        case "!":
                            if count_chr + 1 < len(string) and string[count_chr + 1] == "=":
                                token.append(f"BANG_EQUAL != null")
                                count_chr += 1
                            else:
                                token.append(
                                    f"{operators[string[count_chr]]} {string[count_chr]} null"
                                )
                        case ">":
                            if count_chr + 1 < len(string) and string[count_chr + 1] == "=":
                                token.append(f"GREATER_EQUAL >= null")
                                count_chr += 1
                            else:
                                token.append(
                                    f"{operators[string[count_chr]]} {string[count_chr]} null"
                                )
                        case "<":
                            if count_chr + 1 < len(string) and string[count_chr + 1] == "=":
                                token.append(f"LESS_EQUAL <= null")
                                count_chr += 1
                            elif count_chr + 1 < len(string) and string[count_chr + 1] == "|":
                                while(count_chr<len(string) and string[count_chr ]!=">"):
                                    count_chr+=1  
                            else:
                                token.append(
                                    f"{operators[string[count_chr]]} {string[count_chr]} null"
                                )
                        case "/":
                            if count_chr + 1 < len(string) and string[count_chr + 1] == "/":
                                count_chr += len(string[2:]) + 1
                                pass
                            else:
                                token.append(
                                    f"{operators[string[count_chr]]} {string[count_chr]} null"
                                )
                        case '"':
                            s=""
                            while(count_chr+1 < len(string) and string[count_chr+1]!='"'):
                                s+= string[count_chr+1]
                                count_chr+=1
                            if(count_chr == len(string)-1 and string[count_chr]!='"'):
                                errorcode = 65
                                error_message.append(
                                f"[line {line_number + 1}] Error: Unterminated string."
                                )  
                            else :
                                token.append(
                                f'STRING "{s}" {s}'
                            )
                            count_chr+=1
                        case _:
                            token.append(
                                f"{operators[string[count_chr]]} {string[count_chr]} null"
                            )
                elif string[count_chr] in num :
                    dot = 1
                    s=""
                    while(count_chr <len(string) and (string[count_chr] not in alp) and not ( string[count_chr] in [" ", "\t"]) and ((string[count_chr] in num) or (dot>0 and operators[string[count_chr]]=="DOT" ))):
                        if((string[count_chr] not in num) and operators[string[count_chr]]=="DOT"):
                            s+="."
                            dot-=1
                        else: s+=""+string[count_chr]
                        count_chr+=1
                    if count_chr <len(string) and string[count_chr] in alp:
                        error_message.append(
                            f"[line {line_number + 1}] Error: Wrong Identifier:"
                        )
                    t=s.rstrip('0')
                    if(dot==0):
                        if(t[-1]=='.'):
                            t+='0'
                        token.append(
                        f"NUMBER {s} {t}"
                        )
                    else:
                        token.append(
                        f"NUMBER {s} {s}.0"
                        )
                    continue    
                elif string[count_chr] in [" ", "\t"]:
                    count_chr += 1
                    continue
                elif string[count_chr] in alp :
                    s = ""
                    while(count_chr < len(string) and (string[count_chr] != " " and string[count_chr] != "\t") 
                        and ( string[count_chr] not in operators )):
                        s+=string[count_chr]
                        count_chr+=1
                    if(s in reserved_word):
                        token.append(f"{reserved_word[s]} {s} null")
                    else:
                        token.append(f"IDENTIFIER {s} null")
                    continue
                else:
                    errorcode = 65
                    error_message.append(
                        f"[line {line_number + 1}] Error: Unexpected character: {string[count_chr]}"
                    )
                count_chr += 1
        token.append("EOF  null")
    if command == 'parse' :
        for line_number, string in enumerate(file_contents.split("\n")):
            count = 0 
            fullString = parse(string , line_number , error_message) 
            if fullString != "":
                token.append(fullString)
    if command == 'evaluate':
        for line_number, string in enumerate(file_contents.split("\n")):
            count = 0 
            fullString = evaluate(string , line_number , error_message) 
            if fullString != "":
                if fullString == False :
                    token.append("false")
                if fullString == True :
                    token.append("true")
                else:
                    token.append(fullString)
            if(len(error_message)>0 ):break
    if command == 'run':
        for line_number, string in enumerate(file_contents.split(";")):
            line_count+=1
            count = 0 
            fullString = runIt(string , line_number , error_message) 
            if fullString != "":
                if fullString == False :
                    token.append("false")
                if fullString == True :
                    token.append("true")
                else:
                    token.append(fullString)
            if(len(error_message)>0):break
    if(scope_count > 0 ):
        errorcode = 65
        line_count = len(file_contents.split('\n'))
        error_message.append(f"[line {line_count-1}]Error at end: Expect '{'}'}'")
    print("\n".join(error_message), file=sys.stderr)
    if(scope_count == 0):
        print("\n".join(token))
    exit(errorcode)

if __name__ == "__main__":
    main()
