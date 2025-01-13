from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# Initialize the Flask app
app = Flask(__name__)

# Load the pre-trained lightweight model
model = joblib.load('logistic_model.pkl')

@app.route('/')
def home():
    return render_template('index.html', prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Receive and process input data from the form
        sepal_length = float(request.form['sepal_length'])
        sepal_width = float(request.form['sepal_width'])
        petal_length = float(request.form['petal_length'])
        petal_width = float(request.form['petal_width'])

        # Prepare data for prediction
        features = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)
        prediction = model.predict(features)[0]
        species = ['setosa', 'versicolor', 'virginica']

        return render_template('index.html', prediction=species[int(prediction)],
                               sepal_length=sepal_length,
                               sepal_width=sepal_width,
                               petal_length=petal_length,
                               petal_width=petal_width)

    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
