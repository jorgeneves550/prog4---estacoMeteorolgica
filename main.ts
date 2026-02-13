input.onButtonPressed(Button.A, function () {
    I2C_LCD1602.clear()
})
let uvAnterior = 0
let maxUV = 0
let indiceUV = 0
let luzAnterior = 0
let maxLuz = 0
let luz = 0
let registar = 0
let tempAnterior = 0
let maxTemp = 0
let temp = 0
datalogger.setColumnTitles(
"temperatura",
"luminosidade",
"indice_uv"
)
I2C_LCD1602.LcdInit(39)
I2C_LCD1602.BacklightOn()
I2C_LCD1602.clear()
let minTemp = 50
let minUV = 1000
let minLuz = 1000
basic.forever(function () {
    I2C_LCD1602.clear()
    temp = pins.analogReadPin(AnalogPin.P0) * 3300 / 1023 / 10
    if (temp > maxTemp) {
        maxTemp = temp
    }
    if (temp < minTemp) {
        minTemp = temp
    }
    if (temp != tempAnterior) {
        registar = 1
        tempAnterior = temp
    }
    I2C_LCD1602.ShowString("Temp.atual: " + convertToText(Math.round(temp)) + ".c", 0, 0)
    I2C_LCD1602.ShowString("Max:" + convertToText(Math.round(maxTemp)), 0, 1)
    I2C_LCD1602.ShowString("Min:" + convertToText(Math.round(minTemp)), 9, 1)
    basic.pause(5000)
    I2C_LCD1602.clear()
    luz = Math.trunc(pins.analogReadPin(AnalogReadWritePin.P1) / 1023 * 100)
    if (luz < minLuz) {
        minLuz = luz
    }
    if (luz > maxLuz) {
        maxLuz = luz
    }
    if (luz != luzAnterior) {
        registar = 1
        luzAnterior = luz
    }
    I2C_LCD1602.ShowString("Luminosid: " + convertToText(luz) + "%", 0, 0)
    I2C_LCD1602.ShowString("Max:" + convertToText(maxLuz) + "%", 0, 1)
    I2C_LCD1602.ShowString("Min:" + convertToText(minLuz) + "%", 9, 1)
    basic.pause(5000)
    I2C_LCD1602.clear()
    indiceUV = pins.analogReadPin(AnalogReadWritePin.P2)
    if (maxUV < indiceUV) {
        maxUV = indiceUV
    }
    if (minUV > indiceUV) {
        minUV = indiceUV
    }
    if (indiceUV != uvAnterior) {
        registar = 1
        uvAnterior = indiceUV
    }
    I2C_LCD1602.ShowString("Ix UV atual: " + convertToText(indiceUV), 0, 0)
    I2C_LCD1602.ShowString("Max: " + convertToText(maxUV), 0, 1)
    I2C_LCD1602.ShowString("Min: " + convertToText(minUV), 8, 1)
    basic.pause(5000)
    if (registar == 1) {
        datalogger.log(
        datalogger.createCV("temperatura", temp),
        datalogger.createCV("indice_uv", indiceUV),
        datalogger.createCV("luminosidade", luz)
        )
        registar = 0
    }
})
