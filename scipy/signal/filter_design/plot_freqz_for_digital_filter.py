import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def plot_freqz(b, a=1, worN=512, whole=False, plot=None, fs=6.283185307179586, include_nyquist=False, freq_unit='rad/sample'):
    """
        Compute the frequency response of a digital filter.
        Given the M-order numerator `b` and N-order denominator `a` of a digital
        filter, compute its frequency response::
                    jw                 -jw              -jwM
            jw    B(e  )    b[0] + b[1]e    + ... + b[M]e
        H(e  ) = ------ = -----------------------------------
                    jw                 -jw              -jwN
                A(e  )    a[0] + a[1]e    + ... + a[N]e
        Parameters
        ----------
        b : array_like
            Numerator of a linear filter. If `b` has dimension greater than 1,
            it is assumed that the coefficients are stored in the first dimension,
            and ``b.shape[1:]``, ``a.shape[1:]``, and the shape of the frequencies
            array must be compatible for broadcasting.
        a : array_like
            Denominator of a linear filter. If `b` has dimension greater than 1,
            it is assumed that the coefficients are stored in the first dimension,
            and ``b.shape[1:]``, ``a.shape[1:]``, and the shape of the frequencies
            array must be compatible for broadcasting.
        worN : {None, int, array_like}, optional
            If a single integer, then compute at that many frequencies (default is
            N=512). This is a convenient alternative to::
                np.linspace(0, fs if whole else fs/2, N, endpoint=include_nyquist)
            Using a number that is fast for FFT computations can result in
            faster computations (see Notes).
            If an array_like, compute the response at the frequencies given.
            These are in the same units as `fs`.
        whole : bool, optional
            Normally, frequencies are computed from 0 to the Nyquist frequency,
            fs/2 (upper-half of unit-circle). If `whole` is True, compute
            frequencies from 0 to fs. Ignored if w is array_like.
        plot : callable
            A callable that takes two arguments. If given, the return parameters
            `w` and `h` are passed to plot. Useful for plotting the frequency
            response inside `freqz`.
        fs : float, optional
            The sampling frequency of the digital system. Defaults to 2*pi
            radians/sample (so w is from 0 to pi).
            .. versionadded:: 1.2.0
        include_nyquist : bool, optional
            If `whole` is False and `worN` is an integer, setting `include_nyquist` to True
            will include the last frequency (Nyquist frequency) and is otherwise ignored.
            .. versionadded:: 1.5.0
        Returns
        -------
        w : ndarray
            The frequencies at which `h` was computed, in the same units as `fs`.
            By default, `w` is normalized to the range [0, pi) (radians/sample).
        h : ndarray
            The frequency response, as complex numbers.
        See Also
        --------
        freqz_zpk
        sosfreqz
        Notes
        -----
        Using Matplotlib's :func:`matplotlib.pyplot.plot` function as the callable
        for `plot` produces unexpected results, as this plots the real part of the
        complex transfer function, not the magnitude.
        Try ``lambda w, h: plot(w, np.abs(h))``.
        A direct computation via (R)FFT is used to compute the frequency response
        when the following conditions are met:
        1. An integer value is given for `worN`.
        2. `worN` is fast to compute via FFT (i.e.,
        `next_fast_len(worN) <scipy.fft.next_fast_len>` equals `worN`).
        3. The denominator coefficients are a single value (``a.shape[0] == 1``).
        4. `worN` is at least as long as the numerator coefficients
        (``worN >= b.shape[0]``).
        5. If ``b.ndim > 1``, then ``b.shape[-1] == 1``.
        For long FIR filters, the FFT approach can have lower error and be much
        faster than the equivalent direct polynomial calculation.
        Examples
    --------
        >>> from scipy import signal
        >>> b = signal.firwin(80, 0.5, window=('kaiser', 8))
        >>> w, h = signal.freqz(b)
        >>> import matplotlib.pyplot as plt
        >>> fig, ax1 = plt.subplots()
        >>> ax1.set_title('Digital filter frequency response')
        >>> ax1.plot(w, 20 * np.log10(abs(h)), 'b')
        >>> ax1.set_ylabel('Amplitude [dB]', color='b')
        >>> ax1.set_xlabel('Frequency [rad/sample]')
        >>> ax2 = ax1.twinx()
        >>> angles = np.unwrap(np.angle(h))
        >>> ax2.plot(w, angles, 'g')
        >>> ax2.set_ylabel('Angle (radians)', color='g')
        >>> ax2.grid()
        >>> ax2.axis('tight')
        >>> plt.show()
    """
    w, h = signal.freqz(b, a, worN, whole, plot, fs)

    fig, ax1 = plt.subplots()
    ax1.set_title(
        'Digital filter frequency response (fs={}{})'.format(fs, freq_unit))
    amplitudes_in_db = 20 * np.log10(abs(h))
    ax1.plot(w, amplitudes_in_db, 'b')
    ax1.set_ylabel('Amplitude [dB]', color='b')
    ax1.set_xlabel('Frequency [{}]'.format(freq_unit))
    ax2 = ax1.twinx()

    angles = np.unwrap(np.angle(h))
    ax2.plot(w, angles, 'g')
    ax2.set_ylabel('Angle (radians)', color='g')
    ax2.grid()
    ax2.axis('tight')
    plt.show()


if __name__ == "__main__":
    # b = signal.firwin(80, 0.5, window=('kaiser', 8))
    # b= np.array([1, -1])
    b = np.array([1, -0.97])
    a = 1
    fs = 16
    freq_unit = 'kHz'

    plot_freqz(b, a, fs=fs, freq_unit=freq_unit)
