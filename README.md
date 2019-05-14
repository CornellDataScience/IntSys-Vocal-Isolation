# IntSys-Vocal-Isolation

Given a mixture of background music and a speaker's voice, we want to separate the music from the pure human voice. The dataset is assumed to be composed of text-audio pairs, with most audio examples being voice-music mixtures and a small portion being pure voice recordings.

We apply two approaches to achieve this goal:

- **Wave-U-Net** is a fully supervised neural network architecture that works with pure waveforms as input and output (as opposed to spectrograms) in order to separate one audio input into multiple audio outputs ([link to paper](https://arxiv.org/abs/1806.03185)).
- **SVSGAN** is a semi-supervised model that uses GAN architecture to generate magnitude spectrogram of vocal and music from that of their mixture. The generated spectrogram is then combined with the phase spectrogram of mixture to generate the waveform through Inverse Short-Time Fourier Transform (ISTFT) ([link to paper](https://arxiv.org/abs/1710.11428)).

Team Members: Magd Bayoumi, Qian Huang, Xiuyu Li, Zhao Shen, Guandao Yang