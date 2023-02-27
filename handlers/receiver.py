import numpy as np
import sounddevice as sd
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from scipy import signal
from source.sdrplay import SDRPlaySource


class SDRHandler(QObject):
    running = False
    update_sample = pyqtSignal(object, object)
    sdr = SDRPlaySource()
    blocksize = sdr.buff_size - 1024
    stream = sd.OutputStream(channels=1, blocksize=blocksize, dtype='float32', latency='high', dither_off=False)
    stream.start()

    def run(self):
        while True:
            sr, rx_samples = self.sdr.readStream()
            demod = self.ssb_demodulate(self.normArr(rx_samples), self.sdr.frequency, self.sdr.sample_rate)
            self.stream.write(np.ascontiguousarray(demod))
            self.update_sample.emit(sr, rx_samples)
            QThread.msleep(1)

    def normArr(self, arr):
        if np.max(np.abs(arr)) != 0:
            arr = arr / np.max(np.abs(arr))
        return arr
    def decimate(self, samples, sample_rate):
        return signal.decimate(samples, int(sample_rate / 48000), zero_phase=True)

    def ssb_demodulate(self, samples, fc, fs):
        # Create a complex heterodyne mixer
        t = np.arange(len(samples)) / fs
        mixer = np.exp(-1j * 2 * np.pi * fc * t)
        # Mix the SSB signal with the mixer
        mixed = samples * (mixer)
        # Take the real part of the mixed signal to remove the carrier
        demodulated = np.real(mixed)
        # Apply a low-pass filter to remove high-frequency noise or distortion
        nyquist = fs / 2
        cutoff = 2.4e3 / nyquist
        b, a = signal.butter(6, cutoff, 'lowpass')
        filtered = signal.filtfilt(b, a, demodulated)
        decimated = self.decimate(filtered, fs)
        return decimated.astype(np.float32)