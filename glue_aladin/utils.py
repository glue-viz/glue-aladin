from __future__ import absolute_import, division, print_function

from matplotlib.colors import ColorConverter
import numpy as np

from astropy import units as u
try:
    from astropy.coordinates import angular_separation
except ImportError:
    from astropy.coordinates.angle_utilities import angular_separation
from astropy.coordinates.representation import UnitSphericalRepresentation


__all__ = ['center_fov', 'color_to_hex']


def center_fov(lon, lat):

    # We need to filter out any non-finite values
    keep = np.isfinite(lon) & np.isfinite(lat)
    lon, lat = lon[keep], lat[keep]

    lon = u.Quantity(lon, u.deg, copy=False)
    lat = u.Quantity(lat, u.deg, copy=False)

    unit_sph = UnitSphericalRepresentation(lon, lat, copy=False)

    cen = unit_sph.mean()

    sep = angular_separation(lon, lat, cen.lon, cen.lat).to(u.deg).value.max()

    return cen.lon.to(u.deg).value, cen.lat.to(u.deg).value, sep


converter = ColorConverter()


def color_to_hex(color):
    r, g, b = converter.to_rgb(color)
    hexcolor = '#%02x%02x%02x' % (int(r * 256), int(g * 256), int(b * 256))
    return hexcolor
