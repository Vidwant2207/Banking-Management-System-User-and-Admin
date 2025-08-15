import random
def gen_captcha():
     cap=''
     a=str(random.randint(0,9))
     b=chr(random.randint(65,80))
     c=str(random.randint(0,9))
     d=chr(random.randint(96,122))
     cap=a+b+c+d
     return cap
