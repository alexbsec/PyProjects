import matplotlib.pyplot as plt
import numpy as np
from invarpy import nopbc_estimators as nopbc
from invarpy import pbc_estimators as pbc
from numpy.fft import fftn
import time

def test_covariance_against_var(variance_array, covariance_matrix, precmin=9):
    test_count = 0
    code = 0
    for element in variance_array:
        prec = 15
        while np.round(element, prec) != np.round(covariance_matrix[test_count,test_count], prec) and prec >= precmin:
            prec -= 1
            if prec == precmin:
                print("[!!] Mismatch error on element " + str(
                            test_count) + " of the inverse cov matrix \n based on its expected variance: " + str(
                            element) + " != " + str(covariance_matrix[test_count, test_count]) + ". Minimum precision required"
                                                                                          " test has failed.")
                code = 1

        test_count += 1

    if code == 0:
        print("[++] All tests passed with precision of " + str(prec) +" digital figures.")

    return code




#### Params ####
bins = 4
grid_size = 100
samples = 2000
grid = 0

g_matrices = nopbc.geometric_series_matrices(bins)


snr1_nopbc = np.zeros((grid_size, grid_size), dtype='complex')
snr2_nopbc = np.zeros((grid_size, grid_size), dtype='complex')
# snr1_nopbc_cs = np.zeros((grid_size, grid_size), dtype='complex')
# snr2_nopbc_cs = np.zeros((grid_size, grid_size), dtype='complex')
# snr1_pbc = np.zeros((grid_size, grid_size), dtype='complex')
# snr2_pbc = np.zeros((grid_size, grid_size), dtype='complex')
snr1_pbc_cs = np.zeros((grid_size, grid_size), dtype='complex')
snr2_pbc_cs = np.zeros((grid_size, grid_size), dtype='complex')


maxgrids = grid_size**2

