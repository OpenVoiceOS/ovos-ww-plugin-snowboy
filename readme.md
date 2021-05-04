## Description
Mycroft wake word plugin for [Snowboy](https://github.com/seasalt-ai/snowboy)

## Install

`mycroft-pip install jarbas-wake-word-plugin-snowboy`

## Configuration

Each wake word can included several snowboy models, if any of them fires a detection is considered

TIP: you can use this to train a model for each speaker in your house

Add the following to your hotwords section in mycroft.conf

```json
  "hotwords": {
    "my_word": {
        "module": "snowboy_ww_plug",
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
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.6, "model_path": "alexa.umdl"}
         ]
    },
    "hey_extreme": {
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.6, "model_path": "hey_extreme.umdl"}
         ]
    },
    "computer": {
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.6, "model_path": "computer.umdl"}
         ]
    },
    "jarvis": {
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
            {"sensitivity": [0.8, 0.8],"model_path": "jarvis.umdl"}
         ]
    },
    "snowboy": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "snowboy.umdl"}
         ]
    },
    "smart_mirror": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "smart_mirror.umdl"}
         ]
    },
    "subex": {
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
            {"sensitivity": 0.5, "model_path": "subex.umdl"}
         ]
    },
    "neoya": {
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
              {"sensitivity": [0.7, 0.7], "model_path": "neoya.umdl"}
         ]
    },
    "view_glass": {
        "module": "snowboy_ww_plug",
        "apply_frontend": true,
        "models": [
              {"sensitivity": 0.7, "model_path": "view_glass.umdl"}
         ]
    },
    "hey_computer": {
        "module": "snowboy_ww_plug",
        "models": [
              {"sensitivity": 0.5, "model_path": "hey_computer.pmdl"},
              {"sensitivity": 0.5, "model_path": "hey_computer_alt.pmdl"}
         ]
    },
    "hey_neon": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_neon.pmdl"}
         ]
    },
    "hey_device": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_device.pmdl"}
         ]
    },
    "hey_dexter": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_dexter.pmdl"}
         ]
    },
    "dexter": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "dexter.pmdl"}
         ]
    },
    "ó_computador": {
        "module": "snowboy_ww_plug",
        "models": [
             {"sensitivity": 0.5, "model_path": "ó_computador.pmdl"}
         ]
    },
    "ó_jarbas": {
        "module": "snowboy_ww_plug",
        "models": [
             {"sensitivity": 0.5, "model_path": "ó_jarbas.pmdl"}
         ]
    },
    "ó_sauro": {
        "module": "snowboy_ww_plug",
        "models": [
             {"sensitivity": 0.5, "model_path": "ó_sauro.pmdl"}
         ]
    },
    "red_alert": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "red_alert.pmdl"}
         ]
    },
    "thank_you": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "thank_you.pmdl"}
        ]
    },
    "fuck_you": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "fuck_you.pmdl"}
        ]
    },
    "hey_mycroft_snowboy": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "hey_mycroft.pmdl"}
        ]
    },
    "wake_up_snowboy": {
        "module": "snowboy_ww_plug",
        "models": [
            {"sensitivity": 0.5, "model_path": "wake_up.pmdl"}
        ]
    },
    "desperta": {
        "module": "snowboy_ww_plug",
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
