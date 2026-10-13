from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    try:
        # File check
        if not os.path.exists('final_report.csv'):
            return "<h3>Error: final_report.csv file GitHub pe nahi hai! Please upload karo.</h3>"

        df = pd.read_csv('final_report.csv')

        # Safe Top 5
        top5 = df.sort_values(by='Average', ascending=False).head(5)
        top5_html = top5[['Student_ID','Name','Department','Average','Grade']].to_html(classes='table table-bordered table-striped', index=False)

        # Department Average
        dept_avg = df.groupby('Department')['Average'].mean().round(2).reset_index()
        dept_html = dept_avg.to_html(classes='table table-bordered', index=False)

        subjects = ['Python', 'AI_ML', 'Data_Science']
        sub_rows = ""
        for sub in subjects:
            if sub in df.columns:
                sub_rows += f"<tr><td>{sub}</td><td>{round(df[sub].mean(),2)}</td><td>{df[sub].max()}</td><td>{df[sub].min()}</td></tr>"

    except Exception as e:
        return f"<h3>Error in Code: {str(e)}</h3><p>Please check final_report.csv columns</p>"

    return f"""
    <html><head>
    <title>Meenu | Python with AI Project</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head><body style="background:#f8f9fa">
    <nav class="navbar navbar-dark bg-dark"><div class="container"><a class="navbar-brand" href="#">Meenu | MCA | Python with AI</a></div></nav>
    <div class="container mt-4">
        <div class="text-center py-4 bg-white rounded shadow-sm">
            <h3 class="text-primary">Student Performance Analytics</h3>
            <p>By <b>Meenu | MCA Student</b> | Python with AI Project</p>
        </div>
        <div class="mt-4 card p-3 shadow-sm"><h5>🏆 Top 5 Performers</h5>{top5_html}</div>
        <div class="mt-4 row">
            <div class="col-md-6 mb-3"><div class="card p-3 h-100"><h6>Subject-wise</h6><table class="table table-bordered table-sm"><tr><th>Subject</th><th>Avg</th><th>Max</th><th>Min</th></tr>{sub_rows}</table></div></div>
            <div class="col-md-6 mb-3"><div class="card p-3 h-100"><h6>Department-wise</h6>{dept_html}<p class="mt-2">✅ Pass: {len(df[df['Status']=='Pass'])} | ❌ Fail: {len(df[df['Status']=='Fail'])}</p></div></div>
        </div>
        <div class="mt-4 card p-3 shadow-sm"><h5>📋 Final Report</h5><div class="table-responsive">{df.to_html(classes='table table-bordered table-striped table-sm', index=False)}</div></div>
        <div class="mt-4 mb-5 text-center card p-3 bg-dark text-white"><p class="m-0">Project by <b>Meenu</b> | MCA | Python with AI</p></div>
    </div></body></html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
