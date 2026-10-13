from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_csv('final_report.csv')
    top5 = df.sort_values(by='Average', ascending=False).head(5)
    top5_html = top5[['Student_ID','Name','Department','Average','Grade']].to_html(classes='table table-bordered table-striped', index=False)
    dept_avg = df.groupby('Department')['Average'].mean().round(2).reset_index()
    dept_html = dept_avg.to_html(classes='table table-bordered', index=False)
    subjects = ['Python', 'AI_ML', 'Data_Science']
    sub_rows = ""
    for sub in subjects:
        sub_rows += f"<tr><td>{sub}</td><td>{round(df[sub].mean(),2)}</td><td>{df[sub].max()}</td><td>{df[sub].min()}</td></tr>"

    return f"""
    <html><head>
    <title>Meenu | Python with AI Project</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </head><body style="background:#f8f9fa">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
      <div class="container">
        <a class="navbar-brand" href="#">Meenu | MCA</a>
        <div class="collapse navbar-collapse show" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="#dashboard">Dashboard</a></li>
            <li class="nav-item"><a class="nav-link" href="#top">Top 5</a></li>
            <li class="nav-item"><a class="nav-link" href="#analysis">Analysis</a></li>
            <li class="nav-item"><a class="nav-link" href="#report">Report</a></li>
            <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container mt-4">
        <section id="home" class="text-center py-4 bg-white rounded shadow-sm">
            <h2 class="text-primary">Student Performance Analytics</h2>
            <p>Python with AI & Data Science Project</p>
            <p><b>By Meenu | MCA Student</b></p>
        </section>
        <section id="dashboard" class="mt-4">
            <h5>📊 Dashboard Overview</h5>
            <div class="row text-center">
                <div class="col-6 col-md-3 mb-2"><div class="card p-2 shadow-sm">Total Students<br><h5>{len(df)}</h5></div></div>
                <div class="col-6 col-md-3 mb-2"><div class="card p-2 shadow-sm">Pass<br><h5>{len(df[df['Status']=='Pass'])}</h5></div></div>
                <div class="col-6 col-md-3 mb-2"><div class="card p-2 shadow-sm">Class Avg<br><h5>{round(df['Average'].mean(),2)}%</h5></div></div>
                <div class="col-6 col-md-3 mb-2"><div class="card p-2 shadow-sm">Topper<br><b>{top5.iloc[0]['Name']}</b><br>{top5.iloc[0]['Average']}%</div></div>
            </div>
        </section>
        <section id="top" class="mt-4 card p-3 shadow-sm"><h5>🏆 Top 5 Performers</h5>{top5_html}</section>
        <section id="analysis" class="mt-4 row">
            <div class="col-md-6 mb-3"><div class="card p-3 shadow-sm h-100"><h6>Subject-wise</h6><table class="table table-bordered table-sm"><tr><th>Subject</th><th>Avg</th><th>Max</th><th>Min</th></tr>{sub_rows}</table></div></div>
            <div class="col-md-6 mb-3"><div class="card p-3 shadow-sm h-100"><h6>Department-wise</h6>{dept_html}</div></div>
        </section>
        <section id="report" class="mt-4 card p-3 shadow-sm"><h5>📋 Final Report</h5><div class="table-responsive">{df.to_html(classes='table table-bordered table-striped table-sm', index=False)}</div></section>
        <section id="contact" class="mt-4 mb-5 text-center card p-3 bg-dark text-white"><h5>Contact</h5><p class="m-0">Project by <b>Meenu</b> | MCA | Python with AI</p></section>
    </div></body></html>
    """
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
