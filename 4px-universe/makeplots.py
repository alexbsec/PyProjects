import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc, rcParams, rcParamsDefault

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
    if estKind == 2:
        cb = fig.colorbar(axes, ax=ax, ticks=np.linspace(0, 1.1, 10))
    else:
        cb = fig.colorbar(axes, ax=ax, ticks=np.linspace(0,5.5,10))

    cb.set_label(label=r'' + plotType, font=fontdict)

    for t in cb.ax.get_yticklabels():
        t.set_fontsize(13)


    return fig, ax



font = {'family': 'serif',
        'weight': 'normal',
        'size': 16,
        }

file_common = '4px_r=2000_[s0,s1,s0,s1]_gamma'
path = './.npy/'
path_fig = './figures/'

files = next(os.walk('./.npy/'))[2]



file_types = ['1_snr_', '2_snr_']
file_methods = ['nopbc', 'nopbc_cs', 'pbc_fs', 'pbc']

method_dict = {'nopbc': r'Fourier space with no PBC',
               'nopbc_cs': r'Configuration space with no PBC',
               'pbc_cs': r'Configuration space with PBC',
               'pbc': r'Fourier space with PBC'}

for file in files:
    print(file)
    file_content = np.load(path + file)
    if "gamma2" in file:
        kind = 2

    else:
        kind = 1

    if "_snr" in file:
        figs, ax = plot_snr(np.real(file_content), xaxisSig=1, yaxisSig=2, cmap='CMRmap', fontdict=font,
                            estKind=kind, plotType=r'$\mathit{v}_\mathrm{snr}$')
        method = file[len(file_common) + 6:len(file) - 4]
        ax.set_title(ax.get_title()[:28] + ' ' + method_dict[method])
        fig_name = file[:len(file) - 4]
        plt.tight_layout()
        figs.savefig(path_fig + fig_name + '.png', dpi=figs.dpi)

