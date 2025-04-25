# Generates a KDP cover template from provided values
# Requires reportlab
#   $ python3 -m pip install reportlab 

import os
import datetime
import argparse
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import mm, inch
from reportlab.pdfbase.pdfmetrics import stringWidth

MM = 'MM'
INCH = 'INCH'

PAPERBACK = 'PAPERBACK'
HARDCOVER = 'HARDCOVER'

PAPER_BW_WHITE = 'WHITE'
PAPER_BW_CREAM = 'CREAM'
PAPER_COLOR_STANDARD = 'STANDARD'
PAPER_COLOR_PREMIUM = 'PREMIUM'

# No spine text on thin books
MIN_PAPERBACK_SPINE_PAGE_COUNT = 79 
MIN_HARDBACK_SPINE_PAGE_COUNT = 120

# Paper thickness (mm)
PAPER_WHITE_THICKNESS = 0.0572
PAPER_CREAM_THICKNESS = 0.0635
PAPER_STANDARD_THICKNESS = 0.0572
PAPER_PREMIUM_THICKNESS = 0.0596

# Padding inside trim margins for text & images (mm)
PADDING = 3

# Horizontal padding between spine folds (mm)
SPINE_PADDING = 1.6

# Paperback dimensions (mm)
PAPERBACK_BLEED = 3.2

# Hard cover dimensions (mm)
HARDCOVER_WRAP = 15
HARDCOVER_HINGE = 10

# Barcode dimensions (mm)
BARCODE_WIDTH = 50.8
BARCODE_HEIGHT = 30.5
BARCODE_PADDING = 6

# Default font
FONT = 'Helvetica'
FONT_SIZE = 10

parser = argparse.ArgumentParser()

parser.add_argument("--pages", help="Number of pages in the book", type=int, required=True)
parser.add_argument("--height", help="Final (trimmed) height of the printed book", type=float, required=True)
parser.add_argument("--width", help="Final (trimmed) width of the printed book", type=float, required=True)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--hardcover", help="Build a hard cover template", action="store_true")
group.add_argument("--paperback", help="Build a paperback template", action="store_true")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--paper-white", help="B&W print on white paper", action="store_true")
group.add_argument("--paper-cream", help="B&W print on cream paper", action="store_true")
group.add_argument("--paper-standard", help="Color print on standard paper", action="store_true")
group.add_argument("--paper-premium", help="Color print on premium paper", action="store_true")

group = parser.add_mutually_exclusive_group()
group.add_argument("--mm", help="Width and height in millimetres (default)", action="store_true")
group.add_argument("--inch", help="Width and height in inches", action="store_true")

parser.add_argument("--no-barcode", help="Exclude barcode from the template (default included)", action="store_true")
parser.add_argument("--title", help="Included in template and filename if provided")
parser.add_argument("--author", help="Included in template if provided")
parser.add_argument("-d", "--directory", help="Directory to write template file to (default current)", default=".")

def mm_to_inch(val): return (val * mm) / inch
def inch_to_mm(val): return (val * inch) / mm

# Parse inputs
args = parser.parse_args()
title = args.title
author = args.author
path = args.directory
page_count = args.pages
show_barcode = not args.no_barcode
trim_width = inch_to_mm(args.width) if args.inch else args.width
trim_height = inch_to_mm(args.height) if args.inch else args.height

if args.hardcover: binding_type = HARDCOVER
if args.paperback: binding_type = PAPERBACK

if args.paper_white:
    paper_type = PAPER_BW_WHITE
    paper_thickness = PAPER_WHITE_THICKNESS
if args.paper_cream:
    paper_type = PAPER_BW_CREAM
    paper_thickness = PAPER_CREAM_THICKNESS
if args.paper_standard:
    paper_type = PAPER_COLOR_STANDARD
    paper_thickness = PAPER_STANDARD_THICKNESS
if args.paper_premium:
    paper_type = PAPER_COLOR_PREMIUM
    paper_thickness = PAPER_PREMIUM_THICKNESS

file_name = "cover-template-%s.pdf" % binding_type
if title: file_name = "-".join([title.replace(" ", "_"), file_name])

file_path = os.path.join(path, file_name)

is_hardcover = binding_type == HARDCOVER
is_paperback = binding_type == PAPERBACK

# Set dimensions from options
bleed = HARDCOVER_WRAP if is_hardcover else PAPERBACK_BLEED
hinge = HARDCOVER_HINGE if is_hardcover else 0

