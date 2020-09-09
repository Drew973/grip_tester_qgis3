
#dict {key:string}
#returnd {key:type}


def types(d):
    strings={key:value for (key,value) in d.items() if is_int(value)}
    #for k in d    
    return strings
    
    
def best_postgres_type(s):
    if is_int(s):
        return 'int'
    if is_float(s):
        return 'float'
    return 'varchar'    


def ints(d):
    return{key:value for (key,value) in d.items() if is_int(value)}

def is_int(s):
    try:
        int(s)
        return True
    except:
        return False
    
    
    
def floats(d):
    return{key:value for (key,value) in d.items() if is_float(value)}


def is_float(s):
    try:
        float(s)
        return True
    except:
        return False
    
    
# convert string v to int,float or string in that order
def to_best_type(v):
    try:
        return int(v)
    except:
        try:
            return float(v)
        except:
            return str(v)
    
def dict_convert(d):
    return {key:to_best_type(value) for (key,value) in d.items()}
           
#print(dict_convert({1:'a',2:'20','3':'2.1'}))
    
print(best_postgres_type('b'))