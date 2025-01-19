from app import create_app

# Kreiranje aplikacije
app = create_app()

# Pokretanje aplikacije
if __name__ == '__main__':
    app.run(debug=True)