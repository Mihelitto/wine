import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
if os.getenv("DATA_FILE"):
    DATA_FILE = os.getenv("DATA_FILE")
else:
    DATA_FILE = "wine.xlsx"

excel_data_df = pd.read_excel(DATA_FILE, keep_default_na=False, index_col=0)
categories = sorted(list(set(excel_data_df.index.to_list())))
drinks = dict()
for category in categories:
    drinks[category] = excel_data_df.loc[category].to_dict(orient="records")

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
years = date.today().year - 1920
if 10 < years / 100 < 20:
    years = str(years) + " лет"
elif years % 100 == 1:
    years = str(years) + " год"
elif 1 < years % 100 < 5:
    years = str(years) + " годa"

render_page = template.render(years=years, drinks=drinks)

with open("index.html", "w", encoding="utf8") as file:
    file.write(render_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
