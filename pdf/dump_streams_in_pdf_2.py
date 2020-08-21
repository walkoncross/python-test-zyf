#!/usr/bin/env python2
# coding=utf-8
"""
Extract all images from .pdf file into .txt files.
Author: Zhao Yafei (zhaoyafei0210@gmail.com)

Adapted from https://github.com/mstamy2/PyPDF2/blob/master/Scripts/pdf-image-extractor.py
Extract images from PDF without resampling or altering.

Which is adapted from work by Sylvain Pelissier
http://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python

"""
import sys
import os
import os.path as osp
import PyPDF2
from PIL import Image


def dump_streams_from_pdf(pdf_fn, save_dir='./'):
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

    pdf = PyPDF2.PdfFileReader(open(pdf_fn, "rb"))
    print('===> type(pdf): ', type(pdf))

    pdf_fn_base = osp.splitext(osp.basename(pdf_fn))[0]

    print("---> pdf:  \n", pdf)

    n_pages = pdf.getNumPages()
    print('===> {} pages intotal'.format(n_pages))

    stream_count = 0
    for i in range(n_pages):
        print('===> page #{:03d}: '.format(i+1))

        page = pdf.getPage(i)
        print('---> type(page): ', type(page))
        print('---> page:  \n', page)

        contents = page['/Contents'].getObject()
        print('---> type(contents): ', type(contents))
        print('---> contents: \n', contents)

        if '/Filter' in contents:
            print('---> filter type:', contents['/Filter'])

            if contents['/Filter'] == '/FlateDecode':
                stream_count += 1
                print('---> stream #{:3d}'.format(stream_count))

                data = contents.getData()
                save_fn = osp.join(
                    save_dir, pdf_fn_base + '.deflate_stream.{:03d}.txt'.format(stream_count))
                
                fp = open(save_fn, 'w')

                contents_str = str(data)
                contents_str = contents_str.replace('\\n', '\n')
                fp.write(contents_str)

                # n_bytes = 512
                # for i in range(0, len(data), n_pages):
                #     tmp_str = str(data[i:i+n_bytes])
                #     tmp_str = tmp_str.replace('\\n', '\n')
                #     fp.write(tmp_str)

                fp.close()
                # img = Image.frombytes(mode, size, data)
                # img.save(save_fn_base + ".png")


if __name__ == '__main__':
    import argparse

    def _make_argparser():
        parser = argparse.ArgumentParser(
            description="Dump all FlateDecode streams in .pdf file into .txt files.")
        parser.add_argument('pdf_fn', help="Path to input .pdf file")
        parser.add_argument('save_dir', nargs='?', default='./pdf_dumped_streams_2/', help='Output dir, '
                            'default: ./pdf_dumped_streams_2/')
        return parser

    parser = _make_argparser()
    args = parser.parse_args()

    dump_streams_from_pdf(args.pdf_fn, args.save_dir)
