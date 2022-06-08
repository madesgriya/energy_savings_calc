from CoolProp.HumidAirProp import HAPropsSI
from math import sin

from user_input import cur_SP, avg_RH, desired_SP, airflow, op_hours

class prelim_data:
    def __init__(self):
        self.facility = input("Choose your facility type: \n(a) apartment\n(b) auditorium\n(c) school\n(d) industrial\n(e) hospital\n(f) hotel\n(g) library\n(h) office\n(i) residential\n(j) server\n(k) shop\n\n")
        self.equip = input("What kind of cooling system do you have in your facility?\n(a) air-cooled chiller plant\n(b) water-cooled chiller plant\n(c) Variable Refrigerant Volume (VRV)\n(d) Split Unit (residential)\n\n")
    def get_hours(self):
        facility = self.facility
        if facility == "a":
            return 24
        elif facility == "b":
            return 24
        elif facility == "c":
            return 24
        elif facility == "d":
            return 24
        elif facility == "e":
            return 24
        elif facility == "f":
            return 24
        elif facility == "g":
            return 24
        elif facility == "h":
            return 24
        elif facility == "i":
            return 24
        elif facility == "j":
            return 24
        elif facility == "k":
            return 24
        else:
            return 24
    def get_airflow(self):
        """
        estimating the airflow based on the area and type of building 
        source: https://www.engproguides.com/ruleofthumbcalculator.pdf
        other source: https://www.ashrae.org/file%20library/technical%20resources/standards%20and%20guidelines/standards%20addenda/62_1_2013_p_20150707.pdf
        
        cubic feet per minute per square foot:
        a apartment 0.8-1.2
        b auditorium 1.0-3.0
        c school 1.2-2.0
        d industrial factory 2.4-4.0
        e hospital 1.1-1.5
        f hotel 1.2-1.4
        g library 1.1.-1.6
        h office 1.0-1.6
        i residential 0.7-1.1
        j server 4.0-12.0
        k shop 1.0-1.6
        l outside air (lab, hospital) 1.2-2.0 

        1 cfm = 1.699 m^3/h:
        1sqm = 10.7639 sqft

        1 cfm/sqft = 1.699 m^3/h/sqft
        1 sqm/sqft = 18.2878661 m^3/h/sqm

        """
        area = float(input("Enter the area of the building in square meters: "))
        convert_air = 18.2878661
        facility = self.facility
        if facility == "a":
            return area * convert_air * 1.0
        elif facility == "b":
            return area * convert_air * 2.0
        elif facility == "c":
            return area * convert_air * 1.6
        elif facility == "d":
            return area * convert_air * 3.2
        elif facility == "e":
            return area * convert_air * 1.3
        elif facility == "f":
            return area * convert_air * 1.3
        elif facility == "g":
            return area * convert_air * 1.35
        elif facility == "h":
            return area * convert_air * 1.3
        elif facility == "i":
            return area * convert_air * 0.9
        elif facility == "j":
            return area * convert_air * 8.0
        elif facility == "k":
            return area * convert_air * 1.3
        else:
            return area * convert_air * 1.2

    def getEquipEff(self): #getting equipment COP
        if self.equip == "a":
            return 4.0
        elif self.equip == "b":
            return 6.8
        elif self.equip == "c":
            return 3.5
        elif self.equip == "d":
            return 3.0
        else:
            return 3.0

    def enthalpy_diff(self):
        """
        calcualting the enthalpy difference between the desired set point and the current temperature
        doc: http://www.coolprop.org/apidoc/CoolProp.CoolProp.html
        """
        af = self.get_airflow() #m^3/h
        hours = self.get_hours() 
        COP = self.getEquipEff() #kWr/kW

        #current condition 
        temp1 = cur_SP() + 273.15 #deg. C
        rh1 = avg_RH() / 100 #%
        SV1 = HAPropsSI('V','T',temp1,'P',101325,'R',rh1)  #specific volume m^3/kg
        m_dot1 = af * (1/SV1) #kg/h
        h1 = HAPropsSI('H','T',temp1,'P',101325,'R',rh1) #enthalpy J/kg
        q1 = m_dot1 * h1 #heat input J/h

        #desired condition
        temp2 = desired_SP() + 273.15 #deg. C
        rh2 = rh1
        SV2 = HAPropsSI('V','T',temp2,'P',101325,'R',rh2)  #specific volume m^3/kg
        m_dot2 = af * (1/SV2) #kg/h
        h2 = HAPropsSI('H','T',temp2,'P',101325,'R',rh2) #enthalpy J/kg
        q2 = m_dot2 * h2 #heat input J/h

        dQ = q2 - q1 #heat differece J/h
        Js = dQ / 3600 #J/s
        kWr = Js / 1000 #kW

        kWrh_day = kWr * hours #kWh/day 
        kWrh_yr = kWrh_day * 365 #kWh/yr

        # creating the cooling to electrical efficiency logic
        kWh_yr = kWrh_yr / COP

        elec_bill = 0.12 #S$/kWh 

        sgd_yr = kWh_yr * elec_bill #S$/yr
        
        if sgd_yr < 0:
            print("You're wasting " + str(round(sgd_yr*0.85*(-1))) + " to " + str(round(sgd_yr*1.05*(-1))) + (" SGD/year"))
        else:
            print(("Your potential energy saving is: ") + str(round(sgd_yr*0.85)) + " to " + str(round(sgd_yr*1.05)) + (" SGD/year"))

prelim_data().enthalpy_diff()


