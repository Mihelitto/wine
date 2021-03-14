from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas as pd

excel_data_df = pd.read_excel("wine3.xlsx", keep_default_na=False, index_col=0)
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

render_page = template.render(years=years, drinks=drinks)

with open("index.html", "w", encoding="utf8") as file:
    file.write(render_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
