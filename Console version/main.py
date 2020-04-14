import os
import datetime
#Returning current date and time
def curTime():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
#Record activity in history file
def updateUserHistory(massege):
    if(not os.path.isdir("History")):
        os.mkdir("History/")
    fw = open("History/User", "a")
    fw.write(massege)
    fw.close()
def updateRechargeHistory(massege):
    if(not os.path.isdir("History")):
        os.mkdir("History/")
    fw = open("History/Recharge", "a")
    fw.write(massege)
    fw.close()
    
# SignUp class
class SignUp:
    def signUp():
        ID = input("Enter 10 digit phone number :\t")
        #For validity of phone number
        while(not ID.isdigit() or len(ID) != 10):
            ID = input("Please! Enter valid 10 digit phone number :\t")
        file = "Passwords/" + ID
        #Check if this number is already registered
        if(not os.path.isfile(file)):
            firstTime = True
            while(True):
                if(firstTime):
                    print("Enter password :\t")
                else:
                    print("Retype password :\t")
                password = input()
                print("Enter Confirm password :\t")
                confirmPassword = input()

                if(password == confirmPassword):
                    break
                print("\n\tPassword didn't match\n\n")
                firstTime = False
            
            print("\n\tYour phone number is successfully registred!\n\n")
            if(not os.path.isdir("Passwords")):
                os.mkdir("Passwords/")
            fw = open(file, "w")
            fw.write(password)
            fw.close()

            updateUserHistory(curTime() + "\tPhone no. " + ID + " registred. " + "\n")
        else:
            print("\n\tThis phone number is already registred.\n\n")

#LogiIn class
class LogIn:
    def login():
        ID = input("Enter 10 digit phone number :\t")
        #For validity of phone number
        while(not ID.isdigit() or len(ID) != 10):
            ID = input("Please! Enter valid 10 digit phone number :\t")
        file = "Passwords/" + ID
        #Check if this number is registered
        if(os.path.isfile(file)):
            fr = open(file, "r")
            password = fr.read()
            fr.close()
            while(True):
                enteredPass = input("Enter password :\t")
                if(password == enteredPass):
                    print("\n\tSuccessfully LogIn!\n")
                    updateUserHistory(curTime() + "\tPhone no. " + ID + " loged in. " + "\n")
                    LogIn.afterLogIn(ID)
                    break
                else:
                    print("\n\tWrong password\n\n")
        else:
            print("\n\tThis phone number is not registred.\n\n")
    
    def afterLogIn(ID):
        choice = 0;
        while(choice != 4):
            print("\n1.Recharge\n2.Data plans\n3.Current status of account\n4.LogOut")
            choice = int(input("Enter your choice here :\t"))

            if(choice == 1):
                LogIn.recharge(ID)
            elif(choice == 2):
                LogIn.dataPlans(ID)
            elif(choice == 3):
                LogIn.status(ID)
            elif(choice == 4):
                print("\n\tSuccessfully LogOut!\n")
            else:
                print("\n\tEnter valid option!\n")

    def recharge(ID):
        prevAmount = 0
        #Balance before recharge
        if(os.path.isfile("BalanceInfo/r"+ID)):
            fr = open("BalanceInfo/r"+ID, "r")
            prevAmount = float(fr.read())
            fr.close()

        amount = float(input("\nEnter the amount of recharge :\t"))
        amount += prevAmount
        #Make directory if not exist
        if(not os.path.isdir("BalanceInfo")):
            os.mkdir("BalanceInfo/")
        fw = open("BalanceInfo/r"+ID, "w")
        fw.write(str(amount))
        fw.close()

        updateRechargeHistory(curTime() + "\tPhone no. " + ID + " recharge of " + str(amount - prevAmount) + "\n")
        print("\n\t" + curTime() + " Your current balance is " + str(amount) + "\n")
        
    def dataPlans(ID):
        #Check if any plan is activated
        if(not os.path.isfile("BalanceInfo/dp" + ID)):
            for i in range(1, 4):
                plan = open("DataPlans/" + str(i))
                frmt = open("DataPlans/Formate.txt")
                
                print("\nData Plan: " + str(i))
                for p,f in zip(plan.readlines(),frmt.readlines()):
                    print("  " + f[:-1] + p[:-1])

                plan.close()
                frmt.close()

            choice = 0
            firstTime = True
            while(choice > 3 or choice < 1):
                if(not firstTime):
                    print("Choose correct option from 1, 2, 3.\n")
                choice = int(input("Select any plan from the given plan : "))
                firstTime = False

            if(not os.path.isdir("BalanceInfo")):
                os.mkdir("BalanceInfo/")
            fw = open("BalanceInfo/dp" + ID, "w")
            fw.write(str(choice))
            fw.close()

            updateRechargeHistory(curTime() + "\tPhone no. " + ID + " has selected Data plan " + str(choice) + "\n")
            print("\n\t" + curTime() + " Plan " + str(choice) + " successfully activated.")
        else:
            print("\n\tCurrently, One data plan is Activated in your phone no.\n" + 
                                "\tSo, You can't buy another plan.\n")
            
    def status(ID):
        #Balance
        balance = 0
        if(os.path.isfile("BalanceInfo/r"+ID)):
            fr = open("BalanceInfo/r"+ID, "r")
            balance = fr.read()
            fr.close()
        print("\n\tCurrent balance : " + str(balance) + "\n");

        #Data Plan
        if(os.path.isfile("BalanceInfo/dp"+ID)):
            fr = open("BalanceInfo/dp"+ID, "r")
            planID = fr.read()
            fr.close()
            
            plan = open("DataPlans/" + planID)
            frmt = open("DataPlans/Formate.txt")
            print("\tCurrent activated Data plan : " + planID)
            for p,f in zip(plan.readlines(),frmt.readlines()):
                print("\t  " + f[:-1] + p[:-1])
            plan.close()
            frmt.close()
        else:
            print("\tCurrentely, No data plan is activated.\n")
            
