# Taken from https://medium.com/datadriveninvestor/finding-outliers-in-dataset-using-python-efc3fce6ce32
import numpy as np
import pandas as pd


class Separate_samples():

    def get_delta_time(self, time_series):
        delta_time = [(0, 0)]
        time_series = time_series.tolist()
        for i in range(1, len(time_series)):
            delta = (i, time_series[i] - time_series[i-1])
            delta_time.append(delta)
        return delta_time

    def get_mjd_as_list(self, delta_time):
        mjd = []
        for t in delta_time:
            mjd.append(t[1])
        return mjd

    def detect_outliers(self, data):
        outliers = []
        threshold = 3
        mean = np.mean(data)
        std_1 = np.std(data)
        for y in data:
            z_score = (y - mean)/std_1
            if np.abs(z_score) > threshold:
                outliers.append(y)
        return outliers

    def get_indexes(self, delta_time, outliers):
        indexes = []
        for t in delta_time:
            for o in outliers:
                if t[1] == o:
                    indexes.append(t[0])
        return indexes

    def get_intervals(self, time_series, flux, indexes):
        flag = 0
        items = 0
        final_list = []
        time = time_series.tolist()
        flux = flux.tolist()
        index_length = len(indexes)
        time_length = len(time)

        for i in range(0, index_length):
            sublist_time = time[flag:indexes[i]]
            sublist_flux = flux[flag:indexes[i]]

            d = {'mjd': sublist_time, 'flux': sublist_flux}
            sublist = pd.DataFrame(d)

            final_list.append(sublist)

            items = items + len(sublist)
            flag = indexes[i]

        if items < time_length:
            sublist_time = time[flag:time_length]
            sublist_flux = flux[flag:time_length]

            d = {'mjd': sublist_time, 'flux': sublist_flux}
            sublist = pd.DataFrame(d)

            final_list.append(sublist)

        return final_list

    def get_separated_samples(self, object):
        delta_time = self.get_delta_time(object['mjd'])
        delta_time_as_list = self.get_mjd_as_list(delta_time)
        outliers = self.detect_outliers(delta_time_as_list)
        indexes = self.get_indexes(delta_time, outliers)
        samples = self.get_intervals(object['mjd'], object['flux'], indexes)
        return samples