for l in range(grid_size):
    for k in range(grid_size):
        st = time.time()

        gamma1_cov_part1_nopbc = np.zeros((bins, bins), dtype='complex')
        gamma2_cov_part1_nopbc = np.zeros((bins, bins), dtype='complex')

        s1_nopbc = np.zeros((bins), dtype='complex')
        s2_nopbc = np.zeros((bins), dtype='complex')

        # s1_nopbc_cs = np.zeros((bins), dtype='complex')
        # s2_nopbc_cs = np.zeros((bins), dtype='complex')

        # s1_pbc = np.zeros((bins), dtype='complex')
        # s2_pbc = np.zeros((bins), dtype='complex')

        s1_pbc_cs = np.zeros((bins), dtype='complex')
        s2_pbc_cs= np.zeros((bins), dtype='complex')

        field_in, pspec = np.zeros((bins)), np.zeros((bins))

        var1, var2, var3 = 1 + 0.1 * k, 1 + 0.1 * l, 1 + 0.1 * k
        var0 = var2 + var3 - var1

        for i in range(samples):
            field_in[0], field_in[1], field_in[2], field_in[3] = np.random.normal(
                scale=np.sqrt(var0)), np.random.normal(scale=np.sqrt(var1)), np.random.normal(
                scale=np.sqrt(var2)), np.random.normal(scale=np.sqrt(var3))
            field_fft = fftn(field_in)

            pspec = (i / (i + 1)) * pspec + (1 / (1 + i)) * np.abs(field_fft) ** 2

            s1in_nopbc = nopbc.sigma(field_fft)
            s2in_nopbc = nopbc.sigma(field_fft, estimator_kind=2)

            # s1in_nopbc_cs = nopbc.sigma_cs(field_in, g_matrices)
            # s2in_nopbc_cs = nopbc.sigma_cs(field_in, g_matrices, estimator_kind=2)

            # s1in_pbc = pbc.sigma(field_fft)
            # s2in_pbc = pbc.sigma(field_fft, estimator_kind=2)

            s1in_pbc_cs = 4*pbc.sigma_cs(field_in)
            s2in_pbc_cs = 4*pbc.sigma_cs(field_in, estimator_kind=2)



            s2_nopbc = (i / (1 + i)) * s2_nopbc + (1 / (1 + i)) * s2in_nopbc
            s1_nopbc = (i / (1 + i)) * s1_nopbc + (1 / (1 + i)) * s1in_nopbc

            # s2_nopbc_cs = (i / (1 + i)) * s2_nopbc_cs + (1 / (1 + i)) * s2in_nopbc_cs
            # s1_nopbc_cs = (i / (1 + i)) * s1_nopbc_cs + (1 / (1 + i)) * s1in_nopbc_cs

            s2_pbc_cs = (i / (1 + i)) * s2_pbc_cs + (1 / (1 + i)) * s2in_pbc_cs
            s1_pbc_cs = (i / (1 + i)) * s1_pbc_cs + (1 / (1 + i)) * s1in_pbc_cs

            # s2_pbc = (i / (1 + i)) * s2_pbc + (1 / (1 + i)) * s2in_pbc
            # s1_pbc = (i / (1 + i)) * s1_pbc + (1 / (1 + i)) * s1in_pbc

            gamma1_cov_part1_nopbc = (i / (i + 1)) * gamma1_cov_part1_nopbc + (1 / (1 + i)) * np.outer(s1in_nopbc, np.conjugate(s1in_nopbc))
            gamma2_cov_part1_nopbc = (i / (i + 1)) * gamma2_cov_part1_nopbc + (1 / (1 + i)) * np.outer(s2in_nopbc, np.conjugate(s2in_nopbc))


        gamma1_cov_nopbc = gamma1_cov_part1_nopbc - np.outer(s1_nopbc, np.conjugate(s1_nopbc))
        gamma2_cov_nopbc = gamma2_cov_part1_nopbc - np.outer(s2_nopbc, np.conjugate(s2_nopbc))

        print(np.real(gamma1_cov_nopbc))

        print('inverse diagonal ', 1/np.diag(np.real(gamma1_cov_nopbc)))

        # Testing
        # response1 = test_covariance_against_var(s1std**2, gamma1_cov)
        # response2 = test_covariance_against_var(s2std**2, gamma2_cov)

        try:
            gamma1_cov_nopbc = np.linalg.inv(gamma1_cov_nopbc)
        except:
            gamma1_cov_nopbc = np.identity(4)*(np.diag(gamma1_cov_nopbc))**(-1)

        try:
            gamma2_cov_nopbc = np.linalg.inv(gamma2_cov_nopbc)
        except:
            gamma2_cov_nopbc = np.identity(4)*(np.diag(gamma2_cov_nopbc))**(-1)

        print(np.real(gamma1_cov_nopbc))

        K = np.arange(bins)

        # s1_inv_nopbc = nopbc.sigma_bias(pspec)
        # s2_inv_nopbc = nopbc.sigma_bias(pspec, estimator_kind=2)
        #
        # s1_inv_pbc = pbc.sigma(pspec, assume_invariance=True)
        # s2_inv_pbc = pbc.sigma(pspec, estimator_kind=2, assume_invariance=True)
        #
        s1_inv_pbc_cs = 4*pbc.sigma_cs(pspec, assume_invariance=True)
        s2_inv_pbc_cs = 4*pbc.sigma_cs(pspec, estimator_kind=2, assume_invariance=True)


        #
        # gamma1_nopbc = s1_nopbc - s1_inv_nopbc
        # gamma2_nopbc = s2_nopbc - s2_inv_nopbc

        # gamma1_nopbc_cs = s1_nopbc_cs - s1_inv_nopbc
        # gamma2_nopbc_cs = s2_nopbc_cs - s2_inv_nopbc
        #
        # gamma1_pbc = s1_pbc - s1_inv_pbc
        # gamma2_pbc = s2_pbc - s2_inv_pbc

        gamma1_pbc_cs = s1_pbc_cs - s1_inv_pbc_cs
        gamma2_pbc_cs = s2_pbc_cs - s2_inv_pbc_cs


        #
        # snr1_nopbc[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma1_nopbc), gamma1_cov_nopbc), gamma1_nopbc))
        # snr2_nopbc[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma2_nopbc), gamma2_cov_nopbc), gamma2_nopbc))

        # snr1_nopbc_cs[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma1_nopbc_cs), gamma1_cov_nopbc), gamma1_nopbc_cs))
        # snr2_nopbc_cs[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma2_nopbc_cs), gamma2_cov_nopbc), gamma2_nopbc_cs))
        #
        # snr1_pbc[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma1_pbc), gamma1_cov_nopbc), gamma1_pbc))
        # snr2_pbc[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma2_pbc), gamma2_cov_nopbc), gamma2_pbc))

        snr1_pbc_cs[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma1_pbc_cs), gamma1_cov_nopbc), gamma1_pbc_cs))
        snr2_pbc_cs[k, l] = np.sqrt(np.dot(np.dot(np.conjugate(gamma2_pbc_cs), gamma2_cov_nopbc), gamma2_pbc_cs))
        grid += 1
        end = time.time()
        speed = 1/(end-st)
        time_remaining = (maxgrids - grid) / speed

        if grid%2 == 0:
            print('Approximately ' + str(int(time_remaining/3600)) + ' h ' + str(np.round((time_remaining/60)%60,0)) + ' min remaining.', end="\r")

file_name1_nopbc = '4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_nopbc.npy'
file_name2_nopbc = '4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_nopbc.npy'

file_name1_nopbc_cs = '4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_nopbc_cs.npy'
file_name2_nopbc_cs = '4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_nopbc_cs.npy'

file_name1_pbc = '4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_pbc.npy'
file_name2_pbc = '4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_pbc.npy'

file_name1_pbc_cs = '4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_pbc_cs.npy'
file_name2_pbc_cs = '4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_pbc_cs.npy'

# np.save('./.npy/' + file_name1_nopbc, snr1_nopbc)
# np.save('./.npy/' + file_name2_nopbc, snr2_nopbc)

# np.save('./.npy/' + file_name1_nopbc_cs, snr1_nopbc_cs)
# np.save('./.npy/' + file_name2_nopbc_cs, snr2_nopbc_cs)

# np.save('./.npy/' + file_name1_pbc, snr1_pbc)
# np.save('./.npy/' + file_name2_pbc, snr2_pbc)

np.save('./.npy/' + file_name1_pbc_cs, snr1_pbc_cs)
np.save('./.npy/' + file_name2_pbc_cs, snr2_pbc_cs)


