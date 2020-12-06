To compile the snowboy lib for your platform

- apt-get install swig3.0
- apt-get install libatlas-base-dev
- git clone https://github.com/Kitt-AI/snowboy
- cd snowboy/swig/Python3
- edit snowboy/swig/Python3/Makefile
    - replace ```SWIG := swig``` with ```SWIG := swig3.0```
- make
- copy generated ```_snowboydetect.so``` and ```snowboydetect.py``` to ```jarbas_wake_word_plugin_snowboy/lib/{your_platform}```
- edit ```jarbas_wake_word_plugin_snowboy/snowboydecoder.py``` to also check for your platform
```python
# load the correct pre-compiled .so file for this platform
system = platform.system()
LOG.info("Running on: " + system)
if system == "Linux":
    machine = platform.machine()
    LOG.info("Platform: " + machine)
    if machine == "x86_64":
        from jarbas_wake_word_plugin_snowboy.lib.linux import snowboydetect
    elif machine == "armv6l":
        from jarbas_wake_word_plugin_snowboy.lib.rpi import snowboydetect
    elif machine == "armv7l":
        from jarbas_wake_word_plugin_snowboy.lib.rpi import snowboydetect
    else:
        raise ImportError("Machine not supported")
elif system == "Windows":
    raise ImportError("Windows is currently not supported")
else:
    raise ImportError("Your OS is currently not supported")
```
- if import is still failing you need to do the following edit or equivalent in ```jarbas_wake_word_plugin_snowboy/lib/{your_platform}/snowboydetect.py```
```python
def swig_import_helper():
    import importlib
    pkg = __name__.rpartition('.')[0]
    mname = '.'.join((pkg, '_snowboydetect')).lstrip('.')
    try:
        return importlib.import_module(mname)
    except ImportError:
        # this section was added by me
        from os.path import dirname
        import sys
        sys.path.append(dirname(__file__))
        return importlib.import_module('_snowboydetect')
```
- send a Pull Request!