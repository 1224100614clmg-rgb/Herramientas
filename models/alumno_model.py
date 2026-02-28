from config import get_db_connection
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

def registrar_alumno(matricula, nombre_completo, correo, carrera, contrasena):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        hash_pass = generate_password_hash(contrasena)
        
        cursor.execute("""
            INSERT INTO alumnos (matricula, nombre_completo, correo, carrera, contrasena_hash)
            VALUES (%s, %s, %s, %s, %s)
        """, (matricula, nombre_completo, correo, carrera, hash_pass))
        
        conn.commit()
        return {"ok": True}
    
    except Exception as e:
        conn.rollback()
        return {"ok": False, "error": str(e)}
    
    finally:
        cursor.close()
        conn.close()

def buscar_alumno_por_matricula(matricula):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM alumnos WHERE matricula = %s", (matricula,))
    alumno = cursor.fetchone()
    
    cursor.close()
    conn.close()
    return alumno


def buscar_laboratorista(usuario):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM laboratoristas WHERE usuario = %s", (usuario,))
    lab = cursor.fetchone()
    cursor.close()
    conn.close()
    return lab

