import random



def generate_code(length=8):
    data = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' # all numbers and letters
    code = ''.join(random.choice(data) for x in range(length)) # generate code without repeating
    return code