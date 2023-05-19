import mysql.connector as ms
mycon=ms.connect(host="localhost",user="root",passwd="1234",database="flightproject")
if mycon.is_connected():
    print("successfully connected")
mycursor=mycon.cursor()
def admin_space():
    ans='yes'
    while ans=='yes':
        print("1.display employee details")
        print("2.insert employee details")
        print("3.edit employee details")
        print("4.remove employee details")
        print("5.display job detils")
        print("6.insert job detils")
        print("7.edit job detils")
        choice=int(input("enter your choice"))
        if choice==1:
            empid=input("enter employee id")
            mycursor.execute("select * from Employee where employeeid={}".format(empid))
            data=mycursor.fetchall()
            for i in data:
                print(data)
        if choice==2:
            Employeeid=int(input("enter employee id"))
            Name=input("enter name")
            Sales=int(input("enter sales"))
            Jobid=int(input("enter job id"))
            mycursor.execute("insert into Employee values({},'{}',{},{})".format(Employeeid,Name,Sales,Jobid))
            mycon.commit()
        if choice==3:
            print("1. update Name")
            print("2. update Sales")
            print("3. update Jobid")
            choice=int(input("enter your choice"))
            if choice==1:
                no=int(input("enter employeeid"))
                mycursor.execute("select Name from Employee where employeeid={}".format(no))
                on=mycursor.fetchall()
                print("old name is",on)
                nn=input("enter new name")
                qu="update Employee set Name='{}' where employeeid={}".format(nn,no)
                mycursor.execute(qu)
                mycon.commit()
            elif choice==2:
                no=int(input("enter Employeeid"))
                mycursor.execute("select Sales from Employee where employeeid={}".format(no))
                on=mycursor.fetchall()
                print("old sales is",on)
                nn=int(input("enter new Sales"))
                qu="update Employee set Sales={} where employeeid={}".format(nn,no)
                mycursor.execute(qu)
                mycon.commit()
            elif choice==3:
                no=int(input("enter Employeeidid"))
                mycursor.execute("select Jobid from Employee where employeeid={}".format(no))
                on=mycursor.fetchall()
                print("old jobid is",on)
                nn=int(input("enter new Jobid"))
                qu="update Employee set Jobid={} where employeeid={}".format(nn,no)
                mycursor.execute(qu)
                mycon.commit()
        if choice==4:
            print("1.delete row on basis of Employeeid")
            print("2. delete row on basis of Name")
            choice=int(input("enter your choice"))
            if choice == 1:
                empid=int(input("enter Employee id whose datails you want deleted"))
                q="select * from Employee where employeeid={}".format(empid)
                mycursor.execute(q)
                a=mycursor.fetchall()
                print("the details of Employee with employeeid",empid,"is:")
                for i in a:
                    print(i)
                b=input("do you still want to delete the details?")
                if b=="yes":
                    qu="delete from Employee where employeeid={}".format(empid)
                    mycursor.execute(qu)
                    mycon.commit()
                    print("successfully deleted the record")
            if choice == 2:
                empname=input("enter name whose datails you want deleted")
                q="select * from Employee where Name='{}'".format(empname)
                mycursor.execute(q)
                a=mycursor.fetchall()
                print("the details of Employee with Name",empname,"is:")
                for i in a:
                    print(i)
                b=input("do you still want to delete the details?")
                if b=="yes":
                    qu="delete from Employee where Name='{}'".format(empname)
                    mycursor.execute(qu)
                    mycon.commit()
                    print("successfully deleted the record")
        if choice==5:
            mycursor.execute("select * from Job")
            data=mycursor.fetchall()
            print(data)
        if choice==6:
            Jobid=int(input("enter job id"))
            Jobtitle=input("enter job title")
            Salary=int(input("enter salary"))
            mycursor.execute("insert into Job values({},'{}',{})".format(Jobid,Jobtitle,Salary))
            mycon.commit()
        if choice==7:
            print("1. Update jobtitle")
            print("2. update salary")
            choice=int(input("enter your choice"))
            if choice==1:
                no=int(input("enter Jobid"))
                mycursor.execute("select Jobtitle from Job where Jobid={}".format(no))
                on=mycursor.fetchall()
                print("old jobtitle is",on)
                nn=input("enter new Jobtitle")
                qu="update Job set Jobtitle='{}' where Jobid={}".format(nn,no)
                mycursor.execute(qu)
                mycon.commit()
            if choice==2:
                no=int(input("enter Jobid"))
                mycursor.execute("select Salary from Job where Jobid={}".format(no))
                on=mycursor.fetchall()
                print("old Salary is",on)
                nn=int(input("enter new Salary"))
                qu="update Job set salary={} where Jobid={}".format(nn,no)
                mycursor.execute(qu)
                mycon.commit()
        ans=input('do you want to continue')
