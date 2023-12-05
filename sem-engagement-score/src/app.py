from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS

import json
import score

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://sem-frontend.40063427.qpc.hal.davecutting.uk/"}})
#CORS(app, resources={r"/*": {"origins": "http://semproxy.40063427.qpc.hal.davecutting.uk"}})

@app.route('/')

def student_engagement_score():

    rlec = request.args.get('attendance_1')
    rlab = request.args.get('attendance_2')
    rsupp = request.args.get('attendance_3')
    rcan = request.args.get('attendance_4')


    if not rlec:
          r = "Lecture session data is missing"
          response = Response(response=r, status=400)
          return response
     
    if not rlab:
          r = "Lab session data is missing"
          response = Response(response=r, status=400)
          return response
     
    if not rsupp:
          r = "Support sessions data is missing"
          response = Response(response=r, status=400)
          return response
     
    if not rcan:
          r = "Canvas activities data is missing"
          response = Response(response=r, status=400)
          return response

    try:
          lec = int(rlec)
          lab = int(rlab)
          supp = int(rsupp)
          can = int(rcan)
    except ValueError:
          r = "You must provide valid integers"
          response = Response(response=r, status=400)
     
    engagementscore = score.scorecalc(lec,lab,supp,can,)

    r = {
          "error": False,
          "answer": engagementscore,
     }
    reply = json.dumps(r)

    response = Response(response=reply, status=200, mimetype='application/json')
    response.headers["Content-Type"]="application/json"
    response.headers["Access-Control-Allow-Origin"]="*"
     
    return response

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=80)