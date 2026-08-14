# Stock Strategy Tester

Allows you to test out various investment strategies on historical broad market index data.

## Setup

Install Python and make a virtual environment inside the repo:

`python -m venv venv`

Activate virtual environment:

``` bash
# Windows
venv\Scripts\activate.bat

# Linux
./venv/Scripts/activate
```

Instal requirements:

`pip install -r requirements.txt`

## Usage

Download stock data with `download.py`:

`python -m download`

The data will be stored inside `data/`, which will be automatically created upon running the download script for the first time.

## Development Environment

- Windows 11
- Python 3.12.5