# Admin class
class Administrator:
    def admin():
        userName = input("Enter Admin User Name :\t")
        if(os.path.isfile("Administrator/"+userName)):
            fr = open("Administrator/"+userName)
            password = fr.read()
            fr.close()
            
            while(True):
                enteredPass = input("Enter password :\t");
                if(enteredPass == password):
                    print("\n\tSuccessfully LogIn!\n")
                    Administrator.afterLogIn()
                    break
                else:
                    print("\n\tWrong password\n")
        else:
            print("\n\tYou have entered wrong User Name.\n")

    def afterLogIn():
        choice = 0
        while(True):
            print("\n1.Recharge History\n2.LogIn/SignUp History\n3.LogOut")
            choice = int(input("Enter your choice here :\t"))
            if(choice == 1):
                Administrator.rechargeHistory()
            elif(choice == 2):
                Administrator.userHistory()
            #elif(choice == 3):
            #    Administrator.updateDataPlan()
            elif(choice == 3):
                print("\n\tSuccessfully LogOut!\n")
                break
            else:
                print("\n\tEnter valid option")

    def rechargeHistory():
        print()
        if(os.path.isfile("History/Recharge")):
            file = open("History/Recharge")
            print(file.read())
            file.close()
        else:
            print("\tNo recharge history recorded yet!")

    def userHistory():
        print()
        if(os.path.isfile("History/User")):
            file = open("History/User")
            print(file.read())
            file.close()
        else:
            print("\tNot any user activity history has been recorded yet!")

# Main class
class Main:
    def main():
        choice = 1
        while(True):
            if(choice <= 3 and choice >= 1):
                print("\nIn Main menu\n")
            choice = int(input("1.Adminstrative LogIn\n" +
                                "2.User LogIn\n" + 
                                "3.User SignUp\n" + 
                                "4.Exit\n" + 
                                "ENTER CHOICE HERE :\t"))
            if(choice == 1):
                Main.adminLogIn()
            elif(choice == 2):
                Main.logIn()
            elif(choice == 3):
                Main.signUp()
            elif(choice == 4):
                print("Thanks for using this app")
                break
            else:
                print("\n\tEnter Valid Choice\n")

    def adminLogIn():
        print("\n\nIn Administrator LogIn\n")
        Administrator.admin()
        #print("Admin LogIn process completed\n")

    def logIn():
        print("\n\nIn User LogIn\n")
        LogIn.login()
        #print("\nUser LogIn process completed\n")

    def signUp():
        print("\n\nIn User SignUp\n")
        SignUp.signUp()
        
Main.main()