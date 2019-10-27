import os

search_path = "C:/Users/Ryan/Desktop/lfw/"
output_path = "C:/Users/Ryan/Desktop/lfw/"
img_num = 0

for root, dirs, files in os.walk(search_path, topdown=False): # Walk through all directories found within the search path
    for file in files: # Loop all files found
        if '.jpg' in file.lower() or '.jpeg' in file.lower(): # If the file is a .jpg / .jpeg
            img_num += 1
            os.rename(root + '/' + file, '{}{}.jpeg'.format(output_path, img_num)) # Rename it and move it to the output directory