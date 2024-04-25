def compact_size_calculator(number):
    if number < 0:
        raise ValueError("Number must be non-negative.")

    if number < 253:
        return format(number, '02x')  # Single byte representation
    elif number <= 0xFFFF:
        return 'fd' + format(number, '04x')  # FD prefix + 2-byte representation
    elif number <= 0xFFFFFFFF:
        return 'fe' + format(number, '08x')  # FE prefix + 4-byte representation
    elif number <= 0xFFFFFFFFFFFFFFFF:
        return 'ff' + format(number, '016x')  # FF prefix + 8-byte representation
    else:
        raise ValueError("Number is too large to be represented with compact size.")

# Test the function
# number = 22
# compact_size = compact_size_calculator(number)
# print("Compact Size Representation:", compact_size)
