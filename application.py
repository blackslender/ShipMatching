from flask import Flask, request
app = Flask(__name__)

import numpy as np
import json

@app.route("/")
def hello():
    return "Hello world!"
import alg
@app.route("/cal")
def cal():
    # If an error occur, it will be return to client automatically
    response = {
        "success": False,
        "data": None,
        "error": None
    }
    try:
        data = json.loads(request.get_data().decode("utf-8"))["data"]
        result,profitability = alg.parse(alg.cal(data),data)
        response["success"] = True 
        response["data"] = {
            "profitability":profitability,
            "pairs":result
        }
        response["error"] = None
    except Exception as e:
        response["success"] = False
        response["data"] = None
        response["error"] = e.__class__.__name__ +":  " + str(e)

    return json.dumps(response)
