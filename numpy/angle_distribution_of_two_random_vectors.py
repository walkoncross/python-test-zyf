#!/usr/bin/env python
"""
Plot the distribution of angles between two random vectors in N-dim Euclidean space.

https://kexue.fm/archives/7076

test-1:
---> dim=   2, mean=89.88, std=51.96
---> dim=   3, mean=89.98, std=39.18
---> dim=   4, mean=90.02, std=32.53
---> dim=   5, mean=90.01, std=28.37
---> dim=   6, mean=90.00, std=25.46
---> dim=   7, mean=90.03, std=23.29
---> dim=   8, mean=90.01, std=21.58
---> dim=   9, mean=90.00, std=20.20
---> dim=  10, mean=90.01, std=19.06
---> dim=  16, mean=89.98, std=14.78
---> dim=  32, mean=89.99, std=10.29
---> dim=  64, mean=90.00, std= 7.22
---> dim= 128, mean=89.98, std= 5.13
---> dim= 256, mean=90.00, std= 3.66
---> dim= 512, mean=90.00, std= 2.63
---> dim=1024, mean=89.95, std= 2.81

test-2:
---> dim=   2, mean=90.08, std=51.95
---> dim=   3, mean=89.95, std=39.17
---> dim=   4, mean=90.01, std=32.53
---> dim=   5, mean=89.97, std=28.37
---> dim=   6, mean=90.00, std=25.47
---> dim=   7, mean=89.97, std=23.29
---> dim=   8, mean=90.01, std=21.59
---> dim=   9, mean=89.98, std=20.20
---> dim=  10, mean=90.00, std=19.06
---> dim=  16, mean=90.00, std=14.78
---> dim=  32, mean=90.00, std=10.29
---> dim=  64, mean=90.00, std= 7.22
---> dim= 128, mean=89.99, std= 5.13
---> dim= 256, mean=89.99, std= 3.66
---> dim= 512, mean=89.99, std= 2.63
---> dim=1024, mean=89.95, std= 2.81
"""
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import normalize
from numpy.linalg import norm
from scipy.special import gamma


def generate_angles__uniformly_sampling_hypercube(dim: int, n_samples: int, batch: int = 100, deg: bool = True, verbose=False):
    """Generate angles between two random vectors, which are uniformly sampled from a hyper cube.
    """
    # print(type(n_samples))
    fixed_vector = np.zeros((1, dim))
    fixed_vector[0] = 1

    min_samples = 100
    if n_samples < min_samples:
        n_samples = min_samples

    angles = np.zeros(n_samples)

    n_samples = n_samples // dim

    # for i in range(0, n_samples, batch):
    start_idx = 0
    for i in range(0, n_samples, batch):
        _batch = batch
        if i + batch > n_samples:
            _batch = n_samples - i

        # col_vectors = 0.5 - np.random.rand(_batch, dim)
        col_vectors = np.random.rand(_batch, dim) - 0.5

        if verbose:
            print('===> random col vetors: ')
            print(col_vectors)

        col_vectors = normalize(col_vectors)

        if verbose:
            print('===> random col vetors after L2-normalization: ')
            print(col_vectors)
            print(norm(col_vectors[0]))

        # # batch_cosine = np.matmul(fixed_vector, col_vectors.T)
        # batch_consine = col_vectors[:, 0]
        # batch_angles = np.arccos(batch_consine)

        # if deg:
        #     batch_angles = np.rad2deg(batch_angles)

        # angles[i:i+_batch] = batch_angles

        # if verbose:
        #     print(f"===> angles[{i}:{i+_batch}]: ")
        #     print(angles[i:i+_batch])
        # batch_cosine = np.matmul(fixed_vector, col_vectors.T)
        batch_consine = col_vectors.flatten()
        batch_angles = np.arccos(batch_consine)

        if deg:
            batch_angles = np.rad2deg(batch_angles)

        angles[start_idx: start_idx+_batch*dim] = batch_angles
        start_idx += _batch*dim

        if verbose:
            print(f"===> angles[{i}:{i+_batch}]: ")
            print(angles[i:i+_batch])

    angles = np.array(angles)

    return angles


