from pydub import AudioSegment
import math

# Indlæs lydfilen
input_file = r"C:\Users\ruk\Downloads\Akraft\AK høring.mp3"
audio = AudioSegment.from_mp3(input_file)

# Definer segmentlængden (40 minutter i millisekunder)
segment_length_ms = 40 * 60 * 1000

# Beregn antal segmenter
num_segments = math.ceil(len(audio) / segment_length_ms)

# Gem hver segment som en ny fil
for i in range(num_segments):
    start_time = i * segment_length_ms
    end_time = min((i + 1) * segment_length_ms, len(audio))
    segment = audio[start_time:end_time]
    output_file = f"C:\\Users\\ruk\\Downloads\\Akraft\\AK_høring_part_{i + 1}.mp3"
    segment.export(output_file, format="mp3")
    print(f"Segment {i + 1} gemt som {output_file}")

print("Opdeling af lydfil er færdig.")
