def clearscreen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def tableprint(lst):
    widths = []
    columns = []
    border = '|'
    separator = '+' 
    length= ['' for i in range(len(lst[0]))]
    for i in range(len(lst[0])):
        length[i] = max(list(map(lambda x: len(str(x[i])), lst)))
    
    i=0
    for cd in cur.description:
        widths.append(max(length[i], len(cd[0])))
        columns.append(cd[0])
        i+=1

    for w in widths:
        border += " %-"+"%ss |" % (w,)
        separator += '-'*w + '--+'

    print(separator)
    print(border % tuple(columns))
    print(separator)
    for row in lst:
        print(border % row)
    print(separator)

def addtocart():
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
        print("\n1. Continue shopping")
        print("2. View Cart / checkout")
        choice=int(input("\nEnter choice: "))
        if choice==2:
            viewcart()
    print()
    
def viewcart():
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



import mysql.connector

conobj=mysql.connector.connect(host="localhost",user="root",passwd="")
cur=conobj.cursor()

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

cur.execute("insert into records values('SA001','THE DARK SIDE OF THE MOON','PINK FLOYD','ROCK','STUDIO ALBUM',13000000,1973)")
cur.execute("insert into records values('SA002','WISH YOU WERE HERE','PINK FLOYD','ROCK','STUDIO ALBUM',5000000,1975)")
cur.execute("insert into records values('SA003','THE WALL','PINK FLOYD','ROCK','STUDIO ALBUM',1900000,1979)")
cur.execute("insert into records values('SL001','ONE OF MY TURNS','PINK FLOYD','ROCK','SINGLE',60000,1979)")
cur.execute("insert into records values('EP001','THE FINAL CUT','PINK FLOYD','ROCK','EP',300000,1983)")
cur.execute("insert into records values('SA004','RUBBER SOUL','THE BEATLES','ROCK','STUDIO ALBUM',1200000,1965)")
cur.execute("insert into records values('SA005','REVOLVER','THE BEATLES','ROCK','STUDIO ALBUM',600000,1966)")
cur.execute("insert into records values('SA006','ABBEY ROAD','THE BEATLES','ROCK','STUDIO ALBUM',5600000,1969)")
cur.execute("insert into records values('EP002','YESTERDAY','THE BEATLES','ROCK','EP',100000,1966)")
cur.execute("insert into records values('EP003','LONG TALL SALLY','THE BEATLES','ROCK','EP',110000,1964)")
cur.execute("insert into records values('SA007','NEVERMIND','NIRVANA','ROCK','STUDIO ALBUM',10000000,1991)")
cur.execute("insert into records values('SA008','BLEACH','NIRVANA','ROCK','STUDIO ALBUM',1900000,1989)")
cur.execute("insert into records values('SA009','IN UTERO','NIRVANA','ROCK','STUDIO ALBUM',1500000,1993)")
cur.execute("insert into records values('EP004','BLEW','NIRVANA','ROCK','EP',100000,1989)")
cur.execute("insert into records values('SL002','SMELLS LIKE TEEN SPIRIT','NIRVANA','ROCK','SINGLE',3000000,1989)")
cur.execute("insert into records values('SA010','A NIGHT AT THE OPERA','QUEEN','ROCK','STUDIO ALBUM',1000000,1975)")
cur.execute("insert into records values('SA011','SHEER HEART ATTACK','QUEEN','ROCK','STUDIO ALBUM',700000,1974)")
cur.execute("insert into records values('SA012','JAZZ','QUEEN','ROCK','STUDIO ALBUM',900000,1978)")
cur.execute("insert into records values('SA013','HOT SPACE','QUEEN','ROCK','STUDIO ALBUM',700000,1982)")
cur.execute("insert into records values('SL003','BOHEMIAN RHAPSODY','QUEEN','ROCK','SINGLE',1000000,1975)")
cur.execute("insert into records values('SA101','YEEZUS','KANYE WEST','HIP HOP','STUDIO ALBUM',750000,2013)")
cur.execute("insert into records values('SA102','THE COLLEGE DROPOUT','KANYE WEST','HIP HOP','STUDIO ALBUM',3358000,2003)")
cur.execute("insert into records values('SA103','MY BEAUTIFUL DARK TWISTED FANTASY','KANYE WEST','HIP HOP','STUDIO ALBUM',1350000,2010)")
cur.execute("insert into records values('EP101','YE','KANYE WEST','HIP HOP','EP',1500000,2018)")
cur.execute("insert into records values('SL101','STRONGER','KANYE WEST','HIP HOP','SINGLE',483000,2007)")
cur.execute("insert into records values('SA104','ASTROWORLD','TRAVIS SCOTT','HIP HOP','STUDIO ALBUM',2700000,2018)")
cur.execute("insert into records values('SA105','BIRDS IN THE TRAP SING MCKNIGHT','TRAVIS SCOTT','HIP HOP','STUDIO ALBUM',530000,2016)")
cur.execute("insert into records values('SA106','RODEO','TRAVIS SCOTT','HIP HOP','STUDIO ALBUM',1100000,2015)")
cur.execute("insert into records values('EP102','JACKBOYS','TRAVIS SCOTT','HIP HOP','EP',790000,2019)")
cur.execute("insert into records values('SL102','SICKO MODE','TRAVIS SCOTT','HIP HOP','SINGLE',2700000,2018)")
cur.execute("insert into records values('SA107','KAMIKAZE','EMINEM','HIP HOP','STUDIO ALBUM',252000,2018)")
cur.execute("insert into records values('SA108','THE MARSHALL MATHERS LP','EMINEM','HIP HOP','STUDIO ALBUM',10600000,2000)")
cur.execute("insert into records values('SA109','THE EMINEM SHOW','EMINEM','HIP HOP','STUDIO ALBUM',13500000,2002)")
cur.execute("insert into records values('EP103','SLIM SHADY EP','EMINEM','HIP HOP','EP',600000,1997)")
cur.execute("insert into records values('SL103','LOSE YOURSELF','EMINEM','HIP HOP','SINGLE',2000000,1973)")
cur.execute("insert into records values('SA110','DAMN.','KENDRICK LAMAR','HIP HOP','STUDIO ALBUM',3137000,2017)")
cur.execute("insert into records values('SA111','GOOD KID, M.A.A.D CITY','KENDRICK LAMAR','HIP HOP','STUDIO ALBUM',1002000,2012)")
cur.execute("insert into records values('SA112','TO PIMP A BUTTERFLY','KENDRICK LAMAR','HIP HOP','STUDIO ALBUM',1850000,2015)")
cur.execute("insert into records values('EP104','UNTITLED UNMASTERED','KENDRICK LAMAR','HIP HOP','EP',1500000,2016)")
cur.execute("insert into records values('SL104','HUMBLE','KENDRICK LAMAR','HIP HOP','SINGLE',1300000,2017)")
cur.execute("insert into records values('SA201','AFTER HOURS','THE WEEKND','R&B','STUDIO ALBUM',2400000,2020)")
cur.execute("insert into records values('SA202','STARBOY','THE WEEKND','R&B','STUDIO ALBUM',4480000,2016)")
cur.execute("insert into records values('SA203','BEAUTY BEHIND THE MADNESS','THE WEEKND','R&B','STUDIO ALBUM',3700000,2015)")
cur.execute("insert into records values('EP201','MY DEAR MELANCHOLY','THE WEEKND','R&B','EP',769000,2018)")
cur.execute("insert into records values('SL201','THE HILLS','THE WEEKND','R&B','SINGLE',1000000,2015)")
cur.execute("insert into records values('SA204','BLONDE','FRANK OCEAN','R&B','STUDIO ALBUM',4200000,2016)")
cur.execute("insert into records values('SA205','CHANNEL ORANGE','FRANK OCEAN','R&B','STUDIO ALBUM',621000,2012)")
cur.execute("insert into records values('SA206','NOSTALGIA, ULTRA','FRANK OCEAN','R&B','STUDIO ALBUM',325000,2011)")
cur.execute("insert into records values('SL202','IN MY ROOM','FRANK OCEAN','R&B','EP',600000,2019)")
cur.execute("insert into records values('SL203','CHANEL','FRANK OCEAN','R&B','SINGLE',621000,2017)")
cur.execute("insert into records values('SA207','AMERICAN TEEN','KHALID','R&B','STUDIO ALBUM',1220000,2017)")
cur.execute("insert into records values('SA208','FREE SPIRIT','KHALID','R&B','STUDIO ALBUM',202000,2019)")
cur.execute("insert into records values('SL204','YOUNG DUMB & BROKE','KHALID','R&B','SINGLE',200000,2017)")
cur.execute("insert into records values('EP202','SUNCITY','KHALID','R&B','EP',128000,2018)")
cur.execute("insert into records values('SL205','LOCATION','KHALID','R&B','SINGLE',1220000,2017)")
cur.execute("insert into records values('SA209','SCORPION','DRAKE','R&B','STUDIO ALBUM',3905000,2017)")
cur.execute("insert into records values('SA210','VIEWS','DRAKE','R&B','STUDIO ALBUM',1730000,2016)")
cur.execute("insert into records values('SA211','TAKE CARE','DRAKE','R&B','STUDIO ALBUM',2260000,2011)")
cur.execute("insert into records values('EP203','SO FAR GONE','DRAKE','R&B','EP',1350000,2009)")
cur.execute("insert into records values('SL206','ONE DANCE','DRAKE','R&B','SINGLE',3250000,2016)")
cur.execute("insert into records values('EP301','SEVEN','MARTIN GARRIX','ELECTRONIC','EP',100000,2016)")
cur.execute("insert into records values('EP302','BREAK THROUGH THE SILENCE','MARTIN GARRIX','ELECTRONIC','EP',230000,2015)")
cur.execute("insert into records values('EP303','BANGARANG','SKRILLEX','ELECTRONIC','EP',960000,2011)")
cur.execute("insert into records values('SA301','TRUE','AVICCI','ELECTRONIC','STUDIO ALBUM',1200000,2013)")
cur.execute("insert into records values('SA302','SKRILLEX AND DIPLO PRESENT JACK Ü','JACK Ü','ELECTRONIC','STUDIO ALBUM',1400000,2015)")
cur.execute("insert into records values('SA303','RECESS','SKRILLEX','ELECTRONIC','STUDIO ALBUM',900000,2014)")
cur.execute("insert into records values('SA304','18 MONTHS','CALVIN HARRIS','ELECTRONIC','STUDIO ALBUM',940000,2012)")
cur.execute("insert into records values('SA305','ADVENTURE','MADEON','ELECTRONIC','STUDIO ALBUM',600000,2015)")
cur.execute("insert into records values('SL301','SCARED TO BE LONELY','MARTIN GARRIX','ELECTRONIC','SINGLE',800000,2017)")
cur.execute("insert into records values('SL302','NOW THAT I'VE FOUND YOU','MARTIN GARRIX','ELECTRONIC','SINGLE',100000,2016)")
cur.execute("insert into records values('SA306','READY FOR THE WEEKEND','CALVIN HARRIS','ELECTRONIC','STUDIO ALBUM',900000,2009)")
cur.execute("insert into records values('SA307','STORIES','AVICII','ELECTRONIC','STUDIO ALBUM',2300000,2015)")
cur.execute("insert into records values('EP304','THE DAYS/NIGHTS EP','AVICII','ELECTRONIC','EP',1400000,2014)")
cur.execute("insert into records values('EP305','THE CITY','MADEON','ELECTRONIC','EP',250000,2012)")
cur.execute("insert into records values('EP306','GOLD SKIES','MARTIN GARRIX','ELECTRONIC','EP',500000,2014)")
cur.execute("insert into records values('SL303','IN THE NAME OF LOVE','MARTIN GARRIX','ELECTRONIC','SINGLE',400000,2016)")
cur.execute("insert into records values('SL304','BUN UP THE DANCE','SKRILLEX','ELECTRONIC','SINGLE',1200000,2015)")
cur.execute("insert into records values('SA308','FUNK WAV BOUNCES VOL.1','CALVIN HARRIS','ELECTRONIC','STUDIO ALBUM',6700000,2017)")
cur.execute("insert into records values('SL305','WAKE ME UP','AVICII','ELECTRONIC','SINGLE',1000000,2013)")
cur.execute("insert into records values('SL306','HEY BROTHER','AVICII','ELECTRONIC','SINGLE',950000,2013)")

conobj.commit()

try:
    cur.execute("drop table cart")
except:
    print()

cur.execute("create table cart(Record_ID varchar(5) references records(Record_ID), Name varchar(40), Artist varchar(20), Format varchar(20), Quantity integer)")
conobj.commit()

cur.execute("use music")

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
        cur.execute("set @rank:=0")
        cur.execute("select (@rank:=@rank+1) as Rank, Record_ID, Name, Artist, format(Units_Sold,0) as Copies_Sold, Genre, Format, Year from records order by Units_Sold desc limit 25")
        table=cur.fetchall()
        tableprint(table)
        addtocart()

    elif choice==2:
        clearscreen()
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
        print("\nThanks for visiting !\n")
        break

    else:
        print("\nInvalid choice!\n")