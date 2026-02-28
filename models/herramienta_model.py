from config import get_db_connection

def obtener_herramientas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM herramientas ORDER BY nombre")
    herramientas = cursor.fetchall()
    cursor.close()
    conn.close()
    return herramientas

def obtener_herramientas_disponibles():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_herramienta, nombre FROM herramientas WHERE cantidad_disponible > 0 ORDER BY nombre")
    herramientas = cursor.fetchall()
    cursor.close()
    conn.close()
    return herramientas

def agregar_herramienta(codigo, nombre, descripcion, categoria, cantidad):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO herramientas (codigo_inventario, nombre, descripcion, categoria, cantidad_total, cantidad_disponible)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (codigo, nombre, descripcion, categoria, cantidad, cantidad))
        conn.commit()
        return {"ok": True}
    except Exception as e:
        conn.rollback()
        return {"ok": False, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

def editar_herramienta(id_herramienta, codigo, nombre, descripcion, categoria, cantidad_total):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE herramientas
            SET codigo_inventario=%s, nombre=%s, descripcion=%s, categoria=%s, cantidad_total=%s
            WHERE id_herramienta=%s
        """, (codigo, nombre, descripcion, categoria, cantidad_total, id_herramienta))
        conn.commit()
        return {"ok": True}
    except Exception as e:
        conn.rollback()
        return {"ok": False, "error": str(e)}
    finally:
        cursor.close()
        conn.close()

def eliminar_herramienta(id_herramienta):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM herramientas WHERE id_herramienta = %s", (id_herramienta,))
        conn.commit()
        return {"ok": True}
    except Exception as e:
        conn.rollback()
        return {"ok": False, "error": str(e)}
    finally:
        cursor.close()
        conn.close()