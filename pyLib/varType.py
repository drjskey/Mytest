

def varType(var):
    return type(var)

if __name__ == '__main__':
    print(varType('a'))
    print(varType(1))
    print(varType(['a',1]))
    print(varType({"a":1,"b":2}))
