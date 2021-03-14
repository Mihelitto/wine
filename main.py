from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas

excel_data_df = pandas.read_excel("wine2.xlsx", keep_default_na=False, index_col=0)
categories = list(set(excel_data_df.index.to_list()))
wines = dict()
for cat in categories:
    wines[cat] = excel_data_df.loc[cat].to_dict(orient="records")

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
years = date.today().year - 1920

render_page = template.render(years=years, wines=wines)

with open("index.html", "w", encoding="utf8") as f:
    f.write(render_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
