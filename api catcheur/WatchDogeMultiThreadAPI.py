from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import time
import ip_addresses as ip
import requests
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures

app = Flask(__name__)

def job():
    NombreAPIConnected = 0
    time.sleep(1)
    multi_possible(NombreAPIConnected)
    nombremultisql = 0
    checkplusde3(nombremultisql)
    get_info()
    
    
valid_request = ["Mx_..." , "Mx_..."]

def get_info():
    global valid_request

    def make_request(ip, request):
        try:
            response = requests.get(f"http://{ip['RASP']}:8000/{request}")
            print(response.json())
        except Exception as e:
            print(e)

    pool = ThreadPool(4)  # Use 4 threads
    for request in valid_request:
        for ip in ip.ip_addresses.values():
            pool.apply_async(make_request, (ip, request))
    pool.close()
    pool.join() 

def multi_possible(NombreAPIConnected):
    def check_possible(ip):
        try:
            checker = requests.get(f"http://{ip['RASP']}:8000/check_possible")
            if checker.status_code == 200:
                return True
        except Exception as e:
            print(e)
        return False

    def set_multi(ip, value):
        try:
            requests.get(f"http://{ip['RASP']}:8000/multi/{value}")
        except Exception as e:
            print(e)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(check_possible, ip.ip_addresses.values()))
        NombreAPIConnected += sum(results)

    if NombreAPIConnected > 1:
        print("Mode multi disponible")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(set_multi, ip.ip_addresses.values(), ['True']*len(ip.ip_addresses))
    else:
        print("Mode multi indisponible")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(set_multi, ip.ip_addresses.values(), ['False']*len(ip.ip_addresses))

def checkplusde3(nombremultisql):
    if nombremultisql >=3:
        print("Multi sur plus de 3 châssis")
        for ip in ip.ip_addresses.values():
            try:
                requests.get(f"http://{ip['RASP']}:8000/multinbr/True")
            except Exception as e:
                print(e)
    else:
        print("Multi sur moins de 3 châssis")
        for ip in ip.ip_addresses.values():
            try:
                requests.get(f"http://{ip['RASP']}:8000/multinbr/False")
            except Exception as e:
                print(e)


for ip in ip.ip_addresses.values():
    url = f"http://{ip['RASP']}:8000/API_IP/{ip['API']}"
    try:
        response = requests.get(url)
        print(response.json())
    except Exception as e:
        print(e)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(job, 'interval', seconds=1)
scheduler.start()


# Point d'entrée principal pour exécuter l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


