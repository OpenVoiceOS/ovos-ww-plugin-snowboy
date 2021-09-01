# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from ovos_plugin_manager.templates.hotwords import HotWordEngine
from ovos_ww_plugin_snowboy.snowboydecoder import get_detector, \
    find_model
from ovos_ww_plugin_snowboy.exceptions import ModelNotFound


class SnowboyHotWordPlugin(HotWordEngine):
    def __init__(self, key_phrase="hey mycroft", config=None, lang="en-us"):
        super().__init__(key_phrase, config, lang)

        # load models
        apply_frontend = self.config.get("apply_frontend", False)
        models = self.config.get("models") or [{"model_path": key_phrase}]
        if not len(models):
            raise ModelNotFound("config does not include any models!")
        paths = []
        sensitivities = []
        for model in models:
            path = model.get("model_path", key_phrase)
            sensitivity = model.get("sensitivity", 0.5)
            if isinstance(sensitivity, list):
                sensitivities.extend(sensitivity)
            else:
                sensitivities.append(sensitivity)

            paths.append(find_model(path))
            
        # load snowboy
        self.snowboy = get_detector(paths, sensitivity=sensitivities,
                                    apply_frontend=apply_frontend)

    def found_wake_word(self, frame_data):
        wake_word = self.snowboy.RunDetection(frame_data)
        return wake_word >= 1

