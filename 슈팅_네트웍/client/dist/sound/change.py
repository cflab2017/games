
from pydub import AudioSegment

wav_file_path = f'./whoosh2.wav'
audio = AudioSegment.from_mp3('whoosh2.mp3')
audio.export(wav_file_path, format="wav")