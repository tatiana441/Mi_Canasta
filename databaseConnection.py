import psycopg2

def create_connection():

    conn = psycopg2.connect( #conectar a una base de datos
    host="ec2-23-20-208-173.compute-1.amazonaws.com",
    database="d2q63ki9v18tbk",
    user="ckgpkyndtdeeca",
    password="93c77fe594b690c426b911640795bd52c34f36cd660bdf1fc5178f5f9bdea7c1"
    )
    cur = conn.cursor()

    return cur