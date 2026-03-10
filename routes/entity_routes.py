from flask import Blueprint, render_template, request, redirect
from config import get_db_connection

entity_bp = Blueprint("entity", __name__)

@entity_bp.route("/")
def index():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM entity_types")
    entities = cur.fetchall()

    conn.close()

    return render_template("index.html", entities=entities)


@entity_bp.route("/create_entity", methods=["GET","POST"])
def create_entity():

    if request.method == "POST":

        name = request.form["name"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO entity_types (name) VALUES (%s)",
            (name,)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("create_entity.html")


@entity_bp.route("/create_attribute/<entity_id>", methods=["GET","POST"])
def create_attribute(entity_id):

    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":

        name = request.form["name"]
        data_type = request.form["data_type"]

        cur.execute(
            """
            INSERT INTO attributes (entity_type_id,name,data_type)
            VALUES (%s,%s,%s)
            """,
            (entity_id,name,data_type)
        )

        conn.commit()

    cur.execute(
        "SELECT * FROM attributes WHERE entity_type_id=%s",
        (entity_id,)
    )

    attributes = cur.fetchall()

    conn.close()

    return render_template(
        "create_attribute.html",
        entity_id=entity_id,
        attributes=attributes
    )