from flask import Blueprint, render_template, request, redirect
from config import get_db_connection

record_bp = Blueprint("record", __name__)


@record_bp.route("/create_record/<entity_id>")
def create_record(entity_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM attributes WHERE entity_type_id=%s",
        (entity_id,)
    )

    fields = cur.fetchall()

    conn.close()

    return render_template(
        "create_record.html",
        fields=fields,
        entity_id=entity_id
    )


@record_bp.route("/save_record", methods=["POST"])
def save_record():

    entity_id = request.form["entity_id"]

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO entities (entity_type_id) VALUES (%s) RETURNING id",
        (entity_id,)
    )

    new_entity_id = cur.fetchone()[0]

    for key in request.form:

        if key.startswith("attr_"):

            attribute_id = key.split("_")[1]
            value = request.form[key]

            cur.execute(
                """
                INSERT INTO entity_values
                (entity_id,attribute_id,value)
                VALUES (%s,%s,%s)
                """,
                (new_entity_id,attribute_id,value)
            )

    conn.commit()
    conn.close()

    return redirect("/")