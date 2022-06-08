#1st level inputs
def cur_SP():
    while True:
        try:
            user_input = float(input("Enter the current set point in degree Celcius: "))
            if user_input < (-143.15):
                print("The current set point is below the minimum set point of -143.15 degree Celcius.")
                print("Please enter a value above -143.15 degree Celcius.")
                continue
            elif user_input > (350.15):
                print("The current set point is above the maximum set point of 350.15 degree Celcius.")
                print("Please enter a value below 350.15 degree Celcius.")
                continue
            else: 
                return user_input
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            break
    # user_input = float(input("Enter the temperature in degree Celcius: "))
    # try: 
    #     val = float(str(user_input))
    # except ValueError: 
    #     print("Input is not a number")

def avg_RH():
    while True:
        try:
            user_input = float(input("Enter the average relative humidity in %: "))
            if user_input < (0):
                print("The average relative humidity is below the minimum relative humidity of 0%.")
                print("Please enter a value above 0%.")
                continue
            elif user_input > (100):
                print("The average relative humidity is above the maximum relative humidity of 100%.")
                print("Please enter a value below 100%.")
                continue
            else:
                return user_input
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            break
    # avg_rh = input("Enter the average relative humidity in %: ")
    # return int(avg_rh)
        
def desired_SP():
    while True:
        try:
            user_input = float(input("Enter the desired set point in degree Celcius: "))
            if user_input < (-143.15):
                print("The current set point is below the minimum set point of -143.15 degree Celcius.")
                print("Please enter a value above -143.15 degree Celcius.")
                continue
            elif user_input > (350.15):
                print("The current set point is above the maximum set point of 350.15 degree Celcius.")
                print("Please enter a value below 350.15 degree Celcius.")
                continue
            else:
                return user_input
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            break
    # desired_sp = input("Enter the desired set point in degree Celcius: ")
    # return desired_sp

def airflow():
    while True:
        try:
            user_input = float(input("Enter the airflow in m^3/h: "))
            if user_input < (0):
                print("The airflow is below the minimum airflow of 0 m^3/h.")
                print("Please enter a value above 0 m^3/h.")
                continue
            else:
                return user_input
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            break

def op_hours():
    while True:
        try:
            user_input = float(input("Enter the operating hours in hours: "))
            if user_input < (0):
                print("The operating hours is below the minimum operating hours of 0 hours.")
                print("Please enter a value above 0 hours.")
                continue
            elif user_input > (24):
                print("The operating hours is above the maximum operating hours of 24 hours.")
                print("Please enter a value below 24 hours.")
                continue
            else:
                return user_input
        except ValueError:
            print("Invalid Input. Please enter a valid number.")
            break