# Only show spine if we have enough pages
if is_hardcover:
    show_spine = page_count > MIN_HARDBACK_SPINE_PAGE_COUNT
if is_paperback:
    show_spine = page_count > MIN_PAPERBACK_SPINE_PAGE_COUNT

timestamp = datetime.datetime.now().strftime('%c')

def get_paper_type_text(paper_type):
    if paper_type == PAPER_BW_WHITE:
        return "White Paper"
    if paper_type == PAPER_BW_CREAM:
        return "Cream Paper"
    if paper_type == PAPER_COLOR_PREMIUM:
        return "Color Premium Paper"
    if paper_type == PAPER_COLOR_STANDARD:
        return "Color Standard Paper"

def fill_background(canvas):
    canvas.setFillColorRGB(1, 0, 0, 0.3)
    canvas.rect(0, 0, canvas_width * mm, canvas_height * mm, stroke=0, fill=1)

def draw_trim(canvas):
    canvas.setStrokeColorRGB(0, 0, 0, 1)
    x = bleed * mm
    y = bleed * mm
    width = (canvas_width - bleed*2) * mm
    height = (canvas_height - bleed*2) * mm
    canvas.rect(x, y, width, height, stroke=1, fill=0)

def draw_back_cover(canvas):
    canvas.setFillColorRGB(1, 1, 1, 1)
    x = (bleed + PADDING) * mm
    y = (bleed + PADDING) * mm
    width = (trim_width - (PADDING * 2)) * mm
    height = (trim_height - (PADDING * 2)) * mm
    canvas.rect(x, y, width, height, stroke=0, fill=1)

def draw_front_cover(canvas):
    canvas.setFillColorRGB(1, 1, 1, 1)
    x = (bleed + trim_width + (hinge * 2) + spine_width + PADDING) * mm
    y = (bleed + PADDING) * mm
    width = (trim_width - (PADDING * 2)) * mm
    height = (trim_height - (PADDING * 2)) * mm
    canvas.rect(x, y, width, height, stroke=0, fill=1)

def draw_spine(canvas):
    canvas.setFillColorRGB(1, 1, 1, 1)
    x = (bleed + trim_width + hinge + SPINE_PADDING) * mm
    y = (bleed + PADDING) * mm
    width = (spine_width - (SPINE_PADDING * 2)) * mm
    height = (trim_height - (PADDING * 2)) * mm
    canvas.rect(x, y, width, height, stroke=0, fill=1)

def draw_barcode(canvas):
    canvas.setFillColorRGB(0, 1, 0, 0.5)
    x = (bleed + trim_width - BARCODE_WIDTH - BARCODE_PADDING) * mm
    y = (bleed + BARCODE_PADDING) * mm
    width = BARCODE_WIDTH * mm
    height = BARCODE_HEIGHT * mm
    canvas.rect(x, y, width, height, stroke=0, fill=1)

    canvas.setFillColorRGB(0, 0, 0, 1)
    canvas.setFont(FONT, FONT_SIZE * 0.9)
    text_x = (bleed + trim_width - BARCODE_WIDTH - BARCODE_PADDING + PADDING) * mm
    text_y = (bleed + BARCODE_PADDING + BARCODE_HEIGHT - (PADDING * 2)) * mm
    text = canvas.beginText(text_x, text_y)
    text.textLine("Barcode")
    text.textLine("")
    text.textLine("Width = {:0.2f} mm ({:0.2f} inch)".format(BARCODE_WIDTH, mm_to_inch(BARCODE_WIDTH)))
    text.textLine("Height = {:0.2f} mm ({:0.2f} inch)".format(BARCODE_HEIGHT, mm_to_inch(BARCODE_HEIGHT)))
    text.textLine("Margin = {:0.2f} mm ({:0.2f} inch)".format(BARCODE_PADDING, mm_to_inch(BARCODE_PADDING)))
    canvas.drawText(text)

def draw_back_spine_line(canvas):
    canvas.setStrokeColorRGB(0, 0, 1, 1)
    canvas.setDash([4, 4])
    x = (bleed + trim_width + hinge) * mm
    y1 = 0
    y2 = ((bleed * 2) + trim_height) * mm
    canvas.line(x, y1, x, y2)

def draw_front_spine_line(canvas):
    canvas.setStrokeColorRGB(0, 0, 1, 1)
    canvas.setDash([4, 4])
    x = (bleed + trim_width + hinge + spine_width) * mm
    y1 = 0
    y2 = ((bleed * 2) + trim_height) * mm
    canvas.line(x, y1, x, y2)

