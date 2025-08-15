from tkinter import Tk, messagebox, Label, Frame, Entry, Button
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import time
from Gcap import gen_captcha
from table_creation import generate
import sqlite3
from send_email import acc_open, forpass, sendotp
from tkcalendar import DateEntry
from tkinter.ttk import Treeview
import re

def moving_text(label, text, delay=150):
    def move():
        nonlocal text
        text = text[1:] + text[0]  # shift text left
        label.config(text=text)
        label.after(delay, move)
    move()

generate()
def show_dt():
    dt=time.strftime('%A %d %b %Y %r')
    date_lbl.configure(text=dt)
    date_lbl.after(1000, show_dt)

root= Tk()
root.state('zoomed')
root.title("ABC Banking Software")

title_lbl = Label(root,text='Advanced Banking Management System', font=('Arial', 20, 'bold underline'))
title_lbl.pack()

date_lbl=Label(root,font=('Arial', 10))
date_lbl.pack()
show_dt()

image = Image.open('bank logo.png')
image=image.resize((100,100))
photo = ImageTk.PhotoImage(image)
photo_lbl=Label(root, image= photo)
photo_lbl.place(relx=0.0,rely=0.0)
photo_lbl.image = photo


footer_lbl= Label(root,text='Created for testing by VT',font=('Arial', 10))
footer_lbl.pack(side='bottom')
temp_txt='Instant loan approval\n higher intrest on FD/RD'
mov_lbl=Label(root, text=temp_txt, font=('Arial', 10,'bold'))
mov_lbl.pack(side='bottom')
moving_text(mov_lbl,temp_txt,100)

def fp_screen():
    def back():
        frm.destroy()
        main_screen()

    def sendmail():
        uacn=acc_ent.get()
        conn_obj = sqlite3.connect("bank.sqlite")
        curs_obj = conn_obj.cursor()
        query='select acn_name,acn_pass,acn_email from accounts where acn_acno=?'
        curs_obj.execute(query,(uacn,))

        td=curs_obj.fetchone()
        if td:
            forpass(td[0], uacn, td[1],td[2])  # send password email
            messagebox.showinfo("Sent", 'Password has been sent to your registered email ID')
            frm.destroy()
            main_screen()
        else:
            messagebox.showerror("Error", "Account not found")


    frm = Frame(root)
    frm.configure(bg='powder blue')
    frm.place(relx=.1, rely=0.1, relwidth=.8, relheight=0.8, )
    home_but = Button(frm, text='Home 🏠', font=('Arial', 10), command=back)
    home_but.place(relx=0, rely=0)

    acnnum_lbl = Label(frm, text='Account Number', font=('Arial', 10), background='powder blue')
    acnnum_lbl.place(relx=.05, rely=0.18)
    acc_ent = Entry(frm, font=('Arial', 10))
    acc_ent.place(relx=0.15, rely=0.18)

#    email_lbl = Label(frm, text='Enter Email📧', font=('Arial', 10), background='powder blue')
 #   email_lbl.place(relx=0.05, rely=.25)
  #  email_ent = Entry(frm, font=('Arial', 10))
   # email_ent.place(relx=0.15, rely=0.25)

    sub_button = Button(frm, text='Submit', font=('Arial', 10), bd=5,command=sendmail )
    sub_button.place(relx=0.185, rely=0.32)




