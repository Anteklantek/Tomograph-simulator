from PIL import Image

image_dot = Image.open("/home/antq/PycharmProjects/TomographSimulator/Tomograph-simulator/test_images/dot.bmp")

pixels = list(image_dot.getdata())
print(pixels.__class__)
for i in range (0,255):
    for j in range (0,255):
        print(pixels[j], end="")
    print("\n")