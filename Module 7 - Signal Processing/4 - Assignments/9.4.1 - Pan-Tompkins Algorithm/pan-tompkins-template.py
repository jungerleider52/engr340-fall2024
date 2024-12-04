import numpy as np
from ekg_testbench import EKGTestBench
import scipy.signal as sp
from scipy.fft import fft
import matplotlib.pyplot as plt


def plot_fft_response(signal, f_s):
    N = len(signal) // 2
    X = fft(signal)[:N]
    sample_intervals = np.arange(N)
    T = N / f_s
    freq = sample_intervals / T / 2

    plt.stem(freq, np.abs(X), 'b', markerfmt=" ", basefmt="-b")
    plt.xlabel('Freq (Hz)')
    plt.ylabel('FFT Amplitude |X(freq)|')
    plt.title('One-Sided FFT of Signal')
    plt.show()


def detect_heartbeats(filepath):
    """
    Perform analysis to detect location of heartbeats
    :param filepath: A valid path to a CSV file of heart beats
    :return: signal: a signal that will be plotted
    beats: the indices of detected heartbeats
    """
    if filepath == '':
        return list()

    # import the CSV file using numpy
    path = filepath

    # load data in matrix from CSV file; skip first two rows
    data = np.loadtxt(filepath, delimiter=',', skiprows=2)

    # save each vector as own variable
    time = data[:,0]
    v1 = data[:,1]
    v2 = data[:, 2]

    # calculate sampling rate
    f_s = np.average(np.diff(time)) ** -1

    # identify one column to process. Call that column signal
    signal = v1

    # run an fft on the data
    # plot_fft_response(signal, f_s)

    low_fc = 5
    high_fc = 123

    # pass data through LOW PASS FILTER (OPTIONAL)
    filter_order = 4
    b, a = sp.butter(filter_order, high_fc, fs=f_s, btype='lowpass', output='ba')
    signal = sp.filtfilt(b, a, signal)

    # pass data through HIGH PASS FILTER (OPTIONAL) to create BAND PASS result
    b, a = sp.butter(filter_order, low_fc, fs=f_s, btype='highpass', output='ba')
    signal = sp.filtfilt(b, a, signal)

    # pass data through differentiator
    signal = np.asarray(signal)
    signal = np.diff(signal)

    # pass data through square function
    signal = np.square(signal)

    # pass through moving average window
    window = 20
    signal = np.convolve(signal, ([1]*window))

    # find and remove outliers from the signal
    avg = np.average(signal)
    std = np.std(signal)
    signal_copy = np.copy(signal)
    z = 1.4
    for j, sig in enumerate(signal):
        if sig >= avg + (z * std): # avg plus z stds
            signal_copy[j] = avg + (z * std)

    # calculate what height to create the threshold
    H = 0.35
    height = max(signal_copy) * H

    # use find_peaks to identify peaks within averaged/filtered data
    # save the peaks result and return as part of testbench result
    beats, _ = sp.find_peaks(signal, height=height, distance=150)

    # do not modify this line
    return signal, beats


# when running this file directly, this will execute first
def test_(database_name):
    # place here so doesn't cause import error
    import matplotlib.pyplot as plt

    # database name
    #database_name = 'mitdb_201'
    #database_name = 'nstdb_118e00'
    #database_name = 'qtdb_sel104'

    # set to true if you wish to generate a debug file
    file_debug = False

    # set to true if you wish to print overall stats to the screen
    print_debug = False

    # set to true if you wish to show a plot of each detection process
    show_plot = False

    ### DO NOT MODIFY BELOW THIS LINE!!! ###

    # path to ekg folder
    path_to_folder = "../../../data/ekg/"

    # select a signal file to run
    signal_filepath = path_to_folder + database_name + ".csv"

    # call main() and run against the file. Should return the filtered
    # signal and identified peaks
    (signal, peaks) = detect_heartbeats(signal_filepath)

    # matched is a list of (peak, annotation) pairs; unmatched is a list of peaks that were
    # not matched to any annotation; and remaining is annotations that were not matched.
    annotation_path = path_to_folder + database_name + "_annotations.txt"
    tb = EKGTestBench(annotation_path)
    peaks_list = peaks.tolist()
    (matched, unmatched, remaining) = tb.generate_stats(peaks_list)

    # if was matched, then is true positive
    true_positive = len(matched)

    # if response was unmatched, then is false positive
    false_positive = len(unmatched)

    # whatever remains in annotations is a missed detection
    false_negative = len(remaining)

    # calculate f1 score
    f1 = true_positive / (true_positive + 0.5 * (false_positive + false_negative))

    # if we wish to show the resulting plot
    if show_plot:
        # make a nice plt of results
        plt.title('Signal for ' + database_name + " with detections")

        plt.plot(signal, label="Filtered Signal")
        plt.plot(peaks, signal[peaks], 'p', label='Detected Peaks')

        true_annotations = np.asarray(tb.annotation_indices)
        plt.plot(true_annotations, signal[true_annotations], 'o', label='True Annotations')

        plt.legend()

        # uncomment line to show the plot
        plt.show()

    # if we wish to save all the stats to a file
    if file_debug:
        # print out more complex stats to the debug file
        debug_file_path = database_name + "_debug_stats.txt"
        debug_file = open(debug_file_path, 'w')

        # print out indices of all false positives
        debug_file.writelines("-----False Positives Indices-----\n")
        for fp in unmatched:
            debug_file.writelines(str(fp) + "\n")

        # print out indices of all false negatives
        debug_file.writelines("-----False Negatives Indices-----\n")
        for fn in remaining:
            debug_file.writelines(str(fn.sample) + "\n")

        # close file that we writing
        debug_file.close()

    if print_debug:
        print("-------------------------------------------------")
        print("Database|\t\tTP|\t\tFP|\t\tFN|\t\tF1")
        print(database_name, "|\t\t", true_positive, "|\t", false_positive, '|\t', false_negative, '|\t', round(f1, 3))
        print("-------------------------------------------------")

    #print("Done!")

    return round(f1, 3)

if __name__ == "__main__":

    #test_('nstdb_119e24')
    #test_('mitdb_232')
    test_('mitdb_100')


    files = ['mitdb_100','mitdb_102','mitdb_103','mitdb_104','mitdb_107','mitdb_201', 'mitdb_210',
             'mitdb_213','mitdb_219','mitdb_220','nstdb_118e00','nstdb_118e06','qtdb_sel104',
             'mitdb_217','mitdb_219','mitdb_220','mitdb_232','nstdb_118e24','nstdb_119e24', 'qtdb_sel232']

    # remove dupes cuz too lazy to do by hand
    files = list(set(files))
    #print(len(files))

    tot_fp = 0

    for i in range(len(files)):
        f1 = test_(files[i])
        tot_fp += f1
        print(f"{files[i]}: {f1}")

    print(f"average FP: {tot_fp / len(files)}")