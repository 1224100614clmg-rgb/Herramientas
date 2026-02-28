"""
Controlador de Videos Educativos
Maneja las peticiones relacionadas con videos de YouTube
"""
from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from services.youtube_service import YouTubeService

# Crear Blueprint para videos
videos_bp = Blueprint('videos', __name__, url_prefix='/videos')

@videos_bp.route('/educativos')
def videos_educativos():
    """
    Muestra la página de videos educativos con búsqueda dinámica
    Solo accesible para alumnos autenticados
    """
    if 'usuario' not in session or session.get('rol') != 'alumno':
        return redirect(url_for('index'))
    
    # Obtener categorías disponibles
    categorias = YouTubeService.obtener_categorias_disponibles()
    
    # Videos iniciales (opcional, puedes dejarlo vacío)
    videos_iniciales = []
    
    return render_template(
        'videos_educativos.html',
        categorias=categorias,
        videos=videos_iniciales
    )

@videos_bp.route('/buscar', methods=['GET'])
def buscar_videos():
    """
    API REST: Búsqueda personalizada de videos
    Parámetros:
        - q: término de búsqueda
        - max: número máximo de resultados (default: 5)
    """
    if 'usuario' not in session or session.get('rol') != 'alumno':
        return jsonify({'error': 'No autorizado'}), 401
    
    query = request.args.get('q', '').strip()
    max_results = request.args.get('max', 5, type=int)
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Debes ingresar un término de búsqueda'
        }), 400
    
    if max_results > 20:
        max_results = 20  # Límite de seguridad
    
    try:
        videos = YouTubeService.buscar_videos(query, max_results)
        return jsonify({
            'success': True,
            'query': query,
            'total': len(videos),
            'videos': videos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al buscar videos: {str(e)}'
        }), 500

@videos_bp.route('/sugerencias/<categoria>')
def sugerencias_categoria(categoria):
    """
    API REST: Obtiene sugerencias de búsqueda para una categoría
    """
    if 'usuario' not in session or session.get('rol') != 'alumno':
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        sugerencias = YouTubeService.obtener_sugerencias_por_categoria(categoria)
        return jsonify({
            'success': True,
            'categoria': categoria,
            'sugerencias': sugerencias
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@videos_bp.route('/por-herramienta/<nombre>')
def videos_por_herramienta(nombre):
    """
    API REST: Busca videos relacionados con una herramienta específica
    """
    if 'usuario' not in session or session.get('rol') != 'alumno':
        return jsonify({'error': 'No autorizado'}), 401
    
    try:
        videos = YouTubeService.buscar_por_herramienta(nombre)
        return jsonify({
            'success': True,
            'herramienta': nombre,
            'total': len(videos),
            'videos': videos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500