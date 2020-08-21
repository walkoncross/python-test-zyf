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


def extract_images_from_pdf(pdf_fn, save_dir='./'):
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

    n_pages = pdf.getNumPages()
    print('===> {} pages intotal'.format(n_pages))

    img_count = 0
    for i in range(n_pages):
        print('===> page #{:03d}: '.format(i+1))

        page = pdf.getPage(i)
        print('---> type(page): ', type(page))

        if '/XObject' in page['/Resources']:
            xObject = page['/Resources']['/XObject'].getObject()
            print('---> type(xObject): ', type(xObject))

            for obj in xObject:
                print('---> type(obj): ', type(obj))

                if xObject[obj]['/Subtype'] == '/Image':
                    img_count += 1
                    print('---> image #{:3d}'.format(img_count))
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].getData()
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"

                    save_fn_base = osp.join(save_dir, obj[1:])
                    if '/Filter' in xObject[obj]:
                        print('---> filter type:', xObject[obj]['/Filter'])

                        if xObject[obj]['/Filter'] == '/DCTDecode':
                            img = open(save_fn_base + ".jpg", "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/JPXDecode':
                            img = open(save_fn_base + ".jp2", "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/CCITTFaxDecode':
                            img = open(save_fn_base + ".tiff", "wb")
                            img.write(data)
                            img.close()
                        elif xObject[obj]['/Filter'] == '/FlateDecode':
                            try:
                                img = Image.frombytes(mode, size, data)
                                img.save(save_fn_base + ".png")
                            except:
                                print('===> Not a valid .png image')
                    else:
                        try:
                            img = Image.frombytes(mode, size, data)
                            img.save(save_fn_base + ".png")
                        except:
                            print('===> Not a valid .png image')
        else:
            print("No image found.")


if __name__ == '__main__':
    # if (len(sys.argv) != 2):
    #     print("\nUsage: python {} input_file\n".format(sys.argv[0]))
    #     sys.exit(1)

    # pdf_fn = sys.argv[1]
    # extract_images_from_pdf(pdf_fn)
    import argparse

    def _make_argparser():
        parser = argparse.ArgumentParser(
            description="Extract all images from .pdf file into .txt files.")
        parser.add_argument('pdf_fn', help="Path to input .pdf file")
        parser.add_argument('save_dir', nargs='?', default='./pdf_extracted_images/', help='Output dir, '
                            'default: ./pdf_extracted_images/')

        return parser

    parser = _make_argparser()
    args = parser.parse_args()

    extract_images_from_pdf(args.pdf_fn, args.save_dir)

    
