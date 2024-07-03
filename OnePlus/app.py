from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sales')
def sales():
    return render_template('sales.html')

@app.route('/economic')
def economic():
    return render_template('economic.html')

@app.route('/sales_analysis', methods=['POST'])
def sales_analysis():
    oneplus_data = request.form['oneplus_data']
    oneplus_values = list(map(int, oneplus_data.split(',')))

    bbk_data = request.form['bbk_data']
    bbk_values = list(map(int, bbk_data.split(',')))

    # Perform your sales data analysis here
    # Example calculations:
    mx = sum(oneplus_values) / len(oneplus_values)
    my = sum(bbk_values) / len(bbk_values)

    squared_diff_x = sum((xi - mx) ** 2 for xi in oneplus_values)
    sigma_x = (squared_diff_x / len(oneplus_values)) ** 0.5

    squared_diff_y = sum((yi - my) ** 2 for yi in bbk_values)
    sample_sigma_y = (squared_diff_y / len(bbk_values)) ** 0.5

    covariance = sum((xi - mx) * (yi - my) for xi, yi in zip(oneplus_values, bbk_values)) / (len(oneplus_values)-1)

    correlation_coefficient = covariance / (sigma_x * sample_sigma_y)

    if 0.75 <= abs(correlation_coefficient) <= 1:
        relationship = "Strong and Positive"
    elif 0.5 <= abs(correlation_coefficient) < 0.75:
        relationship = "Moderate and Positive"
    elif 0.25 <= abs(correlation_coefficient) < 0.5:
        relationship = "Weak and Positive"
    elif -0.25 <= correlation_coefficient <= 0.25:
        relationship = "Absence of Linear Relationship"
    elif -0.5 <= correlation_coefficient < -0.25:
        relationship = "Weak and Negative"
    elif -0.75 <= correlation_coefficient < -0.5:
        relationship = "Moderate and Negative"
    else:
        relationship = "Strong and Negative"

    results = {
        "sigma_x": sigma_x,
        "sample_sigma_y": sample_sigma_y,
        "covariance": covariance,
        "correlation_coefficient": correlation_coefficient,
        "relationship": relationship
    }

    return render_template('sales_results.html', results=results)

@app.route('/economic_analysis', methods=['POST'])
def economic_analysis():
    economic_data_good = request.form['economic_data_good']
    economic_data_poor = request.form['economic_data_poor']

    economic_data_good_values = list(map(int, economic_data_good.split(',')))
    economic_data_poor_values = list(map(int, economic_data_poor.split(',')))

    a, b, c, d = economic_data_good_values
    e, f, g, h = economic_data_poor_values

    total_students_good = a + b + c + d
    total_students_poor = e + f + g + h
    total_students = total_students_good + total_students_poor

    proportion_dull = (c + g) / total_students
    proportion_total_poor = (e + f + g + h) / total_students
    proportion_good_borderline = d / total_students_good
    percentage_bright_poor = (e / (a + e)) * 100
    percentage_average_good = (b / (b + f)) * 100

    results = {
        "proportion_dull": proportion_dull,
        "proportion_total_poor": proportion_total_poor,
        "proportion_good_borderline": proportion_good_borderline,
        "percentage_bright_poor": percentage_bright_poor,
        "percentage_average_good": percentage_average_good
    }

    return render_template('economic_results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
