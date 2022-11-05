import datetime

def findseason (M) :
     
    # Taken all the possible
    # month numbers in the list.
    list1 = [[12 , 1 , 2], [3 , 4 , 5],
             [6 , 7 , 8], [9 , 10 , 11]]
              
    # Matching the month number
    # with the above list entries
    if M in list1[0] :
        print ( "WINTER" )
    elif M in list1[1] :
        print ( "SPRING" )
    elif M in list1[2] :
        print ( "SUMMER" )
    elif M in list1[3] :
        print ( "AUTUMN" )
    else :
        print ( "Invalid Month Number" )

def findCurrentSeason() :
    now = datetime.datetime.now()
    M = now.strftime('%m')
    print("For Month number:", M);
    findseason ( int(M) )
 
# Driver Code
M = 1
print("For Month number:", M);
findseason ( M )
 
M = 12
print("For Month number:", M);
findseason ( M )

findCurrentSeason()

# inspired by the code contributed by Abhishek
