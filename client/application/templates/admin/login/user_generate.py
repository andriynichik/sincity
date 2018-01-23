
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lib.config.Yaml import Yaml as Config

def main():

    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    user = input("Enter your phone (format: 38063000000): ")
    password = input("Enter your password: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        db.users.insert({"_id": user, "password": pass_hash})
        print ("User created.")
    except DuplicateKeyError:
        print ("User already present in DB.")


if __name__ == '__main__':
    main()