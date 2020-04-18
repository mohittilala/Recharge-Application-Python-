from tkinter import *
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import datetime
#Returning current date and time
def curTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
#Record activity in history table
def updateUserHistory(massege):
    if(not os.path.isdir("history")):
        os.mkdir("history/")
    fw = open("history/user", "a")
    fw.write(massege)
    fw.close()
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="mohit",
  passwd="mohit",
  database="mydb3"
)

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

        Label(register_screen, text="Please enter details below", bg="#bdf").pack()
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
 
        Button(register_screen, text="Register", width=10, height=1, bg="#bdf", command = Register.register_user).pack()

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
            mycursor = mydb.cursor()
            mycursor.execute("select username from useracc")
            usernames=[]
            for x in mycursor:
                usernames.append(x[0])
            if(username_info not in usernames):
                mycursor = mydb.cursor()
                sql = "INSERT INTO useracc (username, passwd) VALUES (%s, %s)"
                val = (username_info, password_info)
                mycursor.execute(sql, val)
                mydb.commit()
                
                #updateUserHistory(curTime() + "\tPhone no. " + username_info + " registred. " + "\n")
                
                mycursor = mydb.cursor()
                sql = "INSERT INTO history (username, time, type) VALUES (%s, %s, %s)"
                val = (username_info, curTime(), "r")
                mycursor.execute(sql, val)
                mydb.commit()
                
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
            mycursor = mydb.cursor()
            mycursor.execute("select username from useracc")
            usernames=[]
            for x in mycursor:
                usernames.append(x[0])
            if(user_username in usernames):
                mycursor = mydb.cursor()
                sql = "SELECT passwd FROM useracc WHERE username = %s"
                val = (user_username, )
                mycursor.execute(sql, val)
                passwd = []
                for x in mycursor:
                    passwd = x[0]
                if(user_password == passwd):
                    user_login_msg.config(text="Successfully Login")
                    user_login_msg.config(fg="green")
                    user_login.destroy()
                    #updateUserHistory(curTime() + "\tPhone no. " + user_username + " loged in. " + "\n")
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO history (username, time, type) VALUES (%s, %s, %s)"
                    val = (user_username, curTime(), "l")
                    mycursor.execute(sql, val)
                    mydb.commit()
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
        user_afterlogin.geometry("300x320")
        user_afterlogin.title("User Activity")
        Label(user_afterlogin, text="Select Your Choice", bg="#cf5", width="300", height="2", font=("Calibri", 13)).pack()
        Label(user_afterlogin, text="Username: "+user_username, bg="#bdf", font=("Calibri", 9)).pack()
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

        Label(reg_screen, text="E-Recharge", bg="#7d2", width="300", height="2", font=("Calibri", 13)).pack()
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
            # Balance before recharge
            prevAmount = 0
            mycursor = mydb.cursor()
            mycursor.execute("SELECT sum(amount) FROM recharge WHERE username = {}".format(user_username))
            for x in mycursor:
                if(type(x[0]) == float):
                    prevAmount = x[0]
            
            # Save balance to database
            amount = float(amount_entered.get())
            amount = float("{:.2f}".format(amount))
            mycursor = mydb.cursor()
            sql = "INSERT INTO recharge (username, amount, time) VALUES (%s, %s, %s)"
            val = (user_username, amount, curTime())
            mycursor.execute(sql, val)
            mydb.commit()
            
            # updateRechargeHistory(curTime() + "\tPhone no. " + user_username + " recharge of " + str(amount - prevAmount) + "\n")
            reg_msg.config(text=curTime() + " Your current balance is " + str(amount + prevAmount))
            reg_msg.config(fg="green")
        
        except ValueError:
            reg_msg.config(text="Enter valid amount")
            reg_msg.config(fg="red")
            
    def readplan(plan):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM plan WHERE plan_id = {}".format(plan))
        plandetail = ""
        for x in mycursor:
            plandetail = "Amount : Rs. {}\nData : {}\nValidity : {}\nDetails : {}\nFacility : {}\n".format(x[1], x[2], x[3], x[4], x[5])
        return plandetail
        
    def dataplan():
        # Check if any plan is activated
        global dp_screen
        dp_screen = Toplevel(user_afterlogin)
        dp_screen.title("Data Plan")
        Label(dp_screen, text="Select Data Plan", bg="#7d2", width="50", height="2", font=("Calibri", 13)).pack()
        Label(dp_screen, text="").pack()
        
        i=1
        Label(dp_screen, text="\nData Plan: " + str(i)).pack()
        Label(dp_screen, text=Login.readplan(i)).pack()
        Button(dp_screen, text="Select", command=Login.plan1).pack()
        Label(dp_screen, text="").pack()
        i=2
        Label(dp_screen, text="\nData Plan: " + str(i)).pack()
        Label(dp_screen, text=Login.readplan(i)).pack()
        Button(dp_screen, text="Select", command=Login.plan2).pack()
        Label(dp_screen, text="").pack()
        i=3
        Label(dp_screen, text="\nData Plan: " + str(i)).pack()
        Label(dp_screen, text=Login.readplan(i)).pack()
        Button(dp_screen, text="Select", command=Login.plan3).pack()
        Label(dp_screen, text="").pack()

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
        mycursor = mydb.cursor()
        mycursor.execute("SELECT plan FROM userplan WHERE username={}".format(user_username))
        activeplan = 0
        for x in mycursor:
            activeplan = x[0]
        if(activeplan == 0):
            mycursor = mydb.cursor()
            sql = "INSERT INTO userplan (username, plan, time) VALUES (%s, %s, %s)"
            val = (user_username, int(choice), curTime())
            mycursor.execute(sql, val)
            mydb.commit()
            # updateRechargeHistory(curTime() + "\tPhone no. " + user_username + " has selected Data plan " + str(choice) + "\n")
            dp_msg.config(text=curTime() + " Plan " + str(choice) + " successfully activated.")
        else:
            dp_screen.destroy()
            dp_error_screen = Toplevel(user_afterlogin)
            dp_error_screen.title("Error!")
            dp_error_screen.geometry("400x200")
            Label(dp_error_screen, text="Currently, Data plan " + str(activeplan) + " is Activated in your phone no.\n" + 
                                "\tSo, You can't buy another plan.").pack()
            Button(dp_error_screen, text="Close", command=dp_error_screen.destroy).pack()
            
    def status():
        st_screen = Toplevel(user_afterlogin)
        st_screen.title("Status")
        Label(st_screen, text="Current Balance", bg="#7d2", width="50", height="2", font=("Calibri", 13)).pack()
        Label(st_screen, text="").pack()
        #Balance
        balance = 0
        mycursor = mydb.cursor()
        mycursor.execute("select sum(amount) from recharge where username = {}".format(user_username))
        for x in mycursor:
            if(type(x[0]) == float):
                balance = x[0]
        Label(st_screen, text="Current balance : " + str(balance)).pack()
        Label(st_screen, text="").pack()

        #Data Plan
        mycursor = mydb.cursor()
        mycursor.execute("SELECT plan FROM userplan WHERE username={}".format(user_username))
        activeplan = 0
        for x in mycursor:
            activeplan = x[0]
        if(activeplan > 0):
            Label(st_screen, text="Current activated Data plan : " + str(activeplan)).pack()
            Label(st_screen, text=Login.readplan(activeplan)).pack()

        else:
            Label(st_screen, text="Currentely, No data plan is activated.").pack()
            Label(st_screen, text="").pack()
            
        Button(st_screen, text="Close", command=st_screen.destroy).pack()
        Label(st_screen, text="").pack()
        
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
        global admin_username
        admin_username = admin_username_verify.get()
        admin_password = admin_password_verify.get()
        admin_username_login_entry.delete(0, END)
        admin_password_login_entry.delete(0, END)
        
        mycursor = mydb.cursor()
        mycursor.execute("select admin_id from adminacc")
        usernames=[]
        for x in mycursor:
            usernames.append(x[0])
        if(admin_username in usernames):
            mycursor = mydb.cursor()
            sql = "SELECT passwd FROM adminacc WHERE admin_id = %s"
            val = (admin_username, )
            mycursor.execute(sql, val)
            passwd = []
            for x in mycursor:
                passwd = x[0]
            if(admin_password == passwd):
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
        admin_afterlogin.geometry("300x380")
        admin_afterlogin.title("User Activity")
        Label(admin_afterlogin, text="Select Your Choice", bg="#cf5", width="300", height="2", font=("Calibri", 13)).pack()
        Label(admin_afterlogin, text="Username: "+admin_username, bg="#bdf", font=("Calibri", 9)).pack()
        Button(admin_afterlogin, text="Recharge History", height="2", width="30", command = Administrator.rechargeHistory).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="LogIn/SignUp History", height="2", width="30", command = Administrator.userHistory).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="Top Users", height="2", width="30", command = Administrator.topUsers).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="Today's stats", height="2", width="30", command = Administrator.todayStat).pack()
        Label(admin_afterlogin, text="").pack()
        Button(admin_afterlogin, text="LogOut", height="2", width="30", command = admin_afterlogin.destroy).pack()

    def rechargeHistory():
        rh = Toplevel(admin_afterlogin)
        t = Text(rh)
        t.pack()
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM recharge")
        rechhist = []
        for x in mycursor:
            rechhist.append("{}\tPhone no. {} recharge of {}\n".format(x[3].strftime("%Y-%m-%d %H:%M:%S"), x[1], x[2]))

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM userplan")
        planhist = []
        for x in mycursor:
            planhist.append("{}\tPhone no. {} has selected Data plan {}\n".format(x[3].strftime("%Y-%m-%d %H:%M:%S"), x[1], x[2]))

        rl = 0
        pl = 0
        rlen = len(rechhist)
        plen = len(planhist)
        hist = ""

        if(rlen > 0 or plen > 0):
            if(rlen > 0 and plen > 0):
                while(True):
                    if(planhist[pl] < rechhist[rl]):
                        hist += planhist[pl]
                        pl += 1

                    else:
                        hist += rechhist[rl]
                        rl += 1

                    if(pl == plen or rl == rlen):
                        break

            if(pl != plen):
                while(True):
                    hist += planhist[pl]
                    pl += 1
                    if(pl == plen):
                        break

            if(rl != rlen):
                while(True):
                    hist += rechhist[rl]
                    rl += 1
                    if(rl == rlen):
                        break

        else:
            hist = "\tNo recharge history recorded yet!"

        t.insert(END, hist)

    def userHistory():
        uh = Toplevel(admin_afterlogin)
        t = Text(uh)
        t.pack()
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM history")
        hist = ""
        for x in mycursor:
            if(x[3] == "r"):
                hist += ("{}\tPhone no. {} registred. \n".format(x[2].strftime("%Y-%m-%d %H:%M:%S"), x[1]))
            else:
                hist += ("{}\tPhone no. {} logged in.\n".format(x[2].strftime("%Y-%m-%d %H:%M:%S"), x[1]))
        
        if(hist != ""):
            t.insert(END, hist)
        else:
            t.insert(END, "\tNot any user activity history has been recorded yet!")
            
    def topUsers():
        tu = Toplevel(admin_afterlogin)
        Label(tu, text="Top Users", bg="#7d2", width="40", height="2", font=("Calibri", 13)).pack()
        Label(tu, text="").pack()
        llist = []
        llist.append(Label(tu, text="1st Rank : No user!\nVisits : 0"))
        llist.append(Label(tu, text=""))
        llist.append(Label(tu, text="2nd Rank : No user!\nVisits : 0"))
        llist.append(Label(tu, text=""))
        llist.append(Label(tu, text="3rd Rank : No user!\nVisits : 0"))
        llist.append(Label(tu, text=""))

        cr = mydb.cursor()
        cr.execute("SELECT username, COUNT(*) as c FROM history WHERE type = 'l' GROUP BY username ORDER BY c DESC LIMIT 3")
        users = []
        for x in cr:
            users.append(x)

        ranklist = []
        visitlist = []
        for i in range(len(users)):
            rank="1st"
            if(i==1):
                rank="2nd"
            elif(i==2):
                rank="3rd"
            llist[i*2].config(text="{} Rank : {}\nVisits : {}".format(rank, users[i][0], users[i][1]))
            ranklist.append(rank)
            visitlist.append(users[i][1])
        for x in llist:
            x.pack()

        if(len(users) != 0):
            from pandas import DataFrame
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            data = {'Top Users': ranklist, 'No. of visits': visitlist}
            df = DataFrame(data,columns=['Top Users','No. of visits'])

            figh = 5
            if(len(users) == 1):
                figh = 1.8
            elif(len(users) == 2):
                figh = 3
            figure = plt.Figure(figsize=(5.2,figh), dpi=70)
            ax = figure.add_subplot(111)
            bar = FigureCanvasTkAgg(figure, tu)
            bar.get_tk_widget().pack(side=LEFT, fill=BOTH)
            df = df[['Top Users','No. of visits']].groupby('Top Users').sum()
            df = df.reindex(index=df.index[::-1])
            df.plot(kind='barh', legend=True, ax=ax, color='g')
            ax.set_title('Visits of User')
            
    def todayStat():
        cr = mydb.cursor()
        cr.execute("SELECT * FROM history")
        today = []
        now = datetime.datetime.now()
        for x in cr:
            if(x[2].strftime("%Y-%m-%d") == now.strftime("%Y-%m-%d") and x[3] == "l"):
                today.append(x)

        hours = []
        visits = []
        for i in range(24):
            visits.append(0)
            hours.append(i)
            for x in today:
                if(int(x[2].strftime("%H")) == i):
                    visits[i] += 1
                
        data = {'Hours': hours, 'No. of visits': visits}
        df = DataFrame(data,columns=['Hours','No. of visits'])

        ts = Toplevel(admin_afterlogin)
        Label(ts, text="Today's stats", bg="#7d2", width="77", height="2", font=("Calibri", 13)).pack()

        figure = plt.Figure(figsize=(10,4), dpi=70)
        ax = figure.add_subplot(111)
        line = FigureCanvasTkAgg(figure, ts)
        line.get_tk_widget().pack(side=LEFT, fill=BOTH)
        df = df[['Hours','No. of visits']].groupby('Hours').sum()
        df.plot(kind='line', legend=True, ax=ax, color='g',marker='o', fontsize=12)
        #ax.set_title('Recent stats')
        
# Main class
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="#57f", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Admin Login", height="2", width="30", command = Administrator.admin).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = Login.login).pack()
    Label(text="").pack()
    Button(text="Signup", height="2", width="30", command = Register.register).pack()

    main_screen.mainloop()
    

main_account_screen()