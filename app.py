from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask (__name__)

# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '' 
app.config['MYSQL_DB'] = 'kdrama'

mysql = MySQL(app)


@app.route('/')
def root():
    return 'Selamat datang di tutorial RESTful API'


@app.route('/person')
def person():
    return jsonify({'name': 'haikal', 'address': 'bandung'})


@app.route('/kdrama_list', methods=['GET', 'POST'])
def kdrama_list():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM kdrama_list")
        
        # Dapatkan nama kolom dari cursor.description
        column_names = [i[0] for i in cursor.description]
        
        # Ambil data dan format menjadi list of dictionaries
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))
        
        cursor.close()
        
        return jsonify(data)

    elif request.method == 'POST':
        # Mengambil data dari request JSON
        data = request.json
        genre = data.get('genre')
        judul = data.get('judul')
        jumlah_episode = data.get('jumlah_episode')

        # Membuka koneksi dan melakukan insert ke database
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO kdrama_list (genre, judul, jumlah_episode) VALUES (%s, %s, %s)"
        val = (genre, judul, jumlah_episode)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil ditambahkan!'})
    

        

@app.route('/detailkdrama')
def detailkdrama():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM kdrama_list WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)

        # Mengambil nama-nama kolom dari cursor.description
        column_names = [i[0] for i in cursor.description]

        # Mengambil data dan memformatnya menjadi list of dictionaries
        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_names, row)))

        cursor.close()
        
        return jsonify(data)
    
@app.route('/deletekdrama', methods=['DELETE'])
def deletekdrama():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM kdrama_list WHERE id = %s"
        val = (request.args['id'],)
        cursor.execute(sql, val)
        
        mysql.connection.commit()
        
        cursor.close()

        return jsonify({'message': 'Data berhasil dihapus!'})
    
@app.route('/editkdrama', methods=['PUT'])
def editkdrama():
    if 'id' in request.args:
        data = request.get_json()
        cursor = mysql.connection.cursor()
        sql = "UPDATE kdrama_list SET genre=%s, judul=%s, jumlah_episode=%s WHERE id = %s"
        val = (data['genre'], data['judul'], data['jumlah_episode'], request.args['id'],)
        cursor.execute(sql, val)
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'Data berhasil diperbarui!'})

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50, debug=True)