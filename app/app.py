import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request



app = Flask(__name__)

# ─────────────────────────────────────────
# Conexión a la base de datos
# ─────────────────────────────────────────

def get_conn():
    """
    Retorna una conexión a PostgreSQL usando las variables de entorno
    definidas en el archivo .env y mapeadas en docker-compose.yml.
    """
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

# ─────────────────────────────────────────
# Ruta raíz — índice de endpoints
# ─────────────────────────────────────────

@app.route("/")
def index():
    return jsonify({
        "mensaje": "API en funcionamiento",
        "endpoints": {
            # Listar aquí todos los endpoints que implementes
            # Ejemplo:
            # "clientes": "/clientes",
        }
    })

# ─────────────────────────────────────────
# ENTIDAD 1: Usuario
# ─────────────────────────────────────────

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM usuario ORDER BY cedula")

    usuarios = cur.fetchall()
    conn.close()

    return jsonify(usuarios)


@app.route("/usuarios/<string:cedula>", methods=["GET"])
def obtener_usuario(cedula):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM usuario WHERE cedula = %s", (cedula,))
    usuario = cur.fetchone()

    conn.close()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(usuario)

@app.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.get_json()

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        """
        INSERT INTO usuario (cedula, nombre, telefono, correo, direccion)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *
        """,
        (
            data["cedula"],
            data.get("nombre"),
            data.get("telefono"),
            data.get("correo"),
            data.get("direccion"),
        )
    )

    nuevo = cur.fetchone()
    conn.commit()
    conn.close()

    return jsonify(nuevo), 201

@app.route("/usuarios/<string:cedula>", methods=["PUT"])
def actualizar_usuario(cedula):
    data = request.get_json()

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        """
        UPDATE usuario
        SET nombre = %s,
            telefono = %s,
            correo = %s,
            direccion = %s
        WHERE cedula = %s
        RETURNING *
        """,
        (
            data.get("nombre"),
            data.get("telefono"),
            data.get("correo"),
            data.get("direccion"),
            cedula
        )
    )

    actualizado = cur.fetchone()
    conn.commit()
    conn.close()

    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(actualizado)

@app.route("/usuarios/<string:cedula>", methods=["DELETE"])
def eliminar_usuario(cedula):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM usuario WHERE cedula = %s RETURNING cedula",
        (cedula,)
    )

    eliminado = cur.fetchone()
    conn.commit()
    conn.close()

    if not eliminado:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"mensaje": f"Usuario {cedula} eliminado correctamente"})

# ─────────────────────────────────────────
# ENTIDAD 2: Lugar
# ─────────────────────────────────────────

@app.route("/lugares", methods=["GET"])
def listar_lugares():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM lugar ORDER BY id")

    lugares = cur.fetchall()
    conn.close()

    return jsonify(lugares)


@app.route("/lugares/<int:id>", methods=["GET"])
def obtener_lugar(id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM lugar WHERE id = %s", (id,))
    lugar = cur.fetchone()

    conn.close()

    if not lugar:
        return jsonify({"error": "Lugar no encontrado"}), 404

    return jsonify(lugar)

@app.route("/lugares", methods=["POST"])
def crear_lugar():
    data = request.get_json()

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        """
        INSERT INTO lugar (nombre, tipo)
        VALUES (%s, %s)
        RETURNING *
        """,
        (data["nombre"], data["tipo"])
    )

    nuevo = cur.fetchone()
    conn.commit()
    conn.close()

    return jsonify(nuevo), 201

@app.route("/lugares/<int:id>", methods=["PUT"])
def actualizar_lugar(id):
    data = request.get_json()

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute(
        """
        UPDATE lugar
        SET nombre = %s,
            tipo = %s
        WHERE id = %s
        RETURNING *
        """,
        (data["nombre"], data["tipo"], id)
    )

    actualizado = cur.fetchone()
    conn.commit()
    conn.close()

    if not actualizado:
        return jsonify({"error": "Lugar no encontrado"}), 404

    return jsonify(actualizado)

