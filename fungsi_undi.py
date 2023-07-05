import random
from PIL import Image
import RPi.GPIO as GPIO
from time import sleep
from flask import redirect
from flask import Flask,render_template,jsonify
app = Flask(__name__)



# Setup GPIO

pir_sensor_pin = 23

led_pin_1 = 17

led_pin_2 = 22

led_pin_3 = 27

GPIO.setmode(GPIO.BCM)

GPIO.setup(pir_sensor_pin, GPIO.IN)

GPIO.setup(led_pin_1, GPIO.OUT)

GPIO.setup(led_pin_2, GPIO.OUT)

GPIO.setup(led_pin_3, GPIO.OUT)



def get_variable(x):

    if x >= 1 and x <= 50:

        return random.choice(['c/mie_goreng.png', 'c/mie_goreng2.jpg', 'c/mie_kari.jpg', 'c/mie_soto.jpg', 'c/minyak.jpg', 'c/gula.jpg'])

    elif x > 50 and x <= 70:

        return random.choice(['uc/detergen.jpeg', 'uc/sabun_muka.JPG'])

    elif x > 70 and x <= 85:

        return random.choice(['r/rice_cooker.jpeg', 'r/kipas_angin.jpg'])

    elif x > 85 and x <= 95:

        return random.choice(['sr/blender.jpg', 'sr/setrika.jpg', 'sr/kompor.png'])

    elif x > 95 and x <= 100:

        return random.choice(['ur/sepeda.jpg', 'ur/tv.jpg'])

    else:

        return []



def button_a_action():

    angka = random.randint(1, 100)

    result = get_variable(angka)

    return [result] if result else []



def button_b_action():

    hasil_angka = []

    for _ in range(10):

        angka = random.randint(1, 100)

        result = get_variable(angka)

        if result:

            hasil_angka.append(result)

    return hasil_angka

    

def get_pir_status(pir_sensor_pin):

    status = GPIO.input(pir_sensor_pin)

    if status == GPIO.HIGH:

        GPIO.output(led_pin_2, GPIO.HIGH)

    else:

        GPIO.output(led_pin_2, GPIO.LOW)

    return status





@app.route('/')

def home():

  return render_template("index.html")

  

#Endpoint untuk tombol a

@app.route('/button_a')

def handle_button_a():

    status = get_pir_status(pir_sensor_pin)

    if status == GPIO.HIGH:

        result = button_a_action()

        GPIO.output(led_pin_1, GPIO.HIGH)

        return render_template('index.html', image_url=result)

    else:

        return render_template('index.html', device_off=True)



# Endpoint untuk tombol b

@app.route('/button_b')

def handle_button_b():

    status = get_pir_status(pir_sensor_pin)

    if status == GPIO.HIGH:

        result = button_b_action()

        return render_template('index.html', image_url=result)

    else:

        return render_template('index.html', device_off=True)

        

# Endpoint untuk tombol c

@app.route('/button_c')

def home():
    status = get_pir_status(pir_sensor_pin)
    if status == GPIO.HIGH:
        GPIO.output(led_pin_3, GPIO.HIGH)
        return render_template("index.html")

    else:

        return render_template('index.html', device_off=True)



# Endpoint untuk link about us

@app.route('/aboutus')

def about_us():

    return render_template("aboutus.html")



# Endpoint apabila user ingin kembali ke page awal

@app.route('/mainpage')

def main_page():

    return redirect('/')



# Metode pengiriman status pir pada web

@app.route('/pir/status', methods=['GET'])

def update_pir_status():

    status = GPIO.input(pir_sensor_pin)

    return jsonify({'status': status})



#Start server

if __name__ == '__main__':

    app.run(port=8080, host='0.0.0.0')



try:

    while True:

        status = get_pir_status(pir_sensor_pin)

        if status == GPIO.HIGH:

            GPIO.output(led_pin_2, GPIO.HIGH)

        else:

            GPIO.output(led_pin_2, GPIO.LOW)

        sleep(0.1)

except KeyboardInterrupt:

    GPIO.cleanup()



