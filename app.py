from flask import Flask, render_template, request

app = Flask(__name__)

# Function to normalize weights
def normalize_weights(weights):
    total_weight = sum(weights)
    return [w / total_weight for w in weights]

# Function to calculate S values
def calculate_s_values(alternatives, weights, criteria_types):
    s_values = []
    for alt in alternatives:
        s = 1
        for i in range(len(weights)):
            if criteria_types[i] == 'benefit':
                s *= alt[i] ** weights[i]
            elif criteria_types[i] == 'cost':
                s *= alt[i] ** (-weights[i])
        s_values.append(s)
    return s_values

# Function to calculate V values
def calculate_v_values(s_values):
    total_s = sum(s_values)
    return [s / total_s for s in s_values]

# Function to execute WP method
def weighted_product_method(alternatives, weights, criteria_types):
    # Normalize the weights
    normalized_weights = normalize_weights(weights)

    # Calculate the S values for each alternative
    s_values = calculate_s_values(alternatives, normalized_weights, criteria_types)

    # Calculate the V values for each alternative
    v_values = calculate_v_values(s_values)

    return v_values

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_alternatives = int(request.form['num_alternatives'])
        num_criteria = int(request.form['num_criteria'])

        alternatives = []
        for i in range(num_alternatives):
            alt = []
            for j in range(num_criteria):
                value = float(request.form[f'alt_{i}_crit_{j}'])
                alt.append(value)
            alternatives.append(alt)

        weights = []
        for j in range(num_criteria):
            weight = float(request.form[f'weight_{j}'])
            weights.append(weight)

        criteria_types = []
        for j in range(num_criteria):
            criteria_type = request.form[f'type_{j}']
            criteria_types.append(criteria_type)

        v_values = weighted_product_method(alternatives, weights, criteria_types)

        return render_template('result.html', v_values=v_values, enumerate=enumerate)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
