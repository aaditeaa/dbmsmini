import subprocess as sp
import pymysql
import pymysql.cursors
import getpass
from datetime import datetime
from matplotlib import pyplot as plt, dates as mdates

user_of_db = []


def checkUsername():
    usr = input("Username(email): ")

    user_of_db.append(usr)

    pwd = input("Password: ")

    query = "SELECT `Email Id`,Password FROM User WHERE `Email Id` = '%s'" % (
            usr)

    cur.execute(query)

    rows = cur.fetchall()
    con.commit()

    if len(rows) == 0:
        print("Username is incorrect, please enter a valid username")
        return 0
    else:
        if pwd != rows[0]['Password']:
            print("the Password is incorrect")
            return 0
        else:
            return 1

    return 1


def registerUser():
    usr = input("Username(email): ")
    pwd = input("Password: ")
    first_name = input("First Name: ")
    middle_name = input("Middle Name: ")
    last_name = input("Last Name: ")

    user_of_db.append(usr)

    query = "INSERT INTO `User` VALUES ('%s','%s','%s','%s','%s')" % (
        usr, first_name, middle_name, last_name, pwd)

    try:
        cur.execute(query)

        con.commit()

        print("User successfully registered!")
        return 1

    except:
        print("Error In registering User")
        exit()


def insert_called(query):
    try:
        if query[1] == "COMPANIES":
            print(query)
            exe_que = "insert into Companies VALUES ('%s','%d','%s','%d','%f')" % (
                query[2], int(query[3]), query[4], int(query[5]), float(query[6]))
            cur.execute(exe_que)
            con.commit()
        elif query[1] == "FAVORITES":
            exe_que = "insert into Favorites VALUES ('%s','%s')" % (
                query[2], str(user_of_db[0]))
            cur.execute(exe_que)
            con.commit()
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def delete_called(query):
    try:
        if query[1] == "FAVORITES":
            exe_que = "delete from Favorites where `Company_Name` = '%s'" % (
                query[2])
            cur.execute(exe_que)
            con.commit()
        elif query[1] == "USER":
            exe_que = "delete from User where `Email Id` = '%s'" % (
                user_of_db[0])
            cur.execute(exe_que)
            con.commit()

            exit()
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def search_called(query):
    try:
        temp = query[2]
        query[2] += '%'
        if query[1] == "COMPANIES":
            exe_que = "select Company_Name,Sector,`Dividend Yield` from Companies where `Company_Name` like '%s' " % (
                query[2])
            cur.execute(exe_que)

            rows = cur.fetchall()
            con.commit()

            print("Details about Companies whose name start with letter '%s' is:" %
                  (temp))

            for j in rows:
                print(j)
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def project_(query):
    try:
        if query[1] == "COMPANIES":
            exe_que = "select Company_Name,`Sector` FROM Companies WHERE `Dividend Yield` > '%d'" % (
                int(query[2]))
            cur.execute(exe_que)
            rows = cur.fetchall()
            con.commit()

            print("Details about Companies having Dividend Yield > '%s' is:" %
                  (query[2]))

            for j in rows:
                print(j)
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def select_(query):
    try:
        if query[1] == "COMPANIES":
            exe_que = "select Company_Name,`Dividend Yield` FROM Companies WHERE Sector = '%s'" % (
                query[2])
            cur.execute(exe_que)
            rows = cur.fetchall()
            con.commit()

            print("Details about Companies in Sector '%s' is:" %
                  (query[2]))

            for j in rows:
                print(j)
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def aggregate_pe(query):
    try:
        if query[1] == "COMPANIES":
            exe_que = "select AVG(`P/E Ratio`) from Stocks AS S INNER JOIN Companies AS C ON S.Company_Name = C.Company_Name WHERE Sector = '%s'" % (
                query[2])
            cur.execute(exe_que)
            rows = cur.fetchall()
            con.commit()

            print("Aggregate of P/E Ratio of Companies in Sector '%s' is:" %
                  (query[2]), end=' ')
            print(rows[0]['AVG(`P/E Ratio`)'])
        else:
            print("the search can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def update_(query):
    try:
        if query[1] == "USER":
            exe_que = "update User SET `Email Id` = '%s' WHERE `Email Id` = '%s'" % (
                query[2], user_of_db[0])
            user_of_db[0] = query[2]
            cur.execute(exe_que)
            con.commit()
            print("Username Updated Successfully")
        elif query[1] == "COMPANY":
            exe_que = "update Companies SET `Company_Name` = '%s' WHERE `Company_Name` = '%s'" % (
                query[3], query[2])
            cur.execute(exe_que)
            con.commit()
            print("Company Name Updated Successfully")
        elif query[1] == "DIVIDEND":
            exe_que = "update Companies SET `Dividend Yield` = '%f' WHERE `Company_Name` = '%s'" % (
                float(query[3]), query[2])
            cur.execute(exe_que)
            con.commit()
            print("Company Dividend Yield Updated Successfully")
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def analysis(query):
    try:
        if query[1] == "BOD%":
            exe_que = "SELECT C.Company_Name,C.Sector,`Percentage Shares held by BOD` FROM Companies C INNER JOIN `Board Members` B ON C.Company_Name=B.Company_Name where `Percentage Shares held by BOD` > '%f'" % (
                float(query[2]))
            cur.execute(exe_que)

            rows = cur.fetchall()
            con.commit()

            for j in rows:
                print(j)
        elif query[1] == "FAVORITES":
            exe_que = "select Company_Name FROM Favorites Group By Company_Name ORDER BY COUNT(*) DESC LIMIT 1"
            cur.execute(exe_que)

            rows = cur.fetchall()
            con.commit()

            print("Company which is favorite of maximum users is: ", end='')
            print(rows[0]['Company_Name'])
        else:
            print("the query can't be done on the given relation")
    except:
        print("The format/input of the query is incorrect")


def plot_g(query):
    try:
        if(query[1] == 'COMPANIES'):
            exe_que = "select Date,`Current Price` FROM Stocks WHERE Company_Name = '%s'" % (
                query[2])
            cur.execute(exe_que)

            rows = cur.fetchall()

            con.commit()

            date_time = []
            data = []

            for j in rows:
                temp_date = str(j['Date'])
                date_time.append(temp_date)
                data.append(j['Current Price'])

            plt.rcParams["figure.figsize"] = [7.50, 3.50]
            plt.rcParams["figure.autolayout"] = True

            x = [datetime.strptime(d, "%Y-%m-%d").date() for d in date_time]
            y = data

            ax = plt.gca()
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.plot(x, y)

            temp_name = 'Data For Company: ' + query[2]
            plt.ylabel('Stock Prices')
            plt.xlabel('Dates')
            plt.title(temp_name)

            plt.show()

        else:
            print("the query can't be done on the given relation")

    except:
        print("The format/input of the query is incorrect")


def queryselector():
    print("INSERT")
    print("\t:insert FAVORITES [Company_Name]")
    print(
        "\t:insert COMPANIES [Company_Name Founder_ID Sector StockUID DividendYield]")
    print("DELETE")
    print("\t:delete FAVORITES [Company_Name]")
    print("\t:delete USER")
    print("SEARCH")
    print("\t:search COMPANIES [starting letter]")
    print("UPDATE")
    print("\t:update USER [new email-id]")
    print("\t:update COMPANY [Prev_Company_Name New_Company_Name]")
    print("\t:update DIVIDEND [Company_Name New_Dividend_Yield]")
    print("SELECT")
    print("\t:select COMPANIES [company-sector]")
    print("AGGREGATE")
    print("\t:aggregate COMPANIES [company-sector]")
    print("ANALYSIS")
    print("\t:analysis BOD% [Min.Percentage of stocks held by BOD]")
    print("\t:analysis FAVORITES")
    print("GRAPH ANALYSIS")
    print("\t:plot COMPANIES [Company-Name]")

    print("enter query in the correct format as mentioned")
    while 1:
        que = input(">")
        temp_que = que
        operations = temp_que.split(" ")
        if operations[0] == "insert":
            print("insert called")
            insert_called(operations)
        elif operations[0] == "delete":
            print("delete called")
            delete_called(operations)
        elif operations[0] == "search":
            print("search called")
            search_called(operations)
        elif operations[0] == "update":
            print("update called")
            update_(operations)
        elif operations[0] == "aggregate":
            print("aggregate called")
            aggregate_pe(operations)
        elif operations[0] == "select":
            print("select called")
            select_(operations)
        elif operations[0] == "project":
            print("project called")
            project_(operations)
        elif operations[0] == "analysis":
            print("analysis called")
            analysis(operations)
        elif operations[0] == "plot":
            print("graph plot called")
            plot_g(operations)
        elif operations[0] == "exit":
            exit()
        else:
            print("Wrong Query to the Database")


# Global
while(1):
    tmp = sp.call('clear', shell=True)

    # Can be skipped if you want to hardcode username and password
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        con = pymysql.connect(host='localhost',
                              user=username,
                              password=password,
                              db='dbmsstock',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        cur = con.cursor()
        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                ans = input(
                    "Are you a registered user of the database (y/n): ")
                if ans == "y":
                    check = 0
                    while check != 1:
                        check = checkUsername()
                        if check == 1:
                            print("Pls proceed with the queries!")
                            queryselector()
                        else:
                            exit()
                else:
                    ans_2 = input(
                        "Do you want to register for the Database (y/n): ")
                    if ans_2 == 'y':
                        registered = registerUser()
                        queryselector()
                    else:
                        print("Hope you change your mind!")
                        exit()

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")
