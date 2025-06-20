from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("payments.pkl", "rb"))

# Transaction type encoding mapping
TYPE_MAPPING = {
    'PAYMENT': 0,
    'TRANSFER': 1,
    'CASH_OUT': 2,
    'DEBIT': 3,
    'CASH_IN': 4
}

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
            # Get form data
            step = float(request.form['step'])
            transaction_type = request.form['type']
            amount = float(request.form['amount'])
            oldbalance_org = float(request.form['oldbalanceOrg'])
            newbalance_orig = float(request.form['newbalanceOrig'])
            oldbalance_dest = float(request.form['oldbalanceDest'])
            newbalance_dest = float(request.form['newbalanceDest'])
            
            # Encode transaction type
            type_encoded = TYPE_MAPPING.get(transaction_type, 0)
            
            # Create feature array - adjust the order based on your model's training
            # Common order for payment fraud models: [step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest]
            features = [step, type_encoded, amount, oldbalance_org, newbalance_orig, oldbalance_dest, newbalance_dest]
            
            # Convert to numpy array
            final_input = np.array([features])
            
            # Make prediction
            prediction = model.predict(final_input)
            result = 'Fraudulent Transaction' if prediction[0] == 1 else 'Genuine Transaction'
            
            print(f"Input features: {features}")  # Debug print
            print(f"Prediction: {prediction[0]}")  # Debug print
            
        except Exception as e:
            result = f'Error processing transaction: {str(e)}'
            print(f"Error: {str(e)}")  # Debug print
            
        return render_template('predict.html', prediction_text=result)
    return render_template('predict.html', prediction_text='Waiting for input...')

if __name__ == '__main__':
    app.run(debug=True)