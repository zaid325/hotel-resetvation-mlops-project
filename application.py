import joblib
import numpy as np
from config.paths_config import MODEL_OUTPUT_PATH
from flask import Flask , render_template , request

app=Flask(__name__)

loaded_model=joblib.load(MODEL_OUTPUT_PATH)

@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method=='POST':
        no_of_adults= int(request.form["no_of_adults"])

        no_of_children=int(request.form["no_of_children"])
        no_of_weekend_nights=int(request.form["no_of_weekend_nights"])
        no_of_week_nights=int(request.form["no_of_week_nights"])
        type_of_meal_plan=int(request.form["type_of_meal_plan"])
        required_car_parking_space=int(request.form["required_car_parking_space"])
        room_type_reserved=int(request.form["room_type_reserved"])
        lead_time=int(request.form["lead_time"])
        arrival_year=int(request.form["arrival_year"])
        arrival_month=int(request.form["arrival_month"])


        features=np.array([[no_of_adults , no_of_children , no_of_weekend_nights , no_of_week_nights , type_of_meal_plan , required_car_parking_space , room_type_reserved , lead_time , arrival_year , arrival_month]])
        predictions=loaded_model.predict(features)

        return render_template('index.html' , predictions=predictions[0])
    return render_template("index.html" , predictions=None)

if __name__=="__main__":
    app.run(debug=True , host='0.0.0.0', port=5000)