def employee_space():
    ans='yes'
    while ans=='yes':
        print("1. display flight details")
        print("2. book flight tickets")
        print("3. display passenger details for a flight")
        print("4. update flight timings")
        print("5. delete passenger details")
        choice=int(input("enter your choice"))
        if choice==1:
            flightser=input("enter flight series")
            flightno=int(input("enter flight number"))
            mycursor.execute("select * from flight where flightseries='{}' and flightnumber={}".format(flightser,flightno))
            data=mycursor.fetchall()
            for i in data:
                print(i)
        if choice==2:
            a=int(input("how many passengers will be travelling"))
            flightser=input("enter flight series")
            flightno=int(input("enter flight number"))
            mycursor.execute("select available from flight where flightseries='{}' and flightnumber={}".format(flightser,flightno))
            available=mycursor.fetchone()
            if available[0]>a:
                print("please enter the passengers details")
                for i in range(a):
                    name=input("enter your name")
                    passportser=input("enter passport serial alphabet")
                    passportno=int(input("enter passport number"))
                    dob=input("enter date of birth")
                    passportdoi=(input("enter passport date of issue"))
                    passportdoe=(input("enter passport date of expiry"))
                    visano=int(input("enter visa number"))
                    q="insert into passenger values('{}',{},'{}','{}',{},'{}','{}','{}',{})".format(flightser,flightno,name,passportser,passportno,dob,passportdoi,passportdoe,visano)
                    mycursor.execute(q)
                mycon.commit()
                r="update flight set available={} where flightseries='{}' and flightnumber={}".format(available[0]-a,flightser,flightno)
                mycursor.execute(r)
                mycon.commit()
            else:
                print("not enough seats available")
        if choice==3:
            passportser=input("enter passport serial alphabet")
            passportno=int(input("enter passport number"))
            mycursor.execute("select * from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno))
            data=mycursor.fetchone()
            print(data)
        if choice==4:
            flightser=input("enter flight series")
            flightno=int(input("enter flight number"))
            a=input("change time of arrival or departure ?")
            if a=="arrival":
                arival=input("enter updated time of arrival")
                r="update flight set toa='{}' where flightseries='{}' and flightnumber={}".format(arival,flightser,flightno)
                mycursor.execute(r)
                mycon.commit()
            if a=="departure":
                depart=input("enter updated time of departure")
                r="update flight set tod='{}' where flightseries='{}' and flightnumber={}".format(depart,flightser,flightno)
                mycursor.execute(r)
                mycon.commit()
        if choice==5:
            passportser=input("enter passport serial alphabet")
            passportno=int(input("enter passport number"))
            mycursor.execute("select * from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno))
            data=mycursor.fetchall()
            r="update flight set available=available+1 where flightseries='{}' and flightnumber={}".format(data[0][0],data[0][1])
            mycursor.execute(r)
            mycon.commit()
            mycursor.execute("delete from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno))
            mycon.commit()
        ans=input('do you want to continue')
def passenger_space():
    ans='yes'
    while ans=='yes':
        print("1.check my details")
        print("2.cancel my flight")
        print("3.check my flight details")
        choice=int(input("enter your choice"))
        if choice==1:
            passportser=input("enter passport serial alphabet")
            passportno=int(input("enter passport number"))
            mycursor.execute("select * from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno))
            data=mycursor.fetchall()
            for i in data:
                print(i)
        if choice==2:
            passportser=input("enter passport serial alphabet")
            passportno=int(input("enter passport number"))
            mycursor.execute("select flightserial,flightnumber from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno))
            data=mycursor.fetchall()
            a=[]
            for i in data:
                a.append(i)
            r="update flight set available=available+1 where flightseries='{}' and flightnumber={}".format(a[0][0],a[0][1])
            mycursor.execute(r)
            mycon.commit()
            mycursor.execute("delete from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno))
            mycon.commit()
        if choice==3:
            passportser=input("enter passport serial alphabet")
            passportno=int(input("enter passport number"))
            a="select flightserial,flightnumber from passenger where passportserial='{}' and passportnumber={}".format(passportser,passportno)
            mycursor.execute(a)
            flightdet=mycursor.fetchall()
            a=[]
            for i in flightdet:
                a.append(i)
            mycursor.execute("select flightseries,flightnumber,toa,tod from flight where flightseries='{}' and flightnumber={}".format(a[0][0],a[0][1]))
            data=mycursor.fetchall()
            for i in data:
                print(i)
        ans=input('do you want to continue')
#main
print("welcome")
print("please select one of the following options")
print("1.admin")
print("2.employee")
print("3.passenger")
choice=int(input("enter your option "))
if choice==1:
    pas=int(input("enter your password"))
    mycursor.execute("select * from admin")
    r=mycursor.fetchall()
    for i in r:
        if i[1]==pas:
            mycursor.execute("select name from admin where password={}".format(pas))
            nam=mycursor.fetchone()
            print("welcome",nam[0])
            admin_space()
    else:
        print("password is incorect")
if choice==2:
    pas=int(input("enter your password"))
    mycursor.execute("select * from employeepass")
    r=mycursor.fetchall()
    for i in r:
        if i[1]==pas:
            mycursor.execute("select name from employeepass where password={}".format(pas))
            nam=mycursor.fetchone()
            print("welcome",nam[0])
            employee_space()
    else:
        print("password incorrect")
if choice==3:
    passenger_space()