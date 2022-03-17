# Hamamatsu HPD-TA ITEX img file parser

This is a binary parser for the ITEX `.img` file that is used by Hamamatsu
streak cameras.

## Installation

Dependencies can be installed with `pip`
```sh
pip install -r requirements.txt
```
And this package can be install to your system path with
```sh
python setup.py install --user
```
It's generally recommended to install into virtualenv or user prefix in
your user home.

## Usage

Everything is included in the iteximg.ITEX class.
```python
from iteximg import ITEX

parser = ITEX()
parser.load_file('{your_img_file}.img')
```

The structure of the parser quite closely follows the spec on the manual.

## Features

## Contributing
