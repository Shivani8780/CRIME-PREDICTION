from flask import Flask, request, render_template 
import pickle 
import math

model = pickle.load(open('Model/model.pkl', 'rb')) 

app = Flask(__name__) 

@app.route('/') 
def index(): 
    return render_template("index.html") 

@app.route('/predict', methods=['POST']) 
def predict_result(): 
    try:
        city_names = { '0': 'Ahmedabad', '1': 'Bengaluru', '2': 'Chennai', '3': 'Coimbatore', '4': 'Delhi', '5': 'Ghaziabad', '6': 'Hyderabad', '7': 'Indore', '8': 'Jaipur', '9': 'Kanpur', '10': 'Kochi', '11': 'Kolkata', '12': 'Kozhikode', '13': 'Lucknow', '14': 'Mumbai', '15': 'Nagpur', '16': 'Patna', '17': 'Pune', '18':'Surat'}
        crimes_names = { '0': 'Crime Committed by Juveniles', '1': 'Crime against SC', '2': 'Crime against ST', '3': 'Crime against Senior Citizen', '4': 'Crime against children', '5': 'Crime against women', '6': 'Cyber Crimes', '7': 'Economic Offences', '8': 'Kidnapping', '9':'Murder'}
        population = { '0': 63.50, '1': 85.00, '2': 87.00, '3': 21.50, '4': 163.10, '5': 23.60, '6': 77.50, '7': 21.70, '8': 30.70, '9': 29.20, '10': 21.20, '11': 141.10, '12': 20.30, '13': 29.00, '14': 184.10, '15': 25.00, '16': 20.50, '17': 50.50, '18':45.80}
        
        city_code = request.form["city"]
        crime_code = request.form['crime']
        year = request.form['year']

        # Validate inputs
        if not (city_code.isdigit() and crime_code.isdigit() and year.isdigit()):
            return render_template('error.html', message="Inputs must be numeric values.")
        
        city_code = int(city_code)
        crime_code = int(crime_code)
        year = int(year)
        
        if city_code not in range(0, 19):
            return render_template('error.html', message="Invalid city code.")
        
        if crime_code not in range(0, 10):
            return render_template('error.html', message="Invalid crime code.")
        
        if year < 2000 or year > 2100:  # Example range check for the year
            return render_template('error.html', message="Year must be between 2000 and 2100.")
        
        pop = population[str(city_code)]

        # Here increasing / decreasing the population as per the year.
        # Assuming that the population growth rate is 1% per year.
        year_diff = year - 2011
        pop = pop + 0.01 * year_diff * pop
        
        # Model expects a 2D array
        crime_rate = model.predict([[year, city_code, pop, crime_code]])[0]
        
        city_name = city_names[str(city_code)]
        crime_type = crimes_names[str(crime_code)]
        
        if crime_rate <= 1:
            crime_status = "Very Low Crime Area"
        elif crime_rate <= 5:
            crime_status = "Low Crime Area"
        elif crime_rate <= 15:
            crime_status = "High Crime Area"
        else:
            crime_status = "Very High Crime Area"
        
        cases = math.ceil(crime_rate * pop)
        
        return render_template('result.html', city_name=city_name, crime_type=crime_type, year=year, crime_status=crime_status, crime_rate=crime_rate, cases=cases, population=pop)
    
    except Exception as e:
        return render_template('error.html', message=str(e))

if __name__ == '__main__':
    app.run(debug=False)