def main_screen():
    cap=gen_captcha()
    def ref_cap():
        new_cap=gen_captcha()
        captcha_val_lbl.configure(text=new_cap)

    frm= Frame(root)
    frm.configure(bg='powder blue')
    frm.place(relx=.1, rely=0.1, relwidth=.8, relheight=0.8)

    def forgot():
        frm.destroy()
        fp_screen()

    def login():
        user_type=accn_CB.get()
        user_acc= acc_ent.get()
        user_pass= pass_ent.get()
        ucap = captcha_ent.get()

        if user_type=="Admin":
            if user_acc=='admin' and user_pass=='password':

                if ucap!=cap:
                    messagebox.showerror('Failure','Invalid captcha')
                else:
                    frm.destroy()
                    admin_screen()
            else:
                messagebox.showerror('Failure',"wrong credentials")
        else:
            if ucap==cap:

                conn_obj = sqlite3.connect("bank.sqlite")
                curs_obj = conn_obj.cursor()
                query='select * from accounts where acn_acno=? and acn_pass=?'
                curs_obj.execute(query,(user_acc,user_pass))
                temp_row=curs_obj.fetchone()
                if temp_row==None:
                    messagebox.showerror("Error!","Invalid username or password")
                else:
                    frm.destroy()
                    user_screen(temp_row)
            else:
                messagebox.showerror('Failure','Invalid Captcha')


    def newu():
            messagebox.showwarning ('Alert','Kinldy connect with bank executive to create new account')


    image = Image.open('10840.jpg')
    image=image.resize((450,450))

    photo = ImageTk.PhotoImage(image)
    photo_lbl=Label(frm, image= photo)
    photo_lbl.place(relx=0.5,rely=0.05)
    photo_lbl.image = photo

    acntype_lbl=Label(frm, text='Account type',font=('Arial', 10), background='powder blue')
    acntype_lbl.place(relx=0.05, rely=0.1)
    accn_CB=Combobox(frm,values=['User','Admin'])
    accn_CB.place(relx=0.15, rely=0.1)

    acnnum_lbl = Label(frm, text='User Name', font=('Arial', 10), background='powder blue')
    acnnum_lbl.place(relx=.05, rely=0.18)
    acc_ent=Entry(frm, font=('Arial', 10))
    acc_ent.place(relx=0.15, rely=0.18)

    pass_lbl=Label(frm, text='Password',font=('Arial', 10), background='powder blue')
    pass_lbl.place(relx=0.05, rely=.25)
    pass_ent=Entry(frm, font=('Arial', 10), show='*')
    pass_ent.place(relx=0.15, rely=0.25)

    captcha_lbl = Label(frm, text='Enter Captcha', font=('Arial', 10), background='powder blue')
    captcha_lbl.place(relx=0.05, rely=.32)

    captcha_val_lbl = Label(frm, text=cap, font=('Arial', 10))
    captcha_val_lbl.place(relx=0.15, rely=.32)

    ref_cap= Button(frm, text='refreh 🔃',font=('Arial', 10), command=ref_cap)
    ref_cap.place(relx=.35, rely=0.32)

    captcha_ent = Entry(frm, font=('Arial', 10))
    captcha_ent.place(relx=0.2, rely=0.32)

    sub_button=Button(frm,text='Login',font=('Arial', 10),bd=5, command=login)
    sub_button.place(relx=0.2,rely=0.39)

    for_pw_button = Button(frm, text='Forgot Password', command=forgot, font=('Arial', 10), bd=5)
    for_pw_button.place(relx=0.05, rely=0.5)

    new_user_button = Button(frm, text='New User', font=('Arial', 10), bd=5, command=newu)
    new_user_button.place(relx=0.3, rely=0.5)






