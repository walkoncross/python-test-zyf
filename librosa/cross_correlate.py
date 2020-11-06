#!/usr/bin/env python
from __future__ import print_function
import json
import numpy as np

import matplotlib.pyplot as plt
import librosa
import librosa.display
from yin import compute_yin


def cross_correlate(audio1, audio2, load_seconds=5, corr_seconds=2, plot=False):
    sig1, sr1 = librosa.load(audio1, duration=load_seconds)
    # if sig1.ndim > 1:
    #     sig1 = sig1[0]
    sig1 -= np.mean(sig1)
    sig1 *= 1.0 / np.max(sig1)

    sig2, sr2 = librosa.load(audio2, duration=load_seconds)
    # if sig2.ndim > 1:
    #     sig2 = sig2[0]
    sig2 -= np.mean(sig2)
    sig2 *= 1.0 / np.max(sig2)

    if sr1 != sr2:
        raise Exception(
            'Input audios do not have the same sample rate!!! ({} vs. {})'.format(sr1, sr2))

    sig_list = [sig1, sig2]
    sr_list = [sr1, sr2]
    start_pos = [0, 0]

    for i, sig in enumerate(sig_list):
        print('---> audio[{}]: '.format(i))
        print('     loaded length: ', sig.shape)
        print('     sample rate: ', sr_list[i])

        for j in range(0, sig.shape[0]):
            if sig[j] != 0:
                start_pos[i] = j
                break

    # start_pos[0] = 0
    # start_pos[1] = 0
    print('start_pos: ', start_pos)
    corr_len = int(corr_seconds * sr1)
    print('corr_len: ', corr_len)

    # sig1_part = sig1[start_pos[0]:start_pos[0]+corr_len*2]
    sig1_part = sig1[start_pos[0]:start_pos[0]+corr_len]

    sig2_part = sig2[start_pos[1]:start_pos[1]+corr_len]
    
    corr_res = np.correlate(sig1_part, sig2_part, mode='same')
    # corr_res = np.correlate(sig1_part, sig2_part, mode='valid')
    print('---> corr_res.shape:{}'.format(corr_res.shape))

    corr_max_pos = np.argmax(corr_res)
    corr_max_pos -= int(corr_res.shape[0] / 2)
    # corr_max_pos = abs(corr_max_pos)
    print('---> corr_max_pos:{}'.format(corr_max_pos))

    align_pos_list = [start_pos[0] + corr_max_pos, start_pos[1]]

    if align_pos_list[0] < 0:
        align_pos_list[1] -= align_pos_list[0]
        align_pos_list[0] = 0

    print(
        '---> align position: sig1[{}] <--> sig2[{}]'.format(align_pos_list[0], align_pos_list[1]))
    print('---> align position in seconds: sig1[{}] <--> sig2[{}]'.format(
        float(align_pos_list[0])/sr1, float(align_pos_list[1])/sr1))

    corr_max = np.max(corr_res)
    corr_res *= 1.0 / corr_max

    if plot:
        plt.figure()
        plt.plot(sig1_part+1, label='audio1[{}:{}]'.format(start_pos[0], start_pos[0]+corr_len))
        plt.plot(sig2_part+2, label='audio2[{}:{}]'.format(start_pos[1], start_pos[1]+corr_len))
        plt.plot(sig1[align_pos_list[0]:align_pos_list[0]+corr_len] + 3, label='align_audio1[{}:{}]'.format(align_pos_list[0], align_pos_list[0]+corr_len))
        plt.plot(sig2[align_pos_list[1]:align_pos_list[1]+corr_len] + 4, label='align_audio2[{}:{}]'.format(align_pos_list[1], align_pos_list[1]+corr_len))
        plt.plot(corr_res, label='corr')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    audio1 = '/Users/zhaoyafei/work/combine_pufa01_new.wav'
    audio2 = '/Users/zhaoyafei/work/demo_pufa_man.wav'

    cross_correlate(audio1, audio2, plot=True)
