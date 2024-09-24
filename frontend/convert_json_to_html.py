import json
from jinja2 import Template

# Load the JSON data
with open('trivy-report.json') as json_file:
    data = json.load(json_file)

# Define a simple HTML template
html_template = """
<html>
<head>
    <title>Trivy Report</title>
</head>
<body>
    <h1>Trivy Vulnerability Report</h1>
    <ul>
    {% for vulnerability in data['Results'][0]['Vulnerabilities'] %}
        <li>{{ vulnerability['VulnerabilityID'] }} - {{ vulnerability['Title'] }}</li>
    {% endfor %}
    </ul>
</body>
</html>
"""

# Create the HTML report
template = Template(html_template)
html_content = template.render(data=data)

# Save the HTML output
with open('trivy-report.html', 'w') as html_file:
    html_file.write(html_content)
