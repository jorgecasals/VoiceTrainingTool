class SoundAnalyzer:
    def __init__(self):
        pass

    def CalculateLtas(self, sound, bandwidth):
        autoSpectrum = self.sound_to_spectrum(sound, True)
        autoLtas = self.spectrum_to_ltas(autoSpectrum.get(), bandwidth)
        self.apply_correction()

        return autoLtas

    def apply_correction(self):
        pass
        #correction = -10.0 * log10(thy dx * my nx * my dx)
        #for (iband = 1; iband <= his nx; iband ++):
        #    his z[1][iband] += correction

    def sound_to_spectrum(self, sound, boolean):
        return 5

    def spectrum_to_ltas(self, spectrum, bandwidth):
        return 6