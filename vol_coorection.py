import math

# Standard temperature
temperature_standard = 15


def get_b_c_values(conv_dens):
    density_thresholds = [771, 787, 838.5, 1075]
    b_values = [346.4228, 2680.3206, 594.5418, 186.9696]

    for threshold, b_value in zip(density_thresholds, b_values):
        if float(conv_dens) <= threshold:
            return b_value, get_c_value(conv_dens, threshold)


def get_c_value(conv_dens, threshold):
    if float(conv_dens) <= threshold:
        if float(conv_dens) <= 771:
            return 0.4388
        elif float(conv_dens) <= 787:
            return -0.00336312
        elif float(conv_dens) <= 838.5:
            return 0
        elif float(conv_dens) <= 1075:
            return 0.4862
    return None


def calculate_d(conv_dens):
    b, c = get_b_c_values(conv_dens)
    if c is not None:
        if c >= 0:
            d = ((b) / conv_dens ** 2) + (c / conv_dens)
        else:
            d = (b / (conv_dens ** 2)) + c
        return round(d, 7)
    return None


def calculate_temp_cor_factor(temp, d):
    try:
        temp_value = int((int(temp) * 4 + 0.5) / 4 - 15)
        temp_cor_factor = round(math.exp(-d * temp_value * (1 + 0.8 * float(d) * temp_value)), 4)
        return temp_cor_factor
    except ValueError:
        return None


def calculate_weight_cor_factor(conv_dens):
    return float(conv_dens / 1000 - 0.0011)


def calculate_real_volume(volume_value, temp_cor_factor, weight_cor_factor):
    q = float(volume_value) * float(temp_cor_factor)
    real_vol = round((q * weight_cor_factor), 2)
    return str(real_vol)


def vol_correction_factor_calc(conv_dens, volume_value, temp):
    try:
        d = calculate_d(conv_dens)

        if d is not None:
            if volume_value == 0:
                temp_cor_factor = calculate_temp_cor_factor(temp, d)
            else:
                try:
                    if -1 < float(temp) < 150:
                        temp_cor_factor = calculate_temp_cor_factor(temp, d)
                    else:
                        temp = temperature_standard
                        temp_cor_factor = calculate_temp_cor_factor(temp, d)
                except ValueError:
                    temp = temperature_standard
                    temp_cor_factor = calculate_temp_cor_factor(temp, d)

                weight_cor_factor = calculate_weight_cor_factor(conv_dens)
                result = calculate_real_volume(volume_value, temp_cor_factor, weight_cor_factor)
                return result
    except KeyError:
        pass
