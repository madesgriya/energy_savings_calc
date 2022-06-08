# from distutils.command.config import config
# import argparse
# import config
import json
import os

class bca_eui():
    # def parse():
    #     with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
    #         cfg = json.load(f)
    #         return cfg

    def calc_eui(self, buildingSize, kWh_yr):
        """
        calculating the building's carbon emissions
        recomendation to achieve higher quartile
        recomendation on thermal comfort 
        source: https://www.bca.gov.sg/bess/benchmarkingreport/benchmarkingreport.aspx
        """
        #calculating EUI
        aircon_ratio = 0.6
        overall_energy = kWh_yr / aircon_ratio
        eui = float(overall_energy) / float(buildingSize)
        return eui
    
    def getQuartile(self, response, size, eui):
        """
        getting the EUI quartile
        """
        # parser = argparse.ArgumentParser(description="EUI parser")
        # parser.add_argument("-c", "--config", default="config.json", type=str, help="EUI values")
        # args = parser.parse_args()

        # cfg = config.parse(args.config)
        
        # cfg = self.parse()
        with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
            cfg = json.load(f)

        size = float(size)

        response = str(response)
        commercial = ["office", "hotel", "shop"]
        others = ["school", "hospital", "library", "auditorium"]
        if response in commercial:
            if size >= 15000.0:
                if eui >= cfg["EUI"][response]["large"]["3rdQuartile"]:
                    return "on the bottom quartile"
                elif cfg["EUI"][response]["large"]["2ndQuartile"] <= eui < cfg["EUI"][response]["large"]["3rdQuartile"]:
                    return "on the 3nd quartile"
                elif cfg["EUI"][response]["large"]["topQuartile"] <= eui < cfg["EUI"][response]["large"]["2ndQuartile"]:
                    return "on the 2nd quartile"
                elif eui <= cfg["EUI"][response]["large"]["topQuartile"]:
                    return "on the top quartile"
            elif 5000.0 <= size < 15000.0:
                if eui >= cfg["EUI"][response]["medium"]["3rdQuartile"]:
                    return "on the bottom quartile"
                elif cfg["EUI"][response]["medium"]["2ndQuartile"] <= eui < cfg["EUI"][response]["medium"]["3rdQuartile"]:
                    return "on the 3nd quartile"
                elif cfg["EUI"][response]["medium"]["topQuartile"] <= eui < cfg["EUI"][response]["medium"]["2ndQuartile"]:
                    return "on the 2nd quartile"
                elif eui <= cfg["EUI"][response]["medium"]["topQuartile"]:
                    return "on the top quartile"
        elif response in others:
            if size >= 5000.0:
                if eui < cfg["EUI"][response]["average"]:
                    return "better than the average"
                elif eui > cfg["EUI"][response]["average"]:
                    return "worse than the average"
            else:
                return ""
        else:
            return "Invalid response"

# print (bca_eui().getQuartile("school", 15001, 123))

# def parse():
#     with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
#         cfg = json.load(f)
#         return cfg

# cfg = parse()
# print(cfg["EUI"]["office"]["large"]["3rdQuartile"])