def draw_dimensions(canvas):
    canvas.setFillColorRGB(0, 0, 0, 1)
    canvas.setFont(FONT, FONT_SIZE)
    text_x = (bleed + (PADDING * 2)) * mm
    text_y = ((trim_height + bleed) - (PADDING * 3)) * mm
    text = canvas.beginText(text_x, text_y)
    text.textLine("Number of Pages = %d" % page_count)
    text.textLine("Binding Type = %s" % ("Hard Cover" if is_hardcover else "Paperback"))
    text.textLine("Paper Type = %s" % get_paper_type_text(paper_type))
    text.textLine("")
    text.textLine("Black Solid Line is Trim Size")
    text.textLine("Blue Dashed Line is Spine Fold")
    text.textLine("White Area is Live Area")
    if is_paperback: text.textLine("Red Area is Bleed/Out of Live")
    if is_hardcover: text.textLine("Red Area is Wrap/Out of Live")
    text.textLine("Green Area is Barcode")
    text.textLine("")
    text.textLine("Template Width = {:0.2f} mm ({:0.2f} inch)".format(canvas_width, mm_to_inch(canvas_width)))
    text.textLine("Template Height = {:0.2f} mm ({:0.2f} inch)".format(canvas_height, mm_to_inch(canvas_height)))
    text.textLine("")
    text.textLine("Trim Width = {:0.2f} mm ({:0.2f} inch)".format(trim_width, mm_to_inch(trim_width)))
    text.textLine("Trim Height = {:0.2f} mm ({:0.2f} inch)".format(trim_height, mm_to_inch(trim_height)))
    text.textLine("")
    text.textLine("Spine Width = {:0.2f} mm ({:0.2f} inch)".format(spine_width, mm_to_inch(spine_width)))
    text.textLine("Edge Bleed = {:0.2f} mm ({:0.2f} inch)".format(bleed, mm_to_inch(bleed)))
    if is_hardcover: text.textLine("Spine Hinge = {:0.2f} mm ({:0.2f} inch)".format(hinge, mm_to_inch(hinge)))
    text.textLine("Safe Area Padding = {:0.2f} mm ({:0.2f} inch)".format(PADDING, mm_to_inch(PADDING)))
    text.textLine("Spine Padding = {:0.2f} mm ({:0.2f} inch)".format(SPINE_PADDING, mm_to_inch(SPINE_PADDING)))
    text.textLine("")
    if is_hardcover: 
        text.textLine("Refer to the KDP hard cover template guide at:")
        text.textLine("https://kdp.amazon.com/en_US/help/topic/GDTKFJPNQCBTMRV6")
    if is_paperback: 
        text.textLine("Refer to the KDP paperback template guide at:")
        text.textLine("https://kdp.amazon.com/en_US/help/topic/G201953020")
    canvas.drawText(text)

def draw_center_text(canvas, title, text_y = bleed * 4 * mm, font_size=FONT_SIZE):
    canvas.setFillColorRGB(0, 0, 0, 1)
    canvas.setFont(FONT, font_size)
    title_width = stringWidth(title, FONT, font_size) / mm
    text_x = (bleed + trim_width + spine_width + (hinge * 2) + ((trim_width - title_width) / 2.0)) * mm
    text = canvas.beginText(text_x, text_y)
    text.textLine(title)
    canvas.drawText(text)

# Calculate template dimensions
spine_width = page_count * paper_thickness
canvas_width = (2 * (bleed + trim_width + hinge)) + spine_width
canvas_height = bleed + trim_height + bleed

# Create template canvas
canvas = Canvas(file_path, pagesize=(canvas_width * mm, canvas_height * mm))

# Draw template guides
fill_background(canvas)
draw_trim(canvas)
draw_back_cover(canvas)
draw_front_cover(canvas)
draw_back_spine_line(canvas)
draw_front_spine_line(canvas)
draw_dimensions(canvas)
draw_center_text(canvas, file_name, (bleed + (PADDING * 5)) * mm)
draw_center_text(canvas, timestamp, (bleed + (PADDING * 3)) * mm)

if show_barcode: draw_barcode(canvas)
if show_spine: draw_spine(canvas)
if title: draw_center_text(canvas, title, ((trim_height + bleed) - (PADDING * 10)) * mm, font_size=24)
if author: draw_center_text(canvas, author, ((trim_height + bleed) - (PADDING * 14)) * mm, font_size=18)

# Save file
canvas.showPage()
canvas.save()