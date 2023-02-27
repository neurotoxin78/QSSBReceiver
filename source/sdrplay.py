from SoapySDR import Device, errToStr
import numpy
from SoapySDR import *  # SOAPY_SDR_ constants


class SDRPlaySource:
    sample_rate = 2.4e6
    freq = 7e6
    gain = 30
    buff_size = 1024 * 64
    bandwidth = 200e3
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
        #sampleRates = self.sdr.getSampleRateRange(SOAPY_SDR_RX, 0)
        #for srRange in sampleRates: print(srRange)
        bands = self.sdr.getBandwidthRange(SOAPY_SDR_RX, 0)
        for b in bands: print(b)
        self.rxStream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [0])
        self.sdr.activateStream(self.rxStream, 0, 0, int(self.buff_size))  # start streaming
        self.buff = numpy.array([0]*self.buff_size, numpy.complex64)

    def readStream(self):
        status = self.sdr.readStream(self.rxStream, [self.buff], len(self.buff), timeoutUs=int(1e6))
        # stash time on first buffer

        return status, self.buff

    @property
    def frequency(self):
        return self.sdr.getFrequency(SOAPY_SDR_RX, 0)

    @frequency.setter
    def frequency(self, freq):
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, freq)
