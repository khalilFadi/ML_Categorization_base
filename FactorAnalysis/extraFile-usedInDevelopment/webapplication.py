from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML_TEMPLATE = '''
<!doctype html>
<html>
<head><title>Run Program</title></head>
<body>
    <h1>Run Program</h1>
    <form action="/run" method="post" enctype="multipart/form-data">
        <label for="file">Select file:</label>
        <input type="file" name="file" required><br><br>
        <label for="var1">Variable 1:</label>
        <input type="number" name="var1" step="any" required><br><br>
        <label for="var2">Variable 2:</label>
        <input type="number" name="var2" step="any" required><br><br>
        <input type="submit" value="Run">
    </form>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/run', methods=['POST'])
def run():
    file = request.files['file']
    var1 = float(request.form['var1'])
    var2 = float(request.form['var2'])
    
    # Save the file and process it
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    # Replace this with your actual processing code
    return f"Running program on {file_path} with variables {var1} and {var2}"

if __name__ == '__main__':
    app.run(debug=True)
