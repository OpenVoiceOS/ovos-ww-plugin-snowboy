#!/usr/bin/env python
import platform
import os
import logging
from ovos_ww_plugin_snowboy.exceptions import ModelNotFound
from os.path import isfile, join, expanduser

# create logger
logging.basicConfig()
LOG = logging.getLogger("snowboy")
LOG.setLevel(logging.INFO)

# load the correct pre-compiled .so file for this platform
system = platform.system()
LOG.info("Running on: " + system)
if system == "Linux":
    machine = platform.machine()
    LOG.info("Platform: " + machine)
    if machine == "x86_64":
        from ovos_ww_plugin_snowboy.lib.linux import snowboydetect
    elif machine == "armv6l":
        # TODO not sure this is functional!!!
        from ovos_ww_plugin_snowboy.lib.rpi import snowboydetect
    elif machine == "armv7l":
        from ovos_ww_plugin_snowboy.lib.rpi import snowboydetect
    else:
        raise ImportError("Machine not supported")
elif system == "Windows":
    raise ImportError("Windows is currently not supported")
else:
    raise ImportError("Your OS is currently not supported")

PKG_ROOT = os.path.dirname(os.path.abspath(__file__))
RESOURCE_FILE = os.path.join(PKG_ROOT, "resources/common.res")


def find_model(model):
    # check if it's a full path
    if isfile(expanduser(model)):
        return expanduser(model)

    # check in bundled models
    bundled_models_path = join(PKG_ROOT, "resources", "models")
    model_no_ext = model.split("/")[-1].split(".")[0].replace(" ", "_")
    model_no_ext = join(bundled_models_path, model_no_ext)
    if isfile(model_no_ext + ".umdl"):
        # universal model found
        model = model_no_ext + ".umdl"
    elif isfile(model_no_ext + ".pmdl"):
        # personal model found
        model = model_no_ext + ".pmdl"
    else:
        raise ModelNotFound("could not find " + model)
    return model


def get_detector(decoder_model,
                 resource=RESOURCE_FILE,
                 sensitivity=None,
                 audio_gain=1,
                 apply_frontend=False):
    """
    :param decoder_model: decoder model file path, a string or a list of strings
    :param resource: resource file path.
    :param sensitivity: decoder sensitivity, a float of a list of floats.
                              The bigger the value, the more senstive the
                              decoder. If an empty list is provided, then the
                              default sensitivity in the model will be used.
    :param audio_gain: multiply input volume by this factor.
    :param apply_frontend: applies the frontend processing algorithm if True.
    """
    sensitivity = sensitivity or []
    tm = type(decoder_model)
    ts = type(sensitivity)
    if tm is not list:
        decoder_model = [decoder_model]
    if ts is not list:
        sensitivity = [sensitivity]
    model_str = ",".join(decoder_model)

    detector = snowboydetect.SnowboyDetect(resource_filename=resource.encode(),
                                           model_str=model_str.encode())
    detector.SetAudioGain(audio_gain)
    detector.ApplyFrontend(apply_frontend)
    num_hotwords = detector.NumHotwords()

    if len(decoder_model) > 1 and len(sensitivity) == 1:
        sensitivity = sensitivity * num_hotwords
    if len(sensitivity) != 0:
        assert num_hotwords == len(sensitivity), \
            "number of hotwords in decoder_model (%d) and sensitivity " \
            "(%d) does not match" % (num_hotwords, len(sensitivity))
    sensitivity_str = ",".join([str(t) for t in sensitivity])
    if len(sensitivity) != 0:
        detector.SetSensitivity(sensitivity_str.encode())
    return detector


# Code bellow is not used by the plugin directly, but made available for
# standalone usage, this was lifted directly from snowboy github with minor
# changes made:
# - the get_detector method above was extracted from HotwordDetector
# - pyaudio was made optional
# - pep8 fixes

import collections
import time
import wave
from ctypes import *
from contextlib import contextmanager

try:
    import pyaudio
except ImportError:
    # made optional, since we might be feeding frames to detector some other
    # way
    pyaudio = None

DETECT_DING = os.path.join(PKG_ROOT, "resources/ding.wav")
DETECT_DONG = os.path.join(PKG_ROOT, "resources/dong.wav")


def py_error_handler(filename, line, function, err, fmt):
    pass


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int,
                               c_char_p)

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def no_alsa_error():
    try:
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield
        pass


class RingBuffer:
    """Ring buffer to hold audio from PortAudio"""

    def __init__(self, size=4096):
        self._buf = collections.deque(maxlen=size)

    def extend(self, data):
        """Adds data to the end of buffer"""
        self._buf.extend(data)

    def get(self):
        """Retrieves data from the beginning of buffer and clears it"""
        tmp = bytes(bytearray(self._buf))
        self._buf.clear()
        return tmp


def play_audio_file(fname=DETECT_DING):
    """Simple callback function to play a wave file. By default it plays
    a Ding sound.

    :param str fname: wave file name
    :return: None
    """
    ding_wav = wave.open(fname, 'rb')
    ding_data = ding_wav.readframes(ding_wav.getnframes())
    if pyaudio is None:
        raise ImportError("pyaudio is not installed")
    with no_alsa_error():
        audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format=audio.get_format_from_width(ding_wav.getsampwidth()),
        channels=ding_wav.getnchannels(),
        rate=ding_wav.getframerate(), input=False, output=True)
    stream_out.start_stream()
    stream_out.write(ding_data)
    time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()


