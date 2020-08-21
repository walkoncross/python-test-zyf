#!/usr/bin/env python3
# coding=utf-8
# """
# Convert pages in .pdf file into .jpg images.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import sys
import os
import os.path as osp

import tempfile
from pdf2image import convert_from_path


def convert_pdf_pages_to_images(pdf_fn, save_dir='./'):
    """
    Extract text content from pdf file, and save into a .txt file.

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
        os.makedirs(save_dir)

    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(
            pdf_fn, output_folder=path)

    base_pdf_fn = os.path.splitext(os.path.basename(pdf_fn))[0]

    for idx, page_img in enumerate(images):
        print('---> save page #{:03d}'.format(idx+1))
        print('---> type(page_img): ', type(page_img))
        save_fn = os.path.join(
            save_dir, base_pdf_fn + '_page{:03d}.jpeg'.format(idx+1))
        page_img.save(save_fn, 'JPEG')

        print('---> Image saved into: ', save_fn)


if __name__ == '__main__':
    import argparse

    def _make_argparser():
        parser = argparse.ArgumentParser(
            description="Extract text content from pdf file, and save into a .txt file.")
        parser.add_argument('pdf_fn', help="Path to input .pdf file")
        parser.add_argument('save_dir', nargs='?', default='./pdf_converted_images/', help='Output dir, '
                            'default: ./pdf_converted_images/')

        return parser

    parser = _make_argparser()
    args = parser.parse_args()

    convert_pdf_pages_to_images(args.pdf_fn, args.save_dir)
