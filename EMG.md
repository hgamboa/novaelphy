EMG
---
_by Maria Marta Santos and Hugo Gamboa_

###Physiological Principal

A motor neuron receives an electrical signal form the Central Nervous System, which is transmitted through 
motor fibers and a skeletal muscle contraction occurs. The signal is transmitted by diffusion, generating a 
cascade of electrophysiological and physiological events - nervous impulse. [1], [2]


###Sensor working principle

To obtain an EMG signal is necessary to monitor muscle activation. Therefore, two electrodes are positioned on the 
skin over the muscle of interest, in order to measure the difference of potential between them and acquire and amplify 
the signal. [1], [3] This is preferred to the more invasive method of insert needle electrodes into the muscle. [4]


###The signal - Image

![EMG signal](/EMG.png)

Examples of sEMG signal recorded, during the same contraction, with different spatial filter configurations. [5]


### Characteristics

* Frequency band: 25HZ to 450Hz
* Amplitude: 1mV
* Noise imunity (snr): ~90dB   

###Features

#### Real time 
* activation intensity
* contraction’s duration
* variability
* biofeedback information


#### Time domain:
* Mean Absolut value;
* Zero-crossing
* Slope sign changes
* Waveform length
* Willison amplitude
* Variance
* v-Order
* Autoregression coefficients
* others [6],[7]

#### Frequency domain:
* Signal-to-noise ratio
* Spectral moments
* Frequency ratio 
* Total power
* others [6],[7]


###Signal processing algorithms

Low level processing:

Time-domain:
* Rectification (half wave or full wave)
* Filters (butter band pass filter of 30 – 2000 Hz)

Frequency domain
* Frequency spectra (FFT analysis) [1]

Higher level processing
* Coherence
* Phase Locking Factor
* Wavelet analysis
[1],[2]


###Use cases

* neurology
* rehabilitation
* orthopedics (example: EHW chip development for prosthetic hand control)
* ergonomics
* sports
* diagnostic tool [2],[3]:
  * neuromuscular diseases
  * low back pain assessment
  * kinesiology
  * disorders of motor control



###References

[1] Camara, Mafalda (2013) Coherence and Phase Locking Disruption in Electromyograms of Patients with Amyotrophic Lateral Sclerosis - Dissertation to Obtain Master Degree in Biomedical Engineering, Faculdade de Ciências e Tecnologia da Universidade Nova de Lisboa

[2] Reaz, B. I., Hussain, M. S., Mohd-Yasin, F. (2006) Techniques of EMG signal analysis: detection, processing, classification and applications, Biol. Proced. Online 2006; 8(1): 11-35.

[3] Plux Wireless Biosignals SA - catalog

[4] Siriprayoonsak, Saksit (2005) Real-Time Measurement of Prehensile EMG Signals, San Diego State University

[5] Merletti, Roberto; Botter, Alberto; Troiano, Amedeo; Merlo, Enrico; Minetto, Marco Alessandro (2009) Technology and instrumentation for detection and conditioning of the surface electromyographic signal: State of the art, Clinical Biomechanics 24. 122–134

[6] Tkach, Dennis; Huang, He; Kuiken, Todd A (2010) Study of stability of time-domain features for electromyographic pattern recognition. Tkach et al. Journal of NeuroEngineering and Rehabilitation. 7:21

[7] Phinyomark, Angkoon; Quainea, Franck; Charbonniera, Sylvie; Servierea, Christine; Tarpin-Bernardb, Franck; Laurillaub, Yann. EMG Feature Evaluation for Improving Myoelectric Pattern Recognition Robustness

