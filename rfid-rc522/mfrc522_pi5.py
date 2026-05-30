import spidev
import gpiod
import time

class MFRC522:
    NRSTPD = 25  # RST-Pin (GPIO 25, physisch Pin 22)
    MAX_LEN = 16
    PCD_IDLE       = 0x00
    PCD_TRANSCEIVE = 0x0C
    PCD_RESETPHASE = 0x0F
    PCD_CALCCRC    = 0x03
    PICC_REQIDL    = 0x26
    PICC_REQALL    = 0x52
    PICC_ANTICOLL  = 0x93
    PICC_SELECTTAG = 0x93
    PICC_AUTHENT1A = 0x60
    PICC_READ      = 0x30
    PICC_WRITE     = 0xA0
    PICC_HALT      = 0x50
    MI_OK       = 0
    MI_NOTAGERR = 1
    MI_ERR      = 2
    Reserved00    = 0x00
    CommandReg    = 0x01
    CommIEnReg    = 0x02
    DivlEnReg     = 0x03
    CommIrqReg    = 0x04
    DivIrqReg     = 0x05
    ErrorReg      = 0x06
    Status1Reg    = 0x07
    Status2Reg    = 0x08
    FIFODataReg   = 0x09
    FIFOLevelReg  = 0x0A
    WaterLevelReg = 0x0B
    ControlReg    = 0x0C
    BitFramingReg = 0x0D
    CollReg       = 0x0E
    ModeReg       = 0x11
    TxControlReg  = 0x14
    TxASKReg      = 0x15
    CRCResultRegM = 0x21
    CRCResultRegL = 0x22
    TModeReg      = 0x2A
    TPrescalerReg = 0x2B
    TReloadRegH   = 0x2C
    TReloadRegL   = 0x2D

    def __init__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0
        # GPIO RST-Pin via gpiod -- Pi 5 verwendet gpiochip4 (RP1-Chip)
        self.chip = gpiod.Chip('gpiochip4')
        self.rst_line = self.chip.get_line(self.NRSTPD)
        self.rst_line.request(consumer='rc522', type=gpiod.LINE_REQ_DIR_OUT)
        self.MFRC522_Init()

    def MFRC522_Reset(self):
        self.Write_MFRC522(self.CommandReg, self.PCD_RESETPHASE)

    def Write_MFRC522(self, addr, val):
        self.spi.xfer2([(addr << 1) & 0x7E, val])

    def Read_MFRC522(self, addr):
        val = self.spi.xfer2([((addr << 1) & 0x7E) | 0x80, 0])
        return val[1]

    def MFRC522_Init(self):
        self.rst_line.set_value(1)
        self.MFRC522_Reset()
        self.Write_MFRC522(self.TModeReg,      0x8D)
        self.Write_MFRC522(self.TPrescalerReg, 0x3E)
        self.Write_MFRC522(self.TReloadRegL,   0x1E)
        self.Write_MFRC522(self.TReloadRegH,   0x00)
        self.Write_MFRC522(self.TxASKReg,      0x40)
        self.Write_MFRC522(self.ModeReg,       0x3D)
        self.AntennaOn()

    def AntennaOn(self):
        temp = self.Read_MFRC522(self.TxControlReg)
        if ~(temp & 0x03):
            self.Write_MFRC522(self.TxControlReg, temp | 0x03)

    def MFRC522_Request(self, reqMode):
        self.Write_MFRC522(self.BitFramingReg, 0x07)
        TagType = [reqMode]
        (status, backData, backBits) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, TagType)
        if status != self.MI_OK or backBits != 0x10:
            status = self.MI_ERR
        return (status, backData)

    def MFRC522_Anticoll(self):
        serNumCheck = 0
        serNum = [self.PICC_ANTICOLL, 0x20]
        (status, backData, backBits) = self.MFRC522_ToCard(self.PCD_TRANSCEIVE, serNum)
        if status == self.MI_OK:
            if len(backData) == 5:
                for i in range(4):
                    serNumCheck = serNumCheck ^ backData[i]
                if serNumCheck != backData[4]:
                    status = self.MI_ERR
        return (status, backData)

    def MFRC522_ToCard(self, command, sendData):
        backData = []
        backLen  = 0
        status   = self.MI_ERR
        irqEn    = 0x77 if command == self.PCD_TRANSCEIVE else 0x12
        waitIRq  = 0x30 if command == self.PCD_TRANSCEIVE else 0x10
        self.Write_MFRC522(self.CommIEnReg,   irqEn | 0x80)
        self.Write_MFRC522(self.CommIrqReg,   0x7F)
        self.Write_MFRC522(self.FIFOLevelReg, 0x80)
        self.Write_MFRC522(self.CommandReg,   self.PCD_IDLE)
        for val in sendData:
            self.Write_MFRC522(self.FIFODataReg, val)
        self.Write_MFRC522(self.CommandReg, command)
        if command == self.PCD_TRANSCEIVE:
            self.Write_MFRC522(self.BitFramingReg, 0x80)
        i = 2000
        while True:
            n = self.Read_MFRC522(self.CommIrqReg)
            i -= 1
            if not (i != 0 and not (n & 0x01) and not (n & waitIRq)):
                break
        self.Write_MFRC522(self.BitFramingReg, 0x00)
        if i != 0:
            if (self.Read_MFRC522(self.ErrorReg) & 0x1B) == 0x00:
                status = self.MI_OK
                n = self.Read_MFRC522(self.FIFOLevelReg)
                backLen = self.Read_MFRC522(self.ControlReg) & 0x07
                backLen = (n - 1) * 8 + backLen if backLen != 0 else n * 8
                if n == 0: n = 1
                if n > self.MAX_LEN: n = self.MAX_LEN
                for _ in range(n):
                    backData.append(self.Read_MFRC522(self.FIFODataReg))
        return (status, backData, backLen)

    def cleanup(self):
        self.rst_line.set_value(0)
        self.rst_line.release()
        self.chip.close()
        self.spi.close()
