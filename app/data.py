from flask import Flask, render_template_string, Response
import pandas as pd
import matplotlib.pyplot as plt
import io

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

@app.route('/cat_1970s_yearly_agg')
def cat_1970s_yearly_agg():
    try:
        # Ensure 'Date' is datetime and extract year
        df = df_70s.copy()
        df['Year'] = df['Date'].dt.year

        # Group by year and calculate average of OHLC
        yearly_avg = df.groupby('Year')[['Open', 'High', 'Low', 'Close']].mean()

        # Plot
        plt.figure(figsize=(12, 6))
        for col in ['Open', 'High', 'Low', 'Close']:
            plt.plot(yearly_avg.index, yearly_avg[col], marker='o', label=col)

        plt.title("Caterpillar Inc. (CAT) — Yearly Average OHLC (1970s)", fontsize=16)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Average Price", fontsize=12)
        plt.legend()
        plt.grid(True)

        # Stream plot to PNG response
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return Response(buf, mimetype='image/png')

    except Exception as e:
        return f"An error occurred while generating the plot: {e}"

@app.route('/cat_2000s_yearly_agg')
def cat_1980s_1990s_yearly_agg():
    try:
        # Ensure 'Date' is datetime and extract year
        df = df_2000s.copy()
        df['Year'] = df['Date'].dt.year

        # Group by year and calculate average of OHLC
        yearly_avg = df.groupby('Year')[['Open', 'High', 'Low', 'Close']].mean()

        # Plot
        plt.figure(figsize=(12, 6))
        for col in ['Open', 'High', 'Low', 'Close']:
            plt.plot(yearly_avg.index, yearly_avg[col], marker='o', label=col)

        plt.title("Caterpillar Inc. (CAT) — Yearly Average OHLC (2000s)", fontsize=16)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Average Price", fontsize=12)
        plt.legend()
        plt.grid(True)

        # Stream plot to PNG response
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return Response(buf, mimetype='image/png')

    except Exception as e:
        return f"An error occurred while generating the plot: {e}"
    
@app.route('/cat_1980s-1990s_yearly_agg')
def cat_1980s_1990s_yearly_agg():
    try:
        # Ensure 'Date' is datetime and extract year
        df = df_80s_90s.copy()
        df['Year'] = df['Date'].dt.year

        # Group by year and calculate average of OHLC
        yearly_avg = df.groupby('Year')[['Open', 'High', 'Low', 'Close']].mean()

        # Plot
        plt.figure(figsize=(12, 6))
        for col in ['Open', 'High', 'Low', 'Close']:
            plt.plot(yearly_avg.index, yearly_avg[col], marker='o', label=col)

        plt.title("Caterpillar Inc. (CAT) — Yearly Average OHLC (1970s)", fontsize=16)
        plt.xlabel("Year", fontsize=12)
        plt.ylabel("Average Price", fontsize=12)
        plt.legend()
        plt.grid(True)

        # Stream plot to PNG response
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return Response(buf, mimetype='image/png')

    except Exception as e:
        return f"An error occurred while generating the plot: {e}"

if __name__ == '__main__':
    app.run(debug=True)
