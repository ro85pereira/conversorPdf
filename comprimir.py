from flask import Flask, request, jsonify, send_file
import io
import pikepdf

app = Flask(__name__)

@app.route("/comprimir", methods=["POST"])
def comprimir_pdf():
    # Verifica se veio arquivo
    if "file" not in request.files:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    arquivo = request.files["file"]

    try:
        # Abre o PDF com pikepdf
        pdf = pikepdf.open(arquivo)

        # Cria um novo PDF comprimido
        output = io.BytesIO()
        pdf.save(output, optimize_version=True)  # aplica otimização/compressão
        output.seek(0)

        # Retorna o PDF comprimido para download
        return send_file(
            output,
            as_attachment=True,
            download_name="comprimido.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return jsonify({"erro": f"Falha ao comprimir: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)

    