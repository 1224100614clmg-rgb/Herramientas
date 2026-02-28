from flask import Blueprint, request, jsonify

mapa_bp = Blueprint("mapa", __name__)

@mapa_bp.route("/guardar_ubicacion", methods=["POST"])
def guardar_ubicacion():
    data = request.json

    lat = data.get("latitud")
    lng = data.get("longitud")

    return jsonify({
        "mensaje": "Ubicación recibida",
        "latitud": lat,
        "longitud": lng
    })