# James Fallon 
# 4/15/2019
# Interpretor Project

from sys import*

varslist = []
tok = []
expression = []

def get(data):
  print(data)
  #Token storage
  token = ""
  pretoken = ""
  contents = list(data)                                     # Put data on list
  # Remove newline
  contents.remove("\n")
  #Push all contents of list onto the stack and give error for invalid contents
  for char in contents:
    token += char
    if token == "T":
      tok.append("T")
      token = ""
    elif token == "F":
      tok.append("F")
      token = ""
    elif token == "#":
      tok.append("#")
      token = ""
    elif token == "(":
      tok.append("(")
      token = ""
    elif token == ")":
      tok.append(")")
      token = ""
    elif token == "~":
      tok.append("~")
      token = ""
    elif token == ";":
      tok.append(";")
      token = ""
    elif token == "-":
      tok.append("-")
      token = ""
    elif token == ".":
      tok.append(".")
      token = ""
    elif token == "^":  # Or condition
      tok.append("^")
      token = ""
    elif token == "V":  # And condition
      tok.append("V")
      token = ""
    # var condition
    elif(token.islower()):
      tok.append(token)
      varslist.append(token)    # Append to var stack
      token = ""
    # Append :=  and -> together
    elif(not not pretoken):
        if(pretoken == "-" and token == ">"):
            tok.append("->")
            token = ""
            pretoken = ""
        elif(pretoken == ":" and token == "="):
            tok.append(":=")
            token = ""
            pretoken = ""
        else:                                                           
            print("Error, Can't put white space in between -> or := tokens")    #Throw error if whitespace
            return False
    elif token == ":":
        pretoken = ":"
        token = ""
    elif token == "-":
      pretoken = "-"
      token = ""
    # White space remover
    elif token  == " ":
      token = ""
      pretoken = ""
    else:
      print("Error, given token doesn not exist")
      return False
  tok.reverse()             # Reverse tokens before pop()
  return tok


# Bool_def
def B():
  
  if(VA(tok.pop())):                         # Check VA
    if IT(tok.pop()):                        # Check IT
        if(tok.pop() == "."):                # Check "."
            return True
        else:
            return False
    else:
        return False
  else:
    return False
    
    
# Variable Assignment
def VA(lex):
  
  if(lex == "#"):                           # Check "#"
      tem1 = tok.pop()
      if(tem1.islower()):                   # Check for var
          tem1 = tok.pop()
          if(tem1 == ":="):                 # Check ":="
              tem1 = tok.pop()
              if(IT(tem1)):                 # Check IT
                  if not tok:   
                    if VA(tok):             # Check VA
                        return True
                    else:
                        return False
                  elif("." in tok and "#" not in tok):    # Complete iteration?
                        return True
                  else:
                        tem1 = tok.pop()
                        if(VA(tem1)):
                            return True
                        else:
                            return False
              else:
                return False
          else:
              return False
      else:
          return False
  elif(not lex):                            # Check empty
    return True
  else:
    return False


# Implied Term
def IT(lex):
  tem = ""
  if(CT(lex)):                  # Call connect Term
      if not tok:
        if(IT_Tail(tok)):       # Call implied Term Tail
            return True
        else:
            return False
      else:
        # Continue
        tem = tok.pop()
        if(tem == ";"):
            tok.append(";")
            return True
        elif(tem == "."):
            tok.append(".")
            return True
        elif(IT(tem)):
            return True
        else:
            return False
  else:
      return False
     
        
# Implied Term Tail
def IT_Tail(lex):   
  if(lex == "->"):                  # Check for "->""
      if(CT(tok.pop())):
    
        # Expression logic for Implied Tail
        tem1 = expression.pop()
        tem2 = expression.pop()
        if(tem1 == "T" and tem2 == "F"):
            expression.append("F")
        else:
            expression.append("T")
        if not tok:
            if IT(tok):
                return True
            else:
                return False
        else:
            # Continue
            tem3 = tok.pop()
            if(IT_Tail(tem3)):
                return True
            elif(tem3 == ";"):
                tok.append(";")
                return True
            elif(tem3 == ")"):
                tok.append(")")
                return True
            elif(tem3 == "."):
                tok.append(".")
                return True
            else:
                return False
      else:
        return False
  # Continue
  elif(not lex):
      return True
  elif(lex == ";"):
      tok.append(";")
      return True
  elif(lex == ")"):
      tok.append(")")
      return True
  elif(lex == "."):
      
      tok.append(".")
      return True
  else:
      return False


