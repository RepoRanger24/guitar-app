import streamlit as st

st.title("🎸 Jam Partner")
st.write("Play along with backing tracks and see what you can play!")

# Upload backing track
uploaded_file = st.file_uploader("Upload a backing track", type=["mp3", "wav"])

if uploaded_file:
    st.audio(uploaded_file)

# Key selection
keys = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
key = st.selectbox("Select Key", keys)

# Scale selection
scales = {
    "Minor Pentatonic": [0,3,5,7,10],
    "Blues": [0,3,5,6,7,10],
    "Major": [0,2,4,5,7,9,11]
}
scale_name = st.selectbox("Select Scale", list(scales.keys()))

# Show notes in scale
notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]

root_index = notes.index(key)
scale_notes = [notes[(root_index + i) % 12] for i in scales[scale_name]]

st.write("### Notes you can play:")
st.write(", ".join(scale_notes))
box_mode = st.checkbox("Show Pentatonic Box 1 Only")
box_mode = st.checkbox("Show Pentatonic Box 1 Only")
st.write("### Fretboard (first 12 frets)")
st.caption("Root notes are shown in brackets [ ]")

strings = ["E", "A", "D", "G", "B", "E"]
frets = 12

for string in strings:
    row = []
    for fret in range(frets + 1):
        note_index = (notes.index(string) + fret) % 12
        note = notes[note_index]

        # Box 1 = first 5 frets
        in_box = fret <= 4

        if note in scale_notes:
            if box_mode and not in_box:
                row.append("-")
            else:
                if note == key:
                    row.append(f"[{note}]")
                else:
                    row.append(note)
        else:
            row.append("-")

    st.text(f"{string} | " + " ".join(row))

st.write("### Practice Tip")

if scale_name == "Minor Pentatonic":
    st.info(f"Try landing on {key} at the end of your phrases. That will make your solo sound more resolved.")
elif scale_name == "Blues":
    st.info(f"Use the {key} blues scale, but don’t sit on every note the same. The blue note works best as a passing tone.")
elif scale_name == "Major":
    st.info(f"Try starting and ending phrases on {key}. Then experiment with the 3rd and 5th for a more melodic sound.")

strings = ["E", "A", "D", "G", "B", "E"]
frets = 12

for string in strings:
    row = []
    for fret in range(frets + 1):
        note_index = (notes.index(string) + fret) % 12
        note = notes[note_index]
        if note in scale_notes:
            if note == key:
                row.append(f"[{note}]")  # root note
            else:
                row.append(note)
        else:
            row.append("-")
    st.write(f"{string} | " + " ".join(row))
# Speed control (visual only for now)
speed = st.slider("Playback Speed (%)", 50, 150, 100)

# Loop section
st.write("### Loop Section")
loop_start = st.number_input("Start (seconds)", 0, 300, 0)
loop_end = st.number_input("End (seconds)", 0, 300, 30)

st.write(f"Looping from {loop_start}s to {loop_end}s")
