import mysql.connector
import tabulate
import time
import datetime
con=mysql.connector.connect(host='localhost',user='root',password='sql123')
cur=con.cursor()
cur.execute('create database if not exists hospital')
cur.execute('use hospital')
cur.execute('create table if not exists user_login(id varchar(100), password varchar(100))')
cur.execute('create table if not exists doctor_login(id varchar(100), password varchar(100))')
cur.execute('create table if not exists admin_login(id varchar(100), password varchar(100))')
con.commit()
cur.execute("select * from admin_login")
test=cur.fetchall()
if len(test)==0:
    cur.execute("insert into admin_login values('admin','admin' )") 
cur.execute('create table if not exists bill_list(item_code varchar(100),item varchar(100), cost float)')
cur.execute('create table if not exists patient_list(id varchar(100), fname varchar(100), lname varchar(100), sex varchar(100), age int, job varchar(100), marital_status varchar(100), notifications varchar(100))')
cur.execute('create table if not exists doctor_list(id varchar(100), name varchar(100), speciality varchar(100), experience int, status varchar(100))')
con.commit()

admin_activity=False # to check if admin is entering or user is entering user_interface
#---------------------------------------------------------------------------------------------------------------------------------------------------------
def reset_bill():
    cur.execute("drop table bill_list")
    cur.execute('create table if not exists bill_list(item_code varchar(100),item varchar(100), cost float)')
    f=open('bill_item_list.txt','r')
    bill_item_query="insert into bill_list values"+f.read()
    #print(items)
    cur.execute(bill_item_query)
    con.commit()

