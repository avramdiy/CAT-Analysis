from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

@app.route('/')
def load_dataframe():
    file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 32\cat.us.txt"
    try:
        df = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)

        html_table = df.to_html(classes='table table-striped', index=False)

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Caterpillar Inc. (CAT) Data</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="mb-4">Caterpillar Inc. (CAT) - Raw Data</h1>
                {html_table}
            </div>
        </body>
        </html>
        """
        return render_template_string(html_template)

    except Exception as e:
        return f"An error occurred while processing the file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