class HotwordDetector:
    """
    Snowboy decoder to detect whether a keyword specified by `decoder_model`
    exists in a microphone input stream.

    :param decoder_model: decoder model file path, a string or a list of strings
    :param resource: resource file path.
    :param sensitivity: decoder sensitivity, a float of a list of floats.
                              The bigger the value, the more senstive the
                              decoder. If an empty list is provided, then the
                              default sensitivity in the model will be used.
    :param audio_gain: multiply input volume by this factor.
    :param apply_frontend: applies the frontend processing algorithm if True.
    """

    def __init__(self, decoder_model,
                 resource=RESOURCE_FILE,
                 sensitivity=None,
                 audio_gain=1,
                 apply_frontend=False):
        self.detector = get_detector(decoder_model, resource, sensitivity,
                                     audio_gain, apply_frontend)
        self.num_hotwords = self.detector.NumHotwords()
        self.ring_buffer = RingBuffer(
            self.detector.NumChannels() * self.detector.SampleRate() * 5)
        self._running = False
        self.stream_in = None
        self.audio = None
        self.recordedData = []

    def start(self, detected_callback=play_audio_file,
              interrupt_check=lambda: False,
              sleep_time=0.03,
              audio_recorder_callback=None,
              silent_count_threshold=15,
              recording_timeout=100):
        """
        Start the voice detector. For every `sleep_time` second it checks the
        audio buffer for triggering keywords. If detected, then call
        corresponding function in `detected_callback`, which can be a single
        function (single model) or a list of callback functions (multiple
        models). Every loop it also calls `interrupt_check` -- if it returns
        True, then breaks from the loop and return.

        :param detected_callback: a function or list of functions. The number of
                                  items must match the number of models in
                                  `decoder_model`.
        :param interrupt_check: a function that returns True if the main loop
                                needs to stop.
        :param float sleep_time: how much time in second every loop waits.
        :param audio_recorder_callback: if specified, this will be called after
                                        a keyword has been spoken and after the
                                        phrase immediately after the keyword has
                                        been recorded. The function will be
                                        passed the name of the file where the
                                        phrase was recorded.
        :param silent_count_threshold: indicates how long silence must be heard
                                       to mark the end of a phrase that is
                                       being recorded.
        :param recording_timeout: limits the maximum length of a recording.
        :return: None
        """
        if pyaudio is None:
            raise ImportError("pyaudio is not installed")

        def audio_callback(in_data, frame_count, time_info, status):
            self.ring_buffer.extend(in_data)
            play_data = chr(0) * len(in_data)
            return play_data, pyaudio.paContinue

        with no_alsa_error():
            self.audio = pyaudio.PyAudio()
        self.stream_in = self.audio.open(
            input=True, output=False,
            format=self.audio.get_format_from_width(
                self.detector.BitsPerSample() / 8),
            channels=self.detector.NumChannels(),
            rate=self.detector.SampleRate(),
            frames_per_buffer=2048,
            stream_callback=audio_callback)

        if interrupt_check():
            LOG.debug("detect voice return")
            return

        tc = type(detected_callback)
        if tc is not list:
            detected_callback = [detected_callback]
        if len(detected_callback) == 1 and self.num_hotwords > 1:
            detected_callback *= self.num_hotwords

        assert self.num_hotwords == len(detected_callback), \
            "Error: hotwords in your models (%d) do not match the number of " \
            "callbacks (%d)" % (self.num_hotwords, len(detected_callback))

        LOG.debug("detecting...")

        state = "PASSIVE"
        recording_count = 0
        silent_count = 0
        self._running = True
        while self._running is True:
            if interrupt_check():
                LOG.debug("detect voice break")
                break
            data = self.ring_buffer.get()
            if len(data) == 0:
                time.sleep(sleep_time)
                continue

            status = self.detector.RunDetection(data)
            if status == -1:
                LOG.warning(
                    "Error initializing streams or reading audio data")

            # small state machine to handle recording of phrase after keyword
            if state == "PASSIVE":
                if status > 0:  # key word found
                    self.recordedData = []
                    self.recordedData.append(data)
                    silent_count = 0
                    recording_count = 0
                    message = "Keyword " + str(status) + " detected at time: "
                    message += time.strftime("%Y-%m-%d %H:%M:%S",
                                             time.localtime(time.time()))
                    LOG.info(message)
                    callback = detected_callback[status - 1]
                    if callback is not None:
                        callback()

                    if audio_recorder_callback is not None:
                        state = "ACTIVE"
                    continue

            elif state == "ACTIVE":
                stop_recording = False
                if recording_count > recording_timeout:
                    stop_recording = True
                elif status == -2:  # silence found
                    if silent_count > silent_count_threshold:
                        stop_recording = True
                    else:
                        silent_count = silent_count + 1
                elif status == 0:  # voice found
                    silent_count = 0

                if stop_recording:
                    fname = self.save_message()
                    audio_recorder_callback(fname)
                    state = "PASSIVE"
                    continue

                recording_count = recording_count + 1
                self.recordedData.append(data)

        LOG.debug("finished.")

    def save_message(self):
        """
        Save the message stored in self.recordedData to a timestamped file.
        """
        filename = 'output' + str(int(time.time())) + '.wav'
        data = b''.join(self.recordedData)

        # use wave to save data
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(
            self.audio.get_format_from_width(
                self.detector.BitsPerSample() / 8)))
        wf.setframerate(self.detector.SampleRate())
        wf.writeframes(data)
        wf.close()
        LOG.debug("finished saving: " + filename)
        return filename

    def terminate(self):
        """
        Terminate audio stream. Users can call start() again to detect.
        :return: None
        """
        if self.stream_in is not None:
            self.stream_in.stop_stream()
            self.stream_in.close()
        if self.audio is not None:
            self.audio.terminate()
        self._running = False