# Connected Term
def CT(lex):
  if(L(lex)):                   # Call Literal
      
      if not tok:
    
          if CT_Tail(tok):      # Call CT_Tail
              return True
          else:
              return False
      else:
          tem = tok.pop()
          if(CT_Tail(tem)):     # Call CT_Tail
             
              return True
          else:
              
              return False
  else:
      
      return False
      

def CT_Tail(lex):

    if(lex == "V"):             # Check if or
        if(L(tok.pop())):       # Call Literal
            
            tem1 = expression.pop()
            tem2 = expression.pop()
            # Logic for Or
            if(tem1 == "T" or tem2 == "T"):
                expression.append("T")
            else:
                expression.append("F")
            if not tok:
                if(CT_Tail(tok)):   # Call CT tail
                    return True
                else:
                    return False
            else:
                tem3 = tok.pop()
                # Continue
                if(CT(tem3)):
                    return True
                elif(tem3 == "->"):
                    tok.append("->")
                    return True
                elif(tem3 == ";"):
                    tok.append(";")
                    return True
                elif(tem3 == ")"):
                    tok.append(")")
                    return True
                elif(tem3 == "."):
                    tok.append(".")
                    return True
                else:
                    return False
        else:
            return False    
    elif(lex =="^"):                    # Check if And
        
        if(L(tok.pop())):

            tem1 = expression.pop()
            tem2 = expression.pop()
            # Logic for And
            if(tem1 == "T" and tem2 == "T"):
                expression.append("T")
            else:
                expression.append("F")
            if not tok:
                if(CT_Tail(tok)):
                    return True
                else:
                    return False
            else:
                # Continue
                tem3 = tok.pop()
                if(CT_Tail(tem3)):
                    return True
                elif(tem3 == "->"):
                    tok.append("->")
                    return True
                elif(tem3 == ";"):
                    tok.append(";")
                    return True
                elif(tem3 == ")"):
                    tok.append(")")
                    return True
                elif(tem3 == "."):
                    tok.append(".")
                    return True
                else:
                    return False
        else:
            return False
    # Continue
    elif(not lex):
        return True
    elif(lex == "->"):
        tok.append("->")
        return True
    elif(lex == ";"):
        return True
    elif(lex == ")"):
        tok.append(")")
        return True
    elif(lex == "."):
        tok.append(".")
        return True
    else:
        return False
    
    
# Literal
def L(lex):
    if(A(lex)):                         # Call Atom
        return True
    elif(lex == "~"):                   # Check for ~
        tem1 = tok.pop()
        
        if(L(tem1)):
            expression.pop()
            if(tem1 == "T"):
                expression.append("F")
            else:
                expression.append("T")
            return True
        else:
            return False
    else:
        return False
    
    
# Atom
def A(lex):
  if( lex == "T"):
    expression.append("T")
    return True
  elif(lex == "F"):
    expression.append("F")
    return True
  elif(lex == "("):
      if(IT(tok.pop())):
        if(tok.pop() == ")"):
            return True
        else:
            return False
  elif(lex in varslist):        # Does variable exist?
      return True
  elif(lex == "."):
    tok.append(".")
    return True
  else:
      return False


# Main
def main():
  # Open and read File
  fh = open("testinterpretor.txt","r")
  data = fh.read()

  to = get(data)
    
  # Call the Boolean function
  if(B()):
    print("Value of expression: ", expression.pop())
    print("Valid Syntax")
  else:
    print("Invalid Syntax")
  return
  
main()