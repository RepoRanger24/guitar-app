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

# Speed control (visual only for now)
speed = st.slider("Playback Speed (%)", 50, 150, 100)

# Loop section
st.write("### Loop Section")
loop_start = st.number_input("Start (seconds)", 0, 300, 0)
loop_end = st.number_input("End (seconds)", 0, 300, 30)

st.write(f"Looping from {loop_start}s to {loop_end}s")
