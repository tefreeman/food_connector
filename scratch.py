from measurements import Measurements
t0 = Measurements()
Measurements._load_measurements()
t = Measurements.get_measurement_type('cup')
t1 = Measurements.get_measurement_type('package')
t2 = Measurements.get_measurement_type('axe')
print('done')