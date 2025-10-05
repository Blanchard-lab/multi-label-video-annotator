import subprocess
import sys
import shutil
import tempfile
import os

class AudioPlayer:
    def __init__(self):
        self.audio_process = None
        self._audio_tempfile = None

    def start(self, media_path, start_time=0, volume=50):
        self.stop()
        try:
            ffplay_path = shutil.which('ffplay')
            ffmpeg_path = shutil.which('ffmpeg')
            afplay_path = shutil.which('afplay')

            if sys.platform != 'darwin' and ffplay_path:
                if sys.platform == 'win32':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    self.audio_process = subprocess.Popen([
                        ffplay_path, '-nodisp', '-autoexit', '-ss', str(start_time),
                        '-volume', str(volume), media_path
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
                else:
                    self.audio_process = subprocess.Popen([
                        ffplay_path, '-nodisp', '-autoexit', '-ss', str(start_time),
                        '-volume', str(volume), media_path
                    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            elif sys.platform == 'darwin' and ffmpeg_path and afplay_path:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                tmp_path = tmp.name
                tmp.close()
                try:
                    cmd = [ffmpeg_path, '-hide_banner', '-loglevel', 'error',
                           '-ss', str(start_time), '-i', media_path,
                           '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2',
                           '-y', tmp_path]
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                    self.audio_process = subprocess.Popen([afplay_path, tmp_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
                    self._audio_tempfile = tmp_path
                except Exception:
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
                    self._audio_tempfile = None
                    self.audio_process = None
            elif ffplay_path:
                self.audio_process = subprocess.Popen([
                    ffplay_path, '-nodisp', '-autoexit', '-ss', str(start_time),
                    '-volume', str(volume), media_path
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
            else:
                self.audio_process = None
        except FileNotFoundError:
            self.audio_process = None

    def stop(self):
        if self.audio_process and self.audio_process.poll() is None:
            try:
                self.audio_process.terminate()
            except Exception:
                try:
                    self.audio_process.kill()
                except Exception:
                    pass
            finally:
                self.audio_process = None
        if self._audio_tempfile:
            try:
                os.unlink(self._audio_tempfile)
            except Exception:
                pass
            finally:
                self._audio_tempfile = None

    def restart(self, media_path, start_time=0, volume=50):
        if self.audio_process and self.audio_process.poll() is None:
            self.stop()
        self.start(media_path, start_time=start_time, volume=volume)
