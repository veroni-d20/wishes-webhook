from PIL import Image, ImageFilter
from PIL import ImageFont
from PIL import ImageDraw
import datetime
from flask import Flask, jsonify, request
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import os.path
from git.repo.base import Repo
import git
import traceback

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


@app.route('/wish', methods=['GET'])
def my_func():
	update_photos_folder()
	#def get_picture():
	name = request.args["name"]
	profile_photo = name
  profile = ""

	directory = 'crew-photos'
	for filename in os.listdir(directory):
		if filename == profile_photo:
			#do smth
			profile = Image.open(filename)
			break
		else:
			continue

	im1 = Image.open('birthday_template.jpg')
	im2 = Image.open(profile)
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

#  try:

#webhook = DiscordWebhook(
#url='CHANNEL_LINK')
#my_secret = os.environ['CHANNEL_LINK']

# create embed object for webhook
#embed = DiscordEmbed(title=name,
#description='Pattarai wishes you a very Happy Birthday',color='03b2f8', image ="https://i.imgur.com/ZGPxFN2.jpg")

# set author
#embed.set_author(name='Author Name', url='author url',
# icon_url='author icon url')

# set image
#embed.set_image(url='sample-out.jpg')

# set thumbnail
#embed.set_thumbnail(url='your thumbnail url')

# set footer
#embed.set_footer(text='Embed Footer Text', icon_url='URL of icon')

# set timestamp (default is now)
#embed.set_timestamp()

# add fields to embed
#embed.add_embed_field(name='Field 1', value='Lorem ipsum')
#embed.add_embed_field(name='Field 2', value='dolor sit')

# add embed object to webhook
#webhook.add_embed(embed)

#response = webhook.execute()
#print(response)
#return jsonify("Done")

#except Exception as e:
#print(e)
#      return jsonify("error")


def update_photos_folder():
	# Check if folder empty
  try:
    if not os.listdir(os.path.join(os.path.dirname(__file__), 'crew-photos')):
      full_local_path = os.path.join(os.path.dirname(__file__),
                                    'crew-photos')
      username = os.environ["GIT_USERNAME"]
      password = os.environ["GIT_PASSWORD"]
      remote = f"https://{username}:{password}@github.com/pattarai/crew-photos.git"
      Repo.clone_from(remote, full_local_path)
    # Pull from repo
    else:
      repo = git.Repo('crew-photos')
      o = repo.remotes.origin
      o.pull()
  except Exception as e:
    print(e)
    traceback.print_exc()

if __name__ == "__main__":
	app.run(
	    #host='0.0.0.0',
	    debug=True,
	    port=8080)
