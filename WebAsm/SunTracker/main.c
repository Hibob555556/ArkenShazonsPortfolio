#include <math.h>                  // include to be able to use more advanced math functions
#include <emscripten/emscripten.h> // include to utilize wasm

// define commonly used symbols
#define PI 3.14159265358979323846
#define DEG_TO_RAD (PI / 180.0)
#define RAD_TO_DEG (180.0 / PI)

// Calculates the Julian Day for a given date and time, accounting for time zone offset.
// Returns the Julian Day as a double (fractional days included).
double julian_day(int year, int month, int day, int hour, int min, int sec, int tz_offset_hours)
{
    // Adjust months so that March is month 1, April is 2, ..., January is 11, February is 12 of the previous year
    if (month <= 2)
    {
        year -= 1;   // Move to previous year
        month += 12; // Adjust month accordingly
    }

    // Century-based correction for Gregorian calendar
    int A = year / 100;
    int B = 2 - A + (A / 4); // Gregorian calendar reform correction

    // Convert local time to UTC in fractional hours
    double utc_hour = hour - tz_offset_hours + min / 60.0 + sec / 3600.0;

    // Compute the Julian Day using standard astronomical formula
    // (int) casts are used to ensure truncation towards zero, mimicking floor for positive numbers
    return (int)(365.25 * (year + 4716))  // Days from years
           + (int)(30.6001 * (month + 1)) // Days from months
           + day                          // Current day
           + B                            // Gregorian calendar correction
           - 1524.5                       // Offset to align Julian Day number
           + utc_hour / 24.0;             // Fractional day from UTC time
}

// Calculates the solar declination and the equation of time for a given Julian Day (jd).
// - declination: output pointer to store the solar declination in degrees
// - eqtime: output pointer to store the equation of time in minutes
void solar_declination_eqtime(double jd, double *declination, double *eqtime)
{
    // Number of days since J2000.0 (January 1, 2000 at 12:00 TT)
    double d = jd - 2451545.0;

    // Mean anomaly of the Sun (degrees), i.e., the Sun's angular distance from perihelion
    double g = fmod(357.529 + 0.98560028 * d, 360.0);

    // Mean longitude of the Sun (degrees), corrected for the precession of the equinoxes
    double q = fmod(280.459 + 0.98564736 * d, 360.0);

    // True ecliptic longitude of the Sun (degrees), including orbital eccentricity corrections
    double L = fmod(q + 1.915 * sin(DEG_TO_RAD * g) + 0.020 * sin(2 * DEG_TO_RAD * g), 360.0);

    // Obliquity of the ecliptic (tilt of Earth's axis), slowly changing over time
    double e = 23.439 - 0.00000036 * d;

    // Solar declination (degrees): angle between rays of the Sun and the Earth's equatorial plane
    *declination = asin(sin(DEG_TO_RAD * e) * sin(DEG_TO_RAD * L)) * RAD_TO_DEG;

    // Auxiliary variable used in equation of time calculation
    double y = tan(DEG_TO_RAD * (e / 2.0));
    y *= y;

    // Equation of time (minutes): difference between apparent solar time and mean solar time
    *eqtime = 4.0 * RAD_TO_DEG * (y * sin(2.0 * DEG_TO_RAD * q)                                        // Obliquity correction
                                  - 2.0 * 0.0167 * sin(DEG_TO_RAD * g)                                 // Eccentricity correction
                                  + 4.0 * 0.0167 * y * sin(DEG_TO_RAD * g) * cos(2.0 * DEG_TO_RAD * q) // Combined effect
                                  - 0.5 * y * y * sin(4.0 * DEG_TO_RAD * q)                            // Higher-order term
                                  - 1.25 * 0.0167 * 0.0167 * sin(2.0 * DEG_TO_RAD * g)                 // Another higher-order eccentricity term
                                 );
}

// Applies a basic correction to account for the observer's altitude above sea level.
// This raises the apparent elevation of the Sun slightly due to the higher horizon.
double elevation_correction(double observer_alt_m)
{
    // The correction is roughly 0.0347° per sqrt(meter), derived from atmospheric models.
    return 0.0347 * sqrt(observer_alt_m);
}

// Calculates atmospheric refraction correction for a given solar elevation angle.
// Refraction causes the Sun to appear higher in the sky than its true position when near the horizon.
double refraction_correction(double elevation)
{
    // Use empirical formula for elevations above -0.575° (covers most real solar elevations).
    if (elevation > -0.575)
    {
        // Compute the argument for the tangent in radians using Bennett’s formula.
        double tan_arg = (elevation + 10.3 / (elevation + 5.11)) * DEG_TO_RAD;

        // Return refraction angle in degrees (converted from arcminutes).
        return 1.02 / tan(tan_arg) / 60.0;
    }

    // No correction for very low or below-horizon positions.
    return 0.0;
}

// Calculates the solar elevation angle at a specific date, time, and location.
// Includes corrections for observer altitude and atmospheric refraction.
// Marked EMSCRIPTEN_KEEPALIVE to expose this function to JavaScript in WebAssembly.
EMSCRIPTEN_KEEPALIVE
double get_solar_elevation(double latitude, double longitude,
                           int year, int month, int day,
                           int hour, int min, int sec,
                           double observer_alt_m, int tz_offset_hours)
{
    // Convert local date and time to Julian Day.
    double jd = julian_day(year, month, day, hour, min, sec, tz_offset_hours);

    // Calculate solar declination and equation of time for this Julian Day.
    double decl, eqtime;
    solar_declination_eqtime(jd, &decl, &eqtime);

    // Calculate local and UTC time in minutes since midnight.
    double local_minutes = hour * 60.0 + min + sec / 60.0;
    double utc_minutes = local_minutes - 60.0 * tz_offset_hours;

    // Compute time offset in minutes (equation of time + longitude correction).
    double time_offset = eqtime + 4.0 * longitude;

    // True Solar Time in minutes.
    double tst = utc_minutes + time_offset;

    // Hour angle of the Sun in degrees (how far the Sun has moved across the sky).
    double ha = (tst / 4.0) - 180.0;

    // Convert angles to radians for trigonometric calculations.
    double lat_rad = DEG_TO_RAD * latitude;
    double decl_rad = DEG_TO_RAD * decl;
    double ha_rad = DEG_TO_RAD * ha;

    // Calculate the solar elevation angle (before corrections).
    double raw_elevation = asin(sin(lat_rad) * sin(decl_rad) +
                                cos(lat_rad) * cos(decl_rad) * cos(ha_rad)) *
                           RAD_TO_DEG;

    // Apply correction for observer's altitude.
    double elev_corr = raw_elevation + elevation_correction(observer_alt_m);

    // Apply atmospheric refraction correction.
    double refraction = refraction_correction(elev_corr);

    // Final solar elevation angle including both corrections.
    return elev_corr + refraction;
}
