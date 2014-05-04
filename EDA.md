EDA – Electrodermal Activity Signal
-----------------------------------


###Physiology
Temperature regulation, emotion and cognitive processing activate the sympathetic chain resulting in the production of sweat by the eccrine sweat glands. This leads to alterations in the skin electrical conductivity quantified by the electrodermal activity (EDA). [1], [2]



###EDA Sensor Working Principle
This sensor measure skin impedance and include low noise signal conditioning and amplification circuitry. [5]

### Steps
1. Prepare. Select two spots on the hand or finger palm. The surfaces
   should not touch each other. 

2. No movement should occur on the monitored hand.    

3. Connect. Ask 7*8, and see the reaction on opensignals.


#### Trouble shooting

* ***Saturation***: The level of the signal may be to high for some persons
with sweting hands. Try to dry the hands with some tissue or paper.

* ***Low signal***: Some persons react very little, and the physiological reaction may be very weak. The signals should be amplified to detect events.



###The Signal
![EDA signal](http://www.biosignalsplux.com/downloads/bitalino_manual/img/sensor-02.png)

EDA signal is composed by two parts:
* Tonic activity or electrodermal level (EDL) or skin conductance level (SCL) - related to the thermal regulation and expressed by very low frequency base variations 
* Phasic activity or electrodermal response (EDR) or skin conductance response (SCR) – related to exterior stimuli and expressed by fast changing variations in the signal. 
[1], [2]


###Real Time features
To detection stimuli responses the most important features are:
* Amplitude
* Latency [2], [4]


###Long Time features
Detection of stimuli responses by clustering with the same features as in real time.


###Signal Processing Algorithms
1.	filter the signal with low pass filter (2-5 Hz)
2.	detect second order derivative zeros 
3.	for each pair of zeros: compute a, b and t0
4.	compute SCL


###Use cases
Chirurgic procedures like Endoscopic Thoracic Sympathectomy (ETS) [5]

Psychophysiological Investigations (analyze changes in attention, cognition and emotion). For example studies in Depersonalization Disorder [3]


###References
1. H. Gamboa, A. Fred, An Electrodermal Activity Phsycophysiological Model, Proceedings of Med-e-Tel 2007, Luxembourg, April 2007.
2. Silva H, Fred A, Lourenco A. Electrodermal response propagation time as a potential psychophysiological marker. Engineering in Medicine and Biology Society (EMBC), 2012 Annual International Conference of the IEEE [Internet]. 2012 [cited 2013 Nov 14]. p. 6756–9. 
3. Schoenberg P, Sierra M, David A. Psychophysiological Investigations in Depersonalization Disorder and Effects of Electrodermal Biofeedback. Journal of Trauma & Dissociation. 2012 May;13(3):311–29. 
4. Green S, Kragel P, Fecteau M, LaBar K. Development and validation of an unsupervised scoring system (Autonomate) for skin conductance response analysis. International Journal of Psychophysiology [Internet]. 2013 [cited 2013 Nov 14]; Available from: http://www.sciencedirect.com/science/article/pii/S0167876013003103
5. Catálogo PLUX
