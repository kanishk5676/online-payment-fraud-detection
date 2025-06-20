from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("payments.pkl", "rb"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/submit')
def submit():
    return render_template('submit.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            features = [float(x) for x in request.form.values()]
            final_input = np.array([features])
            prediction = model.predict(final_input)
            result = 'Fraudulent Transaction' if prediction[0] == 1 else 'Genuine Transaction'
        except:
            result = 'Invalid input format. Please try again.'
        return render_template('predict.html', prediction_text=result)
    return render_template('predict.html', prediction_text='Waiting for input...')

if __name__ == '__main__':
    app.run(debug=True)
