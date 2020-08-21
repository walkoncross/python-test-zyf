#!/usr/bin/env python3
# coding=utf-8
# """
# Merge multiple .input pdf files into one output .pdf file.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import sys
import os
import os.path as osp

from PyPDF2 import PdfFileMerger


def merge_pdfs(pdf_files, save_fn):
    """
    Extract text content from pdf file, and save into a .txt file.

    @params:
        pdf_files: list of str
            List of .pdf file paths;
        save_fn: str
            Output file name;

    @return:
        No returns.

    """

    print("===> Input .pdf files: ", pdf_files)
    if osp.isfile(save_fn):
        print("===> output .pdf file already exists: ", save_fn)
        exit(-1)
    print("===> output .pdf file: ", save_fn)

    merger = PdfFileMerger()
    
    for pdf in pdf_files:
        merger.append(pdf)
    
    merger.write(save_fn)
    print('===> Saved output .pdf file')


if __name__ == '__main__':
    import argparse

    def _make_argparser():
        parser = argparse.ArgumentParser(
            description="Merge multiple .input pdf files into one output .pdf file.")
        parser.add_argument('pdf_files', nargs='+', help="Input .pdf files")
        parser.add_argument('--output', '-o', 
                            dest='save_fn', 
                            type=str,
                            default='./merged.pdf', 
                            help='Output filename for merged pdf, '
                            'default: ./merged.pdf')

        return parser

    parser = _make_argparser()
    args = parser.parse_args()

    merge_pdfs(args.pdf_files, args.save_fn)
