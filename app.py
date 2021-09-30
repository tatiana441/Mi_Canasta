from flask import Flask
from flask import render_template,request,redirect,flash
from flask import send_from_directory
from flask.helpers import url_for
from flaskext.mysql import MySQL
from pymysql.cursors import Cursor

import os

app= Flask(__name__)
app.secret_key="MisionTIC2022"
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='1234'
app.config['MYSQL_DATABASE_DB']='canasta'
mysql.init_app(app)

CARPETA= os.path.join('img')
app.config['CARPETA']=CARPETA

@app.route('/img/<imgName>')
def img(imgName):
    return send_from_directory(app.config['CARPETA'],imgName)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index_product')
def index_product():
    sql="SELECT * FROM productos;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('files/index_product.html', productos=productos)

@app.route('/create_product')
def create_product():
    return render_template('files/create_product.html')

@app.route('/edit_product/<int:idProd>')
def edit_product(idProd):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE idProd=%s", (idProd))
    productos=cursor.fetchall()
    conn.commit()
    return render_template('files/edit_product.html', productos=productos)

@app.route('/update_product', methods=['POST'])
def update_product():
    _name=request.form['txtNombre']
    _price=request.form['txtCosto']
    _idCat=request.form['txtCategoria']
    idProd=request.form['txtId']
    sql="UPDATE productos SET name=%s, price=%s, idCat=%s WHERE idProd=%s;"
    datos=(_name, _price, _idCat, idProd)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/store_product', methods=['POST'])
def storage_product():
    _name=request.form['txtNombre']
    _price=request.form['txtCosto']
    _idCat=request.form['txtCategoria']

    if _name=='' or _price=='' or _idCat=='':
        flash('Ningún campo puede ir vacio')
        return redirect(url_for('create_product'))

    sql="INSERT INTO productos (`idProd`, `name`, `price`, `idCat`, `id_user_rol`) VALUES (NULL, %s, %s, %s, '1');"
    datos=(_name, _price, _idCat)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/')

@app.route('/destroy_product/<int:idProd>')
def destroy_product(idProd):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM productos WHERE idProd=%s", (idProd))
    conn.commit()
    return redirect('/')

@app.route('/index_category')
def index_category():
    sql="SELECT * FROM categorias;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    categorias=cursor.fetchall()
    conn.commit()
    return render_template('files/index_category.html', categorias=categorias)

@app.route('/create_category')
def create_category():
    return render_template('files/create_category.html')

@app.route('/edit_category/<int:idCat>')
def edit_category(idCat):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM categorias WHERE idCat=%s", (idCat))
    categorias=cursor.fetchall()
    conn.commit()
    return render_template('files/edit_category.html', categorias=categorias)

@app.route('/update_category', methods=['POST'])
def update_category():
    _nameCat=request.form['txtNombre']
    idCat=request.form['txtId']
    sql="UPDATE categorias SET nameCat=%s WHERE idCat=%s;"
    datos=(_nameCat, idCat)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/index_category')

@app.route('/store_category', methods=['POST'])
def storage_category():
    _nameCat=request.form['txtNombre']

    if _nameCat=='':
        flash('Ningún campo puede ir vacio')
        return redirect(url_for('create_category'))

    sql="INSERT INTO categorias (`idCat`, `nameCat`) VALUES (NULL, %s);"
    datos=(_nameCat)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/index_category')

@app.route('/destroy_category/<int:idCat>')
def destroy_category(idCat):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM categorias WHERE idCat=%s", (idCat))
    conn.commit()
    return redirect('/index_category')

if __name__== '__main__':
    app.run(debug=True)

