from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import sys
from flask_cors import CORS
from config import Config
from models.alumno_model import registrar_alumno, buscar_alumno_por_matricula, buscar_laboratorista
from models.herramienta_model import obtener_herramientas, agregar_herramienta, editar_herramienta, eliminar_herramienta, obtener_herramientas_disponibles

# ================= CREAR APP PRIMERO =================

app = Flask(__name__, template_folder="views/templates")
app.secret_key = 'tu_clave_secreta_aqui_cambiala_en_produccion'

# Configuración
app.config.from_object(Config)
CORS(app)

# ================= CONFIGURACIÓN BASE =================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# ================= IMPORTAR BLUEPRINTS =================

from controllers.mapa_controller import mapa_bp
from controllers.videos_controller import videos_bp
from controllers.pagos_controller import pagos_bp
from services.youtube_service import YouTubeService

app.register_blueprint(videos_bp)
app.register_blueprint(mapa_bp)
app.register_blueprint(pagos_bp)

# ================= "BASE DE DATOS" SIMULADA =================


herramientas_db = {
    1: {'nombre': 'Multímetro Digital', 'descripcion': 'Multímetro digital FLUKE 87V', 'cantidad_total': 10, 'cantidad_disponible': 10, 'categoria': 'Medición'},
    2: {'nombre': 'Osciloscopio', 'descripcion': 'Osciloscopio digital 100MHz', 'cantidad_total': 5, 'cantidad_disponible': 5, 'categoria': 'Medición'},
}

solicitudes_db = {}
solicitud_counter = 1
historial_db = []

# ================= RUTAS GENERALES =================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('index'))

    usuario    = request.form.get('usuario')
    contrasena = request.form.get('contrasena')

    # Verificar si es laboratorista
    lab = buscar_laboratorista(usuario)
    if lab and check_password_hash(lab['contrasena_hash'], contrasena):
        session['usuario'] = lab['usuario']
        session['nombre']  = lab['nombre_completo']
        session['rol']     = 'laboratorista'
        return redirect(url_for('dashboard_laboratorista'))

    # Verificar si es alumno
    alumno = buscar_alumno_por_matricula(usuario)
    if alumno and check_password_hash(alumno['contrasena_hash'], contrasena):
        session['usuario'] = alumno['matricula']
        session['nombre']  = alumno['nombre_completo']
        session['rol']     = 'alumno'
        return redirect(url_for('dashboard_alumno'))

    return redirect(url_for('index', error='credenciales'))

# ================= DASHBOARD ALUMNO =================

@app.route("/dashboard-alumno")
def dashboard_alumno():
    if 'usuario' not in session or session.get('rol') != 'alumno':
        return redirect(url_for('index'))

    mis_solicitudes = {k: v for k, v in solicitudes_db.items() if v['alumno_id'] == session['usuario']}

    return render_template(
        "dashboard_alumno.html",
        usuario=session['nombre'],
        solicitudes=mis_solicitudes
    )

# ================= SOLICITAR HERRAMIENTA =================

@app.route("/solicitar-herramienta", methods=['GET', 'POST'])
def solicitar_herramienta():
    if 'usuario' not in session or session.get('rol') != 'alumno':
        return redirect(url_for('index'))

    global solicitud_counter

    if request.method == 'POST':
        import json

        herramientas_json = request.form.get('herramientas_json')
        grupo = request.form.get('grupo')
        fecha_solicitud = request.form.get('fecha_solicitud')

        if not herramientas_json or not grupo or not fecha_solicitud:
            flash('Por favor complete todos los campos', 'error')
            return redirect(url_for('solicitar_herramienta'))

        try:
            herramientas = json.loads(herramientas_json)
        except:
            flash('Error al procesar las herramientas', 'error')
            return redirect(url_for('solicitar_herramienta'))

        for herramienta_item in herramientas:
            herramienta_id = int(herramienta_item['id'])
            cantidad = int(herramienta_item['cantidad'])

            if herramienta_id not in herramientas_db:
                continue

            herramienta = herramientas_db[herramienta_id]

            if cantidad > herramienta['cantidad_disponible']:
                flash(f'No hay suficiente stock de {herramienta["nombre"]}', 'error')
                continue

            solicitudes_db[solicitud_counter] = {
                'alumno_id': session['usuario'],
                'alumno_nombre': session['nombre'],
                'grupo': grupo,
                'herramienta_id': herramienta_id,
                'herramienta_nombre': herramienta['nombre'],
                'cantidad': cantidad,
                'fecha_solicitud': fecha_solicitud + ' ' + datetime.now().strftime('%H:%M:%S'),
                'estado': 'Pendiente',
                'laboratorista': None,
                'fecha_entrega': None,
                'fecha_devolucion': None
            }

            solicitud_counter += 1

        flash('Solicitud enviada correctamente', 'success')
        return redirect(url_for('dashboard_alumno'))

    herramientas_disponibles = obtener_herramientas_disponibles()
    return render_template("solicitar_herramienta.html", herramientas=herramientas_disponibles)

