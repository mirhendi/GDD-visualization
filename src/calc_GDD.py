def calc_GDD(tmin, tmax, tbase):
    if ((tmin + tmax) / 2) < tbase:
        return 0.0
    else:
        return ((tmin + tmax) / 2 - tbase)
