from escpos.printer import Usb
import qrcode
from PIL import Image, ImageDraw
import datetime
import sys

accusations = {
	"finger": "Ihnen wird vorgeworfen, unserem Artefakt ROVER einen Mittelfinger gezeigt zu haben.",
	"cig": "Ihnen wird vorgeworfen, eine Zigarette auf den Boden geworfen zu haben.",
	"poop": "Ihnen wird vorgeworfen, Hundekot nicht regelkonform entsorgt zu haben.",
}

fines = {
	"finger": "4000 EUR",
	"cig": "150 EUR",
	"poop": "15 EUR",
}

class Printer:
	def __init__(self):
		try:
			self.printer = Usb(0x4b43, 0x3538, in_ep=0x81, out_ep=0x03)
			self.printer._raw(b'\x18')
			self.printer.profile.profile_data['media']['width']['pixels'] = 480
		except Exception as e:
				print(e)
				print(["Connection error"])

	

	def ticket(self, crime):
		try:
			accusation = accusations[crime]
			fine = fines[crime]

			""" self.printer.set(align='left', bold=True, custom_size=True, width=2, height=2, density=8)
			self.printer.textln("be seeing you")
			self.printer.set(align='left', bold=True)
			self.printer.textln(f"Tatbestand: {crime}")
			self.printer.set(align='left', bold=True)
			self.printer.textln("Tatvorwurf:")
			self.printer.set(align='left', bold=False)
			self.printer.textln(accusation)
			self.printer.set(align='left', bold=True)
			self.printer.textln("Verwarnungsgeldhoehe:")
			self.printer.set(align='left', bold=False)
			self.printer.textln(fine)
			self.printer.set(align='left', bold=True)
			self.printer.textln("Wichtige Hinweise:")
			self.printer.image("footer.png") """

			self.printer.image("footer_ud.png")
			self.printer.textln("Wichtige Hinweise:")
			self.printer.set(align='left', bold=True, flip=True)
			self.printer.textln(fine)
			self.printer.set(align='left', bold=False, flip=True)
			self.printer.textln("Verwarnungsgeldhoehe:")
			self.printer.set(align='left', bold=True, flip=True)
			self.printer.textln(accusation)
			self.printer.set(align='left', bold=False, flip=True)
			self.printer.textln("Tatvorwurf:")
			self.printer.set(align='left', bold=True, flip=True)
			self.printer.textln(f"Tatbestand: {crime}")
			self.printer.set(align='left', bold=True, flip=True)
			self.printer.textln("be seeing you")
			self.printer.set(align='left', bold=True, custom_size=True, width=2, height=2, density=8, flip=True)
		except Exception as e:
			print(e)
			print(["Print error"])


if __name__ == "__main__":
	printer = Printer()
	printer.ticket("poop")
