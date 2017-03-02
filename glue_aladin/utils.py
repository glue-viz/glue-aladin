from matplotlib.colors import ColorConverter

converter = ColorConverter()


def color_to_hex(color):
    r, g, b = converter.to_rgb(color)
    hexcolor = '#%02x%02x%02x' % (int(r * 256), int(g * 256), int(b * 256))
    return hexcolor
