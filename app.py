from flask import (
    Flask,
    g,
    render_template,
    request,
    redirect,
    flash,
    session,
    url_for
)
from flask.helpers import url_for
from flaskext.mysql import MySQL
from pymysql.cursors import Cursor

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin', password='1234'))
users.append(User(id=1, username='usuario', password='1234'))
users.append(User(id=1, username='invitado', password='1234'))

app= Flask(__name__)
app.secret_key='MisionTIC2022'
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='1234'
app.config['MYSQL_DATABASE_DB']='canasta'
mysql.init_app(app)

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('index_product'))
        
        return redirect(url_for('login'))

    return render_template('login.html', error=error)

@app.route('/index_product')
def index_product():
    if not g.user:
        return redirect(url_for('login'))

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
    return redirect('/index_product')

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
    return redirect('/index_product')

@app.route('/destroy_product/<int:idProd>')
def destroy_product(idProd):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM productos WHERE idProd=%s", (idProd))
    conn.commit()
    return redirect('/index_product')

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
    app.run(debug=True, port=82, host="192.168.1.2")
