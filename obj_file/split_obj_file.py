#!/usr/bin/env python3
# coding=utf-8

"""Split .obj file containing multiple polygon meshes into multiple .obj file (with name base_name+'_split_%d.obj').

Author: zhaoyafei0210@gmail.com
"""

from __future__ import print_function
import sys
import os
import os.path as osp
import json


def split_obj_file(obj_fn):
    """Split .obj file containing multiple polygon meshes into multiple .obj file (with name base_name+'_split_%d.obj').

    Args:
        obj_fn: str
            Path to input .obj file

    Return:
        No return.
    """
    prefix_lines = [
    ]  # lines before the first v_line (line starting with 'v ')
    mtllib_list = []  # lines starts with 'mtllib '

    line_cnt = 0    # count for all lines

    o_list = []      # lines starts with 'o '
    s_list = []      # lines starts with 's '
    g_list = []      # lines starts with 'g '
    usemtl_list = []      # lines starts with 'usemtl '

    v_cnt = 0   # line count for all vertex
    vt_cnt = 0  # line count for all vertex texture coordinates
    vn_cnt = 0  # line count for all vertex normals
    f_cnt = 0   # line count for all faces

    v_cnt_till_last_mesh = 0
    vt_cnt_till_last_mesh = 0
    vn_cnt_till_last_mesh = 0

    f_cnt_till_last_mesh = 0

    vx_cnt_till_last_mesh = [
        v_cnt_till_last_mesh,
        vt_cnt_till_last_mesh,
        vn_cnt_till_last_mesh
    ]

    obj_cnt = 0  # count how many polygon meshes
    is_last_line_vline = 0

    base_name, _ = osp.splitext(obj_fn)

    fp_out = None

    with open(obj_fn, 'r') as fp:
        for line in fp:
            line_cnt += 1

            if line.startswith('mtllib '):
                mtllib_list.append('line #{}: '.format(line_cnt) + line)
                is_last_line_vline = 0
            elif line.startswith('o '):
                o_list.append('line #{}: '.format(line_cnt) + line)
                is_last_line_vline = 0
            elif line.startswith('s '):
                s_list.append('line #{}: '.format(line_cnt) + line)
                is_last_line_vline = 0
            elif line.startswith('g '):
                g_list.append('line #{}: '.format(line_cnt) + line)
                is_last_line_vline = 0
            elif line.startswith('usemtl '):
                usemtl_list.append('line #{}: '.format(line_cnt) + line)
                is_last_line_vline = 0

            if not line.startswith('v') and obj_cnt < 1:
                prefix_lines.append(line)  # lines before the first v_line
                is_last_line_vline = 0

                continue

            if obj_cnt < 1:
                print('===> prefix lines:')
                print('-' * 32 + '\n')
                print(''.join(prefix_lines))
                print('-' * 32 + '\n')
                print('mtllib list: \n', mtllib_list)

                print('-' * 32 + '\n')
                print('===> lines starts with "o ": ')
                print(json.dumps(o_list, indent=2))
                print('===> lines starts with "s ":')
                print(json.dumps(s_list, indent=2))
                print('===> lines starts with "g ":')
                print(json.dumps(g_list, indent=2))
                print('===> lines starts with "usemtl": ')
                print(json.dumps(usemtl_list, indent=2))
                print('=' * 32 + '\n')

            if line.startswith('v '):
                v_cnt += 1

                if not is_last_line_vline:
                    obj_cnt += 1

                    if obj_cnt > 1:
                        print('===> mesh # ', obj_cnt - 1)
                        print('-' * 32)
                        print('===> # of vertices = ',
                              v_cnt - 1 - v_cnt_till_last_mesh)
                        print('===> # of vertex texture coordinates = ',
                              vt_cnt - vt_cnt_till_last_mesh)
                        print('===> # of vertex normals = ',
                              vn_cnt - vn_cnt_till_last_mesh)
                        print('===> # of faces = ',
                              f_cnt - f_cnt_till_last_mesh)

                        print('-' * 32)
                        print('===> lines starts with "o ": ')
                        print(json.dumps(o_list, indent=2))
                        print('===> lines starts with "s ":')
                        print(json.dumps(s_list, indent=2))
                        print('===> lines starts with "g ":')
                        print(json.dumps(g_list, indent=2))
                        print('===> lines starts with "usemtl": ')
                        print(json.dumps(usemtl_list, indent=2))

                    if fp_out:
                        fp_out.close()

                    new_obj_fname = base_name + '_split_{}.obj'.format(obj_cnt)
                    fp_out = open(new_obj_fname, 'w')
                    fp_out.writelines(prefix_lines)

                    v_cnt_till_last_mesh = v_cnt - 1
                    vt_cnt_till_last_mesh = vt_cnt
                    vn_cnt_till_last_mesh = vn_cnt
                    f_cnt_till_last_mesh = f_cnt

                    vx_cnt_till_last_mesh = [
                        v_cnt_till_last_mesh,
                        vt_cnt_till_last_mesh,
                        vn_cnt_till_last_mesh
                    ]

                    print('=' * 32 + '\n')
                    print('===> v_cnt_till_last_mesh = ', v_cnt_till_last_mesh)
                    print('===> vt_cnt_till_last_mesh = ',
                          vt_cnt_till_last_mesh)
                    print('===> vn_cnt_till_last_mesh = ',
                          vn_cnt_till_last_mesh)
                    print('===> f_cnt_till_last_mesh = ', f_cnt_till_last_mesh)
                    print('=' * 32 + '\n')

                    o_list = []
                    s_list = []
                    g_list = []
                    usemtl_list = []

                fp_out.write(line)
                is_last_line_vline = 1

            elif line.startswith('f '):
                f_cnt += 1

                if obj_cnt > 1:
                    split_parts = line.split(' ')
                    write_line = 'f'

                    for index_part in split_parts[1:]:
                        ind_parts = index_part.split('/')
                        write_line += ' '
                        for ii, ind in enumerate(ind_parts):
                            ind = int(ind) - vx_cnt_till_last_mesh[ii]
                            # if ii==1:
                            #     ind -=137
                            ind_parts[ii] = str(ind)

                        write_line += '/'.join(ind_parts)
                    fp_out.write(write_line + '\n')
                else:
                    fp_out.write(line)

                is_last_line_vline = 0
            else:
                fp_out.write(line)
                is_last_line_vline = 0

                if line.startswith('vt '):
                    vt_cnt += 1
                elif line.startswith('vn '):
                    vn_cnt += 1

        if obj_cnt > 0:
            print('===> mesh # ', obj_cnt)
            print('-' * 32 + '\n')
            print('===> # of vertices = ', v_cnt - v_cnt_till_last_mesh)
            print('===> # of vertext texture coordinates = ',
                  vt_cnt - vt_cnt_till_last_mesh)
            print('===> # of vertex normals = ',
                  vn_cnt - vn_cnt_till_last_mesh)
            print('===> # of faces = ', f_cnt - f_cnt_till_last_mesh)

            print('-' * 32 + '\n')
            print('===> lines starts with "o ": ')
            print(json.dumps(o_list, indent=2))
            print('===> lines starts with "s ":')
            print(json.dumps(s_list, indent=2))
            print('===> lines starts with "g ":')
            print(json.dumps(g_list, indent=2))
            print('===> lines starts with "usemtl": ')
            print(json.dumps(usemtl_list, indent=2))

            # print('-' * 32 + '\n')
            # print('===> v_cnt_till_last_mesh = ', v_cnt_till_last_mesh)
            # print('===> vt_cnt_till_last_mesh = ', vt_cnt_till_last_mesh)
            # print('===> vn_cnt_till_last_mesh = ', vn_cnt_till_last_mesh)
            # print('===> f_cnt_till_last_mesh = ', f_cnt_till_last_mesh)
            print('=' * 32 + '\n')

        if fp_out:
            fp_out.close()

        fp.close()


if __name__ == '__main__':
    def print_usage():
        """Print usage info.
        """
        usage = 'USAGE: \n'
        usage += 'python ' + sys.argv[0] + \
            ' <obj_file_path> [<obj_file2_path> ...]\n'
        print(usage)

    # obj_fname = '/Users/zhaoyafei/work/baidu/acg-facial-algorithms/face-3d-algorithms/material/tangdi/render_data/uv_coords.obj'
    # split_obj_file(obj_fname)

    if len(sys.argv) > 1:
        for obj_fname in sys.argv[1:]:
            split_obj_file(obj_fname)
    else:
        print_usage()
