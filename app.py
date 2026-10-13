from flask import Flask
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def home():
    df = pd.read_csv('final_report.csv')

    # Top 5
    top5 = df.sort_values(by='Average', ascending=False).head(5)
    top5_html = top5[['StudentID','Name','Department','Average','Grade']].to_html(classes='table table-bordered table-striped table-sm', index=False)

    # Department Wise Analytics
    dept_avg = df.groupby('Department')['Average'].mean().round(2).reset_index()
    dept_avg.columns = ['Department', 'Average Marks']
    dept_count = df['Department'].value_counts().reset_index()
    dept_count.columns = ['Department', 'Total Students']
    dept_merge = pd.merge(dept_count, dept_avg, on='Department')
    dept_html = dept_merge.to_html(classes='table table-bordered table-sm', index=False)

    # Subject Wise Analytics
    subjects = ['Math', 'Physics', 'Chemistry']
    sub_data = []
    for sub in subjects:
        if sub in df.columns:
            sub_data.append({
                'Subject': sub,
                'Average': round(df[sub].mean(), 2),
                'Highest': df[sub].max(),
                'Lowest': df[sub].min(),
                'Topper': df.loc[df[sub].idxmax(), 'Name']
            })
    sub_df = pd.DataFrame(sub_data)
    sub_html = sub_df.to_html(classes='table table-bordered table-sm', index=False)

    # Overall
    full_html = df.to_html(classes='table table-bordered table-striped table-sm', index=False)

    return f"""
    <html>
    <head>
        <title>Meenu | Python with AI Project</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body style="background:#f8f9fa">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
      <div class="container">
        <a class="navbar-brand" href="#">Meenu | MCA | Python with AI</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item"><a class="nav-link" href="#home">Home</a></li>
            <li class="nav-item"><a class="nav-link" href="#top">Top 5</a></li>
            <li class="nav-item"><a class="nav-link" href="#subject">Subject Wise</a></li>
            <li class="nav-item"><a class="nav-link" href="#dept">Department Wise</a></li>
            <li class="nav-item"><a class="nav-link" href="#report">Full Report</a></li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4">
        <section id="home" class="text-center py-4 bg-white rounded shadow-sm">
            <h3 class="text-primary">Student Performance Analytics</h3>
            <p>Developed by <b>Meenu</b> | MCA Student | Python with AI & Data Science</p>
            <div class="row text-center mt-3">
                <div class="col-4"><div class="card p-2">Total<br><b>{len(df)}</b></div></div>
                <div class="col-4"><div class="card p-2">Class Avg<br><b>{round(df['Average'].mean(),2)}%</b></div></div>
                <div class="col-4"><div class="card p-2">Topper<br><b>{top5.iloc[0]['Name']}</b></div></div>
            </div>
        </section>

        <section id="top" class="mt-4 card p-3 shadow-sm">
            <h5>🏆 Top 5 Performers</h5>
            <div class="table-responsive">{top5_html}</div>
        </section>

        <section id="subject" class="mt-4 card p-3 shadow-sm">
            <h5>📚 Subject Wise Analytics</h5>
            <p>Math, Physics, Chemistry - Average, Highest, Lowest</p>
            <div class="table-responsive">{sub_html}</div>
        </section>

        <section id="dept" class="mt-4 card p-3 shadow-sm">
            <h5>🏫 Department Wise Analytics</h5>
            <p>BCA vs BSc Performance Comparison</p>
            <div class="table-responsive">{dept_html}</div>
        </section>

        <section id="report" class="mt-4 card p-3 shadow-sm">
            <h5>📋 Complete Final Report - {len(df)} Students</h5>
            <div class="table-responsive">{full_html}</div>
        </section>

        <div class="mt-4 mb-5 text-center card p-3 bg-dark text-white">
            <p class="m-0">Project by Meenu | MCA | Python with AI Project</p>
            <p class="m-0" style="font-size:12px">Student Performance Analytics System</p>
        </div>
    </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
