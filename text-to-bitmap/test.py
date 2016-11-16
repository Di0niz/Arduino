import mraa as mraa
import random as rand

# byte max7219_reg_noop        = 0x00;
# byte max7219_reg_digit0      = 0x01;
# byte max7219_reg_digit1      = 0x02;
# byte max7219_reg_digit2      = 0x03;
# byte max7219_reg_digit3      = 0x04;
# byte max7219_reg_digit4      = 0x05;
# byte max7219_reg_digit5      = 0x06;
# byte max7219_reg_digit6      = 0x07;
# byte max7219_reg_digit7      = 0x08;
# byte max7219_reg_decodeMode  = 0x09;
# byte max7219_reg_intensity   = 0x0a;
# byte max7219_reg_scanLimit   = 0x0b;
# byte max7219_reg_shutdown    = 0x0c;
# byte max7219_reg_displayTest = 0x0f;


x = mraa.Gpio(7)
#x.dir(mraa.PIN_OUT)

dev = mraa.Spi(7)

dev.mode(mraa.SPI_MODE0)

def spiTransfer(spi, addr, opcode, data):
    tx = bytearray(2)
    tx[0] = opcode 
    tx[1] = data
    ret = spi.write(tx)


x.write(0)
spiTransfer(dev, 1, 0x0f, 0x00)
x.write(1)

print "Done"
