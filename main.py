from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("birthday_template.jpg")
draw = ImageDraw.Draw(img)

# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 65)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((45,520),"Sample guy",(255,255,255),font=font)

# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 16)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((10, 0),"Feb 31",(255,255,255),font=font)

img.save('sample-out.jpg')