#---------------------------------------------------------------------------------------------------------------------------------------------------------
def reset_doctor():
    cur.execute("select * from doctor_login")
    doctor_ids=cur.fetchall()
    for i in doctor_ids:
        q="drop table "+i[0]+"_appointment_request"
        cur.execute(q)
        q="drop table "+i[0]+"_patient_list"
        cur.execute(q)
        q=f"delete from doctor_login where id='{i[0]}'"
        cur.execute(q)
        q=f"delete from doctor_list where id='{i[0]}'"
        cur.execute(q)
        con.commit()

    f=open("doctor_list.txt",'r')
    line=' '
    line=f.read()
    line=line.split('\n')
    for details in line:
        if details=='':
            break
        record=details.split(',')
        d_id=record[0]
        pwd=d_id
        doc_name=record[1]
        doc_speciality=record[2]
        exp=record[3]
        #print(f"insert into doctor_login values({d_id},{pwd})")
        cur.execute(f"insert into doctor_login values('{d_id}','{pwd}')")
        cur.execute(f"insert into doctor_list values('{d_id}','{doc_name}','{doc_speciality}',{exp},'available')")
        cur.execute(f"create table if not exists {d_id}_patient_list(patient_id varchar(100), name varchar(100))")
        cur.execute(f"create table if not exists {d_id}_appointment_request(patient_id varchar(100), name varchar(100), message varchar(100))")
        con.commit()
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------
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
        print()
        print('='*120)

        try:
            ch=int(input('-->'))
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------


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
        print(' '*(60-len('1. Edit Admin')//2),'4. Edit Bill List')
        print(' '*(60-len('1. Edit Admin')//2),'5. Logout')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)

        try:
            ch=int(input('-->'))
            if ch==1:
                admin_edit()
               
            elif ch==2:
                #log report
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                f=open('report.txt','a')
                temp='['+current_time+'] : '+'DOCTOR EDITING'
                f.write(temp)
                f.write('\n\n')
                f.close()
                #log report
                while True:
                    print('='*120)
                    print()
                    print(' '*(60-len('DOCTOR EDIT')//2),'DOCTOR EDIT')
                    print()
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'1. Edit Doctor Profile')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'2. Edit Doctor Patients/Appointments')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'3. Edit Doctor Login Details')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'4. Add New Doctor')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'5. Delete Doctor')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'6. Back')
                    print()
                    print(' '*(60-len('Enter your choice')//2),'Enter your choice')
                    print()
                    print('='*120)    
                    try:
                        ch=int(input('-->'))
                        if ch==1:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('DOCTOR PROFILE')//2),'DOCTOR PROFILE')
                            print()
                            q="select * from doctor_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','Name','Speciality','Experience','Status']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            print('='*120)
                        
                            q=f"select id from doctor_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                
                            else:
                                doctor_profile(id)

                        elif ch==2:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('DOCTOR PATIENT')//2),'DOCTOR PATIENT')
                            print()
                            q="select * from doctor_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','Name','Speciality','Experience','Status']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            print('='*120)
                        
                            q=f"select id from doctor_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                            else:
                                doctor_patient(id)

                        elif ch==3:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('DOCTOR LOGIN DETAILS')//2),'DOCTOR LOGIN DETAILS')
                            print()
                            q="select * from doctor_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','Name','Speciality','Experience','Status']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            q=f"select id from doctor_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                
                                print('='*120)
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                            else:
                               
                                print()
                                print(' '*(60-len('Enter New Password : ')//2),'Enter New Password : ',end='')
                                PWD=input()
                                print('='*120)
                                q=f'update doctor_login set password="{PWD}" where id="{id}"'
                                cur.execute(q)
                                con.commit()
                                print()
                                print('*'*120)
                                print(' '*(60-len('PASSWORD CHANGED')//2),'PASSWORD CHANGED')
                                print('*'*120)

                        elif ch==4:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('DOCTOR CREATION')//2),'DOCTOR CREATION')
                            print()
                            
                            while True:
                                print(' '*(60-len('Enter Doctor ID (format=d###) : ')//2),'Enter Doctor ID (format=d###) : ',end='')
                                d_id=input()
                                print()
                                cur.execute(f"select * from doctor_login where id='{d_id}'")
                                temp=cur.fetchall()
                                if len(temp)==0:
                                    break
                                else:
                                    print()
                                    print('*'*120)
                                    print(' '*(60-len(f'DOCTOR WITH ID : "{d_id}" ALREADY EXISTS')//2),f'DOCTOR WITH ID : "{d_id}" ALREADY EXISTS')
                                    print('*'*120)
                                    print()
                                
                            print(' '*(60-len('Enter Doctor ID (format=d###) : ')//2),'Enter Doctor Name : ',end='')
                            doc_name=input()
                            print()
                            print(' '*(60-len('Enter Doctor ID (format=d###) : ')//2),'Enter Doctor Speciality : ',end='')
                            doc_speciality=input()
                            doc_speciality=doc_speciality.lower()
                            
                            while True:
                                try:
                                    print()
                                    print(' '*(60-len('Enter Doctor ID (format=d###) : ')//2),'Enter Doctor Experience(yrs) : ',end='')
                                    exp=int(input())
                                    print()
                                    break
                                except ValueError:
                                    print()
                                    print('*'*120)
                                    print(' '*(60-len('Enter Age in Integer Format')//2),'Enter Age in Integer Format')
                                    print('*'*120)
                                    print()
                            
                            print(' '*(60-len('Enter Doctor ID (format=d###) : ')//2),'Enter Login Password : ',end='')
                            pwd=input()
                            print()
                            print('='*120)
                            cur.execute(f"insert into doctor_login values('{d_id}','{pwd}')")
                            cur.execute(f"insert into doctor_list values('{d_id}','{doc_name}','{doc_speciality}',{exp},'available')")
                            cur.execute(f"create table if not exists {d_id}_patient_list(patient_id varchar(100), name varchar(100))")
                            cur.execute(f"create table if not exists {d_id}_appointment_request(patient_id varchar(100), name varchar(100), message varchar(100))")

                            cur.execute(f"select * from doctor_list where id='{d_id}'")
                            data=cur.fetchall()
                            heading=['ID','Name','Speciality','Experience','Status']
                            print()
                            print('='*120)
                            print()
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print('='*120)
                            print()
                            print('*'*120)
                            print(' '*(60-len('NEW DOCTOR ACCOUTN CREATED')//2),'NEW DOCTOR ACCOUNT CREATED')
                            print('*'*120)
                            print()
                            
                        elif ch==5:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('DOCTOR DELETE')//2),'DOCTOR DELETE')
                            print()
                            q="select * from doctor_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','Name','Speciality','Experience','Status']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            print('='*120)
                        
                            q=f"select id from doctor_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                
                            else:
                                print()
                                print('='*120)
                                print()
                                print(' '*(60-len('ARE YOU SURE?')//2),'ARE YOU SURE?')
                                print(' '*(60-len('THIS PROCESS IS IRREVERSIBLE')//2),'THIS PROCESS IS IRREVERSIBLE')
                                print()
                                print(' '*(60-len('ENTER (Y/N) : ')//2),'ENTER (Y/N) : ',end='')
                                ch=input()
                                if ch in "Yy":
                                    q1=f"delete from doctor_login where id='{id}' "
                                    q2=f"delete from doctor_list where id='{id}' "
                                    q3="drop table "+id+"_patient_list"
                                    q4="drop table "+id+"_appointment_request"
                                    cur.execute(q1)
                                    cur.execute(q2)
                                    cur.execute(q3)
                                    cur.execute(q4)
                                    con.commit()
                                    print()
                                    print('*'*120)
                                    print(' '*(60-len('ACCOUNT DELETED SUCCESSFULLY')//2),'ACCOUNT DELETED SUCCESSFULLY')
                                    print('*'*120) 
                        elif ch==6:
                            reset_doctor()
                            print()
                            print('='*120)
                            print()
                            print('*'*120)
                            print(' '*(60-len('RESET TO DEFAULT')//2),'RESET TO DEFAULT')
                            print('*'*120)
                            print()

                        elif ch==7:
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
  
            elif ch==3:
                while True:
                    print('='*120)
                    print()
                    print(' '*(60-len('USER EDIT')//2),'USER EDIT')
                    print()
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'1. Edit User Profile')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'2. Edit User Login Details')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'3. Add New User')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'4. Delete User')
                    print(' '*(60-len('1. Edit Doctor Profile')//2),'5. Back')
                    print()
                    print(' '*(60-len('Enter your choice')//2),'Enter your choice')
                    print()
                    print('='*120)
                    try:
                        ch=int(input('-->'))
                        if ch==1:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('USER PROFILE')//2),'USER PROFILE')
                            print()
                            q="select * from patient_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','FName','LName','Sex','Age','Occupation','Marital_status','Messages']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            print('='*120)
                        
                            q=f"select id from patient_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                
                            else:
                                user_profile(id)
                        elif ch==2:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('USER LOGIN DETAILS')//2),'USER LOGIN DETAILS')
                            print()
                            q="select * from patient_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','FName','LName','Sex','Age','Occupation','Marital_status','Messages']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            
                        
                            q=f"select id from patient_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                print('='*120)
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                
                            else:
            
                                print(' '*(60-len('Enter New Password : ')//2),'Enter New Password : ',end='')
                                PWD=input()
                                print()
                                print('='*120)
                                q=f'update user_login set password="{PWD}" where id="{id}"'
                                cur.execute(q)
                                con.commit()
                                print()
                                print('*'*120)
                                print(' '*(60-len('PASSWORD CHANGED')//2),'PASSWORD CHANGED')
                                print('*'*120)
                                print()



                        elif ch==3:
                            global admin_activity
                            admin_activity=True
                            user_signup() 
                            admin_activity=False
                        elif ch==4:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('USER DELETE')//2),'USER DELETE')
                            print()
                            q="select * from patient_list"
                            cur.execute(q)
                            data=cur.fetchall()
                            heading=['ID','FName','LName','Sex','Age','Occupation','Marital_status','Messages']
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter id to be edited : ')//2),'Enter id to be edited : ',end='')
                            id=input()
                            print()
                            print('='*120)
                        
                            q=f"select id from patient_list where id='{id}'"
                            cur.execute(q)
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                                print('*'*120)
                                print()
                
                            else:
                                print()
                                print('='*120)
                                print()
                                print(' '*(60-len('ARE YOU SURE?')//2),'ARE YOU SURE?')
                                print(' '*(60-len('THIS PROCESS IS IRREVERSIBLE')//2),'THIS PROCESS IS IRREVERSIBLE')
                                print()
                                print(' '*(60-len('ENTER (Y/N) ')//2),'ENTER (Y/N) ',end='')
                                ch=input('-->')
                                if ch in "Yy":
                                    q1=f"delete from user_login where id='{id}' "
                                    q2=f"delete from patient_list where id='{id}' "
                                    temp=id+'_bill'
                                    q3=f"drop table {temp}"
                                    cur.execute("select id from doctor_login")
                                    doctor_id_list=cur.fetchall()
                                    for i in doctor_id_list:
                                        table_name=i[0]+'_patient_list'
                                        q=f"delete from {table_name} where patient_id='{id}'"
                                        cur.execute(q)
                                        table_name=i[0]+'_appointment_request'
                                        q=f"delete from {table_name} where patient_id='{id}'"
                                        cur.execute(q)
                                        
                                    cur.execute(q1)
                                    cur.execute(q2)
                                    cur.execute(q3)
                                    con.commit()
                                    print()
                                    print('*'*120)
                                    print(' '*(60-len('ACCOUNT DELETED SUCCESSFULLY')//2),'ACCOUNT DELETED SUCCESSFULLY')
                                    print('*'*120)

                        elif ch==5:
                            break
                              
                    except ValueError:
                        print()
                        print('*'*120)
                        print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
                        print('*'*120)
                        print()
            elif ch==4:
                while True:
                    print()
                    print('='*120)
                    print()
                    print(' '*(60-len('BILL UPDATE')//2),'BILL UPDATE')
                    print()
                    q="select * from bill_list"
                    cur.execute(q)
                    data=cur.fetchall()
                    heading=['Item_Code','Item','Cost']
                    print(tabulate.tabulate(data,headers=heading))
                    print()
                    print(' '*(60-len('1. Add New Item')//2),'1. Add New Item')
                    print(' '*(60-len('1. Add New Item')//2),'2. Delete Item')
                    print(' '*(60-len('1. Add New Item')//2),'3. Update Item')
                    print(' '*(60-len('1. Add New Item')//2),'4. Back')
                    print(' '*(60-len('1. Add New Item')//2),'5. Reset to Default')
                    print()
                    print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
                    print()
                    print('='*120)
                    try:
                        ch=int(input('-->'))
                        if ch==1:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('NEW ITEM')//2),'NEW ITEM')
                            while True:
                                print()
                                print(' '*(60-len('Enter Item Code : ')//2),'Enter Item Code : ',end='')
                            
                                item_code=input()
                                
                                cur.execute(f"select * from bill_list where item_code='{item_code}'")
                                data=cur.fetchone()
                                if data!=None:
                                    print()
                                    print('*'*120)
                                    print(' '*(60-len('ITEM CODE ALREADY IN USE')//2),'ITEM CODE ALREADY IN USE')
                                    print('*'*120)
                                    print()
                                else:
                                    break
                            print()
                            print(' '*(60-len('Enter Item Name : ')//2),'Enter Item Name : ',end='')
                            item_name=input()
                            print()
                            print(' '*(60-len('Enter Item Cost : ')//2),'Enter Item Cost : ',end='')
                            item_cost=float(input())
                            cur.execute(f"insert into bill_list values('{item_code}','{item_name}',{item_cost})")
                            con.commit()
                            print()
                            print('='*120)
                            print()
                            print('*'*120)
                            print(' '*(60-len('ITEM ADDED')//2),'ITEM ADDED')
                            print('*'*120)
                            print()

                        elif ch==2:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('ITEM DELETION')//2),'ITEM DELETION')
                            print()
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter Item Code to DELETE : ')//2),'Enter Item Code to DELETE : ',end='')
                            item_code=input()
                            cur.execute(f"select * from bill_list where item_code='{item_code}'")
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('ITEM CODE DOESNT EXIST')//2),'ITEM CODE DOESNT EXIST')
                                print('*'*120)
                                print()

                            else:
                                cur.execute(f"delete from bill_list where item_code='{item_code}'")
                                con.commit()
                                print()
                                print('='*120)
                                print()
                                print('*'*120)
                                print(' '*(60-len('ITEM DELETED')//2),'ITEM DELETED')
                                print('*'*120)
                                print()


                            
                        elif ch==3:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('ITEM UPDATION')//2),'ITEM UPDATION')
                            print()
                            print(tabulate.tabulate(data,headers=heading))
                            print()
                            print(' '*(60-len('Enter Item Code to Update : ')//2),'Enter Item Code to Update : ',end='')
                            item_code=input()
                            cur.execute(f"select * from bill_list where item_code='{item_code}'")
                            data=cur.fetchone()
                            if data==None:
                                print()
                                print('*'*120)
                                print(' '*(60-len('ITEM CODE DOESNT EXIST')//2),'ITEM CODE DOESNT EXIST')
                                print('*'*120)
                                print()

                            else:
                                print(' '*(60-len(f'Enter New cost of {item_code} : ')//2),f'Enter New cost of {item_code} : ',end='')
                                item_price=input()
                                cur.execute(f"update bill_list set cost={item_price} where item_code='{item_code}'")
                                con.commit()
                                print()
                                print('='*120)
                                print()
                                print('*'*120)
                                print(' '*(60-len('ITEM UPDATED')//2),'ITEM UPDATED')
                                print('*'*120)
                                print()


                        elif ch==4:
                            break
                        elif ch==5:
                            reset_bill()
                            print()
                            print('='*120)
                            print()
                            print('*'*120)
                            print(' '*(60-len('RESET TO DEFAULT LIST')//2),'RESET TO DEFAULT LIST')
                            print('*'*120)
                            print()
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
                
            elif ch==5:
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
                f.write('\n')
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------


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
#---------------------------------------------------------------------------------------------------------------------------------------------------------
def doctor_profile(id): #can be used in admin module also
    while True:
        q=f"select * from doctor_list where id='{id}'"
        cur.execute(q)
        data=cur.fetchone()
        print()
        print('='*120)
        print()
        print(' '*(60-len('PROFILE')//2),'PROFILE')
        print()
        print(' '*(60-len('ID                    : d101')//2),'ID\t\t\t: ',data[0])
        print(' '*(60-len('ID                    : d101')//2),'NAME\t\t\t: ',data[1])
        print(' '*(60-len('ID                    : d101')//2),'SPECIALITY\t\t: ',data[2])
        print(' '*(60-len('ID                    : d101')//2),'EXPERIENCE\t\t: ',data[3])
        print(' '*(60-len('ID                    : d101')//2),'STATUS\t\t\t: ',data[4])
        print()
        print(' '*(60-len('ID                    : d101')//2),'-'*40)
        print()
        print(' '*(60-len('1. Update Name')//2),'1. Update Name')
        print(' '*(60-len('1. Update Name')//2),'2. Update Speciality')
        print(' '*(60-len('1. Update Name')//2),'3. Update Experience')
        print(' '*(60-len('1. Update Name')//2),'4. Update Status')
        print(' '*(60-len('1. Update Name')//2),'5. Change Password')
        print(' '*(60-len('1. Update Name')//2),'6. DELETE ACCOUNT')
        print(' '*(60-len('1. Update Name')//2),'7. Back')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)
        try:
            ch=int(input('-->'))
            if ch==1:
                print()
                print('='*120)
                print()
                print(' '*(60-len('NAME CHANGE')//2),'NAME CHANGE')
                print()
                print(' '*(60-len('Enter new Name : ')//2),'Enter new Name : ',end='')
                name=input()
                print('='*120)
                q=f'update doctor_list set name="{name}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('NAME CHANGED')//2),'NAME CHANGED')
                print('*'*120)


            elif ch==2:
                print()
                print('='*120)
                print()
                print(' '*(60-len('SPECIALITY UPDATE')//2),'SPECIALITY UPDATE')
                print()
                print(' '*(60-len('Enter Speciality(s) : ')//2),'Enter Speciality(s) : ',end='')
                speciality=input()
                print('='*120)
                q=f'update doctor_list set speciality="{speciality}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('SPECIALITY UPDATED')//2),'SPECIALITY UPDATED')
                print('*'*120)
               
               
            elif ch==3:
                print()
                print('='*120)
                print()
                print(' '*(60-len('EXPERIENCE UPDATE')//2),'EXPERIENCE UPDATE')
                print()
                print(' '*(60-len('Enter Experience : ')//2),'Enter Experience : ',end='')
                exp=int(input())
                print('='*120)
                q=f'update doctor_list set experience={exp} where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('EXPERIENCE UPDATED')//2),'EXPERIENCE UPDATED')
                print('*'*120)

               
            elif ch==4:
                while True:

                    print()
                    print('='*120)
                    print()
                    print(' '*(60-len('STATUS UPDATE')//2),'STATUS UPDATE')
                    print()
                    print(' '*(60-len('1. AVAILABLE')//2),'1. AVAILABLE')
                    print(' '*(60-len('1. AVAILABLE')//2),'2. AWAY')
                    print(' '*(60-len('1. AVAILABLE')//2),'3. BUSY')
                    print(' '*(60-len('1. AVAILABLE')//2),'4. DO NOT DISTURB(wont recieve appointments)')
                    print(' '*(60-len('1. AVAILABLE')//2),'5. Custom')
                    print()
                    print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
                    print()
                    print('='*120)

                    try:
                        ch=int(input('-->'))

                        if ch==1:
                            q=f"update doctor_list set status='available' where id='{id}'"
                            cur.execute(q)
                            con.commit()
                            print()
                            print('*'*120)
                            print(' '*(60-len('STATUS UPDATED')//2),'STATUS UPDATED')
                            print('*'*120)
       
                        elif ch==2:
                            q=f"update doctor_list set status='away' where id='{id}'"
                            cur.execute(q)
                            con.commit()
                            print()
                            print('*'*120)
                            print(' '*(60-len('STATUS UPDATED')//2),'STATUS UPDATED')
                            print('*'*120)
                        elif ch==3:
                            q=f"update doctor_list set status='busy' where id='{id}'"
                            cur.execute(q)
                            con.commit()
                            print()
                            print('*'*120)
                            print(' '*(60-len('STATUS UPDATED')//2),'STATUS UPDATED')
                            print('*'*120)
                        elif ch==5:
                            print()
                            print('='*120)
                            print()
                            print(' '*(60-len('Enter custom Status : ')//2),'Enter custom Status : ',end='')
                            stat=input()
                            print()
                            print('='*120)
                            q=f"update doctor_list set status='{stat}' where id='{id}'"
                            cur.execute(q)
                            con.commit()
                            print()
                            print('*'*120)
                            print(' '*(60-len('STATUS UPDATED')//2),'STATUS UPDATED')
                            print('*'*120)
                        elif ch==4:
                            q=f"update doctor_list set status='dnd' where id='{id}'"
                            cur.execute(q)
                            con.commit()
                            print()
                            print('*'*120)
                            print(' '*(60-len('STATUS UPDATED')//2),'STATUS UPDATED')
                            print('*'*120)

                        else:
                            print()
                            print('*'*120)
                            print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
                            print('*'*120)
                            print()
                        break
                    except ValueError:
                        print()
                        print('*'*120)
                        print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
                        print('*'*120)
                        print()
            elif ch==5:
                print()
                print('='*120)
                print()
                print(' '*(60-len('PASSWORD CHANGE')//2),'PASSWORD CHANGE')
                print()
                print(' '*(60-len('Enter New Password : ')//2),'Enter New Password : ',end='')
                PWD=input()
                print('='*120)
                q=f'update doctor_login set password="{PWD}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('PASSWORD CHANGED')//2),'PASSWORD CHANGED')
                print('*'*120)

            elif ch==6:
                print()
                print('='*120)
                print()
                print(' '*(60-len('ARE YOU SURE?')//2),'ARE YOU SURE?')
                print(' '*(60-len('THIS PROCESS IS IRREVERSIBLE')//2),'THIS PROCESS IS IRREVERSIBLE')
                print()
                print(' '*(60-len('ENTER (Y/N) : ')//2),'ENTER (Y/N) : ',end='')
                ch=input()
                if ch in "Yy":
                    q1=f"delete from doctor_login where id='{id}' "
                    q2=f"delete from doctor_list where id='{id}' "
                    q3="drop table "+id+"_patient_list"
                    q4="drop table "+id+"_appointment_request"
                    cur.execute(q1)
                    cur.execute(q2)
                    cur.execute(q3)
                    cur.execute(q4)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('ACCOUNT DELETED SUCCESSFULLY')//2),'ACCOUNT DELETED SUCCESSFULLY')
                    print('*'*120)
                    break
            elif ch==7:
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------
def doctor_manage_patient(d_id,p_id):
    while True:
        cur.execute(f"select * from patient_list where id='{p_id}'")
        patient_details=cur.fetchall()
        heading=['ID','Fname','Lname','Sex','Age','Job','Marital_Status','Message']
        print()
        print('='*120)
        print()
        print(' '*(60-len(f'MANAGE {p_id}')//2),f'MANAGE {p_id}')
        print()
        print(tabulate.tabulate(patient_details,headers=heading))
        print()
        print(' '*(60-len('1. Send Message')//2),'1. Send Message')
        print(' '*(60-len('1. Send Message')//2),'2. Update Bill')
        print(' '*(60-len('1. Send Message')//2),'3. Discharge Patient')
        print(' '*(60-len('1. Send Message')//2),'4. Back')
        print()
        print(' '*(60-len('Enter your Choice : ')//2),'Enter your Choice : ',end='')
        try:
            ch=int(input())
            print()

            if ch==1:
                print(' '*(60-len('Enter Message : ')//2),'Enter Message : ',end='')
                msg=input()
                msg='doctor : '+msg
                cur.execute(f"update patient_list set notifications='{msg}' where id='{p_id}'")
                con.commit()
                print()
                print('='*120)
                print()
                print('*'*120)
                print(' '*(60-len('Message sent')//2),'MESSAGE SENT')
                print('*'*120)
                print()

            elif ch==2:
                while True:
                    print('='*120)
                    print()
                    print('='*120)
                    print()
                    cur.execute("select * from bill_list")
                    bill_items=cur.fetchall()
                    heading=['ITEM_CODE','ITEM','COST']
                    print(' '*(60-len('BILL UPDATE')//2),'BILL UPDATE')
                    print()
                    print(tabulate.tabulate(bill_items,headers=heading))
                    print()
                    print(' '*(60-len('SEARCH Item Name/Code (type exit to go back) : ')//2),'SEARCH Item Name/Code (type exit to go back) : ',end='')
                    search_term=input()
                    search_term=search_term.lower()
                    print()
                    if search_term  =='exit' or search_term=='back' or search_term=='leave':
                        break
                    cur.execute(f"select * from bill_list where item_code like '{search_term}%' or item like '{search_term}%' ")
                    result=cur.fetchall()
                    if len(result)==0:
                        print(' '*(60-len(f'NO RESULTS FOUND FOR {search_term}')//2),f'NO RESULTS FOUND FOR {search_term}')
                        print()
                        print('='*120)
                        continue

                    else:
                        print(' '*(60-len('SEARCH RESULTS')//2),'SEARCH RESULTS')
                        print()
                        print(tabulate.tabulate(result,headers=heading))
                        print()
                        print(' '*(60-len('Enter Item Code : ')//2),'Enter Item Code : ',end='')
                        item_code=input()
                        print()
                        cur.execute(f"select * from bill_list where item_code='{item_code}'")
                        check=cur.fetchall()
                        if len(check)==0:
                            print(' '*(60-len('INVALID CODE')//2),'INVALID CODE',end='')
                            print()
                            print('='*120)
                            continue
                        
                        else:

                            while True:
                                print(' '*(60-len('Enter qty : ')//2),'Enter qty : ',end='')
                                try:
                                    qty=int(input())
                                    break 
                                except ValueError:
                                    print()
                                    print('='*120)
                                    print()
                                    print('*'*120)
                                    print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
                                    print('*'*120)
                                    print()
                            item_name=check[0][1]
                            item_cost=check[0][2]
                            item_total_cost=qty*item_cost
                            cur.execute(f"insert into {p_id}_bill values('{item_name}',{item_cost},{qty},{item_total_cost})")
                            con.commit()


            elif ch==3:
                cur.execute(f"delete from {d_id}_patient_list where patient_id='{p_id}'")

                cur.execute(f"update patient_list set notifications='You have been discharged by the Doctor, Enter 4 to print your BILL' where id='{p_id}'")
                con.commit()
                print('='*120)
                print()
                print('*'*120)
                print(' '*(60-len('Patient Discharged')//2),'Patient Discharged')
                print('*'*120)
                print()
                break


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

#---------------------------------------------------------------------------------------------------------------------------------------------------------
def doctor_patient(id):
    
    q="select * from "+id+"_patient_list"
    cur.execute(q)
    patient_list=cur.fetchall()
    heading=['ID','Name']
    print()
    print('='*120)
    print()
    print(' '*(60-len('PATIENT LIST')//2),'PATIENT LIST')
    print()
    print(tabulate.tabulate(patient_list,headers=heading))
    print()
    print(' '*(60-len('Enter Patient ID to manage : ')//2),'Enter Patient ID to manage : ',end='')

    p_id=input()
    print()
    print('='*120)
    p_id=p_id.lower()
    q=f'select * from {id}_patient_list where patient_id="{p_id}"'
    cur.execute(q)
    check=cur.fetchall()
    
    if len(check)==0:
        print()
        print('*'*120)
        print(' '*(60-len('ID DOESNT EXIST')//2),'ID DOESNT EXIST')
        print('*'*120)
        print()
    
    else:
        doctor_manage_patient(id,p_id)


#--------------------------------------------------------------------------------------------------------------------------------------------------------- 
def doctor_interface(id):
    while True:
        q=f'select doctor_list.name from doctor_list,doctor_login where doctor_list.id=doctor_login.id and doctor_list.id="{id}"; '
        cur.execute(q)
       
        data=cur.fetchone()
        if data==None :# after deleting acount, needs to exit loop
            break
        name=data[0]
       
        head='DOCTOR '+name.upper()
        print('='*120)
        print()
        print(' '*(60-len(head)//2),head)
        print()
        print(' '*(60-len('1. Profile')//2),'1. Profile')
        print(' '*(60-len('1. Profile')//2),'2. Patients')
        print(' '*(60-len('1. Profile')//2),'3. View Appointments')
        print(' '*(60-len('1. Profile')//2),'4. Delete Appointments')
        print(' '*(60-len('1. Profile')//2),'5. Log Out')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)

        try:
            ch=int(input('-->'))
            if ch==1:
                doctor_profile(id)
               
            elif ch==2:
                #for doctor seeing patients
                doctor_patient(id)
            elif ch==3:
                cur.execute(f"select * from {id}_appointment_request")
                appointment=cur.fetchall()
                
                heading=['PATIENT ID','NAME','MESSAGE']
                print()
                print('='*120)
                print()
                print(' '*(60-len('APPOINTMENT REQUESTS')//2),'APPOINTMENT REQUESTS')
                print()
                print(tabulate.tabulate(appointment,headers=heading))
                print()
                print(' '*(60-len('Enter Patient ID to accept : ')//2),'Enter Patient ID to accept : ',end='')
                p_id=input()            
                print()
                print('='*120)
                for i in appointment:
                    if i[0]==p_id:
                        break
                else:
                    print()
                    print('*'*120)
                    print(' '*(60-len('INVALID ID')//2),'INVALID ID')
                    print('*'*120)
                    print()
                    continue

                cur.execute(f"delete from {id}_appointment_request where patient_id='{p_id}'")
                cur.execute(f"insert into {id}_patient_list values('{p_id}','{i[1]}')")
                cur.execute(f"update patient_list set notifications='APPOINTMENT ACCEPTED BY {id}' where id='{p_id}'")
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('APPOINTMENT ACCEPTED')//2),'APPOINTMENT ACCEPTED')
                print(' '*(60-len('Patient can be viewed under "Patients" section')//2),'Patient can be viewed under "Patients" section')
                print('*'*120)
            elif ch==4:
                cur.execute(f"select * from {id}_appointment_request")
                appointment=cur.fetchall()
                heading=['PATIENT ID','NAME','MESSAGE']
                print()
                print('='*120)
                print()
                print(' '*(60-len('APPOINTMENT REQUESTS')//2),'APPOINTMENT REQUESTS')
                print()
                print(tabulate.tabulate(appointment,headers=heading))
                print()
                print(' '*(60-len('Enter Patient ID to decline : ')//2),'Enter Patient ID to decline : ',end='')
                p_id=input()            
                print()
                print('='*120)
                for i in appointment:
                    if i[0]==p_id:
                        break
                else:
                    print()
                    print('*'*120)
                    print(' '*(60-len('INVALID ID')//2),'INVALID ID')
                    print('*'*120)
                    print()
                    continue

                cur.execute(f"delete from {id}_appointment_request where patient_id='{p_id}'")
                #cur.execute(f"insert into {id}_patient_list values('{p_id}','{i[1]}')")
                cur.execute(f"update patient_list set notifications='APPOINTMENT DECLINED BY {id}' where id='{p_id}'")
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('APPOINTMENT DELETED')//2),'APPOINTMENT DELETED')
                #print(' '*(60-len('Patient can be viewed under "Patients" section')//2),'Patient can be viewed under "Patients" section')
                print('*'*120)

            elif ch==5:
                print()
                print('*'*120)
                print(' '*(60-len('LOGGED OUT')//2),'LOGGED OUT')
                print('*'*120)
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

#---------------------------------------------------------------------------------------------------------------------------------------------------------

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
            doctor_interface(id)
            break
    else:
        print()
        print('*'*120)
        print(' '*(60-len('login failed!')//2),"Login Failed!")
        print(' '*(60-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*120)
        print()

#---------------------------------------------------------------------------------------------------------------------------------------------------------
def user_signup():

    print()
    print('='*120)
    print()
    print(' '*(60-len('USER SIGNIN')//2),'USER SIGNIN')
    print()
    print(' '*(60-len('Enter First Name : ')//2),'Enter First Name : ',end='')
    fname=input()
    print()
    print(' '*(60-len('Enter First Name : ')//2),'Enter Last Name : ',end='')
    lname=input()
    print()
    while True:
        print(' '*(60-len('Enter Sex(M/F) : ')//2),'Enter Sex(M/F) : ',end='')
        sex=input()
        sex=sex.lower()
        if sex!='m' and sex!='f':
            print()
            print('*'*120)
            print(' '*(60-len('INVALID SEX!')//2),"INVALID SEX!")
            print('*'*120)
            print()
        else:
            break
    while True:
        try:
            print()
            print(' '*(60-len('Enter Age : ')//2),'Enter Age : ',end='')
            age=int(input())
            print()
            break
        except ValueError:
            print()
            print('*'*120)
            print(' '*(60-len('The choice has to be an integer!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
            print('*'*120)
            print()
       
   
    print(' '*(60-len('Enter Occupation : ')//2),'Enter Occupation : ',end='')
    job=input()
    print()

    while True:
       
        print(' '*(60-len('Enter Marital status(m/nm) : ')//2),'Enter Marital status(m/nm) : ',end='')
        m_status=input()
        m_status=m_status.lower()
       
        if m_status != 'nm' and m_status!='m':
            print()
            print('*'*120)
            print(' '*(60-len('INVALID INPUT')//2),"INVALID INPUT")
            print('*'*120)
            print()
        else:
            break        
        print()
    id=''
    print()
    print(' '*(60-len('Enter Password : ')//2),'Enter Password : ',end='')
    pwd=input()
    print()
    print('='*120)
   
    #+lname[0:2]+str(age)
    try:
        id+=fname[0:2]
       
    except Exception:
        id+=fname
       
    try:
        id+=lname[0:2]
       
    except Exception:
        id+=lname
       
    id+=str(age)
    temp_id=id
    id_variable=0
    while True:
        #print(f"select id from user_login where id='{temp_id}'")
        cur.execute(f"select id from user_login where id='{temp_id}'")

        existing_id_check=cur.fetchall()
        if existing_id_check==[]:
            break
        else:
            temp_id=id
            id_variable+=1
            temp_id+=str(id_variable)
    id=temp_id  
    notif='none'
    q=f"insert into patient_list values('{id}','{fname}','{lname}','{sex}',{age},'{job}','{m_status}','{notif}')"
   
    cur.execute(q)
    q=f'insert into user_login values("{id}","{pwd}")'
    cur.execute(q)
    table_name=id+'_bill'
    q=f'create table {table_name}(item varchar(100),cost float ,qty int,total_cost float)'
    cur.execute(q)
    con.commit()
    #create table aa1_bill(item varchar(100),cost float ,qty int,total_cost float)
    print()
    print('*'*120)
    print(' '*(60-len('Account Created Successfully')//2),"Account Created Successfully")
    print('*'*120)
    print()
    if admin_activity==False:
        user_interface(id)
#---------------------------------------------------------------------------------------------------------------------------------------------------------              
def user_profile(id):
    while True:
        q=f"select id,fname,lname,sex,age,job,marital_status from patient_list where id='{id}' "
        cur.execute(q)
        data=cur.fetchall()
        
        '''
        fname=data[0]
        lname=data[1]
        sex=data[2]
        age=data[3]
        job=data[4]
        marital_status=data[5]'''

        heading=['ID','FName','LName','Sex','Age','Occupation','Marital_status']

    
        print()
        print('='*120)
        print()
        print(' '*(60-len('PROFILE')//2),'PROFILE')
        print()
        print(tabulate.tabulate(data,headers=heading))
        print()
        print(' '*(60-len('1. Update First Name')//2),'1. Update First Name')
        print(' '*(60-len('1. Update First Name')//2),'2. Update Last Name')
        print(' '*(60-len('1. Update First Name')//2),'3. Update Sex')
        print(' '*(60-len('1. Update First Name')//2),'4. Update Age')
        print(' '*(60-len('1. Update First Name')//2),'5. Update Job')
        print(' '*(60-len('1. Update First Name')//2),'6. Update Marital Status')
        print(' '*(60-len('1. Update First Name')//2),'7. CHANGE PASSWORD')
        print(' '*(60-len('1. Update First Name')//2),'8. DELETE ACCOUNT')
        print(' '*(60-len('1. Update First Name')//2),'9. Back')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)

        

        try:
            ch=int(input('-->'))
            if ch==1:
                print()
                print('='*120)
                print()
                print(' '*(60-len('FIRST-NAME UPDATE')//2),'FIRST-NAME UPDATE')
                print()
                print(' '*(60-len('Enter First Name : ')//2),'Enter First Name : ',end='')
                fname=input()
                print('='*120)
                q=f'update patient_list set fname="{fname}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('FIRST-NAME UPDATED')//2),'FIRST-NAME UPDATED')
                print('*'*120)

            elif ch==2:
                print()
                print('='*120)
                print()
                print(' '*(60-len('LAST-NAME UPDATE')//2),'LAST-NAME UPDATE')
                print()
                print(' '*(60-len('Enter Last Name : ')//2),'Enter Last Name : ',end='')
                lname=input()
                print('='*120)
                q=f'update patient_list set lname="{lname}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('LAST-NAME UPDATED')//2),'LAST-NAME UPDATED')
                print('*'*120)


            elif ch==3:
                print()
                print('='*120)
                print()
                print(' '*(60-len('SEX UPDATE')//2),'SEX UPDATE')
                print()
                print(' '*(60-len('Enter Sex : ')//2),'Enter Sex : ',end='')
                sex=input()
                sex=sex.lower()
                if sex not in'mf':
                    print()
                    print('*'*120)
                    print(' '*(60-len('INVALID SEX!')//2),"INVALID SEX!")
                    print('*'*120)
                    print()
                else:
                    print('='*120)
                    q=f'update patient_list set sex="{sex}" where id="{id}"'
                    cur.execute(q)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('SEX UPDATED')//2),'SEX UPDATED')
                    print('*'*120)

            elif ch==4:
                print()
                print('='*120)
                print()
                print(' '*(60-len('AGE UPDATE')//2),'AGE UPDATE')
                print()
                print(' '*(60-len('Enter Age : ')//2),'Enter Age : ',end='')
                try:
                    age=int(input())
                    print('='*120)
                    q=f'update patient_list set age={age} where id="{id}"'
                    cur.execute(q)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('AGE UPDATED')//2),'AGE UPDATED')
                    print('*'*120)
                except ValueError:
                    print()
                    print('*'*120)
                    print(' '*(60-len('AGE HAS TO BE AN INTEGER!!!')//2),'AGE HAS TO BE AN INTEGER!!!')
                    print('*'*120)
                    print()

               
            elif ch==5:
                print()
                print('='*120)
                print()
                print(' '*(60-len('JOB UPDATE')//2),'JOB UPDATE')
                print()
                print(' '*(60-len('Enter Job : ')//2),'Enter Job : ',end='')
                job=input()
                print('='*120)
                q=f'update patient_list set job="{job}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('JOB UPDATED')//2),'JOB UPDATED')
                print('*'*120)
                
            elif ch==6:
                print()
                print('='*120)
                print()
                print(' '*(60-len('MARITAL STATUS UPDATE')//2),'MARITAL STATUS UPDATE')
                print()
                
       
                print(' '*(60-len('Enter Marital Status(m/nm) : ')//2),'Enter Marital Status(m/nm) : ',end='')
                m_status=input()
                m_status=m_status.lower()
    
                if m_status != 'nm' and m_status!='m':
                    print()
                    print('*'*120)
                    print(' '*(60-len('INVALID INPUT')//2),"INVALID INPUT")
                    print('*'*120)
                    print()
                else:
    
                    print('='*120)
                    q=f'update patient_list set marital_status="{m_status}" where id="{id}"'
                    cur.execute(q)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('MARITAL STATUS UPDATED')//2),'MARITAL STATUS UPDATED')
                    print('*'*120)
    
            elif ch==8:
                print()
                print('='*120)
                print()
                print(' '*(60-len('ARE YOU SURE?')//2),'ARE YOU SURE?')
                print(' '*(60-len('THIS PROCESS IS IRREVERSIBLE')//2),'THIS PROCESS IS IRREVERSIBLE')
                print()
                print(' '*(60-len('ENTER (Y/N) ')//2),'ENTER (Y/N) ',end='')
                ch=input('-->')
                if ch in "Yy":
                    q1=f"delete from user_login where id='{id}' "
                    q2=f"delete from patient_list where id='{id}' "
                    temp=id+'_bill'
                    q3=f"drop table {temp}"
                    cur.execute("select id from doctor_login")
                    doctor_id_list=cur.fetchall()
                    for i in doctor_id_list:
                        table_name=i[0]+'_patient_list'
                        q=f"delete from {table_name} where patient_id='{id}'"
                        cur.execute(q)
                        table_name=i[0]+'_appointment_request'
                        q=f"delete from {table_name} where patient_id='{id}'"
                        cur.execute(q)
                        
                    cur.execute(q1)
                    cur.execute(q2)
                    cur.execute(q3)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('ACCOUNT DELETED SUCCESSFULLY')//2),'ACCOUNT DELETED SUCCESSFULLY')
                    print('*'*120)
                    break
            elif ch==7:
                print()
                print('='*120)
                print()
                print(' '*(60-len('PASSWORD CHANGE')//2),'PASSWORD CHANGE')
                print()
                print(' '*(60-len('Enter New Password : ')//2),'Enter New Password : ',end='')
                PWD=input()
                print('='*120)
                q=f'update user_login set password="{PWD}" where id="{id}"'
                cur.execute(q)
                con.commit()
                print()
                print('*'*120)
                print(' '*(60-len('PASSWORD CHANGED')//2),'PASSWORD CHANGED')
                print('*'*120)
            elif ch==9:
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


#---------------------------------------------------------------------------------------------------------------------------------------------------------     
def set_appointment(id):
    
    heading=['ID','Name','Speciality','Experience','Status']
    while True:
        print()
        print('='*120)
        print()
        print(' '*(60-len('APPOINTMENT REQUEST')//2),'APPOINTMENT REQUEST')
        
        print()
        print(' '*(60-len('1. Search For Doctor by ID')//2),'1. Search For Doctor by ID')
        print(' '*(60-len('1. Search For Doctor by ID')//2),'2. Search For Doctor by Name')
        print(' '*(60-len('1. Search For Doctor by ID')//2),'3. Search For Doctor by Speciality')

        print(' '*(60-len('1. Search For Doctor by ID')//2),'4. Back')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)


        try:
            ch=int(input('-->'))
            if ch==1:
                q="select * from doctor_list where status!='dnd'"
                cur.execute(q)
                data=cur.fetchall()
                
                print()
                print('='*120)
                print()
                print(tabulate.tabulate(data,headers=heading))
                print(' '*(60-len('Enter ID of Doctor : ')//2),'Enter ID of Doctor : ',end='')
                doc_id=input()
                doc_id=doc_id.lower()
                print()
                q=f'select * from doctor_list where id="{doc_id}" and status!="dnd"'
                cur.execute(q)
                check=cur.fetchall()
                
                if len(check)==0:
                    print()
                    print('*'*120)
                    print(' '*(60-len('ID DOESNT EXIST')//2),'ID DOESNT EXIST')
                    print('*'*120)
                    print()
                    continue
                else:
                    print(' '*(60-len('Enter Your Appointment Request Message (enter details like date/illness) : ')//2),'Enter Your Appointment Request Message (enter details like date/illness) : ',end='')
                    msg=input()
                    msg='patient : '+msg
                    print()
                    print('='*120)
                    q=f'select fname from patient_list where id="{id}"'
                    cur.execute(q)
                    patient_name=cur.fetchall()
                    patient_name=patient_name[0][0]
                    doc_appointment_table_name=doc_id+'_appointment_request'
                    q=f"insert into {doc_appointment_table_name} values('{id}','{patient_name}','{msg}')"
                    cur.execute(q)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('APPOINTMENT REQUEST SENT SUCCESSFULLY')//2),'APPOINTMENT REQUEST SENT SUCCESSFULLY')
                    print(' '*(60-len('You will recieve a message when the doctor approves your appointment')//2),'You will recieve a message when the doctor approves your appointment')
                    print('*'*120)
                    print()


            elif ch==2:
                q="select * from doctor_list where status!='dnd'"
                cur.execute(q)
                data=cur.fetchall()
                
                print()
                print('='*120)
                print()
                print(' '*(60-len('SEARCH BY DOCTOR NAME')//2),'SEARCH BY DOCTOR NAME')
                print()
                print(tabulate.tabulate(data,headers=heading))
                print()
                print(' '*(60-len('Enter Name of Doctor : ')//2),'Enter Name of Doctor : ',end='')
                doc_name=input()
                doc_name=doc_name.lower()
                print()
                print('='*120)
                q=f'select * from doctor_list where name like "{doc_name}%" and status!="dnd"'
                
                cur.execute(q)
                search_result=cur.fetchall()
                
                if len(search_result)==0:
                    print()
                    print('*'*120)
                    temp=f'DOCTOR BY THE NAME "{doc_name}" DOESNT EXIST'
                    print(' '*(60-len(temp)//2),temp)
                    print('*'*120)
                    print()
                #elif len(search_result)==1:

                else:
                    
                    doc_id=search_result[0][0]
                    print()
                    print('='*120)
                    print()
                    print(' '*(60-len('SEARCH RESULTS')//2),'SEARCH RESULTS')
                    print()
                    print(tabulate.tabulate(search_result,headers=heading))
                    print()

                    if len(search_result)!=1:
                        print(' '*(60-len('Enter ID of Doctor : ')//2),'Enter ID of Doctor : ',end='')
                        doc_id=input()
                        doc_id=doc_id.lower()
                        print()
                        
                        q=f'select * from doctor_list where id="{doc_id}" and status!="dnd"'
                        cur.execute(q)
                        check=cur.fetchone()
                        
                        if len(check)==0:
                            print()
                            print('*'*120)
                            print(' '*(60-len('ID DOESNT EXIST')//2),'ID DOESNT EXIST')
                            print('*'*120)
                            print()
                            continue

                    print()
                    print(' '*(60-len('Enter Your Appoint Request Message (enter details like date/illness) : ')//2),'Enter Your Appoint Request Message (enter details like date/illness) : ',end='')
                    msg=input()
                    msg='patient : '+msg
                    print()
                    print('='*120)
                    q=f'select fname from patient_list where id="{id}"'
                    cur.execute(q)
                    patient_name=cur.fetchone()
                    patient_name=patient_name[0][0]
                    doc_appointment_table_name=doc_id+'_appointment_request'
                    q=f"insert into {doc_appointment_table_name} values('{id}','{patient_name}','{msg}')"
                    cur.execute(q)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('APPOINTMENT REQUEST SENT SUCCESSFULLY')//2),'APPOINTMENT REQUEST SENT SUCCESSFULLY')
                    print(' '*(60-len('You will recieve a message when the doctor approves your appointment')//2),'You will recieve a message when the doctor approves your appointment')
                    print('*'*120)
                    print()

            elif ch==3:#incomplete
                
                print()
                print('='*120)
                print()
                print(' '*(60-len('SEARCH BY SPECIALITY')//2),'SEARCH BY SPECIALITY')
                print()
                print(' '*(60-len('Enter Speciality : ')//2),'Enter Speciality : ',end='')
                
                speciality_search=input('-->')
                speciality_search=speciality_search.lower()
                print()
                print('='*120)
                q=f"select * from doctor_list where speciality like '{speciality_search}%' and status!='dnd' "
                cur.execute(q)
                search_result=cur.fetchall()
                if len(search_result)==0:
                    print()
                    print('*'*120)
                    print(' '*(60-len('NO RESULT')//2),'NO RESULT')
                    print('*'*120)
                    print()
                else:
                    doc_id=search_result[0][0]
                    print()
                    print('='*120)
                    print()
                    print(' '*(60-len('SEARCH RESULTS')//2),'SEARCH RESULTS')
                    print()
                    print(tabulate.tabulate(search_result,headers=heading))
                    print()
                    if len(search_result)!=1:
                        print(' '*(60-len('Enter ID of Doctor : ')//2),'Enter ID of Doctor : ',end='')
                        doc_id=input()
                        doc_id=doc_id.lower()
                        print()
                        
                        q=f'select * from doctor_list where id="{doc_id}" and status!="dnd"'
                        cur.execute(q)
                        check=cur.fetchall()
                        
                        if len(check)==0:
                            print()
                            print('*'*120)
                            print(' '*(60-len('ID DOESNT EXIST')//2),'ID DOESNT EXIST')
                            print('*'*120)
                            print()
                            continue

                    print(' '*(60-len('Enter Your Appoint Request Message (enter details like date/illness) : ')//2),'Enter Your Appoint Request Message (enter details like date/illness) : ',end='')
                    msg=input()
                    msg='patient : '+msg
                    print()
                    print('='*120)
                    q=f'select fname from patient_list where id="{id}"'
                    cur.execute(q)
                    patient_name=cur.fetchall()
                    patient_name=patient_name[0][0]
                    doc_appointment_table_name=doc_id+'_appointment_request'
                    q=f"insert into {doc_appointment_table_name} values('{id}','{patient_name}','{msg}')"
                    cur.execute(q)
                    con.commit()
                    print()
                    print('*'*120)
                    print(' '*(60-len('APPOINTMENT REQUEST SENT SUCCESSFULLY')//2),'APPOINTMENT REQUEST SENT SUCCESSFULLY')
                    print(' '*(60-len('You will recieve a message when the doctor approves your appointment')//2),'You will recieve a message when the doctor approves your appointment')
                    print('*'*120)
                    print()           
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------          
def user_interface(id):
    while True:
        q=f"select notifications from patient_list where id='{id}' "
        cur.execute(q)
        data=cur.fetchone()
        if data==None:
            break
        data=data[0]
        if data=='none':
            notif="NO MESSAGES"
        else:
            notif=data
        print()
        print('='*120)
        print()
        heading="Patient ID : "+id
        print(' '*(60-len(heading)//2),heading)
        print()
        #center allign the notif    
        print('MESSAGES : ',notif)
        print()
        print(' '*(60-len('1. Profile')//2),'1. Profile')
        print(' '*(60-len('1. Profile')//2),'2. Set Appointment')
        print(' '*(60-len('1. Profile')//2),'3. Exit to Main Menu')
        print()
        print(' '*(60-len('Enter your Choice')//2),'Enter your Choice')
        print()
        print('='*120)    
        try:       
            ch=int(input('-->'))
            if ch==1:
                user_profile(id)
            elif ch==2:
                set_appointment(id)
            elif ch==3:
                break               
            elif ch==4:
                cur.execute(f"update patient_list set notifications='none' where id='{id}'")
                con.commit()
                cur.execute(f"select * from {id}_bill")
                bill=cur.fetchall()
                print()
                print('='*120)
                print()
                print(' '*(60-len('BILL PREVIEW')//2),'BILL PREVIEW')
                print()
                print(tabulate.tabulate(bill,headers=['Item Name','Cost','Quantity','Total Price']))
                print()
                
                cur.execute(f"select fname,lname from patient_list where id='{id}'")
                name=cur.fetchall()
                name=name[0][0]+'_'+name[0][1]+'_'+id
                print(' '*(60-len(f'Bill has been generated under the file Name "{name}.txt"')//2),f'Bill has been generated under the file Name "{name}.txt"')
                dt=str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)+"-"+str(datetime.datetime.now().hour)+"-"+str(datetime.datetime.now().minute)+"-"+str(datetime.datetime.now().second)
                invoice =str(dt)  # unique invoice code it makes

                date = str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-" +str(datetime.datetime.now().day)  
                d=str(date)  #date
             
                f=open(name+'.txt','w')
                f.write('='*100)
                f.write('\n')
                t=' '*(50-len('NAGRAJU HOSPITAL')//2)+'NAGRAJU HOSPITAL'
                f.write(t)
                f.write('\n\n')
                t='HOSPITAL BILL'
                f.write(t)
                f.write('\n\n')
                f.write('Invoice: '+invoice+' '*(100-len('Invoice: '+invoice)-len('Date: '+d+' '))+'Date: '+d+' ')
                f.write('\n\n')
                f.write('Patient Name : '+name)
                f.write('\n\n')
                f.write('-'*100)
                f.write('\n')
                t='SL_NO.'+' '*(20-len('SL_NO.'))+'ITEM NAME'+ ' '*(20-len('ITEM NAME'))+ str('UNIT PRICE')+' '*(20-len(str('UNIT PRICE')))+str('QUANTITY')+' '*(20-len(str('QUANTITY')))+str('TOTAL')+' '*(20-len(str('TOTAL')))
                f.write(t)
                f.write('\n')
                f.write('-'*100)
                f.write('\n')
                slno=1
                grand_total=0

                for i in bill:
                    f.write(str(slno)+'.'+' '*(20-len(str(slno)+'.'))+i[0]+' '*(20-len(i[0]))+str(i[1])+' '*(20-len(str(i[1])))+str(i[2])+' '*(20-len(str(i[2])))+str(i[3])+' '*(20-len(str(i[3]))))
                    f.write('\n\n')
                    slno+=1
                    grand_total+=i[3]
                    grand_total=(int(grand_total*100))/100
                    gst=(int(grand_total*18))/100
                    payable_amt=grand_total+gst
                    

                f.write('-'*100)
                f.write('\n')
                f.write(' '*(80-len('GRAND TOTAL : '))+'GRAND TOTAL : '+str(grand_total)+'Rs')
                f.write('\n')
                f.write('-'*100)
                f.write('\n\n')
                f.write(' '*(80-len('GST (18%) : '))+'GST (18%) : '+str(gst)+'Rs')
                f.write('\n\n')
                f.write(' '*(80-len('PAYABLE AMOUNT : '))+'PAYABLE AMOUNT : '+str(payable_amt)+'Rs')
                f.write('\n\n')
                f.write('='*100)
                f.write('\n')
                f.write(' '*(50-len('Thank You For Choosing Nagaraju Hospital')//2)+'Thank You For Choosing Nagaraju Hospital')
                f.write('\n')
                f.write('='*100)
                f.close()

                cur.execute(f"delete from {id}_bill")
                con.commit()
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------  
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
        print()
        print('='*120)
        try:
            ch=int(input('-->'))
            if ch==1:
                user_login()
                break
            elif ch==2:
                user_signup()
                
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------
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
            user_interface(id)
            break
    else:
        print()
        print('*'*120)
        print(' '*(60-len('login failed!')//2),"Login Failed!")
        print(' '*(60-len('Contact Admin to Recover Account')//2),"Contact Admin to Recover Account")
        print(' '*(60-len('Returning to Main Menu')//2),"Returning to Main Menu")
        print('*'*120)
        print()
#---------------------------------------------------------------------------------------------------------------------------------------------------------
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
            ch=int(input('-->'))
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------        
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
            ch=int(input('-->'))
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
#---------------------------------------------------------------------------------------------------------------------------------------------------------   

'''

cur.execute('create table if not exists user_login(id varchar(100), password varchar(100))')
cur.execute('create table if not exists doctor_login(id varchar(100), password varchar(100))')
cur.execute('create table if not exists admin_login(id varchar(100), password varchar(100))')
cur.execute('create table if not exists bill_list(item_code varchar(100),item varchar(100), cost float)')
cur.execute("insert into admin_login values('admin','admin' )")
con.commit()
`````
cur.execute("insert into doctor_login values('d101','d101' )")
cur.execute("insert into doctor_login values('d102','d102' )")
cur.execute("insert into doctor_login values('d103','d103' )")
con.commit()

cur.execute("insert into user_login values('u101','u101' )")
cur.execute("insert into user_login values('u102','u102' )")
cur.execute("insert into user_login values('u103','u103' )")
cur.execute("insert into user_login values('u104','u104' )")
cur.execute("insert into user_login values('u105','u105' )")
con.commit()

cur.execute('create table if not exists doctor_list(id varchar(100), name varchar(100), speciality varchar(100), experience int, status varchar(100))')
cur.execute("insert into doctor_list values('d101','dyan','heart',10,'available')")
#status---available,busy,away,dnd
cur.execute("insert into doctor_list values('d102','nishanth','brain',8,'busy')")
cur.execute("insert into doctor_list values('d103','jeevith','eye',9,'away')")
con.commit()

cur.execute('create table if not exists d101_patient_list(patient_id varchar(100), name varchar(100))')
cur.execute('create table if not exists d102_patient_list(patient_id varchar(100), name varchar(100))')
cur.execute('create table if not exists d103_patient_list(patient_id varchar(100), name varchar(100))')
con.commit()

cur.execute('create table if not exists d101_appointment_request(patient_id varchar(100), name varchar(100), message varchar(100))')
cur.execute('create table if not exists d102_appointment_request(patient_id varchar(100), name varchar(100), message varchar(100))')
cur.execute('create table if not exists d103_appointment_request(patient_id varchar(100), name varchar(100), message varchar(100))')
cur.execute('create table if not exists patient_list(id varchar(100), fname varchar(100), lname varchar(100), sex varchar(100), age int, job varchar(100), marital_status varchar(100), notifications varchar(100))')
cur.execute('create table if not exists doctor_list(id varchar(100), name varchar(100), speciality varchar(100), experience int, status varchar(100))')
'''


'''
#for account deleting checking
cur.execute("insert into doctor_login values('d103','d103' )")
cur.execute("insert into doctor_list values('d103','jeevith','eye',9,'away')")
cur.execute('create table if not exists d103_patient_list(patient_id varchar(100), name varchar(100))')
cur.execute('create table if not exists d103_appointment_request(patient_id varchar(100), name varchar(100))')
con.commit()

cur.execute('create table if not exists patient_list(id varchar(100), fname varchar(100), lname varchar(100), sex varchar(100), age int, job varchar(100), marital_status varchar(100), notifications varchar(100))')
'''



'''

print('='*120)
print()
print(' '*(60-len('')//2),'')
print()
print(' '*(60-len('1. ')//2),'1.')
print(' '*(60-len('1. ')//2),'2.')
print(' '*(60-len('1. ')//2),'3.')
print(' '*(60-len('1. ')//2),'4.')
print(' '*(60-len('1. ')//2),'5.')
print()
print(' '*(60-len('Enter your choice')//2),'Enter your choice')
print()
print('='*120)    
try:
    ch=int(input('-->'))
    if ch==1:
        pass
    elif ch==2:
       pass
    elif ch==3:
        pass
    elif ch==4:
        pass
    elif ch==5:
        print()
        print('='*120)
        print(' '*(60-len('')//2),'')
        print('='*120)
        print()
    else:
        print()
        print('*'*120)
        print(' '*(60-len('INVALID CHOICE!!')//2),'INVALID CHOICE!!')
        print('*'*120)
        print()
except ValueError:
    print()
    print('*'*120)
    print(' '*(60-len('The choice has to be an intger!!!')//2),'THE CHOICE HAS TO BE AN INTEGER!!!')
    print('*'*120)
    print()

'''
'''
#to create query for adding items in bill_list
l=['Abacavir', 'Acyclovir', 'Alemtuzumab', 'Alendronate', 'Allopurinol', 'Amifostine', 'Amikacin', 'Aminocaproic Acid', 'Amitriptyline', 'Amlodipine', 'Amoxicillin', 'Amphotericin B', 'Ampicillin', 'Anti-Inhibitor Coagulant Complex (FEIBA)', 'Anti-thymocyte globulin', 'Aprepitant', 'Asparaginase', 'Atazanavir', 'Atenolol', 'Atovaquone', 'Azithromycin', 'Baclofen', 'Bleomycin', 'Bortezomib', 'Bosentan', 'Busulfan', 'Calcium', 'Captopril', 'Carbamazepine', 'Carboplatin', 'Carmustine', 'Cefaclor', 'Cefepime', 'Cefixime', 'Ceftazidime', 'Cefuroxime', 'Celecoxib', 'Cephalexin', 'Cidofovir', 'Cisplatin', 'Cladribine', 'Clarithromycin', 'Clindamycin', 'Clobazam', 'Clofarabine', 'Codeine', 'Crizanlizumab', 'Crizotinib', 'Cyclobenzaprine', 'Cyclophosphamide', 'Cyclosporine', 'Cyproheptadine', 'Cytarabine', 'Dacarbazine', 'Dactinomycin', 'Dapsone', 'Darunavir', 'Dasatinib', 'Daunorubicin', 'Deferasirox', 'Desmopressin', 'Dexamethasone', 'Diclofenac', 'Didanosine', 'Dinutuximab', 'Dobutamine', 'Dopamine', 'Dornase alfa', 'Doxorubicin', 'Dronabinol', 'Efavirenz', 'Efavirenz', 'Enalapril', 'Enoxaparin', 'Erlotinib', 'Erythromycin', 'Erythropoietin', 'Etonogestrel', 'Etoposide', 'Etravirine', 'Famciclovir', 'Famotidine', 'Fidaxomicin', 'Fluconazole', 'Fludarabine', 'Fluorouracil', 'Foscarnet', 'Furosemide', 'Gabapentin', 'Ganciclovir', 'Gefitinib', 'Gemcitabine', 'Gemtuzumab ozogamicin', 'GM-CSF ', 'Granisetron', 'Heparin Lock Flush for children and young adults', 'Heparin Lock Flush for infants', 'Hydralazine', 'Hydrocodone with acetaminophen', 'Hydrocortisone', 'Hydromorphone', 'Hydroxyurea', 'Hydroxyurea for sickle cell disease', 'Ifosfamide', 'Imatinib', 'Imipenem', 'Immune globulin', 'Interferon alfa-2a and alfa-2b', 'Interferon alfa-2b for melanoma', 'Interleukin-2', 'Irinotecan', 'Isotretinoin', 'Itraconazole', 'Ketoconazole', 'L-glutamine', 'Labetalol', 'Lamivudine', 'Leucovorin with high dose methotrexate', 'Levothyroxine', 'Linezolid', 'Lomustine', 'Lopinavir', 'Lorazepam', 'Lorlatinib', 'Magnesium', 'Maraviroc ', 'Mechlorethamine', 'Megestrol acetate', 'Meloxicam', 'Melphalan', 'Meperidine', 'Mercaptopurine', 'Meropenem', 'Mesna', 'Methadone', 'Methotrexate', 'Methylphenidate', 'Metronidazole', 'Micafungin', 'Mitotane', 'Mitoxantrone', 'Modafinil', 'Morphine', 'Muromonab – CD3', 'Mycophenolate mofetil', 'Nelarabine', 'Nelfinavir', 'Neuromuscular blockers', 'Nevirapine', 'Norepinephrine', 'Omeprazole', 'Ondansetron', 'Oxycodone', 'Paclitaxel', 'PEGaspargase', 'Pegfilgrastim', 'Pemetrexed', 'Penicillin VK', 'Pentamidine (inhaled by mouth)', 'Phenobarbital', 'Phenytoin', 'Phosphorus', 'Posaconazole', 'Potassium', 'Prednisone', 'Probenecid', 'Procarbazine', 'Promethazine', 'Promethazine topical gel', 'Propoxyphene', 'Raltegravir ', 'Ranitidine', 'Rasburicase', 'Regorafenib', 'Rilpivirine', 'Rilpivirine', 'Ritonavir', 'Rituximab', 'Rivaroxaban', 'Ruxolitinib', 'Sacubitril', 'Saquinavir', 'Sirolimus', 'Sorafenib', 'Stavudine', 'Sucralfate', 'Sugammadex', 'Sunitinib', 'Tacrolimus', 'Temozolomide', 'Teniposide', 'Tenofovir', 'Thioguanine', 'Thiotepa', 'Tobramycin', 'Topotecan', 'Tretinoin – applied to the skin', 'Tretinoin – by mouth', 'Trimethoprim', 'Valproic acid', 'Vancomycin', 'Vinblastine', 'Vincristine', 'Voriconazole', 'Vorinostat', 'Voxelotor', 'Warfarin', 'Zidovudine']

item_codes=[]
for i in l:
    integer=r.randrange(1,30)
    integer*=100
    integer1=r.randrange(0,2)
    if integer1==0:
        integer+=99
    else:
        integer+=50

    code=i[0:3].lower()
    temp_code=code
    count=1
    while True:
        #print(temp_code)
        if temp_code not in item_codes:
            item_codes+=[temp_code]
            code=temp_code
            break
        else:
            temp_code=code+str(count)
            
            
        count+=1

    p=(code,i,integer)
    print(p,',')
'''
bill_item_query='''insert into bill_list values('aba1', 'Abacavir-1', 1150) ,
('aba', 'Abacavir', 2450) ,
('acy', 'Acyclovir', 1050) ,
('ale', 'Alemtuzumab', 1599) ,
('ale1', 'Alendronate', 350) ,
('all', 'Allopurinol', 2499) ,
('ami', 'Amifostine', 650) ,
('ami1', 'Amikacin', 1399) ,
('ami2', 'Aminocaproic Acid', 2699) ,
('ami3', 'Amitriptyline', 550) ,
('aml', 'Amlodipine', 2199) ,
('amo', 'Amoxicillin', 150) ,
('amp', 'Amphotericin B', 2199) ,
('amp1', 'Ampicillin', 399) ,
('apr', 'Aprepitant', 2950) ,
('asp', 'Asparaginase', 2550) ,
('ata', 'Atazanavir', 1299) ,
('ate', 'Atenolol', 2799) ,
('ato', 'Atovaquone', 1750) ,
('azi', 'Azithromycin', 1350) ,
('bac', 'Baclofen', 1150) ,
('ble', 'Bleomycin', 1199) ,
('bor', 'Bortezomib', 799) ,
('bos', 'Bosentan', 1550) ,
('bus', 'Busulfan', 1750) ,
('cal', 'Calcium', 450) ,
('cap', 'Captopril', 1099) ,
('car', 'Carbamazepine', 499) ,
('car1', 'Carboplatin', 850) ,
('car2', 'Carmustine', 2399) ,
('cef', 'Cefaclor', 2599) ,
('cef1', 'Cefepime', 2950) ,
('cef2', 'Cefixime', 1250) ,
('cef3', 'Ceftazidime', 699) ,
('cef4', 'Cefuroxime', 2099) ,
('cel', 'Celecoxib', 699) ,
('cep', 'Cephalexin', 750) ,
('cid', 'Cidofovir', 350) ,
('cis', 'Cisplatin', 899) ,
('cla', 'Cladribine', 2350) ,
('cla1', 'Clarithromycin', 1250) ,
('cli', 'Clindamycin', 2550) ,
('clo', 'Clobazam', 1550) ,
('clo1', 'Clofarabine', 2950) ,
('cod', 'Codeine', 1750) ,
('cri', 'Crizanlizumab', 350) ,
('cri1', 'Crizotinib', 2299) ,
('cyc', 'Cyclobenzaprine', 2250) ,
('cyc1', 'Cyclophosphamide', 150) ,
('cyc2', 'Cyclosporine', 299) ,
('cyp', 'Cyproheptadine', 2999) ,
('cyt', 'Cytarabine', 1250) ,
('dac', 'Dacarbazine', 150) ,
('dac1', 'Dactinomycin', 2099) ,
('dap', 'Dapsone', 399) ,
('dar', 'Darunavir', 850) ,
('das', 'Dasatinib', 2650) ,
('dau', 'Daunorubicin', 799) ,
('def', 'Deferasirox', 1050) ,
('des', 'Desmopressin', 2599) ,
('dex', 'Dexamethasone', 750) ,
('dic', 'Diclofenac', 150) ,
('did', 'Didanosine', 2299) ,
('din', 'Dinutuximab', 2250) ,
('dob', 'Dobutamine', 1099) ,
('dop', 'Dopamine', 2799) ,
('dor', 'Dornase alfa', 899) ,
('dox', 'Doxorubicin', 1099) ,
('dro', 'Dronabinol', 1850) ,
('efa', 'Efavirenz', 2550) ,
('efa1', 'Efavirenz', 1899) ,
('ena', 'Enalapril', 2499) ,
('eno', 'Enoxaparin', 1099) ,
('erl', 'Erlotinib', 1950) ,
('ery', 'Erythromycin', 550) ,
('ery1', 'Erythropoietin', 850) ,
('eto', 'Etonogestrel', 750) ,
('eto1', 'Etoposide', 950) ,
('etr', 'Etravirine', 2399) ,
('fam', 'Famciclovir', 2950) ,
('fam1', 'Famotidine', 1650) ,
('fid', 'Fidaxomicin', 2699) ,
('flu', 'Fluconazole', 2450) ,
('flu1', 'Fludarabine', 1099) ,
('flu2', 'Fluorouracil', 599) ,
('fos', 'Foscarnet', 1650) ,
('fur', 'Furosemide', 150) ,
('gab', 'Gabapentin', 650) ,
('gan', 'Ganciclovir', 2199) ,
('gef', 'Gefitinib', 699) ,
('gem', 'Gemcitabine', 1299) ,
('gem1', 'Gemtuzumab-oz', 1250) ,
('gm-', 'GM-CSF ', 599) ,
('gra', 'Granisetron', 1899) ,
('hep', 'Heparin - adults', 2550) ,
('hep1', 'Heparin - infants', 1999) ,
('hyd', 'Hydralazine', 2899) ,
('hyd1', 'Hydrocodone', 850) ,
('hyd2', 'Hydrocortisone', 1650) ,
('hyd3', 'Hydromorphone', 1250) ,
('hyd4', 'Hydroxyurea', 750) ,
('ifo', 'Ifosfamide', 1550) ,
('ima', 'Imatinib', 2399) ,
('imi', 'Imipenem', 1550) ,
('imm', 'Immune globulin', 1550) ,
('int', 'Interferon-2a', 350) ,
('int1', 'Interferon-2b', 1850) ,
('int2', 'Interleukin-2', 1050) ,
('iri', 'Irinotecan', 1999) ,
('iso', 'Isotretinoin', 1499) ,
('itr', 'Itraconazole', 1150) ,
('ket', 'Ketoconazole', 1899) ,
('l-g', 'L-glutamine', 2099) ,
('lab', 'Labetalol', 1250) ,
('lam', 'Lamivudine', 2799) ,
('leu', 'Leucovorin', 1650) ,
('lev', 'Levothyroxine', 2499) ,
('lin', 'Linezolid', 999) ,
('lom', 'Lomustine', 1250) ,
('lop', 'Lopinavir', 1350) ,
('lor', 'Lorazepam', 899) ,
('lor1', 'Lorlatinib', 1750) ,
('mag', 'Magnesium', 2299) ,
('mar', 'Maraviroc ', 1350) ,
('mec', 'Mechlorethamine', 2499) ,
('meg', 'Megestrol acetate', 1299) ,
('mel', 'Meloxicam', 699) ,
('mel1', 'Melphalan', 1999) ,
('mep', 'Meperidine', 1999) ,
('mer', 'Mercaptopurine', 1099) ,
('mer1', 'Meropenem', 2250) ,
('mes', 'Mesna', 1150) ,
('met', 'Methadone', 2899) ,
('met1', 'Methotrexate', 599) ,
('met2', 'Methylphenidate', 1950) ,
('met3', 'Metronidazole', 1150) ,
('mic', 'Micafungin', 499) ,
('mit', 'Mitotane', 699) ,
('mit1', 'Mitoxantrone', 2550) ,
('mod', 'Modafinil', 2250) ,
('mor', 'Morphine', 2699) ,
('mur', 'Muromonab - CD3', 1050) ,
('myc', 'Mycophenolate', 2350) ,
('nel', 'Nelarabine', 1750) ,
('nel1', 'Nelfinavir', 2599) ,
('nev', 'Nevirapine', 2499) ,
('nor', 'Norepinephrine', 499) ,
('ome', 'Omeprazole', 599) ,
('ond', 'Ondansetron', 2450) ,
('oxy', 'Oxycodone', 950) ,
('pac', 'Paclitaxel', 1350) ,
('peg', 'PEGaspargase', 1699) ,
('peg1', 'Pegfilgrastim', 2950) ,
('pem', 'Pemetrexed', 2450) ,
('pen', 'Penicillin VK', 1150) ,
('pen1', 'Pentamidine(mouth)', 550) ,
('phe', 'Phenobarbital', 799) ,
('phe1', 'Phenytoin', 1499) ,
('pho', 'Phosphorus', 450) ,
('pos', 'Posaconazole', 1450) ,
('pot', 'Potassium', 999) ,
('pre', 'Prednisone', 1950) ,
('pro', 'Probenecid', 1099) ,
('pro1', 'Procarbazine', 2099) ,
('pro2', 'Promethazine', 2450) ,
('pro3', 'Promethazine topical gel', 850) ,
('pro4', 'Propoxyphene', 2150) ,
('ral', 'Raltegravir ', 2450) ,
('ran', 'Ranitidine', 2350) ,
('ras', 'Rasburicase', 550) ,
('reg', 'Regorafenib', 399) ,
('ril', 'Rilpivirine', 950) ,
('ril1', 'Rilpivirine', 1599) ,
('rit', 'Ritonavir', 550) ,
('rit1', 'Rituximab', 450) ,
('riv', 'Rivaroxaban', 2599) ,
('rux', 'Ruxolitinib', 1199) ,
('sac', 'Sacubitril', 550) ,
('saq', 'Saquinavir', 2899) ,
('sir', 'Sirolimus', 2399) ,
('sor', 'Sorafenib', 150) ,
('sta', 'Stavudine', 650) ,
('suc', 'Sucralfate', 1499) ,
('sug', 'Sugammadex', 1050) ,
('sun', 'Sunitinib', 2550) ,
('tac', 'Tacrolimus', 1799) ,
('tem', 'Temozolomide', 150) ,
('ten', 'Teniposide', 2199) ,
('ten1', 'Tenofovir', 1599) ,
('thi', 'Thioguanine', 699) ,
('thi1', 'Thiotepa', 1650) ,
('tob', 'Tobramycin', 199) ,
('top', 'Topotecan', 2599) ,
('tre', 'Tretinoin (skin)', 2599) ,
('tre1', 'Tretinoin (mouth)', 2599) ,
('tri', 'Trimethoprim', 199) ,
('val', 'Valproic acid', 299) ,
('van', 'Vancomycin', 750) ,
('vin', 'Vinblastine', 1050) ,
('vin1', 'Vincristine', 2350) ,
('vor', 'Voriconazole', 450) ,
('vor1', 'Vorinostat', 1450) ,
('vox', 'Voxelotor', 2950) ,
('war', 'Warfarin', 2799) ,
('zid', 'Zidovudine', 699)'''

welcome_page()
