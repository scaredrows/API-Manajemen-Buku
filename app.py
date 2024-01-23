# Nama  : Michael Jason
# Kelas : IF 10 R
# NIM   : 2211102361

from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="sql.freedb.tech",
            database="freedb_kapal_lawud",
            user="freedb_ikan_terbang",
            password="z5q!%NCG5wwnPzW",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/kapal", methods=["GET", "POST", "PUT", "DELETE"])
def manage_kapal():
    conn = db_connection()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM data_kapal")
        kapal = [
            dict(
                id=row["id"],
                nama_kapal=row["nama_kapal"],
                tipe_kapal=row["tipe_kapal"],
                tipe_mesin=row["tipe_mesin"],
                max_speed=row["max_speed"],
                harga=row["harga"],
            )
            for row in cursor.fetchall()
        ]
        if kapal is not None:
            return jsonify(kapal)

    if request.method == "POST":
        add_nama_kapal = request.form["nama_kapal"]
        add_tipe_kapal = request.form["tipe_kapal"]
        add_tipe_mesin = request.form["tipe_mesin"]
        add_max_speed = request.form["max_speed"]
        add_harga = request.form["harga"]

        query_insert = """
            INSERT INTO data_kapal (nama_kapal, tipe_kapal, tipe_mesin, max_speed, harga)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query_insert,
            (
                add_nama_kapal,
                add_tipe_kapal,
                add_tipe_mesin,
                add_max_speed,
                add_harga,
            ),
        )
        conn.commit()
        return "Berhasil Menambahkan Data kapal."

    if request.method == "PUT":
        update_id = request.form["id"]
        update_nama_kapal = request.form["nama_kapal"]
        update_tipe_kapal = request.form["tipe_kapal"]
        update_tipe_mesin = request.form["tipe_mesin"]
        update_max_speed = request.form["max_speed"]
        update_harga = request.form["harga"]

        query_update = """
            UPDATE data_kapal
            SET nama_kapal=%s, tipe_kapal=%s, tipe_mesin=%s, max_speed=%s, harga=%s
            WHERE id=%s
        """

        cursor.execute(
            query_update,
            (
                update_nama_kapal,
                update_tipe_kapal,
                update_tipe_mesin,
                update_max_speed,
                update_harga,
                update_id,
            ),
        )
        conn.commit()
        return "Berhasil Memperbarui Data kapal."

    if request.method == "DELETE":
        delete_id = request.form["id"]

        query_delete = """DELETE FROM data_kapal WHERE id=%s"""

        cursor.execute(query_delete, (delete_id,))
        conn.commit()
        return "Berhasil Menghapus Data kapal."


if __name__ == "__main__":
    app.run(debug=True, port=8000, use_reloader=True)
