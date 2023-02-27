from SoapySDR import Device
import numpy
from SoapySDR import *  # SOAPY_SDR_ constants


class SDRPlaySource:
    sample_rate = 2.4e6
    freq = 7101500
    gain = 30
    buff_size = 1024 * 64
    bandwidth = 192e3
    mode = 'SSB'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        driver = dict(driver="sdrplay")
        self.sdr = Device(driver)
        self.sdr.setGainMode(SOAPY_SDR_RX, 0, False)
        self.sdr.setGain(SOAPY_SDR_RX, 0, self.gain)
        self.sdr.setSampleRate(SOAPY_SDR_RX, 0, self.sample_rate)
        self.sdr.setBandwidth(SOAPY_SDR_RX, 0, self.bandwidth)
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, self.freq)
        self.rxStream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
        self.sdr.activateStream(self.rxStream)  # start streaming
        self.buff = numpy.array([0]*self.buff_size, numpy.complex64)

    def readStream(self):
        return self.sdr.readStream(self.rxStream, [self.buff], len(self.buff)), self.buff

    @property
    def frequency(self):
        return self.sdr.getFrequency(SOAPY_SDR_RX, 0)

    @frequency.setter
    def frequency(self, freq):
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, freq)
