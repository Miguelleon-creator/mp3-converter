from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os
import threading
import time

app = Flask(__name__)

def delete_file_later(path, delay=120):
    def delete():
        time.sleep(delay)
        try:
            os.remove(path)
            print(f"Deleted file: {path}")
        except Exception as e:
            print(f"Error deleting file {path}: {e}")
    threading.Thread(target=delete).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert")
def convert():
    video_url = request.args.get("url")
    if not video_url:
        return "Missing URL", 400

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'nocheckcertificate': True,
        'youtube_include_dash_manifest': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            print("Download video title:", info.get('title'))

            base_path = os.path.splitext(ydl.prepare_filename(info))[0]
            mp3_filename = os.path.basename(base_path + ".mp3")
    except Exception as e:
        print("Error:", e)
        return "Conversion Failed", 500

    # Borrar el archivo después de 2 minutos
    delete_file_later(os.path.join("downloads", mp3_filename), delay=120)

    return send_from_directory('downloads', mp3_filename, as_attachment=True)

if __name__ == "__main__":
    print("Loading server Flask...")
    app.run(debug=True)

# Nota importante sobre el nombre del archivo descargado:
# 
# Inicialmente se intentó usar un nombre generado manualmente con UUID para guardar el archivo,
# pero yt_dlp no guarda el archivo con ese nombre, sino que usa su propio patrón basado en el ID del video.
#
# Por eso, si se envía a Flask un archivo con nombre UUID, Flask no lo encuentra y da error FileNotFoundError.
#
# La solución es:
# 1) Usar en ydl_opts el patrón de nombre ('outtmpl') que yt_dlp usará para guardar el archivo, por ejemplo 'downloads/%(id)s.%(ext)s'.
# 2) Luego, obtener el nombre real del archivo descargado con ydl.prepare_filename(info), que devuelve la ruta y nombre con extensión original.
# 3) Cambiar la extensión a '.mp3' porque el postprocesador convierte el archivo a mp3.
# 4) Finalmente, usar ese nombre exacto para enviar el archivo con Flask.
#
# Así garantizamos que Flask enviará un archivo que realmente existe, evitando el error.