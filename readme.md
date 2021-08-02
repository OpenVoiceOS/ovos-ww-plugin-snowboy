## Description
Mycroft wake word plugin for [Snowboy](https://github.com/seasalt-ai/snowboy)

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

All these are bundled with this plugin, the ones ending with ```.umdl``` should have a good accuracy, the others are not very accurate and you should tweak the sensitivity

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
    },
    "hey_computer": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
              {"sensitivity": 0.5, "model_path": "hey_computer.pmdl"},
              {"sensitivity": 0.5, "model_path": "hey_computer_alt.pmdl"}
         ]
    },
    "hey_neon": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_neon.pmdl"}
         ]
    },
    "hey_device": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_device.pmdl"}
         ]
    },
    "hey_dexter": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_dexter.pmdl"}
         ]
    },
    "dexter": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "dexter.pmdl"}
         ]
    },
    "ó_computador": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
             {"sensitivity": 0.5, "model_path": "ó_computador.pmdl"}
         ]
    },
    "ó_jarbas": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
             {"sensitivity": 0.5, "model_path": "ó_jarbas.pmdl"}
         ]
    },
    "ó_sauro": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
             {"sensitivity": 0.5, "model_path": "ó_sauro.pmdl"}
         ]
    },
    "red_alert": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "red_alert.pmdl"}
         ]
    },
    "thank_you": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "thank_you.pmdl"}
        ]
    },
    "fuck_you": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "fuck_you.pmdl"}
        ]
    },
    "hey_mycroft_snowboy": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_mycroft.pmdl"}
        ]
    },
    "wake_up_snowboy": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "wake_up.pmdl"}
        ]
    },
    "desperta": {
        "module": "ovos-ww-plugin-snowboy",
        "models": [
            {"sensitivity": 0.5, "model_path": "desperta_jm.pmdl"},
            {"sensitivity": 0.5, "model_path": "desperta_jm2.pmdl"}
        ]
    }
  }
```

If you want to replace the default mycroft models without changing the wake words

```json
 "listener": {
      "wake_word": "hey_mycroft_snowboy",
      "stand_up_word": "wake_up_snowboy"
 }
 
```

# Training your own wake word

You can train models by following the instructions here [snowboy](https://github.com/seasalt-ai/snowboy)
It is recomended to use the docker method for ease of use.
