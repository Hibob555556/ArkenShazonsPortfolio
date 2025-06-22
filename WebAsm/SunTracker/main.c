#include <stdio.h>
#include <math.h>

#define PI 3.14159265358979323846
#define DEG_TO_RAD (PI / 180.0)
#define RAD_TO_DEG (180.0 / PI)

// Convert local date/time to Julian Day (using UTC offset)
double julian_day(int year, int month, int day, int hour, int min, int sec, int tz_offset_hours) {
    if (month <= 2) {
        year -= 1;
        month += 12;
    }

    int A = year / 100;
    int B = 2 - A + (A / 4);
    double utc_hour = hour - tz_offset_hours + min / 60.0 + sec / 3600.0;

    double JD = (int)(365.25 * (year + 4716)) +
                (int)(30.6001 * (month + 1)) +
                day + B - 1524.5 + utc_hour / 24.0;

    return JD;
}

// Compute solar declination and equation of time
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

// Correct solar elevation for observer altitude
double elevation_correction(double observer_alt_m) {
    return 0.0347 * sqrt(observer_alt_m); // degrees
}

// Correct for atmospheric refraction near horizon
double refraction_correction(double elevation) {
    if (elevation > -0.575) {
        double tan_arg = (elevation + 10.3 / (elevation + 5.11)) * DEG_TO_RAD;
        return 1.02 / tan(tan_arg) / 60.0;
    }
    return 0.0;
}

// Calculate sunrise/sunset, solar noon, and day length
void calculate_solar_events(double latitude, double longitude, double declination,
                            double eqtime, int tz_offset_hours,
                            double* sunrise_local, double* sunset_local,
                            double* solar_noon_local, double* day_length_minutes) {
    double lat_rad = DEG_TO_RAD * latitude;
    double decl_rad = DEG_TO_RAD * declination;

    double cos_ha = (cos(DEG_TO_RAD * 90.833) - sin(lat_rad) * sin(decl_rad)) /
                    (cos(lat_rad) * cos(decl_rad));

    if (cos_ha >= 1.0) {
        *sunrise_local = -1; *sunset_local = -1;
        *solar_noon_local = -1; *day_length_minutes = 0;
        return;
    }
    if (cos_ha <= -1.0) {
        *sunrise_local = -2; *sunset_local = -2;
        *solar_noon_local = -2; *day_length_minutes = 24 * 60;
        return;
    }

    double ha = acos(cos_ha) * RAD_TO_DEG;
    double solar_noon = 720.0 - 4.0 * longitude - eqtime;
    double sunrise_utc = solar_noon - ha * 4.0;
    double sunset_utc = solar_noon + ha * 4.0;

    // Convert to local time
    *sunrise_local = sunrise_utc + 60.0 * tz_offset_hours;
    *sunset_local = sunset_utc + 60.0 * tz_offset_hours;
    *solar_noon_local = solar_noon + 60.0 * tz_offset_hours;
    *day_length_minutes = sunset_utc - sunrise_utc;
}

// Compute solar elevation/azimuth at a given time
void solar_position(double latitude, double longitude,
                    int year, int month, int day,
                    int hour, int min, int sec,
                    double observer_alt_m, int tz_offset_hours) {
    double jd = julian_day(year, month, day, hour, min, sec, tz_offset_hours);

    double decl, eqtime;
    solar_declination_eqtime(jd, &decl, &eqtime);

    // Convert local time to UTC minutes
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
    double apparent_elevation = elev_corr + refraction;

    double azimuth = acos((sin(decl_rad) - sin(lat_rad) * sin(DEG_TO_RAD * raw_elevation)) /
                          (cos(lat_rad) * cos(DEG_TO_RAD * raw_elevation))) * RAD_TO_DEG;
    if (ha > 0) azimuth = 360.0 - azimuth;

    // Solar events
    double sunrise_local, sunset_local, solar_noon_local, day_length;
    calculate_solar_events(latitude, longitude, decl, eqtime, tz_offset_hours,
                           &sunrise_local, &sunset_local,
                           &solar_noon_local, &day_length);

    printf("Solar Elevation (apparent): %.2f°\n", apparent_elevation);
    printf("Solar Azimuth: %.2f°\n", azimuth);

    if (sunrise_local >= 0) {
        printf("Sunrise (Local):     %02d:%02d\n", (int)(sunrise_local / 60), (int)fmod(sunrise_local, 60));
        printf("Sunset  (Local):     %02d:%02d\n", (int)(sunset_local / 60), (int)fmod(sunset_local, 60));
        printf("Solar Noon (Local):  %02d:%02d\n", (int)(solar_noon_local / 60), (int)fmod(solar_noon_local, 60));
        printf("Day Length:          %02d hr %02d min\n", (int)(day_length / 60), (int)fmod(day_length, 60));
    } else if (sunrise_local == -1) {
        printf("Sun never rises on this date at this location.\n");
    } else if (sunrise_local == -2) {
        printf("Sun never sets on this date at this location.\n");
    }
}

// int main() {
//     // Example: June 21, 2025, 12:00:00 (local) in Austin, TX (UTC-5 for CDT)
//     double latitude = 30.2672;
//     double longitude = -97.7431;
//     double altitude_m = 150.0;
//     int tz_offset = -5; // Central Daylight Time (UTC-5)

//     int year = 2025, month = 6, day = 21;
//     int hour = 12, min = 0, sec = 0;

//     solar_position(latitude, longitude, year, month, day, hour, min, sec, altitude_m, tz_offset);
//     return 0;
// }
