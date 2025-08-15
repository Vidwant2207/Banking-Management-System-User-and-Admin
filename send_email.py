import gmail
from Gcap import gen_captcha


def acc_open(uemail, uname, uacc, upass):
    con = gmail.GMail('40vitr40@gmail.com', 'nwlt uuao diwe tllh')
    sub='Your Account has been opened'
    body=f'''Dear {uname} your savings account with account number {uacc} has been opened with our bank.
    Your one time password if {upass} kindly change it post first login. 
    
    Warm Regards,
    ABC Bank
    '''
    msg=gmail.Message(to=uemail,subject=sub,text=body)
    con.send(msg)

def forpass(uname,uacc,upass,uemail):
    con = gmail.GMail('40vitr40@gmail.com', 'nwlt uuao diwe tllh')
    sub = 'Reset Password'
    body = f'''Dear {uname} 
    As you have requested password recovery for account number {uacc}.
    Your one time password if {upass} kindly change it post first login. 

    Warm Regards,
    ABC Bank
    '''
    msg = gmail.Message(to=uemail, subject=sub, text=body)
    con.send(msg)

def sendotp(uacc,uname,uemail):
    otp=gen_captcha()
    con = gmail.GMail('40vitr40@gmail.com', 'nwlt uuao diwe tllh')
    sub = 'Delete Account'
    body = f'''Dear {uname} 
        As you have requested deletion of account number {uacc}.
        Your one time password is {otp}. Kindly share it with the customer executive 

        Warm Regards,
        ABC Bank
        '''
    msg = gmail.Message(to=uemail, subject=sub, text=body)
    con.send(msg)
    return otp