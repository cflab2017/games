from pydub import AudioSegment

#오디오 파일 로드
audio = AudioSegment.from_file("production.mp3")

# 시작 시간과 종료 시간 설정
start_time = 300  # 시작 시간(밀리초)
end_time = 600  # 종료 시간(밀리초)

# 오디오 파일 자르기
trimmed_audio = audio[start_time:end_time]

# 자른 오디오 파일 저장
# trimmed_audio.export("whoosh2.mp3", format="mp3")
trimmed_audio.export("production.wav", format="wav")