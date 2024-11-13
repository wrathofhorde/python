import pywhatkit as pwk

input_image = "./starwars.png"
output_image = "./sw_ascii.txt"

pwk.image_to_ascii_art(input_image, output_image)

# with open(output_image, "r") as f:
#     print(f.read())
