def clearscreen():
    #function that clears all previous output on screen
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def tableprint(lst):
    #prints table in sql format
    print(tabulate(lst, headers=[i[0] for i in cur.description], tablefmt='psql'))

def addtocart():
    #prompts to add item to cart
    choice=input("\nDo you want to add a record to your cart? (y/n): ")
    if choice=='y':
        n=int(input("\nEnter number of records: "))
        for i in range(n):
            id=(input("\nEnter the Record_ID of the record: ")).upper()
            cur.execute("select Name,Artist,Format from records where Record_ID='"+id+"'")
            data=cur.fetchall()
            if data==[]:
                print("\nRecord_ID not found.\n")
                continue
            quan=int(input("Enter quantity of the record: "))
            cur.execute("insert into cart values('{}','{}','{}','{}',{})".format(id,data[0][0],data[0][1],data[0][2],quan))
            conobj.commit()
            print("\n",quan,"units of",data[0][0],"successfully added to cart !")
        #another prompt to either continue shopping or checkout
        print("\n1. Continue shopping")
        print("2. View Cart / checkout")
        choice=int(input("\nEnter choice: "))
        if choice==2:
            viewcart()
    print()
    
def viewcart():
    #shows the cart and prompts for checkout
    clearscreen()
    print("-"*50+"\n\t\t\tCART\n"+"-"*50+"\n")

    cur.execute("select * from cart")
    cart=cur.fetchall()

    if cart==[]:
        print("\nNo items in cart\n")
        input("Press enter to go back to main menu ")
        return
    
    tableprint(cart)
    
    cur.execute("select sum(quantity) from cart where Format='STUDIO ALBUM'")
    albums=cur.fetchall()[0][0]
    
    cur.execute("select sum(quantity) from cart where Format='EP'")
    eps=cur.fetchall()[0][0]
    
    cur.execute("select sum(quantity) from cart where Format='SINGLE'")
    singles=cur.fetchall()[0][0]
    
    if singles==None:
        singles=0
    if eps==None:
        eps=0
    if albums==None:
        albums=0

    price=albums*1500+eps*1000+singles*500

    print("\nPrice per Studio Album : 1500 Rs\t(",albums,"albums in cart )")
    print("Price per EP : 1000 Rs\t\t\t(",eps,"EPs in cart )")
    print("Price per Single : 500 Rs\t\t(",singles,"Singles in cart )\n")

    print("Total Price =",price,"Rupees")
    print("Price with tax (5%) =",price*105/100,"Rupees")
    print("\n1. Remove items")
    print("2. Checkout and exit")
    print("3. Continue shopping")
    choice=int(input("\nEnter choice: "))

    if choice==1:
        record=input("\nEnter Record_ID of the record you want to remove: ")
        cur.execute("delete from cart where Record_ID='"+record+"'")
        print("\nItem Removed!")
        viewcart()
    
    elif choice==2:
        print("\nPurchase Successful!")
        print("Thanks for shopping at Genius Records Store. We hope to see you again soon!\n")
        input("Press enter to exit ")
        global flag
        flag=False

#importing modules and starting sql connection
import mysql.connector
import records
from tabulate import tabulate

conobj=mysql.connector.connect(host="localhost",user="root",passwd="")
cur=conobj.cursor()

#creating database and records table if they dont exist
try:
    cur.execute("create database music")
except:
    print()
cur.execute("use music")
try:
    cur.execute("drop table records")
except:
    print()
cur.execute("create table records(Record_ID varchar(5) primary key, Name varchar(40), Artist varchar(20), Genre varchar(15), Format varchar(20), Units_Sold integer, Year integer)")

#adding records from records.py module
for record in records.load():
    cur.execute("insert into records values"+str(record))

conobj.commit()

#creating cart table
try:
    cur.execute("drop table cart")
except:
    print()

cur.execute("create table cart(Record_ID varchar(5) references records(Record_ID), Name varchar(40), Artist varchar(20), Format varchar(20), Quantity integer)")
conobj.commit()

cur.execute("use music")

#looping through menu
flag=True
while flag:
    clearscreen()
    print("-"*50+"\n\t\tGENIUS RECORD STORE\t\t\n"+"-"*50)
    print("1. Browse bestselling records")
    print("2. Browse by genre")
    print("3. Browse by artist name")
    print("4. Browse by era")
    print("5. View cart / checkout")
    print("6. Exit")
    
    choice = int(input("\nEnter your choice: "))

    if choice==1:
        clearscreen()
        print("-"*50+"\n\t\tBESTSELLING RECORDS\t\t\n"+"-"*50)
        
        #creating rank variable and displaying records with rank
        cur.execute("set @rank:=0")
        cur.execute("select (@rank:=@rank+1) as Rank, Record_ID, Name, Artist, format(Units_Sold,0) as Copies_Sold, Genre, Format, Year from records order by Units_Sold desc limit 25")
        table=cur.fetchall()
        tableprint(table)
        addtocart()

    elif choice==2:
        clearscreen()
        #displaying select genre submenu
        print("-"*50+"\n\t\tSELECT GENRE\t\t\n"+"-"*50)
        cur.execute("select distinct GENRE from records")
        genres=cur.fetchall()
        print()
        for i in range(len(genres)):
            print(str(i+1)+".",genres[i][0])
        
        choice = int(input("\nEnter your choice: "))
        try:
            cur.execute("select * from records where Genre='"+genres[choice-1][0].upper()+"' limit 25")
            table=cur.fetchall()
            tableprint(table)
        except:
            print("\nInvalid choice!\n")
            continue
        addtocart()

    elif choice==3:
        clearscreen()
        #displaying select artist submenu
        print("-"*50+"\n\t\tSELECT ARTIST\t\t\n"+"-"*50)
        cur.execute("select distinct ARTIST from records")
        artists=cur.fetchall()
        print()
        for i in range(len(artists)):
            print(str(i+1)+".",artists[i][0])
        
        choice = int(input("\nEnter your choice: "))
        try:
            cur.execute("select * from records where Artist='"+artists[choice-1][0].upper()+"' limit 25")
            table=cur.fetchall()
            tableprint(table)
        except:
            print("\nInvalid choice!\n")
            continue
        addtocart()
    
    elif choice==4:
        clearscreen()
        #displaying select era submenu
        print("-"*50+"\n\t\tSELECT ERA\t\t\n"+"-"*50)
        print("\n1. 1960s")
        print("2. 1970s")
        print("3. 1980s")
        print("4. 1990s")
        print("5. 2000s")
        print("6. 2010s")
        choice = int(input("\nEnter your choice: "))
        
        if choice==1:
            cur.execute("select * from records where Year between 1960 and 1969 limit 25")
        elif choice==2:
            cur.execute("select * from records where Year between 1970 and 1979 limit 25")
        elif choice==3:
            cur.execute("select * from records where Year between 1980 and 1989 limit 25")
        elif choice==4:
            cur.execute("select * from records where Year between 1990 and 1999 limit 25")
        elif choice==5:
            cur.execute("select * from records where Year between 2000 and 2009 limit 25")
        elif choice==6:
            cur.execute("select * from records where Year between 2010 and 2020 limit 25")
        else:
            print("\nInvalid choice!\n")
            continue
        
        table=cur.fetchall()
        tableprint(table)
        addtocart()
        
    elif choice==5:
        viewcart()
    
    elif choice==6:
        #displays exit message and breaks code
        print("\nThanks for visiting !\n")
        break

    else:
        print("\nInvalid choice!\n")
