from Havel_Hakimi import havel_hakimi
from input_file import readfile
from image_cv import image

filename = input("Enter file name: ")
if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
    degrees = readfile(file.filename)
    degrees_copy = degrees.copy()
else:
    degrees = readfile(file.filename)
    degrees_copy = degrees.copy()

if havel_hakimi(degrees_copy):
    print("graphic")
else:
    print("not graphic")
