import math
import numpy as np

#function to generate message signal
def message_signal(t, cosamp, sinamp, cosfreq, sinfreq):
    message = cosamp * np.cos(2 * np.pi * cosfreq * t) + sinamp * np.sin(2 * np.pi * sinfreq * t)
    return message

#message signal properties
cosfreq = 125 #Hz
sinfreq = 35 #Hz
cosamp = -1
sinamp = 1

bandwith = max(cosfreq, sinfreq) #Hz
sampling_frequency = 2 * 1.5 * bandwith #Hz
duration = 2 #s

t_values = np.arange(start = 0, stop = duration * sampling_frequency) / sampling_frequency

message_samples = message_signal(t_values,cosamp,sinamp,cosfreq,sinfreq)

#peak value of the filter was not specified so I chose the peak value of the signal
amplitude_pmax = np.amax(message_samples)
amplitude_nmax = np.amin(message_samples)

#PCM properties

L = 64
no_of_bits = int(math.log2(L))
level_limits = np.linspace(amplitude_pmax, amplitude_nmax, L + 1)

#half of the difference between two consecutive levels
interval = ((amplitude_pmax - amplitude_nmax) / L) / 2

#an empty memory
quantized_message = np.zeros_like(message_samples)

#this loop takes the value where difference is smaller than the interval that is specified above
#top level is labeled 0, the bottom level is labeles 63
for i in range(len(message_samples)):
    difference = np.abs(message_samples[i] - level_limits)
    quantized_level = np.where(difference <= interval)[0]
    quantized_message[i] = quantized_level[0]


output = [(np.binary_repr(int(quantized_message[i]), no_of_bits)) for i in range(10)]
print(*output, sep="-")


#delta modulation
delta_sampling_frequency = 2 * 6 * bandwith #Hz

t_values_delta = np.arange(start = 0, stop = duration * delta_sampling_frequency) / delta_sampling_frequency
message_sample_delta = message_signal(t_values_delta,cosamp,sinamp,cosfreq,sinfreq)
#step size
delta_epsilon = 0.35

#memory for modulated signal
modulated = np.zeros((len(message_sample_delta),1))
#memory for delta signal
dm_signal = np.zeros_like(modulated)

#this loop starts from 1 because delta signal equals to 0 at t=0
#if difference between mesage signal and modulated signal is smaller than zero it adds delta epsilon vice versa
#then it sets the next modulated signal to previous one
for i, amplitude in enumerate(message_sample_delta[1:]):
    difference = amplitude - modulated[i]
    if difference < 0:
        modulated[i] -= delta_epsilon
        dm_signal[i] = 0
    else:
        modulated[i] += delta_epsilon
        dm_signal[i] = 1
    modulated[i+1] = modulated[i]


output = [dm_signal[i] for i in range(0,20)]
print(*output, sep='-')


