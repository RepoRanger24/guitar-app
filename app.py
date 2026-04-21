import streamlit as st
import streamlit.components.v1 as components
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
box_start = st.slider("Box start fret", 0, 8, 0)
st.write("### Fretboard (first 12 frets)")
st.caption("Root note is red. Other scale notes are blue.")

strings = ["E", "B", "G", "D", "A", "E"]
frets = 12

fretboard_html = """
<style>
.fretboard-wrap {
    overflow-x: auto;
    padding: 10px 0 20px 0;
}
.fretboard {
    position: relative;
    width: 910px;
    height: 300px;
    background: linear-gradient(180deg, #d2a679 0%, #c7925f 100%);
    border: 3px solid #6b4423;
    border-radius: 10px;
    margin-top: 20px;
}
.string-line {
    position: absolute;
    left: 40px;
    right: 20px;
    height: 2px;
    background: #444;
}
.fret-line {
    position: absolute;
    top: 20px;
    bottom: 20px;
    width: 2px;
    background: #555;
}
.nut {
    position: absolute;
    left: 38px;
    top: 20px;
    bottom: 20px;
    width: 6px;
    background: #222;
}
.fret-number {
    position: absolute;
    top: -2px;
    transform: translateX(-50%);
    font-size: 12px;
    color: #222;
}
.string-label {
    position: absolute;
    left: 8px;
    transform: translateY(-50%);
    font-weight: bold;
    color: #222;
}
.note-dot {
    position: absolute;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 11px;
    font-weight: bold;
    color: white;
    box-shadow: 0 1px 4px rgba(0,0,0,0.35);
}
.root-note {
    background: #d62828;
}
.scale-note {
    background: #1d4ed8;
}
.inlay {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.7);
    transform: translate(-50%, -50%);
}
.double-inlay {
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255,255,255,0.7);
    transform: translate(-50%, -50%);
}
</style>
<div class="fretboard-wrap">
  <div class="fretboard">
    <div class="nut"></div>
"""

string_positions = [40, 84, 128, 172, 216, 260]

# First real fret line starts after the nut
first_fret_x = 135
fret_spacing = 65
fret_positions = [first_fret_x + ((f + 1) * fret_spacing) for f in range(frets - 1)]

for i, y in enumerate(string_positions):
    fretboard_html += f'<div class="string-label" style="top:{y}px;">{strings[i]}</div>'
    fretboard_html += f'<div class="string-line" style="top:{y}px;"></div>'

for f, x in enumerate(fret_positions, start=1):
    if f > 1:  # skip the first line next to the nut
        fretboard_html += f'<div class="fret-line" style="left:{x}px;"></div>'
    fretboard_html += f'<div class="fret-number" style="left:{x-32}px;">{f}</div>'

for f, x in enumerate(fret_positions):
    if f > 0:  # skip the line right after the nut
        fretboard_html += f'<div class="fret-line" style="left:{x}px;"></div>'
    if f > 0:
        fretboard_html += f'<div class="fret-number" style="left:{x+32}px;">{f}</div>'   
# Fret markers
for marker_fret in [3, 5, 7, 9]:
    x = 40 + marker_fret * 65 + 32
    fretboard_html += f'<div class="inlay" style="left:{x}px; top:150px;"></div>'

# 12th fret double marker
x12 = 40 + 12 * 65 + 32
fretboard_html += f'<div class="double-inlay" style="left:{x12}px; top:110px;"></div>'
fretboard_html += f'<div class="double-inlay" style="left:{x12}px; top:190px;"></div>'

for s_idx, string in enumerate(strings):
    y = string_positions[s_idx]
    for fret in range(1, frets + 1):
        note_index = (notes.index(string) + fret) % 12
        note = notes[note_index]

        in_box = box_start <= fret <= box_start + 4

        if note in scale_notes:
            if box_mode and not in_box:
                continue

        for fret in range(frets + 1):
        note_index = (notes.index(string) + fret) % 12
        note = notes[note_index]

        x = first_fret_x + ((fret - 1) * fret_spacing) - 32
            css_class = "root-note" if note == key else "scale-note"
            fretboard_html += f'''
            <div class="note-dot {css_class}" style="left:{x}px; top:{y}px;">
                {note}
            </div>
            '''

fretboard_html += """
  </div>
</div>
"""

components.html(fretboard_html, height=360)


st.write("### Practice Tip")

if scale_name == "Minor Pentatonic":
    st.info(f"Try landing on {key} at the end of your phrases. That will make your solo sound more resolved.")
elif scale_name == "Blues":
    st.info(f"Use the {key} blues scale, but don’t sit on every note the same. The blue note works best as a passing tone.")
elif scale_name == "Major":
    st.info(f"Try starting and ending phrases on {key}. Then experiment with the 3rd and 5th for a more melodic sound.")




# Speed control (visual only for now)
speed = st.slider("Playback Speed (%)", 50, 150, 100)

# Loop section
st.write("### Loop Section")
loop_start = st.number_input("Start (seconds)", 0, 300, 0)
loop_end = st.number_input("End (seconds)", 0, 300, 30)

st.write(f"Looping from {loop_start}s to {loop_end}s")
