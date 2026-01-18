from flask import Flask, render_template_string, request
import re

app = Flask(__name__)


HTML_TEMPLATE = """
<!doctype html>
<title>Simple Regex Clone</title>
<h1>Regex Matcher</h1>
<form method="post">
    <label>Regex Pattern:</label><br>
    <input type="text" name="regex" value="{{ request.form.get('regex', '') }}" required><br><br>
    
    <label>Test String:</label><br>
    <textarea name="test_string" rows="5" cols="40">{{ request.form.get('test_string', '') }}</textarea><br><br>
    
    <button type="submit">Submit</button>
</form>

{% if matches is not none %}
    <hr>
    {% if error %}
        <p style="color:red;"><strong>Error:</strong> {{ error }}</p>
    {% else %}
        <h3>Found {{ count }} matches:</h3>
        <ul>
            {% for match in matches %}
                <li>{{ match }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    matches = None
    count = 0
    error = None
    
    if request.method == 'POST':
        regex = request.form.get('regex')
        text = request.form.get('test_string')
        try:
            matches = [m.group() for m in re.finditer(regex, text)]
            count = len(matches)
        except Exception as e:
            error = str(e)

    return render_template_string(HTML_TEMPLATE, matches=matches, count=count, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5000)