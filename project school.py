import mysql.connector
con=mysql.connector.connect(host='localhost',user='root',password='sql123',database='hospital')
cur=con.cursor()

#def admin_interface():
#def doctor_interface(id):    





def admin_login():#print(' '*(50-len('')//2),
    print()
    print('='*100)
    print()
    print(' '*(50-len('ADMIN LOGIN')//2),'ADMIN LOGIN')
    print()
    print(' '*(50-len('Enter your credentials')//2),'Enter your Credentials')
    print(' '*(50-len('Enter your credentials')//2),'ID : ',end='')
    id=input()
    print(' '*(50-len('Enter your credentials')//2),'PASSWORD : ',end='')
    pwd=input()
    print()
    print('='*100)
    cur.execute("select * from admin_login")
    data=cur.fetchall()
    for i in data:
        if i[0]==id and i[1]==pwd:
            print()
            print('*'*100)
            print(' '*(50-len('login successful')//2),"Login Successful!")
            print('*'*100)
            print()
            #admin_interface()
            break
    else:
        print()
        print('*'*100)
        print(' '*(50-len('login failed')//2),"Login Failed!")
        print(' '*(50-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*100)
        print()

def doctor_login():
    print('='*100)
    print()
    print(' '*(50-len('DOCTOR LOGIN')//2),'DOCTOR LOGIN')
    print()
    print(' '*(50-len('Enter your credentials')//2),'Enter your Credentials')
    print(' '*(50-len('Enter your credentials')//2),'ID : ',end='')
    id=input()
    print(' '*(50-len('Enter your credentials')//2),'PASSWORD : ',end='')
    pwd=input()
    print()
    print('='*100)
    cur.execute("select * from doctor_login")
    data=cur.fetchall()
    for i in data:
        if i[0]==id and i[1]==pwd:
            print()
            print('*'*100)
            print(' '*(50-len('login successful')//2),"Login Successful!")
            print('*'*100)
            print()
            #doctor_interface(id)
            break
    else:
        print()
        print('*'*100)
        print(' '*(50-len('login failed!')//2),"Login Failed!")
        print(' '*(50-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*100)
        print()
    
def user_page():
    while True:

        print()
        print('='*100)
        print()
        print(' '*(50-len('USER (SIGNIN/LOGIN)')//2),'USER (SIGNIN/LOGIN)')
        print()
        print(' '*(50-len('1. Sign In To Your Account')//2),'1. Sign In To Your Account')
        print(' '*(50-len('1. Sign In To Your Account')//2),'2. Dont have an account? Sign up')
        print(' '*(50-len('1. Sign In To Your Account')//2),'3. Exit to Main Menu')
        print()
        print(' '*(50-len('Enter your Choice')//2),'Enter your Choice')
        print('='*100)

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
                print('*'*100)
                print(' '*(50-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*100)
                print()

        except ValueError:
            print()
            print('*'*100)
            print(' '*(50-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*100)
            print()


def user_login():
    print()
    print('='*100)
    print()
    print(' '*(50-len('USER LOGIN')//2),'USER LOGIN')
    print()
    print(' '*(50-len('Enter your credentials')//2),'Enter your Credentials')
    print(' '*(50-len('Enter your credentials')//2),'ID : ',end='')
    id=input()
    print(' '*(50-len('Enter your credentials')//2),'PASSWORD : ',end='')
    pwd=input()
    print()
    print('='*100)
    print()
    cur.execute("select * from user_login")
    data=cur.fetchall()
    for i in data:
        if i[0]==id and i[1]==pwd:
            print()
            print('*'*100)
            print(' '*(50-len('login successful')//2),"Login Successful!")
            print('*'*100)
            print()
            #doctor_interface(id)
            break
    else:
        print()
        print('*'*100)
        print(' '*(50-len('login failed!')//2),"Login Failed!")
        print(' '*(50-len('Contact Admin to Recover Account')//2),"Contact Admin to Recover Account")
        print(' '*(50-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*100)
        print()









def menu_page():
    while True:
        print()
        print('='*100)
        print()

        print(' '*(50-len('MAIN MENU')//2),'MAIN MENU')
        print()
        print(' '*(50-len('1. Admin(login)')//2),'1. Admin(login)')
        print(' '*(50-len('1. Admin(login)')//2),'2. Doctor(login)')
        print(' '*(50-len('1. Admin(login)')//2),'3. User(signin/login)')
        print(' '*(50-len('1. Admin(login)')//2),'4. Exit')

        print()
        print(' '*(50-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*100)

    
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
                print('='*100)
                print(' '*(50-len('THANK YOU!!!')//2),'THANK YOU!!!')
                print('='*100)
                break
            else:
                print()
                print('*'*100)
                print(' '*(50-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*100)
                print()
                
            

        except ValueError:
            print()
            print('*'*100)
            print(' '*(50-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*100)
            print()
            




def welcome_page():
    
    print('='*100)
    print()
    print(' '*(50-len('WELCOME TO NAGRAJU HOSPITAL')//2),'WELCOME TO NAGRAJU HOSPITAL')
    print()
    print(' '*(50-len('1. Main Menu')//2),'1. Main Menu')
    print(' '*(50-len('1. Main Menu')//2),'2. Exit')
    print()

    print(' '*(50-len('Enter your choice')//2),'Enter your choice')
    print()
    print('='*100)
    
    while True:
        try:
            ch=int(input())
            if ch==1:
                menu_page()
            elif ch==2:
                print()
                print('='*100)
                print(' '*(50-len('THANK YOU!!!')//2),'THANK YOU!!!')
                print('='*100)
                print()
                break
            else:
                
                print()
                print('*'*100)
                print(' '*(50-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                print('*'*100)
                print()
                welcome_page()
            break  

        except ValueError:
            print()
            print('*'*100)
            print(' '*(50-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            
            print('*'*100)
            print()
            
            welcome_page()




welcome_page()
