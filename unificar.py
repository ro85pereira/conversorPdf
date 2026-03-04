from flask import Flask, request, jsonify, send_file
from PyPDF2 import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def unificar_pdf():
    # Verifica se vieram arquivos
    if not request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400

    # Cria um writer para juntar os PDFs
    writer = PdfWriter()
    nomes_recebidos = []

    # Itera sobre os arquivos enviados na ordem
    for key in sorted(request.files.keys()):
        file = request.files[key]
        nomes_recebidos.append(file.filename)

        # Lê cada PDF
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)

    # Salva o PDF combinado em memória
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    # Retorna o PDF unificado para download
    return send_file(
        output,
        as_attachment=True,
        download_name="unificado.pdf",
        mimetype="application/pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)