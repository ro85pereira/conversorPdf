from flask import Flask, request, jsonify, send_file
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route("/dividir", methods=["POST"])
def dividir_pdf():
    # Verifica se veio arquivo
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["file"]
    intervalos = request.form.get("intervalos", "")

    if not intervalos:
        return jsonify({"erro": "Nenhum intervalo informado"}), 400

    # Lê o PDF enviado
    reader = PdfReader(arquivo)
    total_paginas = len(reader.pages)

    # Função para interpretar intervalos (ex: "1,3-5,8")
    def interpretar_intervalos(intervalos_str):
        paginas = []
        partes = intervalos_str.split(",")
        for parte in partes:
            if "-" in parte:
                inicio, fim = parte.split("-")
                inicio, fim = int(inicio), int(fim)
                paginas.extend(range(inicio, fim+1))
            else:
                paginas.append(int(parte))
        return paginas

    try:
        paginas_para_extrair = interpretar_intervalos(intervalos)
    except Exception:
        return jsonify({"erro": "Intervalos inválidos"}), 400

    # Cria novo PDF com as páginas escolhidas
    writer = PdfWriter()
    for num in paginas_para_extrair:
        if 1 <= num <= total_paginas:  # garante que a página existe
            writer.add_page(reader.pages[num-1])

    # Salva em memória
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    # Retorna o PDF gerado para download
    return send_file(output, as_attachment=True, download_name="resultado.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)