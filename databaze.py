from pymongo import MongoClient
from datetime import datetime, timedelta
import time
import threading

# Globalūs kintamieji žmonių skaičiavimui
total_entered = 0
total_exited = 0

def setup_database():
    client = MongoClient("mongodb://localhost:27017/")  
    db = client["people_counter"]  
    collection = db["people_count"]  
    collection.create_index("timestamp")  
    print("MongoDB duomenų bazė ir kolekcija sėkmingai sukurta!")

def log_people_count(entered, exited):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["people_counter"]
    collection = db["people_count"]
    
    data = {
        "timestamp": datetime.now(),
        "entered": entered,
        "exited": exited
    }
    collection.insert_one(data)
    print("Įrašyti duomenys apie žmonių judėjimą.")

def log_people_count_periodically(interval=5):
    global total_entered, total_exited
    print(f"Logging interval: {interval} seconds")  # Debugging
    while True:
        log_people_count(total_entered, total_exited)
        print(f"Duomenys išsiųsti: Įėjo={total_entered}, Išėjo={total_exited}")  
        time.sleep(interval)

def get_yesterday_count():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["people_counter"]
    collection = db["people_count"]
    
    yesterday = datetime.now() - timedelta(days=1)
    start = datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
    end = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59)
    
    records = collection.find({"timestamp": {"$gte": start, "$lte": end}})
    total_entered = sum(record["entered"] for record in records)
    total_exited = sum(record["exited"] for record in records)
    
    print(f"Vakar įėjo: {total_entered}, išėjo: {total_exited}")
    return total_entered, total_exited

# Funkcija, kuri atnaujina skaičiavimus
def count_people(entered, exited):
    global total_entered, total_exited
    total_entered += entered
    total_exited += exited
    print(f"Atnaujinti duomenys - Įėjo: {total_entered}, Išėjo: {total_exited}")

if __name__ == "__main__":
    setup_database()
    
    # Paleidžiame duomenų siuntimą kas 5 sek.
    log_thread = threading.Thread(target=log_people_count_periodically, daemon=True)
    log_thread.start()
    
    # Simuliuojame žmonių skaičiavimą (čia būtų tavo detektoriaus logika)
    while True:
        count_people(1, 0)  # Pvz., įėjo vienas žmogus
        time.sleep(3)  # Kas 3 sek. pridedame naujus duomenis
