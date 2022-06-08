from flask import Flask, render_template, request
from CoolProp.HumidAirProp import HAPropsSI
from bca import bca_eui
import html

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def result():
    if request.method == 'POST':
        response = {
            # 'firstName': request.form['wpforms[fields][1][first]'],
            # 'lastName': request.form['wpforms[fields][1][last]'],
            # 'email': request.form['wpforms[fields][2]'],
            # 'company': request.form['wpforms[fields][3]'],
            'facility': request.form['wpforms[fields][4]'],
            'buildingSize': request.form['wpforms[fields][7]'],
            'curSP': request.form['wpforms[fields][8]'],
            'humidity': request.form['wpforms[fields][9]'],
            'desiredSP': request.form['wpforms[fields][10]'],
            'system': request.form['wpforms[fields][11]']
        }
        class prelim_data:
            def __init__(self):
                self.facility = response['facility']
                self.equip = response['system']
                self.area = float(response['buildingSize'])
                self.cursp = float(response['curSP'])
                self.humidity = float(response['humidity'])
                self.desiredsp = float(response['desiredSP'])
            
            def get_hours(self): 
                facility = self.facility
                if facility == "apartment":
                    return 8
                elif facility == "auditorium":
                    return 4
                elif facility == "school":
                    return 8
                elif facility == "industrial factory":
                    return 24
                elif facility == "hospital":
                    return 24
                elif facility == "hotel":
                    return 12
                elif facility == "library":
                    return 12
                elif facility == "office":
                    return 8
                elif facility == "residential":
                    return 10
                elif facility == "data center":
                    return 8
                elif facility == "shop":
                    return 10
                elif facility == "outside air (lab, hospital)":
                    return 12
                else:
                    return 12
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
                area = self.area
                convert_air = 18.2878661
                facility = self.facility
                if facility == "apartment":
                    return area * convert_air * 1.0
                elif facility == "auditorium":
                    return area * convert_air * 2.0
                elif facility == "school":
                    return area * convert_air * 1.6
                elif facility == "industrial factory":
                    return area * convert_air * 3.2
                elif facility == "hospital":
                    return area * convert_air * 1.3
                elif facility == "hotel":
                    return area * convert_air * 1.3
                elif facility == "library":
                    return area * convert_air * 1.35
                elif facility == "office":
                    return area * convert_air * 1.3
                elif facility == "residential":
                    return area * convert_air * 1.3
                elif facility == "data center":
                    return area * convert_air * 0.9
                elif facility == "shop":
                    return area * convert_air * 8.0
                elif facility == "outside air (lab, hospital)":
                    return area * convert_air * 1.3
                else:
                    return area * convert_air * 1.2

            def getEquipEff(self): #getting equipment COP
                if self.equip == "water-cooled chiller plant":
                    return 4.0
                elif self.equip == "air-cooled chiller plant":
                    return 6.8
                elif self.equip == "variable refrigerant volume (VRV)":
                    return 3.5
                elif self.equip == "split unit (residential AC split)":
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
                temp1 = self.cursp + 273.15 #deg. C
                rh1 = self.humidity / 100 #%
                SV1 = HAPropsSI('V','T',temp1,'P',101325,'R',rh1)  #specific volume m^3/kg
                m_dot1 = af * (1/SV1) #kg/h
                h1 = HAPropsSI('H','T',temp1,'P',101325,'R',rh1) #enthalpy J/kg
                q1 = m_dot1 * h1 #heat input J/h

                #desired condition
                temp2 = self.desiredsp + 273.15 #deg. C
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

                elec_bill = 0.299 #S$/kWh  #apply different tarrif for different regions

                sgd_yr = kWh_yr * elec_bill #S$/yr
                
                if sgd_yr < 0:
                    return str("You're wasting* " + str(round(sgd_yr*0.85*(-1))) + "** to " + str(round(sgd_yr*1.05*(-1))) + (" SGD/year"))
                else:
                    return str("Your potential energy saving* is: " + str(round(sgd_yr*0.85)) + "** to " + str(round(sgd_yr*1.05)) + ("** SGD/year"))

            def trivial_num(self):
                """
                giving the amopunt of energy wasted in the building /deg.C/m2.year
                """
                af = self.get_airflow() #m^3/h
                hours = self.get_hours() 
                COP = self.getEquipEff() #kWr/kW

                #current condition 
                temp1 = self.cursp + 273.15 #deg. C
                rh1 = self.humidity / 100 #%
                SV1 = HAPropsSI('V','T',temp1,'P',101325,'R',rh1)  #specific volume m^3/kg
                m_dot1 = af * (1/SV1) #kg/h
                h1 = HAPropsSI('H','T',temp1,'P',101325,'R',rh1) #enthalpy J/kg
                q1 = m_dot1 * h1 #heat input J/h

                #desired condition
                temp2 = self.desiredsp + 273.15 #deg. C
                rh2 = 70 / 100 #%
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

                carbon_waste = kWh_yr * 0.4080 #kg CO2/yr 
                #source: https://www.ema.gov.sg/singapore-energy-statistics/Ch02/index2#:~:text=Singapore's%20average%20OM%20GEF%20fell,CO2%2FkWh%20in%202020.

                specific_energy = kWh_yr / self.area / (temp2-temp1)#kWh/C.m2.year
                percentage = (kWh_yr/(q1 / 3600 / 1000 * hours * 365)) * 100 #%
                return specific_energy, carbon_waste, percentage, kWh_yr

        def calc_result(): #params needed for AWS Lambda
            output = str(prelim_data().enthalpy_diff())
            return output   

        specific_energy, carbon_waste, percentage, kWh_yr = prelim_data().trivial_num()

        def bca_output():
            facility = response['facility']
            size = float(response['buildingSize'])
            eui = bca_eui().calc_eui(size,kWh_yr)
            myList = ["office", "hotel", "shop", "school", "hospital", "library", "auditorium"]
            if facility in myList:
                if size >= 5000.0:
                    return str("According to BCA Energy Utilization Index (EUI) Benchmark***, your estimated EUI is currently " + 
                    bca_eui().getQuartile(facility,size,eui) + 
                    " for most " + facility + "s.")
                else:
                    return ""
            else: 
                return ""
        
        def eui_link():
            facility = response['facility']
            size = float(response['buildingSize'])
            myList = ["office", "hotel", "shop", "school", "hospital", "library", "auditorium"]
            if facility in myList:
                if size >= 5000.0:
                    return str('based on BCA 2020 EUI Benchmark***')#, str('https://www.bca.org.sg/en/energy-efficiency/benchmark-eui')
                else:
                    return ""#,""
            else:
                return ""#,""

        # eui_link1, eui_link2 = eui_link()

        output = str(calc_result())
        return render_template("result.html", 
                                amount=output, 
                                typeOfBuilding=response['facility'], 
                                average_low=str(round((specific_energy*0.85),1)), 
                                average_high=str(round((specific_energy*1.15),1)),
                                cooling=response['system'], 
                                carbon_waste=str(round(carbon_waste,1)),
                                percentage=round(percentage,1),
                                eui_output=bca_output(),
                                eui_link=eui_link()
                                # eui_link1 = eui_link1,
                                # eui_link2 = eui_link2
                                )
    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
