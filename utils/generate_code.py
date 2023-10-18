import random



def generate_code(length=8):
    data = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' # all numbers and letters
    code = ''.join(rendom.choic(data) for x in range(length)) # generate code without repeating
    return code