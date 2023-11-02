import mysql.connector
import tabulate
import time
con=mysql.connector.connect(host='localhost',user='root',password='sql123',database='hospital')
cur=con.cursor()
def admin_edit():
    while True:
        print()
        print('='*120)
        print()
        print(' '*(60-len('ADMIN CREDENTIALS')//2),'ADMIN CREDENTIALS')
        print()
        #print list of admin logins in tabular format
        cur.execute('select * from admin_login')
        data=cur.fetchall()
        heading=['ID','PASSWORD']
        print(tabulate.tabulate(data,headers=heading))
        print(' '*(60-len('1. Edit Admin')//2),'1. Add Admin')
        print(' '*(60-len('1. Edit Admin')//2),'2. Delete Admin')
        print(' '*(60-len('1. Edit Admin')//2),'3. Password Change')
        print(' '*(60-len('1. Edit Admin')//2),'4. Back')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print('='*120)

        try:
            ch=int(input())
            if ch==1:
                    c=0
                    print()
                    print('='*120)
                    print()
                    print(' '*(60-len('ADMIN CREATION')//2),'ADMIN CREATION')
                    print()
                    print(' '*(60-len('Enter new Credentials')//2),'Enter new Credentials')
                    print(' '*(60-len('Enter new Credentials')//2),'ID : ',end='')
                    id=input()
                    print(' '*(60-len('Enter new Credentials')//2),'PASSWORD : ',end='')
                    pwd=input()
                    print()
                    print('='*120)
                    for i in data:
                        if id==i[0]:
                            c=1
                    if c==1:
                        print()
                        print('*'*120)
                        print(' '*(60-len('INVALID CHOICE')//2),'INVALID CHOICE')
                        print(' '*(60-len('ID ENTERED ALREADY EXISTS!!')//2),'ID ENTERED ALREADY EXISTS!!')
                        print('*'*120)
                        print()
                        
                    else:
                        cur.execute(f"insert into admin_login values('{id}','{pwd}')")
                        con.commit()
                        print(f"insert into admin_login values('{id}','{pwd}')")
                        print()
                        print('*'*120)
                        print(' '*(60-len('NEW ADMIN USER CREATED!!!')//2),'NEW ADMIN USER CREATED!!!')
                        print('*'*120)

                        #log report
                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        f=open('report.txt','a')
                        temp='['+current_time+'] : '+f"ADMIN CREATED (ID : '{id}', PWD : '{pwd}')"
                        f.write(temp)
                        f.write('\n\n')
                        f.close()
                        # log report over


                        
            elif ch==2:
                if len(data)>1:
                    c=0
                    print()
                    print('='*120)
                    print()
                    print(' '*(60-len('ADMIN DELETION')//2),'ADMIN DELETION')
                    print()
                    print(tabulate.tabulate(data,headers=heading))
                    print()
                    print(' '*(60-len('Enter Admin ID to be deleted : ')//2),'Enter Admin ID to be deleted : ',end='')
                    id=input()
                    for i in data:
                        if id==i[0]:
                            c=1
                    if c==0:
                        print()
                        print('*'*120)
                        print(' '*(60-len('INVALID CHOICE')//2),'INVALID CHOICE')
                        print(' '*(60-len('ID ENTERED DOES NOT EXIST!!')//2),'ID ENTERED DOES NOT EXIST!!')
                        print('*'*120)
                        print()
                    
                    else:
                        cur.execute(f"delete from admin_login where id='{id}'")
                        con.commit()
                        print()
                        print('*'*120)
                        print(' '*(60-len('SELECTED ADMIN CREDENTIALS DELETED')//2),'SELECTED ADMIN CREDENTIALS DELETED')
                        print('*'*120)

                        #log report
                        t = time.localtime()
                        current_time = time.strftime("%H:%M:%S", t)
                        f=open('report.txt','a')
                        temp='['+current_time+'] : '+f"ADMIN DELETED (ID : '{id}')"
                        f.write(temp)
                        f.write('\n\n')
                        f.close()
                        #log report

                else:
                    print()
                    print('*'*120)
                    print(' '*(60-len('DELETION FAILED')//2),'DELETION FAILED')
                    print(' '*(60-len('ATLEAST ONE ADMIN NEEDS TO BE PRESENT')//2),'ATLEAST ONE ADMIN NEEDS TO BE PRESENT')
                    print('*'*120)

                    #log report
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    f=open('report.txt','a')
                    temp='['+current_time+'] : '+"ADMIN DELETION ATTEMPT"
                    f.write(temp)
                    f.write('\n\n')
                    f.close()
                    #log report


            elif ch==3:
                c=0
                print()
                print('='*120)
                print()
                print(' '*(60-len('PASSWORD CHANGE')//2),'PASSWORD CHANGE')
                print()
                print(tabulate.tabulate(data,headers=heading))
                print()
                print(' '*(60-len('Enter your credentials')//2),'Enter your Credentials')
                print()
                print(' '*(60-len('Enter your credentials')//2),'ID : ',end='')
                id=input()
                print(' '*(60-len('Enter your credentials')//2),'NEW PASSWORD : ',end='')
                pwd=input()
                print()
                print('='*120)               
                
                for i in data:
                    if id==i[0]:
                        c=1
                if c==0:
                    print()
                    print('*'*120)
                    print(' '*(60-len('INVALID CHOICE')//2),'INVALID CHOICE')
                    print(' '*(60-len('ID ENTERED DOES NOT EXIST!!')//2),'ID ENTERED DOES NOT EXIST!!')
                    print('*'*120)
                    print()
                
                else:
                    cur.execute(f"update admin_login set password ='{pwd}' where id='{id}'")
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('PASSWORD CHANGED')//2),'PASSWORD CHANGED')
                    print('*'*120)

                    #log report
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    f=open('report.txt','a')
                    temp='['+current_time+'] : '+f"ADMIN PASSWORD CHANGED (ID : '{id}', PWD : '{pwd}')"

                    f.write(temp)
                    f.write('\n\n')
                    f.close()
                    #log report
                
            elif ch==4:
                break
            else:
                print()
                print('*'*120)
                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*120)
                print()

        except ValueError:
            print()
            print('*'*120)
            print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*120)
            print()


def admin_interface():
    while True:
        print()
        print('='*120)
        print()
        print(' '*(60-len('ADMIN MODULE')//2),'ADMIN MODULE')
        print()
        print(' '*(60-len('1. Edit Admin')//2),'1. Edit Admin')
        print(' '*(60-len('1. Edit Admin')//2),'2. Edit Doctors')
        print(' '*(60-len('1. Edit Admin')//2),'3. Edit Users')
        print(' '*(60-len('1. Edit Admin')//2),'4. Logout')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print('='*120)

        try:
            ch=int(input())
            if ch==1:
                admin_edit()
                
            elif ch==2:
                #doctor_edit
                pass
                break
            elif ch==3:
                #user_edit
                pass
                break
            elif ch==4:
                print()
                print('*'*120)
                print(' '*(60-len('LOGGED OUT')//2),'LOGGED OUT')
                print('*'*120)

                #log report
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                f=open('report.txt','a')
                temp='['+current_time+'] : '+'LOGOUT'
                f.write(temp)
                f.write('\n\n')
                f.write('-'*50)
                f.close()
                #log report

                break
            else:
                print()
                print('*'*120)
                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*120)
                print()

        except ValueError:
            print()
            print('*'*120)
            print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*120)
            print()



def admin_login():
    print()
    print('='*120)
    print()
    print(' '*(60-len('ADMIN LOGIN')//2),'ADMIN LOGIN')
    print()
    print(' '*(60-len('Enter your credentials')//2),'Enter your Credentials')
    print(' '*(60-len('Enter your credentials')//2),'ID : ',end='')
    id=input()
    print(' '*(60-len('Enter your credentials')//2),'PASSWORD : ',end='')
    pwd=input()
    print()
    print('='*120)
    cur.execute("select * from admin_login")
    data=cur.fetchall()
    for i in data:
        if i[0]==id and i[1]==pwd:
            print()
            print('*'*120)
            print(' '*(60-len('login successful')//2),"Login Successful!")
            print('*'*120)
            print()

            #log report
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            f=open('report.txt','a')
            f.write('\n\n')
            f.write('-'*50)
            f.write('\n\n')
            temp='['+current_time+'] : '+'LOGIN BY : '+id
            f.write(temp)
            f.write('\n\n')
            f.close()
            #log report over

            admin_interface()
            break
    else:
        print()
        print('*'*120)
        print(' '*(60-len('login failed')//2),"Login Failed!")
        print(' '*(60-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*120)
        print()

def doctor_login():
    print('='*120)
    print()
    print(' '*(60-len('DOCTOR LOGIN')//2),'DOCTOR LOGIN')
    print()
    print(' '*(60-len('Enter your credentials')//2),'Enter your Credentials')
    print(' '*(60-len('Enter your credentials')//2),'ID : ',end='')
    id=input()
    print(' '*(60-len('Enter your credentials')//2),'PASSWORD : ',end='')
    pwd=input()
    print()
    print('='*120)
    cur.execute("select * from doctor_login")
    data=cur.fetchall()
    for i in data:
        if i[0]==id and i[1]==pwd:
            print()
            print('*'*120)
            print(' '*(60-len('login successful')//2),"Login Successful!")
            print('*'*120)
            print()
            #doctor_interface(id)
            break
    else:
        print()
        print('*'*120)
        print(' '*(60-len('login failed!')//2),"Login Failed!")
        print(' '*(60-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*120)
        print()
    
def user_page():
    while True:

        print()
        print('='*120)
        print()
        print(' '*(60-len('USER (SIGNIN/LOGIN)')//2),'USER (SIGNIN/LOGIN)')
        print()
        print(' '*(60-len('1. Sign In To Your Account')//2),'1. Sign In To Your Account')
        print(' '*(60-len('1. Sign In To Your Account')//2),'2. Dont have an account? Sign up')
        print(' '*(60-len('1. Sign In To Your Account')//2),'3. Exit to Main Menu')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print('='*120)

        try:
            ch=int(input())
            if ch==1:
                user_login()
                break
            elif ch==2:
                #user_signup()
                pass
            elif ch==3:
                break
            else:
                print()
                print('*'*120)
                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*120)
                print()

        except ValueError:
            print()
            print('*'*120)
            print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*120)
            print()


def user_login():
    print()
    print('='*120)
    print()
    print(' '*(60-len('USER LOGIN')//2),'USER LOGIN')
    print()
    print(' '*(60-len('Enter your credentials')//2),'Enter your Credentials')
    print(' '*(60-len('Enter your credentials')//2),'ID : ',end='')
    id=input()
    print(' '*(60-len('Enter your credentials')//2),'PASSWORD : ',end='')
    pwd=input()
    print()
    print('='*120)
    print()
    cur.execute("select * from user_login")
    data=cur.fetchall()
    for i in data:
        if i[0]==id and i[1]==pwd:
            print()
            print('*'*120)
            print(' '*(60-len('login successful')//2),"Login Successful!")
            print('*'*120)
            print()
            #user_interface(id)
            break
    else:
        print()
        print('*'*120)
        print(' '*(60-len('login failed!')//2),"Login Failed!")
        print(' '*(60-len('Contact Admin to Recover Account')//2),"Contact Admin to Recover Account")
        print(' '*(60-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*120)
        print()


def menu_page():
    while True:
        print()
        print('='*120)
        print()

        print(' '*(60-len('MAIN MENU')//2),'MAIN MENU')
        print()
        print(' '*(60-len('1. Admin(login)')//2),'1. Admin(login)')
        print(' '*(60-len('1. Admin(login)')//2),'2. Doctor(login)')
        print(' '*(60-len('1. Admin(login)')//2),'3. User(signin/login)')
        print(' '*(60-len('1. Admin(login)')//2),'4. Exit')

        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)

    
        try:
            ch=int(input())

            if ch==1:
                admin_login()
            elif ch==2:
                doctor_login()
            elif ch==3:
                user_page()
            elif ch==4:
                print()
                print('='*120)
                print(' '*(60-len('THANK YOU!!!')//2),'THANK YOU!!!')
                print('='*120)
                break
            else:
                print()
                print('*'*120)
                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*120)
                print()
                
        except ValueError:
            print()
            print('*'*120)
            print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*120)
            print()
            

def welcome_page():
    while True:
        print('='*120)
        print()
        print(' '*(60-len('WELCOME TO NAGRAJU HOSPITAL')//2),'WELCOME TO NAGRAJU HOSPITAL')
        print()
        print(' '*(60-len('1. Main Menu')//2),'1. Main Menu')
        print(' '*(60-len('1. Main Menu')//2),'2. Exit')
        print()

        print(' '*(60-len('Enter your choice')//2),'Enter your choice')
        print()
        print('='*120)
             
        try:
            ch=int(input())
            if ch==1:
                menu_page()
                break
            elif ch==2:
                print()
                print('='*120)
                print(' '*(60-len('THANK YOU!!!')//2),'THANK YOU!!!')
                print('='*120)
                print()
                break
            
            else:
                print()
                print('*'*120)
                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*120)
                print()
                #welcome_page()
            
        except ValueError:
            print()
            print('*'*120)
            print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            
            print('*'*120)
            print()
            
            #welcome_page()
        
welcome_page()
