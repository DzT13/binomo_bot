import os
from bot import bot
from PIL import ImageFont, ImageDraw, Image

async def change_graph(message, full_name, deposit, data, income, broker, active_trading, total_income, broker_income, client_income, name = "image"):
	image = Image.open(f"graph_{broker}.png")
	segoe = ImageFont.truetype("SegoeProDisplay-Regular.ttf", 20)
	segoe_ui = ImageFont.truetype("Segoe UI.ttf", 20)
	nano = ImageFont.truetype("NotoSans-Regular.ttf", 19)

	drawer = ImageDraw.Draw(image)
	style_segoe = ("#707070", segoe)
	segoe_ui = ("#707070", segoe_ui)
	style_nano = ("#707070", nano)

	drawer.text((306, 224), f"{full_name}", *style_segoe)
	drawer.text((481, 225), f"{deposit}₽", *style_nano)
	drawer.text((568, 224), f"{data}", *style_segoe)
	drawer.text((692, 225), f"{income}₽", *style_nano)
	drawer.text((422, 439), f"{active_trading}", *segoe_ui)
	drawer.text((211, 600), f"{total_income:.3f}₽", *style_nano)
	drawer.text((211, 686), f"{broker_income:.3f}₽", *style_nano)
	drawer.text((360, 686), f"{client_income:.3f}₽", *style_nano)

	image.save(name + ".png")
	with open(name + ".png", "rb") as f:
		await bot.send_document(message.chat.id, f)
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name + ".png")
	os.remove(path)

async def change_form(message, full_name, deposit, data, income, name = "Screenshot"):
	image = Image.open("form.png")
	font = ImageFont.truetype("NotoSans-Regular.ttf", 19)
	drawer = ImageDraw.Draw(image)
	style = ("#707070", font)

	drawer.text((680, 364), f"{full_name}", *style)
	drawer.text((852, 364), f"{deposit}₽", *style)
	for i in range(8): drawer.text((936, 364 + 70 * i), f"{data}", *style)
	drawer.text((1060, 364), f"{income}₽", *style)

	image.save(name + ".png")
	with open(name + ".png", "rb") as f:
		await bot.send_document(message.chat.id, f)
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name + ".png")
	os.remove(path)
