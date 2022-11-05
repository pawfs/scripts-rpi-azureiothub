import os
import datetime

def turn_on_heat():
    print("ON HEAT")
    os.system('irsend SEND_ONCE westpoint_ac power-on-heat-low-26')
def turn_off_heat():
    print("OFF winter")
    os.system('irsend SEND_ONCE westpoint_ac power-off-heat-low-26')
def turn_on_cool():
    print("ON COOL")
    os.system('irsend SEND_ONCE westpoint_ac power-on-cool-low-21')
def turn_off_cool():
    print("OFF summer")
    os.system('irsend SEND_ONCE westpoint_ac power-off-cool-low-21')

def find_current_season() :
    now = datetime.datetime.now()
    month_str = now.strftime('%m')
    M = int(month_str)
    #print("For Month number:", M)
    # Taken all the possible
    # month numbers in the list.
    list1 = [[12 , 1 , 2], [3 , 4 , 5],
             [6 , 7 , 8, 9], [10 , 11]]
              
    # Matching the month number
    # with the above list entries
    if M in list1[0]:
        return ("WINTER")
    elif M in list1[1]:
        return ("SPRING")
    elif M in list1[2]:
        return ("SUMMER")
    elif M in list1[3]:
        return ("AUTUMN")
    else:
        return ("Invalid Month Number")

def working_time() :
    dt = datetime.datetime.now()
    #print('Datetime is:', dt)

    # get day of week as an integer
    #0 Monday/ 1 Tuesday /2 Wednesday/ 3 Thursday/ 4 Friday / 5 Saturday/ 6 Sunday
    d = dt.weekday()
    #print('Day of a week is:', d)
    h = dt.hour
    if d < 5 and h > 7 and h < 18 :
        return True
    else:
        return False
        
 
def choose_action(temp, max_sum, min_sum, max_win, min_win):
    #check day of week
    work_time = working_time()
    #check season
    season = find_current_season()
    #print(temp,max_sum, min_sum, max_win, min_win, season)
    if season == "SUMMER":
        if not work_time :
            turn_off_cool()
            return "OFF"
        elif temp > max_sum:
            turn_on_cool()
            return "ON_COOL"
        elif temp < min_sum:
            turn_off_cool()
            return "OFF"
        else:
            # temperature in the middle => don't change state
            return "no_change"
    elif season == "WINTER":
        if not work_time :
            turn_off_heat()
            return "OFF"
        elif temp > max_win:
            turn_off_heat()
            return "OFF"
        elif temp < min_sum:
            turn_on_heat()
            return "ON_HEAT"
        else:
            # temperature in the middle => don't change state
            print("no change")
            return "no_change"
    else:
        print("no change")
        return "no_change"

# Driver Code
#print(find_current_season())
#print('Work tiiime',working_time())

    
