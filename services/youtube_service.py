"""
Servicio de YouTube API para búsquedas dinámicas
Búsquedas relacionadas con herramientas de laboratorio
"""
import requests
from typing import List, Dict, Optional

class YouTubeService:
    """Servicio para obtener videos de YouTube mediante API REST"""
    
    # API Key de YouTube Data API v3
    API_KEY = "AIzaSyA_mVc_IHE8-KhdlDlPfWDlZWj30byM2XA"
    BASE_URL = "https://www.googleapis.com/youtube/v3/search"
    
    # Categorías sugeridas relacionadas con herramientas
    CATEGORIAS_SUGERIDAS = {
        'seguridad': [
            'seguridad en laboratorio de electrónica',
            'normas de seguridad en taller',
            'uso seguro de herramientas eléctricas'
        ],
        'medicion': [
            'cómo usar multímetro tutorial',
            'uso de osciloscopio básico',
            'instrumentos de medición eléctrica'
        ],
        'soldadura': [
            'técnicas de soldadura con cautín',
            'soldadura electrónica tutorial',
            'cómo soldar componentes'
        ],
        'herramientas': [
            'herramientas básicas de electrónica',
            'uso de protoboard tutorial',
            'herramientas de laboratorio'
        ],
        'mantenimiento': [
            'mantenimiento de herramientas',
            'limpieza de equipos de laboratorio',
            'cuidado de instrumentos de medición'
        ]
    }
    
    @staticmethod
    def buscar_videos(query: str, max_results: int = 5, filtros: Optional[Dict] = None) -> List[Dict]:
        """
        Busca videos en YouTube usando la API REST
        
        Args:
            query: Término de búsqueda del usuario
            max_results: Número máximo de resultados
            filtros: Filtros adicionales (duración, idioma, etc.)
            
        Returns:
            Lista de diccionarios con información de videos
        """
        try:
            # Agregar contexto de herramientas a la búsqueda
            query_mejorada = f"{query} herramientas laboratorio tutorial"
            
            params = {
                'part': 'snippet',
                'q': query_mejorada,
                'key': YouTubeService.API_KEY,
                'maxResults': max_results,
                'type': 'video',
                'videoDuration': filtros.get('duracion', 'medium') if filtros else 'medium',
                'relevanceLanguage': 'es',
                'safeSearch': 'strict',
                'order': 'relevance'
            }
            
            response = requests.get(YouTubeService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for item in data.get('items', []):
                video = {
                    'youtube_id': item['id']['videoId'],
                    'titulo': item['snippet']['title'],
                    'descripcion': item['snippet']['description'][:200] + '...' if len(item['snippet']['description']) > 200 else item['snippet']['description'],
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'thumbnail_high': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                    'canal': item['snippet']['channelTitle'],
                    'fecha_publicacion': item['snippet']['publishedAt'][:10],
                    'url_watch': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'url_embed': f"https://www.youtube.com/embed/{item['id']['videoId']}"
                }
                videos.append(video)
            
            return videos
            
        except requests.exceptions.RequestException as e:
            print(f"Error al consultar YouTube API: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []
    
    @staticmethod
    def obtener_sugerencias_por_categoria(categoria: str) -> List[str]:
        """
        Obtiene búsquedas sugeridas para una categoría
        
        Args:
            categoria: Nombre de la categoría
            
        Returns:
            Lista de términos de búsqueda sugeridos
        """
        return YouTubeService.CATEGORIAS_SUGERIDAS.get(categoria.lower(), [])
    
    @staticmethod
    def buscar_por_herramienta(nombre_herramienta: str) -> List[Dict]:
        """
        Busca videos relacionados con una herramienta específica
        
        Args:
            nombre_herramienta: Nombre de la herramienta
            
        Returns:
            Lista de videos relacionados
        """
        query = f"cómo usar {nombre_herramienta} tutorial"
        return YouTubeService.buscar_videos(query, max_results=3)
    
    @staticmethod
    def obtener_categorias_disponibles() -> List[str]:
        """Retorna las categorías disponibles"""
        return list(YouTubeService.CATEGORIAS_SUGERIDAS.keys())