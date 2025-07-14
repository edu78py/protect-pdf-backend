from flask import Flask, request, send_file
from flask_cors import CORS
from pypdf import PdfReader, PdfWriter, Permissions
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/proteger", methods=["POST"])
def proteger():
    try:
        archivo = request.files["file"]
        reader = PdfReader(archivo)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        # Aplica protección: deniega todo (modificar, copiar, imprimir, etc.)
        writer.encrypt(
            user_password="",
            owner_password="1234",
            permissions_flag=0
        )

        output = BytesIO()
        writer.write(output)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="protegido.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return f"Error al proteger PDF: {str(e)}", 500

# Opcional: health check
@app.route("/")
def home():
    return "Backend de protección PDF activo"
