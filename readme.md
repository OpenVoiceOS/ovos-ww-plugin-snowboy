## Description
Mycroft/OpenVoiceOS wake word plugin for [Snowboy](https://github.com/seasalt-ai/snowboy)

## Install

`pip install ovos-ww-plugin-snowboy`

## Configuration

Each wake word can included several snowboy models, if any of them fires a detection is considered

TIP: you can use this to train a model for each speaker in your house

Add the following to your hotwords section in mycroft.conf

```json
  "hotwords": {
    "my_word": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "path/to/first.pmdl"},
            {"sensitivity": 0.5, "model_path": "path/to/second.pmdl"},
            {"sensitivity": 0.5, "model_path": "path/to/third.pmdl"}
         ]
    }
  }
```

Then select what wakeword to use

```json
 "listener": {
      "wake_word": "my_word"
 }
 
```

### Bundled wakeword models

All these are bundled with this plugin, they are universal models ```.umdl``` trained by snowboy and should have a good accuracy


```json
  "hotwords": {
    "alexa": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.6, "model_path": "alexa.umdl"}
         ]
    },
    "hey_extreme": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.6, "model_path": "hey_extreme.umdl"}
         ]
    },
    "computer": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.6, "model_path": "computer.umdl"}
         ]
    },
    "jarvis": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
            {"sensitivity": [0.8, 0.8],"model_path": "jarvis.umdl"}
         ]
    },
    "snowboy": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "snowboy.umdl"}
         ]
    },
    "smart_mirror": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "smart_mirror.umdl"}
         ]
    },
    "subex": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.5, "model_path": "subex.umdl"}
         ]
    },
    "neoya": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
              {"sensitivity": [0.7, 0.7], "model_path": "neoya.umdl"}
         ]
    },
    "view_glass": {
        "module": "ovos-ww-plugin-snowboy",
        "apply_frontend": true,
        "models": [
              {"sensitivity": 0.7, "model_path": "view_glass.umdl"}
         ]
    }
  }
```

# Training your own wake word

You can use the following public instances to train and download your model:
- https://snowboy.2022.us hosted by [@NeonGeckoCom](https://github.com/NeonGeckoCom)
- https://snowboy.jarbasai.online hosted by [@JarbasAi](https://github.com/JarbasAl)

Alternatively you can spin up a docker container locally, this only works in x86

`docker run -it -p 8000:8000 rhasspy/snowboy-seasalt`

then navigate to http://localhost:8000

[training source code](https://github.com/seasalt-ai/snowboy)
