#!/usr/bin/env python2
# coding=utf-8
# """
# Extract info data from decoded pdf content stream.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
from __future__ import print_function
import sys
import os
import os.path as osp

import re
import zlib




def plot_and_save_data(x_values, y_values, fig_fname):
    plt.figure()

    plt.subplot(3, 1, 1)
    plt.scatter(x_values, y_values)

    plt.subplot(3, 1, 2)
    plt.plot(y_values)

    plt.subplot(3, 1, 3)
    plt.plot(x_values)

    plt.savefig(fig_fname)

    # plt.show()    


def extract_info_data(lines, save_fn, do_plot=True, save_sub_tsv_files=True):
    sig_names = [
        'I', 'II', 
        'V1', 'V2', 'V3',
        'V4', 'V5', 'V6',
        'III',
        'aVR', 'aVL', 'aVF',
        'II-1000']
    
    sig_start_level_idx = [
        0, 1,
        0, 1, 2,
        0, 1, 2,
        2,
        0, 1, 2,
        3
    ]

    idx = 0
    # lines = lines.split('\n')
    n_lines = len(lines)
    print('n_lines: ', n_lines)

    # flag = False

    write_lines = []
    while idx < n_lines:
        # # line_ = lines[idx].decode('utf-8')
        line_ = lines[idx].strip()
        # # print('line: ', line_)
        # # print(line_[0])
        # # print(line_[1])
        # # print(line_[2])
        # # print(line_[3])

        # if line_.endswith('0 G'):
        #     # print('line: ', line_)
        #     # flag = True
        #     idx += 1
        #     line_ = lines[idx].strip()
        #     line_1 = lines[idx+1].strip()
        #     while (line_.endswith(' m')
        #             and line_1.endswith(' l')):
        #         write_lines.append(line_.replace(
        #             ' ', '\t'))  # for the line ending with ' m'
        #         idx += 3
        #         line_ = lines[idx].strip()
        #         line_1 = lines[idx+1].strip()

        #     # for the line ending with " l"
        #     write_lines.append(line_1.strip().replace(' ', '\t'))
        #     # flag = False
        #     idx -= 3
        # else:
        #     idx += 1

        if line_.endswith(' m'):
            line_1 = lines[idx+1].strip()

            if line_1.endswith(' l'):
                write_lines.append(line_.replace(
                    ' ', '\t'))  # for the line ending with ' m'

                if not lines[idx+3].strip().endswith(' m'):
                    # for the line ending with " l"
                    write_lines.append(line_1.replace(' ', '\t'))
                    # flag = False
                    idx += 2
                else:
                    idx += 3
            else:
                idx += 1
        else:
            idx += 1

    print("===> len(write_lines) = ", len(write_lines))
    n_outlineer_pts = len(write_lines)-249*12-1000
    print("===> len(write_lines)-249*12-1000 = ",  n_outlineer_pts)

    fp = open(save_fn, 'w')
    write_contents = '\n'.join(write_lines) + '\n'
    fp.write(write_contents)
    fp.close()

    #######################
    # Convert data points into float
    x_list = []
    y_list = []

    for line in write_lines:
        line_splits = line.split('\t')
        x_list.append(float(line_splits[1]))
        y_list.append(float(line_splits[0]))
    
    start_levels = []
    for i in range(4):
        start_levels.append(y_list[87+i*5])
    print('===> start_levels: ', start_levels)
    #######################

    info_dict = dict()
    save_fn_base = osp.splitext(save_fn)[0]
    start_idx = 121

    for i in range(0, 13):
        end_idx = start_idx+249
        if i==12:
            end_idx = len(write_lines)

        x_values = np.array(x_list[start_idx: end_idx])
        y_values = np.array(y_list[start_idx: end_idx])

        x_values -= x_values[0]
        start_level = start_levels[sig_start_level_idx[i]]
        tmp_np = np.full_like(y_values, start_level)
        y_values = tmp_np - y_values

        info_dict[sig_names[i]] = {
            'time_stamps': x_values.tolist(),
            'values': y_values.tolist()
        }

        sub_fn_base = save_fn_base + '.sig-{}'.format(sig_names[i])

        if save_sub_tsv_files:
            fp = open(sub_fn_base+'.tsv', 'w')
            write_contents = '\n'.join(
                write_lines[start_idx: end_idx]) + '\n'
            fp.write(write_contents)
            fp.close()

        if do_plot:
            fig_fname = sub_fn_base + '.png'
            plot_and_save_data(x_values, y_values, fig_fname)

        start_idx += 249


    assert n_outlineer_pts == 121

    save_json_fn = save_fn_base + '.json'
    fp = open(save_json_fn, 'w')
    # json.dump(info_dict, fp, indent=2)
    json.dump(info_dict, fp, sort_keys=True)
    fp.close()


if __name__ == '__main__':
    import argparse

    def _make_argparser():
        parser = argparse.ArgumentParser(
            description="Extract info data from decoded pdf content stream.")
        parser.add_argument('input', help="Path to input file")
        parser.add_argument('save_fn', nargs='?', default='', help='Output filename'
                            'default: <input>.info_data.tsv')

        return parser

    parser = _make_argparser()
    args = parser.parse_args()

    fp = open(args.input, 'rb')
    contents = fp.read()
    # contents = ''.join(contents)
    contents_lines = contents.split('\n')
    print('contents_lines[:5]: ', contents_lines[:5])
    fp.close()

    if not args.save_fn:
        save_fn = args.input + '.info_data.tsv'
    else:
        save_fn = args.save_fn

    extract_info_data(contents_lines, save_fn)
