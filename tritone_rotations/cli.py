import sys
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from music21 import note, chord as m21chord

NOTE_NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
NOTE_NAMES_FLAT = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
NOTE_TO_PC = {
    "C": 0,
    "C#": 1,
    "Db": 1,
    "D": 2,
    "D#": 3,
    "Eb": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "Gb": 6,
    "G": 7,
    "G#": 8,
    "Ab": 8,
    "A": 9,
    "A#": 10,
    "Bb": 10,
    "B": 11,
}


def mod12(x):
    return x % 12


def build_dim7(root):
    return [mod12(root + 3 * i) for i in range(4)]


def chord_to_names(chord, naming_scheme="sharp"):
    names = NOTE_NAMES_SHARP if naming_scheme.lower() == "sharp" else NOTE_NAMES_FLAT
    return [names[n] for n in chord]


def tritone_rotation(chord):
    return [mod12(n + 6) for n in chord]


def single_note_mutations(chord):
    results = []
    for i in range(len(chord)):
        for shift in [-1, 1]:
            new_chord = chord.copy()
            new_chord[i] = mod12(new_chord[i] + shift)
            results.append(new_chord)
    return results


def sequential_shifts(chord):
    results = []
    n = len(chord)
    for start in range(n):
        for end in range(start + 1, n):
            for shift in [-1, 1]:
                new_chord = chord.copy()
                for i in range(start, end + 1):
                    new_chord[i] = mod12(new_chord[i] + shift)
                results.append(new_chord)
    return results


def alternate_shifts(chord):
    even_up = [mod12(n + 1) if i % 2 == 0 else n for i, n in enumerate(chord)]
    even_down = [mod12(n - 1) if i % 2 == 0 else n for i, n in enumerate(chord)]
    odd_up = [mod12(n + 1) if i % 2 == 1 else n for i, n in enumerate(chord)]
    odd_down = [mod12(n - 1) if i % 2 == 1 else n for i, n in enumerate(chord)]
    return [even_up, even_down, odd_up, odd_down]


def plot_pitch_classes(naming_scheme="sharp"):
    names = NOTE_NAMES_SHARP if naming_scheme.lower() == "sharp" else NOTE_NAMES_FLAT
    n = np.arange(12)
    angles = 2 * np.pi * n / 12
    points = np.column_stack((np.cos(angles), np.sin(angles)))
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(points[:, 0], points[:, 1], color="blue")
    for i, (x, y) in enumerate(points):
        ax.text(x * 1.1, y * 1.1, names[i], fontsize=12, ha="center")
    circle = plt.Circle((0, 0), 1, color="gray", fill=False, linestyle="--")
    ax.add_artist(circle)
    ax.set_title("12 Pitch Classes (" + naming_scheme.capitalize() + ")")
    ax.set_xlabel("Cosine")
    ax.set_ylabel("Sine")
    ax.axis("equal")
    plt.show()


def chord_to_midi(chord, base_midi=60):
    root_pc = chord[0]
    midi_notes = []
    for n in chord:
        offset = n - root_pc
        if offset < 0:
            offset += 12
        midi_notes.append(base_midi + offset)
    return midi_notes


def analyze_chord(chord, base_midi=60):
    midi_notes = chord_to_midi(chord, base_midi)
    notes = [note.Note(midi=n) for n in midi_notes]
    m_chord = m21chord.Chord(notes)
    return m_chord.commonName, m_chord.pitchNames


def run_operation(operation, root_pc):
    base_chord = build_dim7(root_pc)
    results = []
    if operation == "base":
        results.append(("Base Dim7 chord", base_chord))
    elif operation == "tritone":
        results.append(("Tritone Rotation", tritone_rotation(base_chord)))
    elif operation == "single":
        for ch in single_note_mutations(base_chord):
            results.append(("Single Mutation", ch))
    elif operation == "sequential":
        for ch in sequential_shifts(base_chord):
            results.append(("Sequential Shift", ch))
    elif operation == "alternate":
        for ch in alternate_shifts(base_chord):
            results.append(("Alternate Shift", ch))
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Music Theory CLI Library: Generate and analyze diminished 7th chords and their mutations.\n\n"
        "Operations:\n"
        "  base       - Show the base diminished 7th chord\n"
        "  tritone    - Apply a tritone rotation to the chord\n"
        "  single     - Shift a single note by ±1 semitone (all possibilities)\n"
        "  sequential - Shift contiguous segments by ±1 semitone\n"
        "  alternate  - Shift even or odd positions by ±1 semitone\n\n"
        "Example usage: tritone-rotations --root B --operation single --naming flat --json",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--root",
        type=str,
        required=True,
        help="Root note (e.g., C, C#, Db, etc.) for the diminished 7th chord",
    )
    parser.add_argument(
        "--operation",
        type=str,
        choices=["base", "tritone", "single", "sequential", "alternate"],
        required=True,
        help="Operation to perform on the chord",
    )
    parser.add_argument(
        "--naming",
        type=str,
        choices=["sharp", "flat"],
        default="sharp",
        help="Naming convention for note names (default: sharp)",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="If provided, displays a matplotlib plot of the 12 pitch classes",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="If provided, outputs the results in JSON format",
    )
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit("No arguments provided. Please see help above.")
    args = parser.parse_args()
    root_input = args.root.strip()
    if root_input not in NOTE_TO_PC:
        sys.exit("Invalid root note. Use standard names like C, C#, Db, etc.")
    root_pc = NOTE_TO_PC[root_input]
    chords = run_operation(args.operation, root_pc)
    output = []
    for label, ch in chords:
        names = chord_to_names(ch, args.naming)
        analysis, pitches = analyze_chord(ch)
        output.append(
            {"label": label, "chord": names, "analysis": analysis, "pitches": pitches}
        )
    if args.json:
        print(json.dumps(output, indent=2))
    else:
        for entry in output:
            print(
                f"{entry['label']}: {entry['chord']} | Analysis: {entry['analysis']} | Pitches: {entry['pitches']}"
            )
    if args.plot:
        plot_pitch_classes(args.naming)


if __name__ == "__main__":
    main()