def generate_angles__uniformly_sampling_hypersphere(dim: int, n_samples: int, batch: int = 100, deg: bool = True, verbose=False):
    """Generate angles between two random vectors, which are uniformly sampled from a hyper sphere.

    Refer to: http://extremelearning.com.au/how-to-generate-uniformly-random-points-on-n-spheres-and-n-balls/
    """
    # print(type(n_samples))
    fixed_vector = np.zeros((1, dim))
    fixed_vector[0] = 1

    min_samples = 100
    if n_samples < min_samples:
        n_samples = min_samples

    angles = np.zeros(n_samples)

    n_samples = n_samples // dim

    # for i in range(0, n_samples, batch):
    start_idx = 0
    for i in range(0, n_samples, batch):
        _batch = batch
        if i + batch > n_samples:
            _batch = n_samples - i

        # col_vectors = 0.5 - np.random.rand(_batch, dim)
        col_vectors = np.random.normal(
            0, 1, (_batch * dim)).reshape(_batch, dim)

        if verbose:
            print('===> random col vetors: ')
            print(col_vectors)

        col_vectors = normalize(col_vectors)

        if verbose:
            print('===> random col vetors after L2-normalization: ')
            print(col_vectors)
            print(norm(col_vectors[0]))

        # # batch_cosine = np.matmul(fixed_vector, col_vectors.T)
        # batch_consine = col_vectors[:, 0]
        # batch_angles = np.arccos(batch_consine)

        # if deg:
        #     batch_angles = np.rad2deg(batch_angles)

        # angles[i:i+_batch] = batch_angles

        # if verbose:
        #     print(f"===> angles[{i}:{i+_batch}]: ")
        #     print(angles[i:i+_batch])
        # batch_cosine = np.matmul(fixed_vector, col_vectors.T)
        batch_consine = col_vectors.flatten()
        batch_angles = np.arccos(batch_consine)

        if deg:
            batch_angles = np.rad2deg(batch_angles)

        angles[start_idx: start_idx+_batch*dim] = batch_angles
        start_idx += _batch*dim

        if verbose:
            print(f"===> angles[{i}:{i+_batch}]: ")
            print(angles[i:i+_batch])

    angles = np.array(angles)

    return angles


if __name__ == '__main__':

    dim: int = 10
    n_samples: int = 1000000
    batch: int = 1000
    vb = False

    dim_list = [x for x in range(2, 11)]
    dim_list += [2**x for x in range(4, 11)]
    # dim_list = [x for x in range(5, 100, 5)]

    mean_list = []
    std_list = []

    for dim in dim_list:
        print('\n')
        print(f'===> dim={dim}')
        pdf_at_half_pi = gamma(dim*0.5)/gamma(dim*0.5 - 0.5) / np.sqrt(np.pi)

        print(f'===> pdf at pi/2: {pdf_at_half_pi}')

        angles = generate_angles__uniformly_sampling_hypersphere(
            dim, n_samples, batch, deg=True, verbose=vb)

        mean = angles.mean()
        std = angles.std()
        var = std*std

        mean_list.append(mean)
        std_list.append(std)

        rad_std = np.deg2rad(std)
        rad_var = rad_std*rad_std
        print(f'===> mean (deg): {mean}')
        print(f'===> std (deg): {std}')
        print(f'===> var (deg): {var}')

        print(f'===> std (rad): {rad_std}')
        print(f'===> var (rad): {rad_var}')

        if dim > 2:
            print(f'===> 1/(dim-2): {1/(dim-2)}')
        # hist = np.histogram(angles, bins=180, range=(0,180), normed = True)

        # bins = np.arange(0, 181, 2)
        # _ = plt.hist(angles, bins=bins, normed=True)
        # plt.title(f"Histogram of angles with dim={dim}")
        # plt.show()

    # print(f'===> dim_list: {dim_list}')
    # print(f'===> mean_list: {mean_list}')
    # print(f'===> std_list: {std_list}')

    for i, dim in enumerate(dim_list):
        print(f'---> dim={dim:4}, mean={mean_list[i]:5.2f}, std={std_list[i]:5.2f}')