def admin_screen():
    def back():
        frm.destroy()
        main_screen()

    def open():

        def openac():
            uname=name_ent.get()
            uemail=email_ent.get()
            umob=mob_ent.get()
            uadhar=adhar_ent.get()
            uadr=adr_ent.get()
            udob=dob_ent.get()
            upass= gen_captcha()
            ubal=0
            uopendate=time.strftime('%A %d %b %Y')
            match = re.fullmatch(r"[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+", uemail)

            if len(uname)==0 or len(uemail)==0 or len(umob)!=10 or len(uadhar)!=12 or len(uadr)==0 or len(udob)==0:
                messagebox.showerror('Failure','Incomplete details, pelase try again')

            elif match==None:
                messagebox.showerror('Failure', 'Invalid email, pelase try again')
            elif re.fullmatch("[6-9][0-9]{9}",umob)==None:
                messagebox.showerror('Failure', 'Invalid mobile number, pelase try again')
            elif uadhar.isdigit()==False:
                messagebox.showerror('Failure', 'Invalid adhar, pelase try again')
            elif uname.isalpha()==False:
                messagebox.showerror('Failure', 'Invalid name, pelase try again')
            elif uadr.isalnum()==False:
                messagebox.showerror('Failure', 'Invalid address, pelase try again')

            else:

                conn_obj = sqlite3.connect("bank.sqlite")
                curs_obj = conn_obj.cursor()
                query='insert into accounts values(null,?,?,?,?,?,?,?,?)'
                curs_obj.execute(query,(uname, upass, uemail, umob, uadhar, udob, ubal, uopendate))
                conn_obj.commit()
                conn_obj.close()

                conn_obj = sqlite3.connect("bank.sqlite")
                curs_obj = conn_obj.cursor()
                curs_obj.execute('select max(acn_acno) from accounts')
                uacn=curs_obj.fetchone()[0]
                conn_obj.close()

                acc_open(uemail, uname,uacn,upass)
                messagebox.showinfo('Success','Account has been created and email sent')
                frm.destroy()
                admin_screen()




        ifrm=Frame(frm)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        open_lbl=Label(ifrm,text=" Open Account Window", font=('Arial', 12, 'bold'), bg='pink')
        open_lbl.pack()

        name_lbl = Label(ifrm, text='Enter Name', font=('Arial', 10), background='pink')
        name_lbl.place(relx=0.05, rely=.1)
        name_ent = Entry(ifrm, font=('Arial', 10))
        name_ent.place(relx=0.24, rely=0.1)

        email_lbl = Label(ifrm, text='Enter email', font=('Arial', 10), background='pink')
        email_lbl.place(relx=0.05, rely=.25)
        email_ent = Entry(ifrm, font=('Arial', 10))
        email_ent.place(relx=0.24, rely=0.25)

        mob_lbl = Label(ifrm, text='Enter Mob number', font=('Arial', 10), background='pink')
        mob_lbl.place(relx=0.05, rely=.4)
        mob_ent = Entry(ifrm, font=('Arial', 10))
        mob_ent.place(relx=0.24, rely=0.4)

        adhar_lbl = Label(ifrm, text='Enter Adhar', font=('Arial', 10), background='pink')
        adhar_lbl.place(relx=0.05, rely=.55)
        adhar_ent = Entry(ifrm, font=('Arial', 10))
        adhar_ent.place(relx=0.24, rely=0.55)

        adr_lbl = Label(ifrm, text='Enter Address', font=('Arial', 10), background='pink')
        adr_lbl.place(relx=0.05, rely=.70)
        adr_ent = Entry(ifrm, font=('Arial', 10))
        adr_ent.place(relx=0.24, rely=0.7)

        dob_lbl = Label(ifrm, text='Enter Date Of Birth', font=('Arial', 10), background='pink')
        dob_lbl.place(relx=0.05, rely=.85)
        dob_ent =DateEntry(ifrm, width=18, background="darkblue",foreground="white", borderwidth=2, date_pattern='dd/mm/yyyy')
        dob_ent.place(relx=0.24, rely=0.85)

        open_acc=Button(ifrm, text='Open Account',command=openac, borderwidth= 3, font=('Arial', 15))
        open_acc.place(relx= 0.7, rely=0.45)

    def close():
        otp_value = None

        def get_otp():
            nonlocal otp_value
            acn = acn_ent.get()
            if not acn:
                messagebox.showerror("Error", "Please enter Account Number first")
                return

            conn_obj = sqlite3.connect("bank.sqlite")
            curs_obj = conn_obj.cursor()
            query = 'SELECT * FROM accounts WHERE acn_acno=?'
            curs_obj.execute(query, (acn,))
            td = curs_obj.fetchone()
            conn_obj.close()

            if not td:
                messagebox.showerror("Error", "Account not found!")
                return

            # td[1] = name, td[3] = email (assuming your table order)
            otp_value = sendotp(acn, td[1], td[3])
            messagebox.showinfo("OTP Sent", "OTP has been sent to your registered email")

        def clo_acc():
            uotp = otp_ent.get()
            acn = acn_ent.get()
            nonlocal otp_value

            if not otp_value:
                messagebox.showerror("Error", "Please get OTP first!")
                return

            if otp_value != uotp:
                messagebox.showerror("Error", "Wrong OTP, please try again!")
                return

            conn_obj = sqlite3.connect("bank.sqlite")
            curs_obj = conn_obj.cursor()
            query = 'DELETE FROM accounts WHERE acn_acno=?'
            curs_obj.execute(query, (acn,))
            conn_obj.commit()
            conn_obj.close()

            messagebox.showinfo('Success', f'Account with {acn} has been deleted')
            ifrm.destroy()
            admin_screen()

        ifrm = Frame(frm)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        open_lbl = Label(ifrm, text="Close Account Window", font=('Arial', 12, 'bold'), bg='pink')
        open_lbl.pack()

        acn_lbl = Label(ifrm, text='Enter Acc Number', font=('Arial', 10), background='pink')
        acn_lbl.place(relx=.05, rely=.1)
        acn_ent = Entry(ifrm, font=('Arial', 10))
        acn_ent.place(relx=.27, rely=.1)

        otp_but = Button(ifrm, text='Get OTP', command=get_otp)
        otp_but.place(relx=.5, rely=.25)

        otp_lbl = Label(ifrm, text='One Time Password (OTP)', font=('Arial', 10), background='pink')
        otp_lbl.place(relx=0.05, rely=.25)
        otp_ent = Entry(ifrm, font=('Arial', 10))
        otp_ent.place(relx=0.27, rely=0.25)

        close_but = Button(ifrm, text='Close Account', command=clo_acc)
        close_but.place(relx=.3, rely=.35)


    def view():
        def details():
            acn = acn_ent.get().strip()
            if not acn:
                messagebox.showerror("Error", "Please enter an Account Number")
                return

            conn_obj = sqlite3.connect("bank.sqlite")
            curs_obj = conn_obj.cursor()
            curs_obj.execute("SELECT * FROM accounts WHERE acn_acno=?", (acn,))
            data = curs_obj.fetchone()
            conn_obj.close()

            if not data:
                messagebox.showerror("Error", "Account not found")
                return

            # Clear old rows
            for row in table.get_children():
                table.delete(row)

            # Insert fetched data into table
            table.insert("", "end", values=data)

        ifrm = Frame(frm, bg='pink')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        open_lbl = Label(ifrm, text="View Account Window", font=('Arial', 12, 'bold'), bg='pink')
        open_lbl.pack(pady=10)

        acn_lbl = Label(ifrm, text="Enter Account Number:", font=('Arial', 10), bg='pink')
        acn_lbl.place(relx=.15, rely=.15)

        acn_ent = Entry(ifrm, font=('Arial', 10))
        acn_ent.place(relx=.45, rely=.15)

        sub_but = Button(ifrm, text='Get Details', command=details)
        sub_but.place(relx=.49, rely=.25)

        # Create a Treeview widget for table display
        cols = ("Account No", "Name", "Password", "Email", "Mobile","Aadhar","DOB","Balance","Account OD")
        table = Treeview(ifrm, columns=cols, show="headings")

        for col in cols:
            table.heading(col, text=col)
            table.column(col, width=100, anchor="center")

        table.place(relx=0.05, rely=0.4, relwidth=0.9, relheight=0.5)

    frm = Frame(root)
    frm.configure(bg='powder blue')
    frm.place(relx=.1, rely=0.1, relwidth=.8, relheight=0.8, )
    home_but = Button(frm, text='Log Out', font=('Arial', 10), command=back)
    home_but.place(relx=0, rely=0)

    open_button = Button(frm, text='Open Acc', font=('Arial', 10), bd=5, command=open)
    open_button.place(relx=0.2, rely=0.1)

    close_acc_button = Button(frm, text='Close Acc', font=('Arial', 10), bd=5, command=close)
    close_acc_button.place(relx=0.46, rely=0.1)

    view_button = Button(frm, text='View Acc', font=('Arial', 10), bd=5, command=view)
    view_button.place(relx=0.7, rely=0.1)