@app.route("/lugares/<int:id>", methods=["DELETE"])
def eliminar_lugar(id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM lugar WHERE id = %s RETURNING id",
        (id,)
    )

    eliminado = cur.fetchone()
    conn.commit()
    conn.close()

    if not eliminado:
        return jsonify({"error": "Lugar no encontrado"}), 404

    return jsonify({"mensaje": f"Lugar {id} eliminado correctamente"})

# ─────────────────────────────────────────
# ENTIDAD 2: Lugar
# ─────────────────────────────────────────

#Ruta para crear turno, recibe cedula y tipo_lugar, retorna numero de turno y datos del turno creado
@app.route("/turno", methods=["POST"])
def crear_turno():
    data = request.get_json()

    cedula = data["cedula"]
    tipo_lugar = data["tipo_lugar"]

    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Verificar usuario
    cur.execute("SELECT * FROM usuario WHERE cedula = %s", (cedula,))
    usuario = cur.fetchone()

    if not usuario:
        cur.execute(
            "INSERT INTO usuario (cedula) VALUES (%s) RETURNING *",
            (cedula,)
        )

    # Calcular posición por tipo de lugar
    cur.execute(
        """
        SELECT COALESCE(MAX(posicion), 0) as max_pos
        FROM turno
        WHERE tipo_lugar = %s
        """,
        (tipo_lugar,)
    )

    max_pos = cur.fetchone()["max_pos"]
    posicion = max_pos + 1

    # Generar número de turno con las primeras 3 letras del tipo de lugar en mayúscula y la posición
    prefijo = tipo_lugar[:3].upper()
    numero_turno = f"{prefijo}-{posicion}"

    # Crear turno
    cur.execute(
        """
        INSERT INTO turno (cedula, tipo_lugar, posicion, fecha, estado)
        VALUES (%s, %s, %s, NOW(), 'pendiente')
        RETURNING *
        """,
        (cedula, tipo_lugar, posicion)
    )

    turno = cur.fetchone()

    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Turno generado",
        "turno": numero_turno,
        "datos": turno
    }), 201

# Ruta para obtener los tipos de lugar disponibles (sin duplicados)
@app.route("/tipos-lugar", methods=["GET"])
def obtener_tipos_lugar():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT tipo FROM lugar")

    tipos = [row[0] for row in cur.fetchall()]

    conn.close()

    return jsonify(tipos)

# Ruta para visualizar turnos en estado "atendiendo" y los siguientes en estado "pendiente", ordenados por tipo de lugar y posición
@app.route("/turnos/visualizacion", methods=["GET"])
def visualizar_turnos():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Turnos en estado "atendiendo" con datos de usuario y lugar
    cur.execute("""
        SELECT t.tipo_lugar, t.posicion, u.nombre as usuario, l.nombre as lugar
        FROM turno t
        LEFT JOIN usuario u ON t.cedula = u.cedula
        LEFT JOIN lugar l ON t.id_lugar = l.id
        WHERE t.estado = 'atendiendo'
        ORDER BY t.tipo_lugar, t.posicion
    """)

    atendiendo = cur.fetchall()

    # Formatear número de turno y datos para la respuesta
    atendiendo_formateado = []
    for t in atendiendo:
        prefijo = t["tipo_lugar"][:3].upper()
        numero = f"{prefijo}{t['posicion']}"

        atendiendo_formateado.append({
            "turno": numero,
            "usuario": t["usuario"],
            "lugar": t["lugar"]
        })

    # Turnos en estado "pendiente" ordenados por tipo de lugar y posición 
    cur.execute("""
        SELECT DISTINCT ON (tipo_lugar)
            tipo_lugar, posicion, cedula
        FROM turno
        WHERE estado = 'pendiente'
        ORDER BY tipo_lugar, posicion ASC
    """)

    siguientes = cur.fetchall()

    # Obtener nombres de usuario y formatear número de turno para la respuesta
    siguientes_formateado = []
    for t in siguientes:
        cur.execute(
            "SELECT nombre FROM usuario WHERE cedula = %s",
            (t["cedula"],)
        )
        usuario = cur.fetchone()

        prefijo = t["tipo_lugar"][:3].upper()
        numero = f"{prefijo}{t['posicion']}"

        siguientes_formateado.append({
            "turno": numero,
            "usuario": usuario["nombre"] if usuario else None
        })

    conn.close()

    return jsonify({
        "atendiendo": atendiendo_formateado,
        "siguientes": siguientes_formateado
    })

