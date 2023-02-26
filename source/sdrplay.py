import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy


class SDRPlaySource:
    sample_rate = 2.4e6
    freq = 7e6
    gain = 30
    buff_size = 2048
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        driver = dict(driver="sdrplay")
        self.samples = numpy.array([0]*1024, numpy.complex64)
        self.sdr = SoapySDR.Device(driver)
        self.sdr.setGainMode(SOAPY_SDR_RX, 0, False)
        self.sdr.setGain(SoapySDR.SOAPY_SDR_RX, 0, self.gain)
        self.sdr.setSampleRate(SOAPY_SDR_RX, 0, self.sample_rate)
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, self.freq)
        self.rxStream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
        self.sdr.activateStream(self.rxStream)  # start streaming
        self.buff = numpy.array([0]*self.buff_size, numpy.complex64)

    def readStream(self):
        return self.sdr.readStream(self.rxStream, [self.buff], len(self.buff)), self.buff