# ================= DASHBOARD LABORATORISTA =================

@app.route("/dashboard-laboratorista")
def dashboard_laboratorista():
    if 'usuario' not in session or session.get('rol') != 'laboratorista':
        return redirect(url_for('index'))

    solicitudes_pendientes = len([s for s in solicitudes_db.values() if s['estado'] == 'Pendiente'])
    prestamos_activos = len([s for s in solicitudes_db.values() if s['estado'] == 'Aprobado'])
    total_herramientas = len(herramientas_db)

    return render_template(
        "dashboard_laboratorista.html",
        usuario=session['nombre'],
        solicitudes_pendientes=solicitudes_pendientes,
        prestamos_activos=prestamos_activos,
        total_herramientas=total_herramientas
    )

# ================= OTRAS VISTAS =================

@app.route("/validar-solicitudes")
def validar_solicitudes():
    return render_template("validar_solicitudes.html")

@app.route("/prestamos-activos")
def prestamos_activos():
    return render_template("prestamos_activos.html")

@app.route("/inventario", methods=['GET', 'POST'])
def inventario():
    if 'usuario' not in session or session.get('rol') != 'laboratorista':
        return redirect(url_for('index'))

    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'agregar':
            resultado = agregar_herramienta(
                request.form.get('codigo'),
                request.form.get('nombre'),
                request.form.get('descripcion'),
                request.form.get('categoria'),
                int(request.form.get('cantidad_total'))
            )
            flash('Herramienta agregada correctamente' if resultado['ok'] else f'Error: {resultado["error"]}')

        elif accion == 'editar':
            resultado = editar_herramienta(
                int(request.form.get('id_herramienta')),
                request.form.get('codigo'),
                request.form.get('nombre'),
                request.form.get('descripcion'),
                request.form.get('categoria'),
                int(request.form.get('cantidad_total'))
            )
            flash('Herramienta actualizada' if resultado['ok'] else f'Error: {resultado["error"]}')

        elif accion == 'eliminar':
            resultado = eliminar_herramienta(int(request.form.get('id_herramienta')))
            flash('Herramienta eliminada' if resultado['ok'] else f'Error: {resultado["error"]}')

        return redirect(url_for('inventario'))

    herramientas = obtener_herramientas()
    return render_template("inventario.html", herramientas=herramientas)


@app.route("/historial")
def historial():
    return render_template("historial.html")

@app.route("/mapa")
def mapa():
    return render_template("mapa.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    # Recoger datos del formulario
    matricula        = request.form.get('numero_control')
    nombre_completo  = request.form.get('nombre_completo')
    correo           = request.form.get('correo')
    carrera          = request.form.get('carrera')
    contrasena       = request.form.get('contrasena')
    confirmar        = request.form.get('confirmar_contrasena')

    # Validaciones básicas
    if contrasena != confirmar:
        return render_template('register.html', error="Las contraseñas no coinciden")
    
    if buscar_alumno_por_matricula(matricula):
        return render_template('register.html', error="Esa matrícula ya está registrada")

    resultado = registrar_alumno(matricula, nombre_completo, correo, carrera, contrasena)
    
    if resultado["ok"]:
        return redirect(url_for('index'))  # o a login
    else:
        return render_template('register.html', error=f"Error: {resultado['error']}")

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgot_password.html")

@app.route('/mis-solicitudes')
def mis_solicitudes():
    return render_template('mis_solicitudes.html')


# ================= TEST API PARA POSTMAN =================

@app.route("/api/test-db", methods=["GET"])
def test_db():
    return {
        "status": "success",
        "message": "API funcionando correctamente",
        "proyecto": "Sistema de Gestión de Herramientas"
    }, 200

# ================= MAIN =================

if __name__ == "__main__":
    app.run(debug=True)
