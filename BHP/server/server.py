from flask import Flask, request, jsonify
import util
app = Flask(__name__)
print("server is running")

@app.route('/get_location_names')
def get_location_names():
    response = jsonify({'locations': util.get_location_names()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['GET','POST'])
def predict_home_price():
    import traceback
    try:
        if request.method == 'POST':
            data = request.form if request.form else request.get_json()
        else:  # GET request for testing
            data = request.args

        sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '').strip()
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

        price = util.get_estimated_price(location, sqft, bhk, bath)
        response = jsonify({'estimated_price': price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return "Server is running!"


if __name__ == "__main__":
    print("Starting Python flask server for house price prediction...")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=5000, debug=True)

