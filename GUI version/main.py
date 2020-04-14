from tkinter import *
import os
import datetime
#Returning current date and time
def curTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
#Record activity in history file
def updateUserHistory(massege):
    if(not os.path.isdir("history")):
        os.mkdir("history/")
    fw = open("history/user", "a")
    fw.write(massege)
    fw.close()
def updateRechargeHistory(massege):
    if(not os.path.isdir("history")):
        os.mkdir("history/")
    fw = open("history/recharge", "a")
    fw.write(massege)
    fw.close()
    
# Register class
class Register:
    def register():
        global r_username
        global r_password
        global r_username_entry
        global r_password_entry
        global register_screen

        register_screen = Toplevel(main_screen) 
        register_screen.title("Register")
        register_screen.geometry("300x250")

        r_username = StringVar()
        r_password = StringVar()

        Label(register_screen, text="Please enter details below", bg="blue").pack()
        Label(register_screen, text="").pack()

        username_lable = Label(register_screen, text="Username * ")
        username_lable.pack()

        r_username_entry = Entry(register_screen, textvariable=r_username)
        r_username_entry.pack()

        password_lable = Label(register_screen, text="Password * ")
        password_lable.pack()

        r_password_entry = Entry(register_screen, textvariable=r_password, show='*')
        r_password_entry.pack()

        Label(register_screen, text="").pack()
 
        Button(register_screen, text="Register", width=10, height=1, bg="blue", command = Register.register_user).pack()

        global register_msg
        register_msg = Label(register_screen, text="", font=("calibri", 11))
        register_msg.pack()

    def register_user():
        username_info = r_username.get()
        password_info = r_password.get()
        
        r_username_entry.delete(0, END)
        r_password_entry.delete(0, END)

        if(not username_info.isdigit() or len(username_info) != 10):
            register_msg.config(text="Please! Enter valid 10 digit phone number")
            register_msg.config(fg="red")
            
        elif(password_info == ""):
            register_msg.config(text="Password shouldn't be Empty!")
            register_msg.config(fg="red")
        
        else:
            path = "data/user/"
            list_of_files = os.listdir(path)
            if(username_info not in list_of_files):
                file = open(path + username_info, "w")
                file.write(password_info)
                file.close()

                updateUserHistory(curTime() + "\tPhone no. " + username_info + " registred. " + "\n")
                register_msg.config(text="Registration Success!")
                register_msg.config(fg="green")

            else:
                register_msg.config(text="This number is already registred")
                register_msg.config(fg="red")