@app.route("/lugar/<int:id>/siguiente", methods=["POST"])
def siguiente_turno(id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Obtener tipo del lugar
    cur.execute("SELECT tipo FROM lugar WHERE id = %s", (id,))
    lugar = cur.fetchone()

    if not lugar:
        conn.close()
        return jsonify({"error": "Lugar no encontrado"}), 404

    tipo_lugar = lugar["tipo"]

    # Obtener primer turno pendiente de ese tipo
    cur.execute("""
        SELECT *
        FROM turno
        WHERE tipo_lugar = %s AND estado = 'pendiente'
        ORDER BY posicion ASC
        LIMIT 1
    """, (tipo_lugar,))

    turno = cur.fetchone()

    if not turno:
        conn.close()
        return jsonify({"mensaje": "No hay turnos pendientes"}), 200

    # Actualizar turno → atendiendo + asignar lugar
    cur.execute("""
        UPDATE turno
        SET estado = 'atendiendo',
            id_lugar = %s
        WHERE id = %s
        RETURNING *
    """, (id, turno["id"]))

    turno_actualizado = cur.fetchone()

    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Turno en atención",
        "turno": turno_actualizado
    })

# Ruta para finalizar turno en un lugar específico, cambia estado a "finalizado"
@app.route("/lugar/<int:id>/finalizar", methods=["POST"])
def finalizar_turno(id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Buscar turno en atención en ese lugar
    cur.execute("""
        SELECT *
        FROM turno
        WHERE id_lugar = %s AND estado = 'atendiendo'
        LIMIT 1
    """, (id,))

    turno = cur.fetchone()

    if not turno:
        conn.close()
        return jsonify({"mensaje": "No hay turno en atención"}), 200

    # Finalizar turno
    cur.execute("""
        UPDATE turno
        SET estado = 'finalizado'
        WHERE id = %s
        RETURNING *
    """, (turno["id"],))

    turno_finalizado = cur.fetchone()

    conn.commit()
    conn.close()

    return jsonify({
        "mensaje": "Turno finalizado",
        "turno": turno_finalizado
    })

# ─────────────────────────────────────────
# GETS de prueba
# ─────────────────────────────────────────

@app.route("/turnos", methods=["GET"])
def listar_turnos():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT t.*, u.nombre as usuario, l.nombre as lugar
        FROM turno t
        LEFT JOIN usuario u ON t.cedula = u.cedula
        LEFT JOIN lugar l ON t.id_lugar = l.id
        ORDER BY t.id
    """)

    turnos = cur.fetchall()
    conn.close()

    return jsonify(turnos)


@app.route("/turnos/<int:id>", methods=["GET"])
def obtener_turno(id):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
        SELECT t.*, u.nombre as usuario, l.nombre as lugar
        FROM turno t
        LEFT JOIN usuario u ON t.cedula = u.cedula
        LEFT JOIN lugar l ON t.id_lugar = l.id
        WHERE t.id = %s
    """, (id,))

    turno = cur.fetchone()
    conn.close()

    if not turno:
        return jsonify({"error": "Turno no encontrado"}), 404

    return jsonify(turno)
# ─────────────────────────────────────────
# Inicio
# ─────────────────────────────────────────

if __name__ == "__main__":
    # El puerto debe coincidir con el expuesto en docker-compose.yml
    app.run(host="0.0.0.0", port=5000, debug=True)
