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
        os.makedirs(save_dir)    #pdf_content = open("some_doc.pdf", "rb").read()
    
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

    for idx, match in enumerate(all_matches):
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
            print('decoded_stream[:64]:')
            print(decoded_stream[:64])

            fp = open(save_fn, 'wb')
            fp.write(decoded_stream)
            fp.close()


if __name__=='__main__':
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