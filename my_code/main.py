import argparse
import os

class Database:
    def __init__(self, path):
        self.path = path
        print("Database connected to DB: {path}")

    def close(self):
            print ("Database is closed")

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument ("--db", default= "data.db")
    parser.add_argument ("--reset", action="store_true")
    parser.add_argument ("--seed",action="store_true")

    return parser.parse_args()

def main():
    args = parse_args()

    #reset database
    if args.reset and os.path.exists(args.db):
        os.remove(args.db)
        print ("DB removed")

    #create database
    db = Database(args.db)

    #seed data
    if args.seed:
        print ("Loading testing data...")

    #Aplication Start 
    print ("Aplication running")

    #Application quit
    db.close()

if __name__ == "__main__":
    main()