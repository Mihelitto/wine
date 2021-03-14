from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import date
import pandas

wine_df = pandas.read_excel("wine.xlsx")
wines = wine_df.to_dict(orient="Records")

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
years = date.today().year - 1920

render_page = template.render(years = years, wines=wines)

with open("index.html", "w", encoding="utf8") as f:
    f.write(render_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