def user_screen(det):
    def logout():
        frm.destroy()
        main_screen()
    def back():
        frm.destroy()
        user_screen(det)


    def view_details():
        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        open_lbl = Label(ifrm, text=" Personal Info Window", font=('Arial', 10))
        open_lbl.pack()

        back_but=Button(ifrm, text='Go Back', font=('Arial', 10), command=back)
        back_but.place(relx=0.0,y=0.0)

        acn_lbl=Label(ifrm,text=f'Account Number\t = \t {det[0]}', font=('Arial', 10), background='white' )
        acn_lbl.place(relx=0.2, rely=.2)
        name_lbl = Label(ifrm, text=f'Account Holder\t = \t {det[1]}', font=('Arial', 10), background='white')
        name_lbl.place(relx=0.2, rely=.35)
        bal_lbl=Label(ifrm, text=f'Account Balance\t = \t {det[7]}', font=('Arial', 10), background='white')
        bal_lbl.place(relx=0.2, rely=.5)
        od_lbl = Label(ifrm, text=f'Opening Date\t = \t {det[8]}', font=('Arial', 10), background='white')
        od_lbl.place(relx=0.2, rely=.65)

    def upd_acc():
        def update_details():
            uname=name_ent.get()
            uemail=email_ent.get()
            umob=mob_ent.get()
            upass=pw_ent.get()

            conn_obj = sqlite3.connect("bank.sqlite")
            curs_obj = conn_obj.cursor()
            query='update accounts set acn_name=?,acn_email=?,acn_mob=?,acn_pass=? where acn_acno=?'
            curs_obj.execute(query,(uname,uemail,umob,upass,det[0]))
            conn_obj.commit()

            messagebox.showinfo('Success','Details updated!!!')

            curs_update=conn_obj.cursor()
            curs_update.execute("SELECT * FROM accounts WHERE acn_acno=?", (det[0],))
            updated_det = curs_update.fetchone()
            conn_obj.close()
            ifrm.destroy()
            user_screen(updated_det)

        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        back_but = Button(ifrm, text='Go Back', font=('Arial', 10), command=back)
        back_but.place(relx=0.0, y=0.0)

        name_lbl = Label(ifrm, text='Enter Name', font=('Arial', 10), background='pink')
        name_lbl.place(relx=0.05, rely=.1)
        name_ent = Entry(ifrm, font=('Arial', 10))
        name_ent.place(relx=0.24, rely=0.1)
        name_ent.insert(0, det[1])

        email_lbl = Label(ifrm, text='Enter email', font=('Arial', 10), background='pink')
        email_lbl.place(relx=0.05, rely=.25)
        email_ent = Entry(ifrm, font=('Arial', 10))
        email_ent.place(relx=0.24, rely=0.25)
        email_ent.insert(0,det[3])

        mob_lbl = Label(ifrm, text='Enter Mob number', font=('Arial', 10), background='pink')
        mob_lbl.place(relx=0.05, rely=.4)
        mob_ent = Entry(ifrm, font=('Arial', 10))
        mob_ent.place(relx=0.24, rely=0.4)
        mob_ent.insert(0,det[4])

        pw_lbl = Label(ifrm, text='Enter Password', font=('Arial', 10), background='pink')
        pw_lbl.place(relx=0.05, rely=.55)
        pw_ent = Entry(ifrm, font=('Arial', 10))
        pw_ent.place(relx=0.24, rely=0.55)
        pw_ent.insert(0,det[2])

        sub_but=Button(ifrm, text='Update Details', font=('Arial', 10,), command=update_details)
        sub_but.place(relx=.45, rely=.8)

    def withdraw():

        def with_amount():
            if float(amo_ent.get())>det[7]:
                messagebox.showerror("Failure",'Insuffecient Balance')
            else:
                amount = float(amo_ent.get())

                conn_obj = sqlite3.connect("bank.sqlite")
                curs_obj = conn_obj.cursor()
                query = 'update accounts set acn_bal=acn_bal-? where acn_acno=?'
                curs_obj.execute(query, (amount, det[0]))
                conn_obj.commit()

                messagebox.showinfo('Sucess', f'Amount {amount} has been withdrawen, current balance is {det[7] - amount}')
                curs_update = conn_obj.cursor()
                curs_update.execute("SELECT * FROM accounts WHERE acn_acno=?", (det[0],))
                updated_det = curs_update.fetchone()
                conn_obj.close()
                ifrm.destroy()
                user_screen(updated_det)

        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        back_but = Button(ifrm, text='Go Back', font=('Arial', 10), command=back)
        back_but.place(relx=0.0, y=0.0)

        depo_lbl = Label(ifrm, text='Enter Amount', font=('Arial', 10), background='pink')
        depo_lbl.place(relx=0.25, rely=.1)

        amo_ent = Entry(ifrm, font=('Arial', 10))
        amo_ent.place(relx=0.4, rely=0.1)

        depo_but = Button(ifrm, text='Withdraw amount', font=('Arial', 10), command=with_amount)
        depo_but.place(relx=.355, rely=.5)


    def trans():

        def send():
            racn=acn_ent.get()
            amount=float(amo_ent.get())
            conn_obj = sqlite3.connect("bank.sqlite")

            curs_obj = conn_obj.cursor()
            query='select * from accounts where acn_acno=?'
            curs_obj.execute(query,(racn,))
            toacn=curs_obj.fetchone()
            if toacn==None:
                messagebox.showerror('Failure',"Account doesnt exist, please recheck details")
            else:
                if det[7]<toacn[7]:
                    messagebox.showerror('Failure','Insuffecient Balance')
                else:
                    query1='update accounts set acn_bal=acn_bal+? where acn_acno=?'
                    query2='update accounts set acn_bal=acn_bal-? where acn_acno=?'
                    curs_obj.execute(query1,(det[7],amount))
                    curs_obj.execute(query2,(amount,det[0]))
                    conn_obj.commit()
                    conn_obj.close()
                    messagebox.showinfo("success",'Amount has been transferred')
                    ifrm.destroy()
                    user_screen(det)




        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        back_but = Button(ifrm, text='Go Back', font=('Arial', 10), command=back)
        back_but.place(relx=0.0, y=0.0)

        acn_lbl = Label(ifrm, text='Enter Receiver A/N', font=('Arial', 10), background='pink')
        acn_lbl.place(relx=0.2, rely=.1)

        acn_ent = Entry(ifrm, font=('Arial', 10))
        acn_ent.place(relx=0.35, rely=0.1)

        amo_lbl = Label(ifrm, text='Enter Amount', font=('Arial', 10), background='pink')
        amo_lbl.place(relx=0.2, rely=.3)

        amo_ent = Entry(ifrm, font=('Arial', 10))
        amo_ent.place(relx=0.35, rely=0.3)

        depo_but = Button(ifrm, text='Transfer amount', font=('Arial', 10), command=send)
        depo_but.place(relx=.355, rely=.5)

    def deposit():

        def depo_amount():

            amount=float(amo_ent.get())

            conn_obj = sqlite3.connect("bank.sqlite")
            curs_obj = conn_obj.cursor()
            query = 'update accounts set acn_bal=acn_bal+? where acn_acno=?'
            curs_obj.execute(query,(amount,det[0]))
            conn_obj.commit()

            messagebox.showinfo('Sucess',f'Amount {amount} has been deposited, current balance is {amount+det[7]}')
            curs_update = conn_obj.cursor()
            curs_update.execute("SELECT * FROM accounts WHERE acn_acno=?", (det[0],))
            updated_det = curs_update.fetchone()
            conn_obj.close()
            ifrm.destroy()
            user_screen(updated_det)

        ifrm = Frame(frm)
        ifrm.configure(bg='white')
        ifrm.place(relx=.1, rely=0.2, relwidth=.8, relheight=0.6)

        back_but = Button(ifrm, text='Go Back', font=('Arial', 10), command=back)
        back_but.place(relx=0.0, y=0.0)

        depo_lbl=Label(ifrm, text='Enter Amount', font=('Arial', 10), background='pink')
        depo_lbl.place(relx=0.25, rely=.1)

        amo_ent = Entry(ifrm, font=('Arial', 10))
        amo_ent.place(relx=0.4, rely=0.1)

        depo_but = Button(ifrm, text='Deposit amount', font=('Arial', 10), command=depo_amount)
        depo_but.place(relx=.45, rely=.5)

    frm = Frame(root)
    frm.configure(bg='powder blue')
    frm.place(relx=.1, rely=0.1, relwidth=.8, relheight=0.8, )
    home_but = Button(frm, text='Log Out', font=('Arial', 10), command=back)
    home_but.place(relx=0, rely=0)
    welc_lbl= Label(frm, text=f'Welcome {det[1]}', font=('Arial', 20, 'bold underline'))
    welc_lbl.pack()

    home_but = Button(frm, text='Log Out', font=('Arial', 10), command=logout)
    home_but.place(relx=0, rely=0)

    view_button = Button(frm, text='Personal Info', font=('Arial', 10), bd=5, command=view_details)
    view_button.place(relx=0.2, rely=0.1)

    update_acc_button = Button(frm, text='Update Details', font=('Arial', 10), bd=5, command=upd_acc)
    update_acc_button.place(relx=0.46, rely=0.1)

    deposit_button = Button(frm, text='Deposit Amount', font=('Arial', 10), bd=5, command=deposit)
    deposit_button.place(relx=0.7, rely=0.1)

    withdraw_button = Button(frm, text='Withdraw Amount', font=('Arial', 10), bd=5, command=withdraw)
    withdraw_button.place(relx=0.2, rely=0.3
                          )

    transfer_button = Button(frm, text='Transfer Amount', font=('Arial', 10), bd=5, command=trans)
    transfer_button.place(relx=0.46, rely=0.3)





main_screen()
root.mainloop()