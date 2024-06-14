#---Take data from MSSQL and update on web---
from flask import Flask, request, render_template
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.orm import Session
import webbrowser

app = Flask(__name__)

# Kết nối đến SQL Server
DATABASE_URI = r'mssql+pyodbc://@LAPTOP-073BBS08\SQLEXPRESS/ITconferences?driver=SQL+Server+Native+Client+11.0'
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Reflect lại bảng từ cơ sở dữ liệu
metadata.reflect(bind=engine)
conferences = Table('Conferences', metadata, autoload_with=engine)

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '').strip().lower()
    with Session(engine) as session:
        stmt = select(conferences).where(
            conferences.c.Name_Conference.ilike(f'%{search_query}%') |
            conferences.c.Place.ilike(f'%{search_query}%')
        )
        result = session.execute(stmt).fetchall()
    return render_template('index.html', conferences=result)


def start_the_web():
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run(debug=True)