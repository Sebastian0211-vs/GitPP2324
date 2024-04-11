import snap7

api = snap7.client.Client()
api.connect("192.168.0.1", 0, 1)

reading = api.db_read(1, 120, 1)
snap7.util.set_bool(reading, 0, 5)
api.db_write(reading, 1, 120, 1)
