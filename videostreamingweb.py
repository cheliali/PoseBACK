from flask import Flask
from flask import request
from flask import render_template
from flask import Response
from flask import jsonify
from flask_cors import CORS, cross_origin

from blazepose import generate, iniciar, terminar

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS']='Content-Type'
app.config['TESTING'] = True


@app.route("/iniciar", methods=['GET'])
@cross_origin()
def iniciarf():
     iniciar()
     return jsonify("ok")

@app.route("/video_feed")
def video_feed():
     return Response(generate(),
          mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route("/terminar", methods=['GET'])
@cross_origin()
def terminarf():
     terminar()
     return jsonify("ok")

if __name__ == "__main__":
     app.run(debug=True)

