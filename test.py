from database import engine

try:
    connection = engine.connect()
    print("Connexion réussie ")
    connection.close()
except Exception as e:
    print(f"Erreur : {e}")

