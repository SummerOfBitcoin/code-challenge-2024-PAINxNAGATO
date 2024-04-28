# code to create an compact size calculator for later use.

def compact_size_calculator(number):
    if number < 0:
        raise ValueError("Number must be non-negative.")

    if number < 253:
        return format(number, '02x') 
     
    elif number <= 0xFFFF:
        return 'fd' + format(number, '04x') 
    
    elif number <= 0xFFFFFFFF:
        return 'fe' + format(number, '08x')  
    
    elif number <= 0xFFFFFFFFFFFFFFFF:
        return 'ff' + format(number, '016x')  
    
    else:
        raise ValueError("Inavlid Number.")

