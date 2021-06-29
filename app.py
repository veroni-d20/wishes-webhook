from PIL import Image, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import datetime
from flask import Flask, jsonify, request
from discord_webhook import DiscordWebhook

app = Flask(__name__)


@app.route('/')
def homePage():
    try:
        res = "<style>body{background:black}</style><h1 style='position: fixed; top: 50%;  left: 50%; transform: translate(-50%, -50%);font-family:Montserrat;color:white'><img src='https://www.pattarai.in/images/pattarai_portrait.svg'/>Birthday API</h1>"
        return res

    except Exception as e:
        print(e)


@app.route('/wish', methods=['GET'])
def my_func():
    name = request.args["name"]

    im1 = Image.open('birthday_template.jpg')
    im2 = Image.open('eg.jpg')
    width = im2.size[0]
    height = im2.size[1]
    # ar = round((width / height),2)
    # print (ar)
    if width > 600 and height > 800:
        if width == height:
            size = (400, 400)
            im2 = im2.resize(size)

        elif width > height:
            left = 300
            top = 0
            right = width - 300
            bottom = height
            im2 = im2.crop((left, top, right, bottom))
            size = (400, 400)
            im2 = im2.resize(size)

        else:
            left = 0
            top = 0
            right = width
            bottom = width
            im2 = im2.crop((left, top, right, bottom))
            size = (400, 400)
            im2 = im2.resize(size)

    else:
        size = (400, 400)
        im2 = im2.resize(size)

    mask_im = Image.new("L", im2.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((15, 15, 396, 383), fill=255)

    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(13))

    back_im = im1.copy()
    back_im.paste(im2, (259, -23), mask_im_blur)

    draw = ImageDraw.Draw(back_im)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 65)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((45, 520), name, (255, 255, 255), font=font)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 18)

    x = datetime.datetime.now()
    # Month name, short version
    month = x.strftime("%b")
    day = x.strftime("%d")

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((10, 0), month, (255, 255, 255), font=font)
    draw.text((55, 1), day, (255, 255, 255), font=font)

    back_im.save('sample-out.jpg', quality=100)
    try:
        webhook = DiscordWebhook(
            url='https://discord.com/api/webhooks/859457851696218122/HmjZy1NAWR5JV4yNaUyNyU83mcYf7pIi81v6-cBo0j3NBw6XMJw6NGMT81F92TA7yIiy')

        # create embed object for webhook
        embed = DiscordEmbed(title='Your Title',
                             description='Lorem ipsum dolor sit', color='03b2f8')

        # set author
        embed.set_author(name='Author Name', url='author url',
                         icon_url='author icon url')

        # set image
        embed.set_image(url='your image url')

        # set thumbnail
        embed.set_thumbnail(url='your thumbnail url')

        # set footer
        embed.set_footer(text='Embed Footer Text', icon_url='URL of icon')

        # set timestamp (default is now)
        embed.set_timestamp()

        # add fields to embed
        embed.add_embed_field(name='Field 1', value='Lorem ipsum')
        embed.add_embed_field(name='Field 2', value='dolor sit')

        # add embed object to webhook
        webhook.add_embed(embed)

        response = webhook.execute()
        return jsonify("Done")

    except Exception as e:
        return jsonify("error")
        print(e)


if __name__ == "__main__":
    app.run(
        # host='0.0.0.0',
        debug=True,
        port=8080
    )
