import datetime
import os, shutil
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

@app.route('/wish', methods=['GET'])
def wish():
    update_photos_folder()
    profileName = request.args["name"]
    directory = 'crew-photos/crew-photos'
    profilePics = os.listdir(directory)

    profilePicsWithoutExtension = [name.split('.')[0] for name in profilePics]

    exists = True if profileName in profilePicsWithoutExtension else False

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
    font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 65)
    draw.text((45, 520), profileName, (255, 255, 255), font=font)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Fonts/Montserrat-Black.ttf", 18)

    x = datetime.datetime.now()
    month = x.strftime("%b")
    day = x.strftime("%d")

    draw.text((10, 0), month, (255, 255, 255), font=font)
    draw.text((55, 1), day, (255, 255, 255), font=font)

    back_im.save('output.jpg', quality=100) 

    webhook = DiscordWebhook(url=os.environ["WISHES_CHANNEL"])
    
    # create embed object for webhook
    embed = DiscordEmbed(
            title=profileName,
            description='Pattarai wishes you a very Happy Birthday',
            color='03b2f8')
    webhook.add_embed(embed)

    with open("output.jpg", "rb") as file:
      webhook.add_file(file=file.read(), filename=profileName+".jpg")
      
    
    try:
      response = webhook.execute()
      print(response)
      return "done"
    except Exception as e:
      return "done: " + e

def update_photos_folder():
    dirname = os.path.dirname(__file__)
    folderName = os.path.join(dirname, 'crew-photos')
    shutil.rmtree(folderName)

    # Clone the Pictures
    username = os.environ["GIT_USERNAME"]
    token = os.environ["GIT_TOKEN"]
    cloneCommand = f"git clone https://{username}:{token}@github.com/pattarai/crew-photos.git"
    os.system(cloneCommand)


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
  app.run(debug=True)

