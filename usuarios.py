import psycopg2
import databaseConnection

class Usuarios:

    id = 0
    nombre = ""
    password = ""
    email = ""
    cantidad_usuarios = 0

    conn = psycopg2.connect( #conectar a una base de datos
    host="ec2-23-20-208-173.compute-1.amazonaws.com",
    database="d2q63ki9v18tbk",
    user="ckgpkyndtdeeca",
    password="93c77fe594b690c426b911640795bd52c34f36cd660bdf1fc5178f5f9bdea7c1"
    )

    cur = conn.cursor()

    def __init__(self, cantidad_usuarios):
        self.cantidad_usuarios = cantidad_usuarios 

    def __init__(self):
        pass

    def __init__(self,nombre,password,email):
        self.nombre = nombre
        self.password = password
        self.email = email

    def __init__(self, nombre):
        self.nombre = nombre
        
        

    def list_usuarios(self):
        usuarios_list = [] 
        self.cur.execute("SELECT * FROM usuarios")
        usuarios_list = self.cur.fetchall()
        self.cur.close() 
        return usuarios_list


    def create(self):
        try:    
            self.cur.execute(
                "INSERT INTO usuarios(nombre,password,email) VALUES (%s,%s,%s)", (self.nombre, self.password, self.email))
            self.conn.commit()
        except Exception:
            print("Error inserting")
        finally:
            self.cur.close()
            self.conn.close()

    def delete(self):
        self.cur.execute("DELETE FROM usuarios WHERE nombre=%S",(self.nombre,))
        self.conn.commit()
        self.cur.close()
        self.conn.close()
<<<<<<< HEAD
    def get_nombre(self):
        self.cur.execute("SELECT * FROM usuarios WHERE nombre=%s", (self.nombre,))
        
        usuarios = self.cur.fetchone()
        self.id = usuarios[3]
        self.nombre = usuarios[0]
        self.email = usuarios[2]
        self.password = usuarios[1]
=======

>>>>>>> 52745f995ae5f7ca0a02a92fd1eb5855c3fd27b1
