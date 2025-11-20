import artscii

# Print the ASCII Art to the console using print_to_console
print("Super simple:")
artscii.print_to_console(artscii.convert(artscii.image_from_path("test.png")))

# Save it to a file by specifying that location
artscii.convert(artscii.image_from_path("test.png"), res_path="test.txt")

# Use a palette by loading it from a json and reverse it incase you are in a darkmode editor
print("Darkmoded palette:")
artscii.print_to_console(artscii.convert(artscii.image_from_path("test.png"), darkmode=True, palette=artscii.load_palette("palettes/big_palette.json")))

# Finally play around with scale and font_ratio
print("Bigger (and wider) is better:")
artscii.print_to_console(artscii.convert(artscii.image_from_path("test.png"), scale=0.4, font_ratio=0.2))