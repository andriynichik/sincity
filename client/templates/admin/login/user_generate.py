
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from lib.config.Yaml import Yaml as Config

def main():
    # Connect to the DB
    # collection = MongoClient()["local"]["users"]
    config = Config('./config/config.yml')
    mongo_config = config.get('mongodb')
    connection = MongoClient(mongo_config['host'], mongo_config['port'])
    db = connection.local
    # Ask for data to store
    user = input("Enter your username: ")
    password = input("Enter your password: ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user in the DB
    try:
        db.users.insert({"_id": user, "password": pass_hash})
        print ("User created.")
    except DuplicateKeyError:
        print ("User already present in DB.")


if __name__ == '__main__':
    main()