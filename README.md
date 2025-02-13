# Tritone Rotations

`tritone-rotations` is a command-line tool for analyzing and generating transformations of diminished seventh chord sequences. It provides functionality for applying structured chromatic rotations, visualizing transformations, and exporting results in JSON format.

## Features

- Generate all possible transformations of a diminished seventh chord by shifting notes chromatically.
- Analyze chord structures using `music21`.
- Optional plotting of transformations using `matplotlib`.
- Export results to JSON for integration with other tools.

## Installation

Using `pip`:
```bash
pip install tritone-rotations
```

Or, build from source:
```bash
python setup.py sdist bdist_wheel
pip install dist/tritone_rotations-0.1.0-py3-none-any.whl
```

## Usage

### Basic Usage
```bash
tritone-rotations --root C --naming flat --operation sequential
```
This generates transformations for the diminished seventh chord by transforming sequential notes. [C, EB, Gb, A] -> [Cb, D, Gb, A].

### Display Help
```bash
tritone-rotations --help
```
Shows available commands and options.

### Enable Plotting
```bash
tritone-rotations --root C --naming flat --operation sequential
 --plot
```
Displays a `matplotlib` plot of transformations.

### Output as JSON
```bash
tritone-rotations --root C --naming flat --operation sequential --json
```
Returns the transformations as structured JSON output.

## License
MIT License
