from enum import Enum

DOMAIN = "elkbledom_melk"

CONF_RESET = "reset"
CONF_DELAY = "delay"

CONF_BRIGHTNESS_MODE = "brightness_mode"
BRIGHTNESS_MODES = ["auto", "rgb", "native"]
DEFAULT_BRIGHTNESS_MODE = "auto"


class EFFECTS(Enum):
    none = 0x00
    jump_red_green_blue = 0x87
    jump_red_green_blue_yellow_cyan_magenta_white = 0x88
    crossfade_red_green_blue = 0x89
    crossfade_red_green_blue_yellow_cyan_magenta_white = 0x8A
    crossfade_red = 0x8B
    crossfade_green = 0x8C
    crossfade_blue = 0x8D
    crossfade_yellow = 0x8E
    crossfade_cyan = 0x8F
    crossfade_magenta = 0x90
    crossfade_white = 0x91
    crossfade_red_green = 0x92
    crossfade_red_blue = 0x93
    crossfade_green_blue = 0x94
    blink_red_green_blue_yellow_cyan_magenta_white = 0x95
    blink_red = 0x96
    blink_green = 0x97
    blink_blue = 0x98
    blink_yellow = 0x99
    blink_cyan = 0x9A
    blink_magenta = 0x9B
    blink_white = 0x9C


EFFECTS_list = [e.name for e in EFFECTS]
EFFECTS_MAP = {e.name: e.value for e in EFFECTS}

EFFECT_PROFILES = {
    "none": {"label": "💡 Static", "icon": "mdi:lightbulb-on", "hint": "Постоянный мягкий свет"},
    "jump_red_green_blue": {"label": "⚡ Jump RGB", "icon": "mdi:led-strip-variant", "hint": "Резкие RGB-переходы"},
    "jump_red_green_blue_yellow_cyan_magenta_white": {"label": "🌈 Jump All", "icon": "mdi:led-strip", "hint": "Быстрое переключение палитры"},
    "crossfade_red_green_blue": {"label": "🌤️ Fade RGB", "icon": "mdi:gradient-horizontal", "hint": "Плавный переход RGB"},
    "crossfade_red_green_blue_yellow_cyan_magenta_white": {"label": "🌈 Smooth Cycle", "icon": "mdi:infinity", "hint": "Мягкое перетекание палитры"},
    "crossfade_red": {"label": "🔴 Fade Red", "icon": "mdi:circle"},
    "crossfade_green": {"label": "🟢 Fade Green", "icon": "mdi:circle"},
    "crossfade_blue": {"label": "🔵 Fade Blue", "icon": "mdi:circle"},
    "crossfade_yellow": {"label": "🟡 Fade Yellow", "icon": "mdi:circle"},
    "crossfade_cyan": {"label": "💠 Fade Cyan", "icon": "mdi:circle"},
    "crossfade_magenta": {"label": "💜 Fade Magenta", "icon": "mdi:circle"},
    "crossfade_white": {"label": "🤍 Fade White", "icon": "mdi:circle-outline"},
    "crossfade_red_green": {"label": "🔴🟢 Fade R-G", "icon": "mdi:circle-multiple"},
    "crossfade_red_blue": {"label": "🔴🔵 Fade R-B", "icon": "mdi:circle-multiple"},
    "crossfade_green_blue": {"label": "🟢🔵 Fade G-B", "icon": "mdi:circle-multiple"},
    "blink_red_green_blue_yellow_cyan_magenta_white": {"label": "🎇 Blink All", "icon": "mdi:lightning-bolt-circle", "hint": "Яркое мигание всеми цветами"},
    "blink_red": {"label": "🔴 Blink Red", "icon": "mdi:flash"},
    "blink_green": {"label": "🟢 Blink Green", "icon": "mdi:flash"},
    "blink_blue": {"label": "🔵 Blink Blue", "icon": "mdi:flash"},
    "blink_yellow": {"label": "🟡 Blink Yellow", "icon": "mdi:flash"},
    "blink_cyan": {"label": "💠 Blink Cyan", "icon": "mdi:flash"},
    "blink_magenta": {"label": "💜 Blink Magenta", "icon": "mdi:flash"},
    "blink_white": {"label": "🤍 Blink White", "icon": "mdi:flash-outline"},
}

EFFECT_LABELS = {key: data["label"] for key, data in EFFECT_PROFILES.items()}

__all__ = [
    "DOMAIN",
    "CONF_RESET",
    "CONF_DELAY",
    "CONF_BRIGHTNESS_MODE",
    "BRIGHTNESS_MODES",
    "DEFAULT_BRIGHTNESS_MODE",
    "EFFECTS",
    "EFFECTS_MAP",
    "EFFECT_LABELS",
    "EFFECT_PROFILES",
]
