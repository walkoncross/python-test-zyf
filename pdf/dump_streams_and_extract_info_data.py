#!/usr/bin/env python2
# coding=utf-8
# """
# Dump all FlateDecode streams in .pdf file into .txt files.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
from __future__ import print_function
import sys
import os
import os.path as osp

import re
import zlib


def extract_info_data(lines, save_fn):
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

    fp = open(save_fn, 'w')
    write_contents = '\n'.join(write_lines) + '\n'
    fp.write(write_contents)
    fp.close()


def dump_streams_in_pdf(pdf_fn, save_dir='./', ):
    """
    Dump all FlateDecode streams in .pdf file into .txt files.

    @params:
        pdf_fn: str
            Path to input .pdf file;
        save_dir: str
            Output file path;

    @return:
        No returns.

    """
    print("===> Input .pdf file: ", pdf_fn)
    if not osp.isdir(save_dir):
        os.makedirs(save_dir)
    print("===> output .txt file: ", save_dir)

    if not osp.isdir(save_dir):
        # pdf_content = open("some_doc.pdf", "rb").read()
        os.makedirs(save_dir)

    fp = open(pdf_fn, "rb")
    pdf_content = fp.read()
    fp.close()

    stream_pattern = re.compile(r'/Filter(.*?)>>.*?stream(.*?)endstream', re.S)

    # match = stream_pattern.search(pdf_content)

    # all_matches = stream_pattern.findall(str(pdf_content))
    all_matches = stream_pattern.findall(pdf_content)

    # match = all_matches[0]
    n_matches = len(all_matches)
    print('===> {} filter streams found'.format(n_matches))

    pdf_fn_base = osp.splitext(osp.basename(pdf_fn))[0]
    save_fn_prefix = osp.join(save_dir, pdf_fn_base)

    for idx, match in enumerate(all_matches[0:1]):
        print('===> Deflate stream #{:03d}: '.format(idx+1))
        # print('match: ', match)
        filter_type_str = match[0].strip()
        splits = filter_type_str.split('/')
        filter_tpyes = []
        for it in splits:
            it = it.strip()
            if it.endswith('Decode'):
                filter_tpyes.append(it)
        print('filter_type_str: ', filter_type_str)
        print('filter types:', filter_tpyes)

        if filter_tpyes[0] == 'FlateDecode':
            # s = pdf_content[match.pos:match.endpos]
            save_fn = save_fn_prefix + '.stream_{:03d}.txt'.format(idx+1)
            stream = match[1]
            stream = stream.strip('\r\n')

            print("stream_length=", len(stream))

            # decoded_stream = zlib.decompress(bytes(stream))
            decoded_stream = zlib.decompress(stream)
            # print('decoded_stream[:64]:')
            # print(decoded_stream[:64])

            fp = open(save_fn, 'wb')
            fp.write(decoded_stream)
            fp.close()

            decoded_lines = decoded_stream.split('\n')
            save_fn2 = save_fn_prefix + \
                '.stream_{:03d}.info_data3.tsv'.format(idx+1)
            extract_info_data(decoded_lines, save_fn2)


if __name__ == '__main__':
    import argparse

    def _make_argparser():
        parser = argparse.ArgumentParser(
            description="Dump all FlateDecode streams in .pdf file into .txt files.")
        parser.add_argument('pdf_fn', help="Path to input .pdf file")
        parser.add_argument('save_dir', nargs='?', default='./pdf_dumped_streams/', help='Output dir, '
                            'default: ./pdf_dumped_streams/')

        return parser

    parser = _make_argparser()
    args = parser.parse_args()

    dump_streams_in_pdf(args.pdf_fn, args.save_dir)
