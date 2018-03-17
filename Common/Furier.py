import Entities.Spectrum.Spectrum as Spectrum
import Entities.SpectrumValue.SpectrumValue as SpectrumValue
import Entities.Sound.Sound as Sound

#Encapsulates the furier funcionality and all the technical situations.
#It is the bridge between our application and all furier related stuff
class Furier:
    def __init__(self):
        pass

    def apply(self, sound):
        spectrum = Spectrum(sound)

        #TODO, make it fast passing the minor greater than sound.samples 2 power
        samples_total = sound.get_samples_total()


        return spectrum

    def invert(self, spectrum):
        pass
