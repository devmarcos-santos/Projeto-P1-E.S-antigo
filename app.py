import csv
import os

from flask import Flask, render_template

app = Flask(__name__)

CSV_IMOVEIS = os.path.join(app.root_path, "data", "imoveis.csv")


def carregar_imoveis():
  if not os.path.exists(CSV_IMOVEIS):
    return []
  with open(CSV_IMOVEIS, newline="", encoding="utf-8") as arquivo:
    return list(csv.DictReader(arquivo))


def carregar_destaques(limite=4):
  destaques = [i for i in carregar_imoveis() if i["destaque"].strip().lower() == "sim"]
  return destaques[:limite]


@app.template_filter("reais")
def formatar_reais(valor):
  numero = f"{float(valor):,.0f}".replace(",", ".")
  return f"R$ {numero}"


@app.route("/")
def index():
  return render_template("index.html", destaques=carregar_destaques())


if __name__ == "__main__":
  app.run(debug=True)
