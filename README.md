# Stock Strategy Tester

Allows you to test out various investment strategies on historical broad market index data.

I wrote a silly little paper using this project, you can read it [here](paper.md).

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

Download the historical market data, then test your strategies on it. That's the flow.

### Download Data

Download stock data with `download.py`:

`python -m download`

The data will be stored inside `data/`, which will be automatically created upon running the download script for the first time. Data downloaded are:

- S&P 500 index price only (from 1927-12-30 to latest)
- S&P 500 index total return (from 1988-01-04 to latest)

### Run Test

Run the following:

`python -m test`

List of result tables will be exported into `report/result.md`.

### Create Strategies

Add any strategy you want to test inside `strategy/`. Use `Strategy` base class in `strategy/strategy.py` as reference to implement your own. Once you've added a new trading strategy, add it to the list of strategies to test inside `test.py`, along with the necessary initializing parameters.

### Parameter Sweep

You can run the parameter sweep for Timed DCA with:

`python -m parameter_sweep_timed_dca`

The output can be found inside `charts/`.

## Development Environment

- Windows 11
- Python 3.12.5
