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
        host=os.environ["NOMBRE DEL HOST"],
        database=os.environ["NOMBRE DE LA DB"],
        user=os.environ["USUARIO DE LA DB"],
        password=os.environ["PASSWORD DEL USUARIO"],
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
# ENTIDAD 1: completar nombre de la entidad
# ─────────────────────────────────────────

# Reemplazar "entidad1" por el nombre real (ej: clientes, productos...)

@app.route("/entidad1", methods=["GET"])
def listar_entidad1():
    """Retorna todos los registros de entidad1."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Escribir la consulta SQL correcta
    cur.execute("SELECT * FROM ???  ORDER BY id")

    registros = cur.fetchall()
    conn.close()
    return jsonify(registros)


@app.route("/entidad1/<int:id>", methods=["GET"])
def obtener_entidad1(id):
    """Retorna un registro por su id. Retorna 404 si no existe."""
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Completar la consulta con el nombre de tabla correcto
    cur.execute("SELECT * FROM ??? WHERE id = %s", (id,))

    registro = cur.fetchone()
    conn.close()

    # ¿Qué debe retornar si el registro no existe?
    if not registro:
        return jsonify({"error": "???"}), ???

    return jsonify(registro)


@app.route("/entidad1", methods=["POST"])
def crear_entidad1():
    """Crea un nuevo registro. Recibe JSON en el body."""
    data = request.get_json()
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Completar con los campos reales de la tabla
    # Ejemplo para tabla clientes:
    # cur.execute(
    #     "INSERT INTO clientes (nombre, email) VALUES (%s, %s) RETURNING *",
    #     (data["nombre"], data["email"])
    # )
    cur.execute(
        "INSERT INTO ??? (???) VALUES (???) RETURNING *",
        (???)
    )

    nuevo = cur.fetchone()
    conn.commit()
    conn.close()
    return jsonify(nuevo), 201


@app.route("/entidad1/<int:id>", methods=["PUT"])
def actualizar_entidad1(id):
    """Actualiza un registro existente por su id."""
    data = request.get_json()
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Completar con los campos de la tabla
    cur.execute(
        "UPDATE ??? SET ??? WHERE id = %s RETURNING *",
        (???, id)
    )

    actualizado = cur.fetchone()
    conn.commit()
    conn.close()

    if not actualizado:
        return jsonify({"error": "???"}), 404

    return jsonify(actualizado)


@app.route("/entidad1/<int:id>", methods=["DELETE"])
def eliminar_entidad1(id):
    """Elimina un registro por su id."""
    conn = get_conn()
    cur = conn.cursor()

    # Completar con el nombre de la tabla
    cur.execute("DELETE FROM ??? WHERE id = %s RETURNING id", (id,))

    eliminado = cur.fetchone()
    conn.commit()
    conn.close()

    if not eliminado:
        return jsonify({"error": "???"}), 404

    return jsonify({"mensaje": f"Registro {id} eliminado correctamente"})


# ─────────────────────────────────────────
# ENTIDAD 2
# ─────────────────────────────────────────

# Implementar CRUD completo para una segunda entidad
# Seguir la misma estructura de entidad1


# ─────────────────────────────────────────
# Inicio
# ─────────────────────────────────────────

if __name__ == "__main__":
    # El puerto debe coincidir con el expuesto en docker-compose.yml
    app.run(host="0.0.0.0", port=5000, debug=True)
