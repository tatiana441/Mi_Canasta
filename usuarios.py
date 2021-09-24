import psycopg2

class Usuarios:

    cantidad_usuarios = 0
    
    def __init__(self, cantidad_usuarios):
        self.cantidad_usuarios = cantidad_usuarios 
        
    def list_usuarios(self):
        usuarios_list = [] #variable dentro del metodo list_usuarios
        conn = psycopg2.connect( 
            host="ec2-23-20-208-173.compute-1.amazonaws.com",
            database="d2q63ki9v18tbk",
            user="ckgpkyndtdeeca",
            password="93c77fe594b690c426b911640795bd52c34f36cd660bdf1fc5178f5f9bdea7c1"
        )
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM usuarios")
        
        usuarios_list = cur.fetchall()
        
        self.cantidad_usuarios = len(usuarios_list)
        
        cur.close() 
        
        return usuarios_list
        
#pregunta: esto se hace por cada tabla creado solo se crear para ser importada al main, y esta al momento de ejecutarse no debe de motrar nada solo se muestra en el main