from flask import Flask, request, render_template
from prometheus_client import Counter, generate_latest, REGISTRY
from prometheus_client.exposition import CONTENT_TYPE_LATEST

app = Flask(__name__)

# Metrics
contact_form_requests_total = Counter('contact_form_requests_total', 'Total number of contact form submissions')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Store form data in a file
    with open('contacts.txt', 'a') as file:
        file.write(f'Name: {name}, Email: {email}, Message: {message}\n')

    # Increment the contact form submission counter metric
    contact_form_requests_total.inc()

    return 'Form submitted successfully!'

@app.route('/metrics')
def metrics():
    # Expose metrics for Prometheus
    return generate_latest(REGISTRY), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(debug=True)
