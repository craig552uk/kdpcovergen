# KDP Cover Template Generator

A python script to generate paperback and hard cover templates for Kindle Direct Publishing.

- [KDP Create A Hardcover Cover](https://kdp.amazon.com/en_US/help/topic/GDTKFJPNQCBTMRV6)
- [KDP Create A Paperback Cover](https://kdp.amazon.com/en_US/help/topic/G201953020)

KDP provides an [online tool for generating book cover templates](https://kdp.amazon.com/cover-calculator), but I wanted a script I could run locally to produce these more easily.

This is that script.


## Installation & Use

Copy `kdpcover.py` to somewhere useful on your machine.

```$ cp kdpcover.py ~/bin```

Install [ReportLab](https://www.reportlab.com).

```$ python3 -m pip install reportlab```

Generate a template.

```$ python3 kdpcover.py --pages 600 --height 198 --width 128 --paper-white --paperback```


## Options

```--pages PAGES```

The number of pages in the book. Required.

```--height HEIGHT```

Final (trimmed) height of the printed book. Default units are millimetres, accepts inches with the `--inch` option. Required. 

```--width WIDTH```

Final (trimmed) width of the printed book. Default units are millimetres, accepts inches with the `--inch` option. Required. 

```--hardcover```
```--paperback```

Build a hard cover or paperback template. One of these is required.

```--paper-white```
```--paper-cream```
```--paper-standard```
```--paper-premium```

Specifies the paper used to print the book.

- B&W print on white paper
- B&W print on cream paper
- Color print on standard paper
- Color print on premium paper

One of these is required.

```--mm```
```--inch```

Specifies the units for `--width` and `--height`. The default is `--mm`.

```--no-barcode```

Exclude barcode from the template. By default this is included.

```--title TITLE```

If provided the title is included on the cover template and in the file name.

```--author AUTHOR```

If provided, the author name is included on the cover template.

```-d, --directory DIRECTORY```

Directory to write template file to. Default is the current directory.

```-h, --help```

Show this help message:

```
usage: kdpcover.py [-h] --pages PAGES --height HEIGHT --width WIDTH (--hardcover | --paperback) (--paper-white | --paper-cream | --paper-standard | --paper-premium) [--mm | --inch] [--no-barcode] [--title TITLE] [--author AUTHOR] [-d DIRECTORY]

options:
  -h, --help                 Show this help message and exit
  --pages PAGES              Number of pages in the book
  --height HEIGHT            Final (trimmed) height of the printed book
  --width WIDTH              Final (trimmed) width of the printed book
  --hardcover                Build a hard cover template
  --paperback                Build a paperback template
  --paper-white              B&W print on white paper
  --paper-cream              B&W print on cream paper
  --paper-standard           Color print on standard paper
  --paper-premium            Color print on premium paper
  --mm                       Width and height in millimetres (default)
  --inch                     Width and height in inches
  --no-barcode               Exclude barcode from the template (default included)
  --title TITLE              Included in template and filename if provided
  --author AUTHOR            Included in template if provided
  -d, --directory DIRECTORY  Directory to write template file to (default current)```