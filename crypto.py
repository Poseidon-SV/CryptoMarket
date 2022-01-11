# Created  a __package__
from crypto_package import app

#Checks if the crypto.py file has executed directly and not imported

if __name__ == "__main__":
    app.run(debug=True)
        
