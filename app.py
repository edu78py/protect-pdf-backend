from flask import Flask, request, send_file
from flask_cors import CORS
from pypdf import PdfReader, PdfWriter
import io

app = Flask(__name__)
CORS(app)

@app.route('/proteger', methods=['POST'])
def proteger():
    file = request.files.get('file')
    if not file:
        return {'error': 'Archivo no recibido'}, 400

    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(user_password="", owner_password="1234", permissions={"modify": False, "copy": False})

    output = io.BytesIO()
    writer.write(output)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name="protegido.pdf", mimetype="application/pdf")

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/proteger', methods=['POST'])
def proteger():
    print("📥 Petición recibida en /proteger")

    file = request.files.get('file')
    if not file:
        print("⚠️ No se recibió ningún archivo.")
        return {'error': 'Archivo no recibido'}, 400

    print(f"✔️ Archivo recibido: {file.filename}")
    ...
