import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from scipy.signal import freqs, iirfilter


def plot_freqs(b, a, worN=200, plot=None):
    """
    Compute frequency response of analog filter.
    Given the M-order numerator `b` and N-order denominator `a` of an analog
    filter, compute its frequency response::
             b[0]*(jw)**M + b[1]*(jw)**(M-1) + ... + b[M]
     H(w) = ----------------------------------------------
             a[0]*(jw)**N + a[1]*(jw)**(N-1) + ... + a[N]
    Parameters
    ----------
    b : array_like
        Numerator of a linear filter.
    a : array_like
        Denominator of a linear filter.
    worN : {None, int, array_like}, optional
        If None, then compute at 200 frequencies around the interesting parts
        of the response curve (determined by pole-zero locations). If a single
        integer, then compute at that many frequencies. Otherwise, compute the
        response at the angular frequencies (e.g., rad/s) given in `worN`.
    plot : callable, optional
        A callable that takes two arguments. If given, the return parameters
        `w` and `h` are passed to plot. Useful for plotting the frequency
        response inside `freqs`.
    Returns
    -------
    w : ndarray
        The angular frequencies at which `h` was computed.
    h : ndarray
        The frequency response.
    See Also
    --------
    freqz : Compute the frequency response of a digital filter.
    Notes
    -----
    Using Matplotlib's "plot" function as the callable for `plot` produces
    unexpected results, this plots the real part of the complex transfer
    function, not the magnitude. Try ``lambda w, h: plot(w, abs(h))``.
    Examples
    --------
    >>> from scipy.signal import freqs, iirfilter
    >>> b, a = iirfilter(4, [1, 10], 1, 60, analog=True, ftype='cheby1')
    >>> w, h = freqs(b, a, worN=np.logspace(-1, 2, 1000))
    >>> import matplotlib.pyplot as plt
    >>> plt.semilogx(w, 20 * np.log10(abs(h)))
    >>> plt.xlabel('Frequency')
    >>> plt.ylabel('Amplitude response [dB]')
    >>> plt.grid()
    >>> plt.show()
    """
    w, h = freqs(b, a, worN)

    # plt.semilogx(w, 20 * np.log10(abs(h)))
    # plt.xlabel('Frequency')
    # plt.ylabel('Amplitude response [dB]')
    # plt.grid()
    # plt.show()
    fig, ax1 = plt.subplots()
    ax1.set_title('Analog filter frequency response')

    amplitudes_in_db = 20 * np.log10(abs(h))
    ax1.semilogx(w, amplitudes_in_db, 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('Frequency [Hz]')
    ax2 = ax1.twinx()

    angles = np.unwrap(np.angle(h))
    ax2.semilogx(w, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()
    # ax2.axis('tight')
    plt.show()

if __name__ == "__main__":
    # b = np.array([1, -0.97])
    # a = 1
    b, a = iirfilter(4, [1, 10], 1, 60, analog=True, ftype='cheby1')
    worN = np.logspace(-1, 2, 1000)

    plot_freqs(b, a, worN)
