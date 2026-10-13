from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Check if CSV file exists
        if not os.path.exists('final_report.csv'):
            return "<h3>Error: final_report.csv not found in repository</h3>"

        df = pd.read_csv('final_report.csv')
        columns = df.columns.tolist()

        # Find average column automatically
        avg_col = None
        for col in columns:
            if 'average' in col.lower() or 'avg' in col.lower() or 'total' in col.lower():
                avg_col = col
                break
        if not avg_col:
            avg_col = columns[-1]

        # Top 5 Students
        top5 = df.sort_values(by=avg_col, ascending=False).head(5)
        top5_html = top5.to_html(classes='table table-bordered table-striped table-sm', index=False)

        # Full Report
        full_html = df.to_html(classes='table table-bordered table-striped table-sm', index=False)

    except Exception as e:
        return f"<h3>Application Error: {str(e)}</h3><p>Please check CSV file</p>"

    # HTML Template
    return f"""
    <html>
    <head>
        <title>Meenu | Python with AI Project</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body style="background:#f8f9fa">
        <nav class="navbar navbar-dark bg-dark sticky-top">
            <div class="container">
                <a class="navbar-brand" href="#">Meenu | MCA | Python with AI Project</a>
            </div>
        </nav>

        <div class="container mt-4">
            <div class="text-center py-4 bg-white rounded shadow-sm">
                <h3 class="text-primary">Student Performance Analytics</h3>
                <p>Developed by <b>Meenu</b> | MCA Student</p>
                <p>Project: Python with AI & Data Science</p>
            </div>

            <div class="mt-4 card p-3 shadow-sm">
                <h5>Top 5 Performers - Sorted by {avg_col}</h5>
                <div class="table-responsive">{top5_html}</div>
            </div>

            <div class="mt-4 card p-3 shadow-sm">
                <h5>Complete Final Report - Total Students: {len(df)}</h5>
                <div class="table-responsive">{full_html}</div>
            </div>

            <div class="mt-4 mb-5 text-center card p-3 bg-dark text-white">
                <p class="m-0">Project by Meenu | MCA | Python with AI</p>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
