from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

def db_connection():
    conn = None
    try:
        conn = pymysql.connect(
            host="sql.freedb.tech",
            database="freedb_Chiabiyyu_DB",
            user="freedb_chi_abiyyu",
            password="6Am9uVaF6%r8X?*",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as e:
        print(e)
    return conn

@app.route("/buku", methods=["GET", "POST", "PUT", "DELETE"])
def manage_buku():
    conn = db_connection()
    cursor = conn.cursor()

    try:
        if request.method == "GET":
            cursor.execute("SELECT * FROM buku")
            buku = [row for row in cursor.fetchall()]
            return jsonify({"data": buku})

        if request.method == "POST":
            data = request.get_json()
            query_insert = """
                INSERT INTO buku (nama_buku, penulis, rating, halaman, tanggal_terbit, penerbit, stok)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query_insert,
                (
                    data["nama_buku"],
                    data["penulis"],
                    data["rating"],
                    data["halaman"],
                    data["tanggal_terbit"],
                    data["penerbit"],
                    data["stok"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Berhasil Menambahkan Data Buku"})

        if request.method == "PUT":
            data = request.get_json()
            query_update = """
                UPDATE buku
                SET nama_buku=%s, penulis=%s, rating=%s, halaman=%s, tanggal_terbit=%s, penerbit=%s, stok=%s
                WHERE idbuku=%s
            """
            cursor.execute(
                query_update,
                (
                    data["nama_buku"],
                    data["penulis"],
                    data["rating"],
                    data["halaman"],
                    data["tanggal_terbit"],
                    data["penerbit"],
                    data["stok"],
                    data["idbuku"],
                ),
            )
            conn.commit()
            return jsonify({"message": "Berhasil Memperbarui Data Buku"})

        if request.method == "DELETE":
            data = request.get_json()
            query_delete = "DELETE FROM buku WHERE idbuku=%s"
            cursor.execute(query_delete, (data["idbuku"],))
            conn.commit()
            return jsonify({"message": "Berhasil Menghapus Data Buku"})

    except Exception as e:
        return jsonify({"error": str(e)})

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
