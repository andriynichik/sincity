
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lib.config.Yaml import Yaml as Config

def main():

    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    user = input("Enter your phone number (format - 380630000000 ): ")
    password = input("Enter your password: ")
    userName = input("Enter your Name: ")
    userEmail = input("Enter your email: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        db.users.insert({"_id": user, "password": pass_hash, "userName": userName, "userEmail":userEmail, "phone": '+'+str(user) })
        print ("User created.")
    except DuplicateKeyError:
        print ("User already present in DB.")


if __name__ == '__main__':
    main()