#include <math.h>
#include <emscripten/emscripten.h>

#define PI 3.14159265358979323846
#define DEG_TO_RAD (PI / 180.0)
#define RAD_TO_DEG (180.0 / PI)

// --- Dependencies (same as in your original code) ---

double julian_day(int year, int month, int day, int hour, int min, int sec, int tz_offset_hours) {
    if (month <= 2) {
        year -= 1;
        month += 12;
    }
    int A = year / 100;
    int B = 2 - A + (A / 4);
    double utc_hour = hour - tz_offset_hours + min / 60.0 + sec / 3600.0;
    return (int)(365.25 * (year + 4716)) + (int)(30.6001 * (month + 1)) +
           day + B - 1524.5 + utc_hour / 24.0;
}

void solar_declination_eqtime(double jd, double* declination, double* eqtime) {
    double d = jd - 2451545.0;
    double g = fmod(357.529 + 0.98560028 * d, 360.0);
    double q = fmod(280.459 + 0.98564736 * d, 360.0);
    double L = fmod(q + 1.915 * sin(DEG_TO_RAD * g) + 0.020 * sin(2 * DEG_TO_RAD * g), 360.0);
    double e = 23.439 - 0.00000036 * d;
    *declination = asin(sin(DEG_TO_RAD * e) * sin(DEG_TO_RAD * L)) * RAD_TO_DEG;

    double y = tan(DEG_TO_RAD * (e / 2.0));
    y *= y;
    *eqtime = 4.0 * RAD_TO_DEG * (
        y * sin(2.0 * DEG_TO_RAD * q) -
        2.0 * 0.0167 * sin(DEG_TO_RAD * g) +
        4.0 * 0.0167 * y * sin(DEG_TO_RAD * g) * cos(2.0 * DEG_TO_RAD * q) -
        0.5 * y * y * sin(4.0 * DEG_TO_RAD * q) -
        1.25 * 0.0167 * 0.0167 * sin(2.0 * DEG_TO_RAD * g)
    );
}

double elevation_correction(double observer_alt_m) {
    return 0.0347 * sqrt(observer_alt_m);
}

double refraction_correction(double elevation) {
    if (elevation > -0.575) {
        double tan_arg = (elevation + 10.3 / (elevation + 5.11)) * DEG_TO_RAD;
        return 1.02 / tan(tan_arg) / 60.0;
    }
    return 0.0;
}

// --- Clean single-purpose function ---

EMSCRIPTEN_KEEPALIVE
double get_solar_elevation(double latitude, double longitude,
                           int year, int month, int day,
                           int hour, int min, int sec,
                           double observer_alt_m, int tz_offset_hours) {
    double jd = julian_day(year, month, day, hour, min, sec, tz_offset_hours);

    double decl, eqtime;
    solar_declination_eqtime(jd, &decl, &eqtime);

    double local_minutes = hour * 60.0 + min + sec / 60.0;
    double utc_minutes = local_minutes - 60.0 * tz_offset_hours;

    double time_offset = eqtime + 4.0 * longitude;
    double tst = utc_minutes + time_offset;
    double ha = (tst / 4.0) - 180.0;

    double lat_rad = DEG_TO_RAD * latitude;
    double decl_rad = DEG_TO_RAD * decl;
    double ha_rad = DEG_TO_RAD * ha;

    double raw_elevation = asin(sin(lat_rad) * sin(decl_rad) +
                                 cos(lat_rad) * cos(decl_rad) * cos(ha_rad)) * RAD_TO_DEG;

    double elev_corr = raw_elevation + elevation_correction(observer_alt_m);
    double refraction = refraction_correction(elev_corr);
    return elev_corr + refraction;
}