# Login class
class Login:
    def login():        
        global user_login
        
        user_login = Toplevel(main_screen)
        user_login.title("User Login")
        user_login.geometry("300x250")
        Label(user_login, text="Please enter details below to login").pack()
        Label(user_login, text="").pack()

        global user_username_verify
        global user_password_verify
    
        global user_username_login_entry
        global user_password_login_entry

        user_username_verify = StringVar()
        user_password_verify = StringVar()

        Label(user_login, text="Username * ").pack()
        user_username_login_entry = Entry(user_login, textvariable=user_username_verify)
        user_username_login_entry.pack()
        Label(user_login, text="").pack()
        Label(user_login, text="Password * ").pack()
        user_password_login_entry = Entry(user_login, textvariable=user_password_verify, show= '*')
        user_password_login_entry.pack()
        Label(user_login, text="").pack()
        Button(user_login, text="Login", width=10, height=1, command=Login.user_login_verification).pack()
        
        global user_login_msg
        user_login_msg = Label(user_login, text="", font=("calibri", 11))
        user_login_msg.pack()
        
    def user_login_verification():
        global user_username
        user_username = user_username_verify.get()
        user_password = user_password_verify.get()
        user_username_login_entry.delete(0, END)
        user_password_login_entry.delete(0, END)

        if(not user_username.isdigit() or len(user_username) != 10):
            user_login_msg.config(text="Please! Enter valid 10 digit phone number")
            user_login_msg.config(fg="red")
        else:
            user_path = "data/user/"
            list_of_files = os.listdir(user_path)
            if user_username in list_of_files:
                file1 = open(user_path + user_username, "r")
                verify = file1.read()
                if(user_password == verify):
                    user_login_msg.config(text="Successfully Login")
                    user_login_msg.config(fg="green")
                    user_login.destroy()
                    updateUserHistory(curTime() + "\tPhone no. " + user_username + " loged in. " + "\n")
                    Login.afterLogIn()

                else:
                    user_login_msg.config(text="Password not recognised")
                    user_login_msg.config(fg="red")

            else:
                user_login_msg.config(text="Username not found")
                user_login_msg.config(fg="red")
    
    def afterLogIn():
        global user_afterlogin
        user_afterlogin = Toplevel(main_screen)
        user_afterlogin.geometry("300x250")
        user_afterlogin.title("User Activity")
        Label(user_afterlogin, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(user_afterlogin, text="").pack()
        Button(user_afterlogin, text="Recharge", height="2", width="30", command = Login.recharge).pack()
        Label(user_afterlogin, text="").pack()
        Button(user_afterlogin, text="Data plans", height="2", width="30", command = Login.dataplan).pack()
        Label(user_afterlogin, text="").pack()
        Button(user_afterlogin, text="Current balance", height="2", width="30", command = Login.status).pack()
        Label(user_afterlogin, text="").pack()
        Button(user_afterlogin, text="LogOut", height="2", width="30", command = user_afterlogin.destroy).pack()

    def recharge():
        global reg_screen
        global amount_entered
        reg_screen = Toplevel(user_afterlogin)
        reg_screen.title("Recharge")
        reg_screen.geometry("350x200")
        amount_entered = StringVar()

        Label(reg_screen, text="E-Recharge", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(reg_screen, text="").pack()
        Label(reg_screen, text="Recharge Amount").pack()
        amount_entry = Entry(reg_screen, textvariable=amount_entered)
        amount_entry.pack()
        Label(reg_screen, text="").pack()
        Button(reg_screen, text="Recharge", height="1", width="20", command = Login.hit_recharge).pack()
        Label(reg_screen, text="").pack()
        global reg_msg
        reg_msg = Label(reg_screen, text="", font=("calibri", 11))
        reg_msg.pack()
        
    def hit_recharge():
        try:
            prevAmount = 0
            #Balance before recharge
            if(os.path.isfile("activity/r"+user_username)):
                fr = open("activity/r"+user_username, "r")
                prevAmount = float(fr.read())
                fr.close()
            amount = float(amount_entered.get())
            amount += prevAmount
            amount = float("{:.2f}".format(amount))
            #Make directory if not exist
            if(not os.path.isdir("activity")):
                os.mkdir("activity/")
            fw = open("activity/r"+user_username, "w")
            fw.write(str(amount))
            fw.close()

            updateRechargeHistory(curTime() + "\tPhone no. " + user_username + " recharge of " + str(amount - prevAmount) + "\n")
            reg_msg.config(text=curTime() + " Your current balance is " + str(amount))
            reg_msg.config(fg="green")
        except ValueError:
            reg_msg.config(text="Enter valid amount")
            reg_msg.config(fg="red")
        
    def dataplan():
        #Check if any plan is activated
        global dp_screen
        dp_screen = Toplevel(user_afterlogin)
        dp_screen.title("Data Plan")
        Label(dp_screen, text="Select Data Plan", bg="blue", width="50", height="2", font=("Calibri", 13)).pack()
        Label(dp_screen, text="").pack()
        
        i=1
        Label(dp_screen, text="\nData Plan: " + str(i)).pack()
        plan = open("dataplan/" + str(i))
        Label(dp_screen, text=plan.read()).pack()
        Button(dp_screen, text="Select", command=Login.plan1).pack()
        Label(dp_screen, text="").pack()
        plan.close()
        i=2
        Label(dp_screen, text="\nData Plan: " + str(i)).pack()
        plan = open("dataplan/" + str(i))
        Label(dp_screen, text=plan.read()).pack()
        Button(dp_screen, text="Select", command=Login.plan2).pack()
        Label(dp_screen, text="").pack()
        plan.close()
        i=3
        Label(dp_screen, text="\nData Plan: " + str(i)).pack()
        plan = open("dataplan/" + str(i))
        Label(dp_screen, text=plan.read()).pack()
        Button(dp_screen, text="Select", command=Login.plan3).pack()
        Label(dp_screen, text="").pack()
        plan.close()

        global dp_msg
        dp_msg = Label(dp_screen, text="", font=("calibri", 11))
        dp_msg.pack()
        
    def plan1():
        Login.planselected(1)
        
    def plan2():
        Login.planselected(2)
        
    def plan3():
        Login.planselected(3)
            
    def planselected(choice):
        if(not os.path.isfile("activity/dp" + user_username)):
            if(not os.path.isdir("activity")):
                os.mkdir("activity/")
            fw = open("activity/dp" + user_username, "w")
            fw.write(str(choice))
            fw.close()

            updateRechargeHistory(curTime() + "\tPhone no. " + user_username + " has selected Data plan " + str(choice) + "\n")
            dp_msg.config(text=curTime() + " Plan " + str(choice) + " successfully activated.")
            
        else:
            dp_screen.destroy()
            fr = open("activity/dp" + user_username)
            choice = fr.read()
            fr.close()
            dp_error_screen = Toplevel(user_afterlogin)
            dp_error_screen.title("Error!")
            dp_error_screen.geometry("400x200")
            Label(dp_error_screen, text="Currently, Data plan " + choice + " is Activated in your phone no.\n" + 
                                "\tSo, You can't buy another plan.").pack()
            Button(dp_error_screen, text="Close", command=dp_error_screen.destroy).pack()
            
    def status():
        st_screen = Toplevel(user_afterlogin)
        st_screen.title("Status")
        Label(st_screen, text="Current Balance", bg="blue", width="50", height="2", font=("Calibri", 13)).pack()
        Label(st_screen, text="").pack()
        #Balance
        balance = 0
        if(os.path.isfile("activity/r"+user_username)):
            fr = open("activity/r"+user_username, "r")
            balance = fr.read()
            fr.close()
        Label(st_screen, text="Current balance : " + str(balance)).pack()
        Label(st_screen, text="").pack()

        #Data Plan
        if(os.path.isfile("activity/dp"+user_username)):
            fr = open("activity/dp"+user_username, "r")
            plan_id = fr.read()
            fr.close()
            
            plan = open("dataplan/" + plan_id)
            Label(st_screen, text="Current activated Data plan : " + plan_id).pack()
            Label(st_screen, text=plan.read()).pack()
            plan.close()

        else:
            Label(st_screen, text="Currentely, No data plan is activated.").pack()
            Label(st_screen, text="").pack()
            
        Button(st_screen, text="Close", command=st_screen.destroy).pack()
        LAbel(st_screen, text="").pack()
        
        
# Admin class
class Administrator:
    def admin():
        global admin_login
        
        admin_login = Toplevel(main_screen)
        admin_login.title("Admin Login")
        admin_login.geometry("300x250")
        Label(admin_login, text="Please enter details below to login").pack()
        Label(admin_login, text="").pack()

        global admin_username_verify
        global admin_password_verify
    
        global admin_username_login_entry
        global admin_password_login_entry

        admin_username_verify = StringVar()
        admin_password_verify = StringVar()


        Label(admin_login, text="Username * ").pack()
        admin_username_login_entry = Entry(admin_login, textvariable=admin_username_verify)
        admin_username_login_entry.pack()
        Label(admin_login, text="").pack()
        Label(admin_login, text="Password * ").pack()
        admin_password_login_entry = Entry(admin_login, textvariable=admin_password_verify, show= '*')
        admin_password_login_entry.pack()
        Label(admin_login, text="").pack()
        Button(admin_login, text="Login", width=10, height=1, command=Administrator.admin_login_verification).pack()
        
        global admin_login_msg
        admin_login_msg = Label(admin_login, text="", font=("calibri", 11))
        admin_login_msg.pack()
        
    def admin_login_verification():
        admin_username = admin_username_verify.get()
        admin_password = admin_password_verify.get()
        admin_username_login_entry.delete(0, END)
        admin_password_login_entry.delete(0, END)

        admin_path = "data/admin/"
        list_of_files = os.listdir(admin_path)
        if admin_username in list_of_files:
            file1 = open(admin_path + admin_username, "r")
            verify = file1.read()
            if(admin_password == verify):
                admin_login_msg.config(text="Successfully Login")
                admin_login_msg.config(fg="green")
                admin_login.destroy()
                Administrator.afterLogIn()

            else:
                admin_login_msg.config(text="Password not recognised")
                admin_login_msg.config(fg="red")

        else:
            admin_login_msg.config(text="Username not found")
            admin_login_msg.config(fg="red")
        
    def afterLogIn():
        global admin_afterlogin
        admin_afterlogin = Toplevel(main_screen)
        admin_afterlogin.geometry("300x250")
        admin_afterlogin.title("User Activity")
        Label(admin_afterlogin, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="Recharge History", height="2", width="30", command = Administrator.rechargeHistory).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="LogIn/SignUp History", height="2", width="30", command = Administrator.userHistory).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="LogOut", height="2", width="30", command = admin_afterlogin.destroy).pack()

    def rechargeHistory():
        rh = Toplevel(admin_afterlogin)
        t = Text(rh)
        t.pack()
        
        if(os.path.isfile("history/recharge")):
            file = open("history/recharge")
            t.insert(END, file.read())
            file.close()
        else:
            t.insert(END, "\tNo recharge history recorded yet!")

    def userHistory():
        uh = Toplevel(admin_afterlogin)
        t = Text(uh)
        t.pack()
        
        if(os.path.isfile("history/user")):
            file = open("history/user")
            t.insert(END, file.read())
            file.close()
        else:
            t.insert(END, "\tNot any user activity history has been recorded yet!")
    
# Main screen
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Admin Login", height="2", width="30", command = Administrator.admin).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = Login.login).pack()
    Label(text="").pack()
    Button(text="Signup", height="2", width="30", command = Register.register).pack()

    main_screen.mainloop()
    

main_account_screen()