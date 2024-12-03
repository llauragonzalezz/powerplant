from flask import Flask, request, jsonify
from marshmallow import ValidationError
from models import Fuels, Powerplant
from schemas import ProductionPlanSchema
import heapq
from flask import jsonify

def set_production_plan(load, fuels, powerplants):
    production_plan = []
    heap = []
    # Calulate the score for each powerplant
    for i, powerplant in enumerate(powerplants):
        score = powerplant.powerplant_score(load, fuels)
        heapq.heappush(heap, (score, i, powerplant))  

    while load > 0 and len(powerplants) > 0:
        _, _, powerplant = heapq.heappop(heap) # choose the one on top (the one with best score)
        powerplants.remove(powerplant) # remove the powerplant
        power = powerplant.max_power_to_generate(load, fuels)
        production_plan.append({"name": powerplant.name, "p": power})
        load -= power

    # the missing powerplants
    for powerplant in powerplants:
        production_plan.append({"name": powerplant.name, "p": 0.0})
    
    # if there is still load left after using all powerplants -> error
    if load > 0:
        production_plan = jsonify({"error": "Not enough powerplants"}), 400

    return production_plan

app = Flask(__name__)

@app.route("/productionplan", methods=['POST'])
def calculate_productionplan():
    try:
        schema = ProductionPlanSchema()
        productionplan_request_data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"error": "Invalid request data", "details": err.messages}), 400

    load = productionplan_request_data["load"]
    fuels = Fuels(**productionplan_request_data["fuels"])
    powerplants = set([Powerplant(**powerplant) for powerplant in productionplan_request_data["powerplants"]])
    
    return set_production_plan(load, fuels, powerplants)


if __name__ == '__main__':
    app.run(port=8888)
    