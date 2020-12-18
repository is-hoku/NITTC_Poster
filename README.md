# NITTC_Poster
NITTC winter poster (school task)
# :sunglasses: Motivation
One of the winter vacation assignments for second-year students at NITTC(Toyota Kosen) is to create an art poster. Students are free to use any method they like, including paints, colored pencils, and photographs.  
However, for busy students, making a poster using paints is a huge burden.  
So I came up with the idea of creating a poster from a single photo by processing the photo and inserting a catchphrase.  

In other words, this is a CUI tool for those who want to have an easy time with their art assignments.

# :art: Usage
1) Clone the repository
2) Run ```poster.py``` in a terminal.
3) Add the fonts and photos you want to use under ```./font``` and ```./img``` respectively.
4) Enter the requested information in the CUI.
5) The poster will be created.

# :camera: Example
**input image**  
<img src="/img/nittc.png" width="320px">  
**cmd**  
```
$ python poster.py
Enter the relative path of the image under ./img! (ex. /nittc.jpg)>> /nittc0.png
Enter a catchphrase! >> 我らが母校 豊田高専
Enter a font size as integer type! (rec = 200) >> 250 
Enter the relative path of the font under ./font (ex. /IPAexfont00401/ipaexm.ttf)>> /2020_sushiki1.4/sushikifont1.4.ttf
Enter the coordinates for your catchphrase! (rec = (100, 100)) >> 100 100
Enter a color for the text! (r, g, b) >> 25 25 112
height, width =  3007 2126 => 3006 2126
 
done!

```
**output image**  
<img src="/img/poster.png" width="320px">  


## :warning: Notes
- The image will be resized to 1:√2.  
- If the image size is large, it may take some time to resize. If the process does not finish, please change the image to a vertical one or roughly resize it in advance using GIMP, etc.  
- If you want to enter multiple lines of text, please leave a space (half-width).
- When inputting coordinates and colors, please separate elements by spaces (half-width characters).
