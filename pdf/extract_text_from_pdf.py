#!/usr/bin/env python3
# coding=utf-8
# """
# Extract text content from pdf file, and save into a .txt file.

# Author: Zhao Yafei (zhaoyafei0210@gmail.com)
# """
import sys
import os
import os.path as osp
import pdftotext


def extract_text_from_pdf(pdf_fn, output_fn=None, password_protected=False):
    """
    Extract text content from pdf file, and save into a .txt file.

    @params:
        pdf_fn: str
            Path to input .pdf file;
        output_fn: str
            Output file path, default: a .txt file as the same path as .pdf file;
        password_protected: bool
            Whether the .pdf file is password-protectd, default: False

    @return:
        output_fn: str
            Output file path, default: a .txt file as the same path as .pdf file;
    """
    print("===> Input .pdf file: ", pdf_fn)
    if not output_fn:
        # output_fn = osp.splitext(pdf_fn)[0] + '.extracted_text.txt'
        output_fn = pdf_fn + '.extracted_text.txt'
    print("===> output .txt file: ", output_fn)

    # Load your PDF
    # with open("lorem_ipsum.pdf", "rb") as f:
    #     pdf = pdftotext.PDF(f)
    # with open("secure.pdf", "rb") as f:
    #     pdf = pdftotext.PDF(f, "secret")

    # Load your PDF
    # If it's password-protected
    if password_protected:
        with open(pdf_fn, "rb") as f:
            pdf = pdftotext.PDF(f, "secret")
    else:
        with open(pdf_fn, "rb") as f:
            pdf = pdftotext.PDF(f)

    n_pages = len(pdf)

    # How many pages?
    print("===> {} pages in total. ".format(n_pages))

    # Iterate over all the pages
    # for page in pdf:
    #     print(page)

    # Read some individual pages
    if n_pages > 0:
        print("===> Text content extracted from the first page: ")
        print(pdf[0])
        # print(pdf[1])

        # all_text_content = "\n\n".join(pdf)
        # Read all the text into one string
        # print(all_text_content)

    fp_out=open(output_fn, 'w')
    for idx, page in enumerate(pdf):
        fp_out.write('===>[Page {}]\n'.format(idx+1))
        fp_out.write(page + '\n\n')
    fp_out.close()
    
    return output_fn


if __name__ == "__main__":
    import argparse

    def _make_argparser():
        parser=argparse.ArgumentParser(
            description="Extract text content from pdf file, and save into a .txt file.")
        parser.add_argument('pdf_fn', help="Path to input .pdf file")
        parser.add_argument('output', nargs='?', default='', help='Output file path, '
                            'default: a .txt file as the same path as .pdf file ')
        parser.add_argument('--protected', '-p',
                            dest='protected',
                            default=False,
                            action='store_true',
                            help='Whether the .pdf file is password-protectd, default: False')

        return parser

    parser=_make_argparser()
    args = parser.parse_args()

    extract_text_from_pdf(args.pdf_fn, args.output,
                          password_protected=args.protected)
