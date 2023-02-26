import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import sounddevice as sd
import scipy.signal as signal


def ssb_demod(samples, freq, rate):
    # Create a complex exponential to shift the signal to baseband
    t = numpy.arange(len(samples))
    shift = numpy.exp(-1j * 2 * numpy.pi * freq * t / rate)
    baseband = samples * shift

    # Use a Hilbert transform to create the complex envelope
    envelope = numpy.abs(numpy.imag(numpy.fft.ifft(numpy.fft.fft(baseband) * 2 * numpy.pi * 1j * numpy.concatenate(
        [numpy.arange(len(baseband) // 2), numpy.arange(-len(baseband) // 2, 0)]))))

    # Decimate the envelope to the audio rate
    audio_rate = 8000
    decimation_factor = int(rate / audio_rate)
    audio = envelope[::decimation_factor]
    return audio

#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results:
    print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="sdrplay")
sdr = SoapySDR.Device(args)

#query device info
print(sdr.listAntennas(SOAPY_SDR_RX, 0))
print(sdr.listGains(SOAPY_SDR_RX, 0))
sdr.setGainMode(SOAPY_SDR_RX, 0, False)
sdr.setGain(SoapySDR.SOAPY_SDR_RX, 0, 30)

freqs = sdr.getFrequencyRange(SOAPY_SDR_RX, 0)
for freqRange in freqs:
    print(freqRange)

#apply settings
sdr.setSampleRate(SOAPY_SDR_RX, 0, 1e6)
sdr.setFrequency(SOAPY_SDR_RX, 0, 7e6)

#setup a stream (complex floats)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
sdr.activateStream(rxStream) #start streaming

#create a re-usable buffer for rx samples
buff = numpy.array([0]*1024, numpy.complex64)

#receive some samples
while True:
    sr = sdr.readStream(rxStream, [buff], len(buff))
    demod = buff * numpy.exp(-1j * 2 * numpy.pi * 7.2e6 / 2e6 * numpy.arange(1024))
    sd.play(demod.real, 48000)
    sd.wait()

#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming