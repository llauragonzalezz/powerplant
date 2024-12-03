from enum import Enum

class PowerplantTypes(Enum):
    GASFIRED = "gasfired"
    TURBOJET = "turbojet"
    WINDTURBINE = "windturbine"


class Fuels:

    def __init__(self, gas, kerosine, co2, wind):
        self.gas = gas # the price of gas
        self.kerosine = kerosine # the price of kerosine
        self.co2 = co2
        self.wind = wind # percentage of wind. 


class Powerplant:

    def __init__(self, name, type_plant, efficiency, pmin, pmax):
        self.name = name
        self.type_plant = type_plant     # [gasfired, turbojet, windturbine]
        self.efficiency = efficiency
        self.pmin = pmin # max amount of power the powerplant generates when switched on
        self.pmax = pmax # max amount of power the powerplant generates when switched on

    def max_power_to_generate(self, load, fuels):
        if self.type_plant == PowerplantTypes.WINDTURBINE.value:
            return fuels.wind * max(min(self.pmax, load), self.pmin) / 100
        
        return max(min(self.pmax, load), self.pmin)
        
    def powerplant_score(self, load, fuels):
        if self.type_plant == PowerplantTypes.WINDTURBINE.value:
            # Wind-turbines do not consume any fuel
            return 0 

        if self.type_plant == PowerplantTypes.TURBOJET.value:
            # turbojet runs on kerosine
            return fuels.kerosine/self.efficiency * max(load, self.pmin)
            
        if self.type_plant == PowerplantTypes.GASFIRED.value:
            # gas-fired runs on gas
            return fuels.gas/self.efficiency * max(load, self.pmin)
