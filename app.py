import datetime
import os
import os.path
import traceback
import git
from discord_webhook import DiscordEmbed, DiscordWebhook
from flask import Flask, jsonify, request
from git.repo.base import Repo
from PIL import Image, ImageDraw, ImageFilter, ImageFont

app = Flask(__name__)


@app.route('/')
def homePage():
    try:
        res = "<style>body{background:black}</style><h1 style='position: fixed; top: 50%;  left: 50%; transform: translate(-50%, -50%);font-family:Montserrat;color:white'><img src='https://www.pattarai.in/images/pattarai_portrait.svg'/>Birthday API</h1>"
        return res

    except Exception as e:
        print(e)


@app.route('/check', methods=['GET'])
def hello():
    try:
        name = request.args["name"]
        webhook = DiscordWebhook(url=os.environ["GIT_USERNAME"])
            # create embed object for webhook
        embed = DiscordEmbed(
                title=name,
                description='Pattarai wishes you a very Happy Birthday',
                color='03b2f8')
        embed.set_image(url='https://i.imgur.com/ZGPxFN2.jpg')

        webhook.add_embed(embed)

        response = webhook.execute()
        print(response)
        return jsonify("Done")
    except Exception as e:
        print(e)
        return jsonify("Fails")




@app.route('/wish', methods=['GET'])
def my_func():
    update_photos_folder()
    profileName = request.args["name"]
    directory = 'crew-photos'

    exists = True if profileName in os.listdir(directory) else False

    template_base = Image.open('birthday_template.jpg')
    profilePicFile = Image.open("default_pic.png")
    
    if exists:
        profilePicFile = Image.open(directory+ "/" + profileName +".jpg")

    width = profilePicFile.size[0]
    height = profilePicFile.size[1]

    if width > 600 and height > 800:
        if width == height:
            size = (400, 400)
            profilePicFile = profilePicFile.resize(size)

        elif width > height:
            left = 300
            top = 0
            right = width - 300
            bottom = height
            profilePicFile = profilePicFile.crop((left, top, right, bottom))
            size = (400, 400)
            profilePicFile = profilePicFile.resize(size)

        else:
            left = 0
            top = 0
            right = width
            bottom = width
            profilePicFile = profilePicFile.crop((left, top, right, bottom))
            size = (400, 400)
            profilePicFile = profilePicFile.resize(size)

    else:
        size = (400, 400)
        profilePicFile = profilePicFile.resize(size)

    mask_im = Image.new("L", profilePicFile.size, 0)
    draw = ImageDraw.Draw(mask_im)
    draw.ellipse((15, 15, 396, 383), fill=255)

    mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(13))

    back_im = template_base.copy()
    back_im.paste(profilePicFile, (259, -23), mask_im_blur)

    draw = ImageDraw.Draw(back_im)

        # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 65)
        # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((45, 520), profileName, (255, 255, 255), font=font)

        # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 18)

    x = datetime.datetime.now()
    # Month name, short version
    month = x.strftime("%b")
    day = x.strftime("%d")

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text((10, 0), month, (255, 255, 255), font=font)
    draw.text((55, 1), day, (255, 255, 255), font=font)

    back_im.save('output.jpg', quality=100)


def update_photos_folder():
    try:
        if not os.listdir(os.path.join(os.path.dirname(__file__), 'crew-photos')):
            full_local_path = os.path.join(os.path.dirname(__file__), 'crew-photos')
            username = os.environ["GIT_USERNAME"]
            password = os.environ["GIT_PASSWORD"]
            remote = f"https://{username}:{password}@github.com/pattarai/crew-photos.git"
            Repo.clone_from(remote, full_local_path)
        else:
            repo = git.Repo('crew-photos')
            o = repo.remotes.origin
            o.pull()
    except Exception as e:
        print(e)
        traceback.print_exc()


        
@app.errorhandler(500)
def forbidden(error=None):
    message = {
        'status': 500,
        'message': 'Forbidden',
        }
    res = jsonify(message)
    res.status_code = 500
    traceback.print_exc()
    return res

if __name__ == "__main__":
  app.run(
        host='0.0.0.0',
        debug=True,
        port=8080)