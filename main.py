def on_button_pressed_a():
    I2C_LCD1602.clear()
input.on_button_pressed(Button.A, on_button_pressed_a)

uvAnterior = 0
maxUV = 0
indiceUV = 0
luzAnterior = 0
maxLuz = 0
luz = 0
registar = 0
tempAnterior = 0
maxTemp = 0
temp = 0
datalogger.set_column_titles("temperatura", "luminosidade", "indice_uv")
I2C_LCD1602.lcd_init(39)
I2C_LCD1602.backlight_on()
I2C_LCD1602.clear()
minTemp = 50
minUV = 1000
minLuz = 1000

def on_forever():
    global temp, maxTemp, minTemp, registar, tempAnterior, luz, minLuz, maxLuz, luzAnterior, indiceUV, maxUV, minUV, uvAnterior
    I2C_LCD1602.clear()
    temp = pins.analog_read_pin(AnalogPin.P0) * 3300 / 1023 / 10
    if temp > maxTemp:
        maxTemp = temp
    if temp < minTemp:
        minTemp = temp
    if temp != tempAnterior:
        registar = 1
        tempAnterior = temp
    I2C_LCD1602.show_string("Temp.atual: " + convert_to_text(Math.round(temp)) + ".c",
        0,
        0)
    I2C_LCD1602.show_string("Max:" + convert_to_text(Math.round(maxTemp)), 0, 1)
    I2C_LCD1602.show_string("Min:" + convert_to_text(Math.round(minTemp)), 9, 1)
    basic.pause(5000)
    I2C_LCD1602.clear()
    luz = int(pins.analog_read_pin(AnalogReadWritePin.P1) / 1023 * 100)
    if luz < minLuz:
        minLuz = luz
    if luz > maxLuz:
        maxLuz = luz
    if luz != luzAnterior:
        registar = 1
        luzAnterior = luz
    I2C_LCD1602.show_string("Luminosid: " + convert_to_text(luz) + "%", 0, 0)
    I2C_LCD1602.show_string("Max:" + convert_to_text(maxLuz) + "%", 0, 1)
    I2C_LCD1602.show_string("Min:" + convert_to_text(minLuz) + "%", 9, 1)
    basic.pause(5000)
    I2C_LCD1602.clear()
    indiceUV = pins.analog_read_pin(AnalogReadWritePin.P2)
    if maxUV < indiceUV:
        maxUV = indiceUV
    if minUV > indiceUV:
        minUV = indiceUV
    if indiceUV != uvAnterior:
        registar = 1
        uvAnterior = indiceUV
    I2C_LCD1602.show_string("Ix UV atual: " + convert_to_text(indiceUV), 0, 0)
    I2C_LCD1602.show_string("Max: " + convert_to_text(maxUV), 0, 1)
    I2C_LCD1602.show_string("Min: " + convert_to_text(minUV), 8, 1)
    basic.pause(5000)
    if registar == 1:
        datalogger.log(datalogger.create_cv("temperatura", temp),
            datalogger.create_cv("indice_uv", indiceUV),
            datalogger.create_cv("luminosidade", luz))
        registar = 0
basic.forever(on_forever)
