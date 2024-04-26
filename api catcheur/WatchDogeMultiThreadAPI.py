import logging
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import time
import ip_addresses as ip
import requests
from multiprocessing.dummy import Pool as ThreadPool
import concurrent.futures

app = Flask(__name__)
# Set up logging
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def execute_in_threadpool(func, *args):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(func, *args)

def job():
    NombreAPIConnected = 0
    time.sleep(1)
    multi_possible(NombreAPIConnected)
    nombremultisql = 0
    checkplusde3(nombremultisql)
    get_info()

def get_info():
    global valid_request

    def make_request(ip, request):
        try:
            response = requests.get(f"http://{ip['RASP']}:8000/{request}")
            logging.info(response.json())
        except Exception as e:
            logging.error(e)

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
            logging.error(e)
        return False

    def set_multi(ip, value):
        try:
            requests.get(f"http://{ip['RASP']}:8000/multi/{value}")
        except Exception as e:
            logging.error(e)

    results = execute_in_threadpool(check_possible, ip.ip_addresses.values())
    NombreAPIConnected += sum(results)

    if NombreAPIConnected > 1:
        logging.info("Mode multi disponible")
        execute_in_threadpool(set_multi, ip.ip_addresses.values(), ['True']*len(ip.ip_addresses))
    else:
        logging.info("Mode multi indisponible")
        execute_in_threadpool(set_multi, ip.ip_addresses.values(), ['False']*len(ip.ip_addresses))

def checkplusde3(nombremultisql):
    def set_multinbr(ip, value):
        try:
            requests.get(f"http://{ip['RASP']}:8000/multinbr/{value}")
        except Exception as e:
            logging.error(e)

    if nombremultisql >=3:
        logging.info("Multi sur plus de 3 châssis")
        execute_in_threadpool(set_multinbr, ip.ip_addresses.values(), ['True']*len(ip.ip_addresses))
    else:
        logging.info("Multi sur moins de 3 châssis")
        execute_in_threadpool(set_multinbr, ip.ip_addresses.values(), ['False']*len(ip.ip_addresses))

for ip in ip.ip_addresses.values():
    url = f"http://{ip['RASP']}:8000/API_IP/{ip['API']}"
    try:
        response = requests.get(url)
        logging.info(response.json())
    except Exception as e:
        logging.error(e)

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(job, 'interval', seconds=1)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)