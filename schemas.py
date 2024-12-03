from marshmallow import Schema, fields, validate
from models import PowerplantTypes

class FuelsSchema(Schema):
    gas = fields.Float(required=True, data_key="gas(euro/MWh)")
    kerosine = fields.Float(required=True, data_key="kerosine(euro/MWh)")
    co2 = fields.Float(required=True, data_key="co2(euro/ton)")
    wind = fields.Float(required=True, data_key="wind(%)")

class PowerplantSchema(Schema):
    name = fields.Str(required=True)
    # type_plant = [gasfired, turbojet, windturbine]
    type_plant = fields.Str(required=True, data_key="type", validate=validate.OneOf([type_plant.value for type_plant in PowerplantTypes])) 
    efficiency = fields.Float(required=True)
    pmin = fields.Float(required=True)
    pmax = fields.Float(required=True)

class ProductionPlanSchema(Schema):
    load = fields.Float(required=True)
    fuels = fields.Nested(FuelsSchema)
    powerplants = fields.List(fields.Nested(PowerplantSchema))