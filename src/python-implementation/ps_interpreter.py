import sys

current_line = 0
total_lines_to_interpret = 0

RESERVED_KEYWORDS = list(enumerate(
    ["DECLARE", "INPUT", "OUTPUT", "FOR", "REPEAT", "WHILE", "IF", "ELSE"]
))

TOKENS_ENUM = list(enumerate(
    [
        "binary_op", "equals", "open_paren", "close_paren",
        "integer", "string", "bool", "real", "identifier", "assignment"
    ]
, start=len(RESERVED_KEYWORDS)))


# read the file
def read_file(file_path:str):
    global total_lines_to_interpret

    f = open(file_path, "r")
    f = f.read()
    f = f"{f} "

    f = f.replace("\n", " ")

    return f

# validate the file path
def validate_file(file_path:str):
    if file_path[-3:] == '.ps':
        return True
    else:
        return False

# simple error printer
def error_handler(line_num:int, message:str):
    print(f"[LINE {line_num}] Error: {message}")

# checking and tokenising functions for alpha types
def is_alpha(a:str):
    return a.upper() != a.lower()
def get_alpha_token(alpha:str):
    for token in TOKENS_ENUM:
        if token[1] == "identifier":
            return (token[0], alpha)

# checking and tokenising for integer types
def is_int(i:str):
    return i.isdigit()
def get_int_token(integer:str):
    for token in TOKENS_ENUM:
        if token[1] == "integer":
            return (token[0], integer)
        
# check for skippable characters
def is_skippable(sk:str):
    return sk == " " or sk == "\t"# or sk == "\n" # we need \n to get current line we are on, for debugging purposes

def create_token(tok:str, t_type:str):
    f = False
    for token in TOKENS_ENUM:
        if token[1] == t_type:
            f = True
            return (token[0], tok)
    
    if f == False:
        print(f"Token type {t_type} for {tok} was not found in TOKEN_ENUM list")
        exit()

# checking for reserved types
def CHECK_FOR_RESERVED(word:str):
    r = RESERVED_KEYWORDS
    r_found = False

    for i in r:
        if i[1] == word:
            r_found = True
            return i, True
        
    if not r_found:
        return None, False

# parse the program
def PARSE(file_contents:str):
    line = 1
    x = 0
    word_formed = ""

    TOKENS = []

    while x < len(file_contents):
        char = file_contents[x]
        word_formed += char

        # checking each formed type
        # checking for int
        if is_int(char):
            integer = ""
            j = x
            while is_int(file_contents[j]):
                integer += file_contents[j]

                j+=1

            x = j-1

            TOKENS.append(get_int_token(integer))

        # checking for anything other than an integer
        elif is_alpha(char):
            alpha = ""
            k = x
            while is_alpha(file_contents[k]):
                alpha += file_contents[k]

                k+=1

            x = k-1

            # alpha could also be a reserved keyword eg: DECLARE
            # so need to check if it is a reserved and add reserved seperately
            r, is_a_reserved = CHECK_FOR_RESERVED(alpha.strip())
            if is_a_reserved:
                TOKENS.append(r)
            else:
                # otherwise just add it as an identifier type
                TOKENS.append(get_alpha_token(alpha))
        
        elif char == "<" and file_contents[x+1] == "-":
            TOKENS.append(create_token(char, "assignment"))
        
        elif is_skippable(char):
            pass

        elif char == "\n":
            line += 1
            
        else:
            error_handler(line, "Unrecognized character found")

        x+=1
    
    print(TOKENS)

def INTERPRET():
    pass


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print("Pseudocode Interpreter usage: ps_interpreter.py [file location to script]")
        exit(1)

    file_path = sys.argv[1]

    is_file_valid = validate_file(file_path)

    if is_file_valid == False:
        print("Please provide a valid pseudocode file, ending in .ps")
        exit(1)
    
    contents = read_file(file_path)

    PARSE(contents)