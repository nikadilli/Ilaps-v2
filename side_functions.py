import numpy as np
from decimal import Decimal
import datetime


def outlier_detection(data):
    # removes outliers from a list of given values by IQR rule
    # returns list of values without outlier
    iqr = np.percentile(data, 75)-np.percentile(data, 25)
    min = np.percentile(data, 25) - 1.5*iqr
    max = np.percentile(data, 75) + 1.5*iqr
    return [x for x in data if x <= max and x >= min]


def element_strip(elem):
    # formatting of element name to match colnames of reference material
    elem = elem.replace('(LR)', '').replace('(MR)', '').replace('(HR)', '')
    elem = ''.join([c for c in elem if c.isalpha()])
    return elem


def elem_resolution(elem):
    elem = elem.replace('(LR)', '').replace('(MR)', '').replace('(HR)', '')
    return elem


def element_formater(elem, lst_of_elems):
    # matches the given element format to the one used in list
    if elem in lst_of_elems:
        return elem
    elif elem not in lst_of_elems:
        elem = elem.replace('(LR)', '').replace('(MR)', '').replace('(HR)', '')
        if elem in lst_of_elems:
            return elem
        elif elem not in lst_of_elems:
            elem = elem + '(LR)'
            if elem in lst_of_elems:
                return elem
            elif elem not in lst_of_elems:
                elem = elem.replace('(LR)', '')
                elem = elem + '(MR)'
                if elem in lst_of_elems:
                    return elem
                elif elem not in lst_of_elems:
                    elem = elem.replace('(MR)', '')
                    elem = elem + '(HR)'
                    if elem in lst_of_elems:
                        return elem
                    elif elem not in lst_of_elems:
                        elem = elem.replace('(HR)', '')
                        elem = ''.join([c for c in elem if c.isalpha()])
                        if elem in lst_of_elems:
                            return elem
                        else:
                            return


def round_me(x, LoD, elem):
    # replace values lower than limit of detection
    # if the value is above LoD, round to specific decimal place
    if x < LoD[elem]:
        return '< LoD'
    else:
        if x >= 100:
            return float(Decimal(x).quantize(Decimal('1')))
        else:
            if x >= 10:
                return float(Decimal(x).quantize(Decimal('0.1')))
            else:
                if x >= 1:
                    return float(Decimal(x).quantize(Decimal('0.01')))
                else:
                    if x >= 0:
                        return float(Decimal(x).quantize(Decimal('0.001')))


def correction(data, elem, internal_std):
    # calculates internal standard correction
    # data: df with quantified values where columns are measured isotopes
    # el: element used as internal standard
    # internal_std: df of values of internal standard  where columns are elements for correction
    # print(elem)
    # print(element_formater(elem, data.columns))
    ratio = data[element_formater(elem, data.columns)].div(
        list(internal_std[elem]))
    return data.apply(lambda x: x/ratio)


def get_timestamp(strTime):
    # format string time from iolite to timestamp
    return datetime.datetime.strptime(strTime, '%Y-%m-%d %H:%M:%S.%f')


def get_difference(start, now):
    # return time in seconds between 2 timestamps
    diff = now - start
    return diff.total_seconds()


def get_index(data, time):
    # return closest index of MS time given time in seconds
    for i in range(len(data.index)-1):
        if (data.index[i] <= time) and (data.index[i+1] > time):
            return i+1


def get_diff_lst(iolite):
    # return list of times in seconds from start to every start and end of laser ablation for spots
    lst = []
    for i in range(1, len(iolite['Timestamp'])-1):
        if (i-4) % 5 == 0:
            lst.append(get_difference(get_timestamp(
                iolite.loc[i-2, 'Timestamp']), get_timestamp(iolite.loc[i, 'Timestamp'])))
            lst.append(get_difference(get_timestamp(
                iolite.loc[i, 'Timestamp']), get_timestamp(iolite.loc[i+1, 'Timestamp'])))
    lst.append(get_difference(get_timestamp(
        iolite.loc[i, 'Timestamp']), get_timestamp(iolite.loc[i+1, 'Timestamp'])))
    return lst


def get_diff_lst_line(iolite):
    # return list of times in seconds from start to every start and end of laser ablation for lines
    lst = []
    for i in range(1, len(iolite['Timestamp'])-1):
        if (i-6) % 7 == 0:
            lst.append(get_difference(get_timestamp(
                iolite.loc[i-2, 'Timestamp']), get_timestamp(iolite.loc[i, 'Timestamp'])))
            lst.append(get_difference(get_timestamp(
                iolite.loc[i, 'Timestamp']), get_timestamp(iolite.loc[i+1, 'Timestamp'])))
    lst.append(get_difference(get_timestamp(
        iolite.loc[i-2, 'Timestamp']), get_timestamp(iolite.loc[i, 'Timestamp'])))
    return lst


def fmt(x, y):
    # show z value on graph
    Xflat, Yflat, Zflat = X.flatten(), Y.flatten(), arr.flatten()
    dist = np.linalg.norm(np.vstack([Xflat - x, Yflat - y]), axis=0)
    idx = np.argmin(dist)
    z = Zflat[idx]
    return 'x={x:.2f}  y={y:.2f}  z={z:.2f}'.format(x=x, y=y, z=z)


def keep_elements(df, elements):
    elem_to_drop = [el for el in df.columns if el not in elements]
    return df.drop(elem_to_drop, axis='columns')


def isotope_to_elem(isotope):
    return ''.join([i for i in isotope if not i.isdigit()])


def names_from_iolite(iolite):
    names = list(iolite[' Comment'].dropna())
    return names
