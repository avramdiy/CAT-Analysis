from flask import Flask, render_template_string
import pandas as pd

app = Flask(__name__)

# Load master dataframe once, drop OpenInt, and define 3 time slices
file_path = r"C:\Users\avram\OneDrive\Desktop\TRG Week 32\cat.us.txt"
df_master = pd.read_csv(file_path, sep=",", engine="python", parse_dates=['Date'], infer_datetime_format=True)

# Drop OpenInt if it exists
if 'OpenInt' in df_master.columns:
    df_master = df_master.drop(columns=['OpenInt'])

# Create filtered DataFrames
df_70s = df_master[(df_master['Date'] >= '1970-01-01') & (df_master['Date'] <= '1979-12-31')]
df_80s_90s = df_master[(df_master['Date'] >= '1980-01-01') & (df_master['Date'] <= '1999-12-31')]
df_2000s = df_master[(df_master['Date'] >= '2000-01-01') & (df_master['Date'] <= '2017-11-10')]

def render_html(title, df):
    html_table = df.to_html(classes='table table-striped', index=False)
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="mb-4">{title}</h1>
            {html_table}
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/cat_1970s')
def show_1970s():
    return render_html("Caterpillar Inc. (CAT) - 1970s", df_70s)

@app.route('/cat_80s_90s')
def show_80s_90s():
    return render_html("Caterpillar Inc. (CAT) - 1980s to 1990s", df_80s_90s)

@app.route('/cat_2000s')
def show_2000s():
    return render_html("Caterpillar Inc. (CAT) - 2000 to 2017", df_2000s)

if __name__ == '__main__':
    app.run(debug=True)
