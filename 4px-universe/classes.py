import numpy as np
import matplotlib.pyplot as plt


def plot_snr(snr, xaxisSig, yaxisSig, cmap='gist_heat_r', extent=[1, 11, 1, 11], fontdict=None,
             xticks_fontsize=14,
             estKind=1, plotType=" snr", method="nopbc"):
    Sigs = [1, 2, 3]
    zaxisSig = 0
    axisSig = [xaxisSig, yaxisSig, zaxisSig]
    zaxisSig = list(set(Sigs).difference(axisSig))[0]

    titleStr = r'$\widehat{\gamma}^{\,\,(' + str(estKind) + r')}$' + plotType + ', with $(\sigma_' + str(
        zaxisSig) + r'^{\,\,2} = \sigma_1^{\,\,2})$' + ' ' + method

    ylabelStr = r'$\sigma_' + str(yaxisSig) + r'^{\,\,2}$'
    xlabelStr = r'$\sigma_' + str(xaxisSig) + r'^{\,\,2}$'

    fig, ax = plt.subplots()

    axes = ax.imshow(snr, origin="lower", cmap=cmap, extent=extent, interpolation="none")
    ax.set_title(titleStr, fontdict=fontdict)
    ax.set_ylabel(ylabelStr, fontdict=fontdict)
    ax.set_xlabel(xlabelStr, fontdict=fontdict)
    ax.tick_params(labelsize=xticks_fontsize)
    cb = fig.colorbar(axes, ax=ax)

    cb.set_label(label=r'' + plotType, font=fontdict)

    for t in cb.ax.get_yticklabels():
        t.set_fontsize(13)

    return fig, ax




file1_pbc = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_pbc.npy'
file2_pbc = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_pbc.npy'

file1_pbc_cs = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_pbc_cs.npy'
file2_pbc_cs = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_pbc_cs.npy'

file1_nopbc_cs = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_nopbc_cs.npy'
file2_nopbc_cs = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_nopbc_cs.npy'

file1_nopbc = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma1_snr_nopbc.npy'
file2_nopbc = './.npy/4px_r=2000_[s0,s1,s2,s3]_gamma2_snr_nopbc.npy'

snr1_pbc = np.load(file1_pbc)
snr2_pbc = np.load(file2_pbc)

snr1_pbc_cs = np.load(file1_pbc_cs)
snr2_pbc_cs = np.load(file2_pbc_cs)

snr1_nopbc = np.load(file1_nopbc)
snr2_nopbc = np.load(file2_nopbc)

snr1_nopbc_cs = np.load(file1_nopbc_cs)
snr2_nopbc_cs = np.load(file2_nopbc_cs)

fig1_pbc, ax1_pbc = plot_snr(np.real(snr1_pbc),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=1, plotType=" snr", method="pbc")
fig2_pbc, ax2_pbc = plot_snr(np.real(snr2_pbc),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=2, plotType=" snr", method="pbc")

fig1_pbc_cs, ax1_pbc_cs = plot_snr(np.real(snr1_pbc_cs),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=1, plotType=" snr", method="pbc_cs")
fig2_pbc_cs, ax2_pbc_cs = plot_snr(np.real(snr2_pbc_cs),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=2, plotType=" snr", method="pbc_cs")

fig1_nopbc_cs, ax1_nopbc_cs = plot_snr(np.real(snr1_nopbc_cs),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=1, plotType=" snr", method="nopbc_cs")
fig2_nopbc_cs, ax2_nopbc_cs = plot_snr(np.real(snr2_nopbc_cs),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=2, plotType=" snr", method="nopbc_cs")

fig1_nopbc, ax1_nopbc = plot_snr(np.real(snr1_nopbc),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=1, plotType=" snr")
fig2_nopbc, ax2_nopbc = plot_snr(np.real(snr2_nopbc),  xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font, estKind=2, plotType=" snr")


