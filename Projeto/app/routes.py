from flask import Flask, request, send_file
import os
import zipfile
import shutil
from ultralytics import YOLO
import tempfile


from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
app = Flask(__name__)

# Carregar o modelo YOLOv8 (certifique-se de que o modelo já está treinado e salvo em algum lugar)
model = YOLO('C:/Users/oliveira/Music/Cimas_Constructions_Patologies_2-main/Projeto/best.pt')

@app.route('/upload-folder', methods=['POST'])
@app.route('/upload-folder', methods=['POST'])
def upload_folder():
    # Cria um diretório temporário para armazenar os arquivos recebidos
    temp_dir = tempfile.mkdtemp()

    # Recebe os arquivos da pasta
    if 'images' not in request.files:
        return "No files part", 400

    files = request.files.getlist('images')

    # Salva as imagens no diretório temporário
    for file in files:
        file.save(os.path.join(temp_dir, file.filename))

    # Processa as imagens com o modelo YOLOv8 e salva as predições
    output_dir = tempfile.mkdtemp()  # Diretório temporário para salvar as imagens com predições

    for file in files:
        img_path = os.path.join(temp_dir, file.filename)

        # Realiza a predição com o modelo YOLOv8
        results = model.predict(img_path)

        # Salva a imagem predita no diretório de saída
        results[0].save(save_dir=output_dir)

    # Verifica se os arquivos foram realmente salvos
    print("Arquivos em output_dir:", os.listdir(output_dir))

    # Compacta a pasta com as imagens preditas em um arquivo zip
    zip_path = tempfile.mktemp(suffix='.zip')
    shutil.make_archive(zip_path.replace('.zip', ''), 'zip', root_dir=output_dir)

    # Remove os diretórios temporários
    shutil.rmtree(temp_dir)
    shutil.rmtree(output_dir)

    # Retorna o arquivo zip para o cliente
    return send_file(zip_path, as_attachment=True, download_name="predicted_images.zip")
