DOMAIN = "melk_led"

WRITE_UUID = "0000fff3-0000-1000-8000-00805f9b34fb"

# MELK-OA / MELK-Ox style login (must be sent after connect)
LOGIN_1 = bytes([0x7E, 0x07, 0x83])
LOGIN_2 = bytes([0x7E, 0x04, 0x04])

# Power (MELK-OA family — tested variants)
CMD_ON = bytes([0x7E, 0x00, 0x04, 0xF0, 0x00, 0x01, 0xFF, 0x00, 0xEF])
CMD_OFF = bytes([0x7E, 0x00, 0x04, 0x00, 0x00, 0x00, 0xFF, 0x00, 0xEF])

# Alternate power (some MELK-Ox / Lotus)
CMD_ON_ALT = bytes([0x7E, 0x07, 0x04, 0xFF, 0x00, 0x01, 0x02, 0x01, 0xEF])
CMD_OFF_ALT = bytes([0x7E, 0x07, 0x04, 0x00, 0x00, 0x00, 0x02, 0x01, 0xEF])

# Effects map (name -> byte)
EFFECTS = {
    "none": 0x00,
    "jump_rgb": 0x87,
    "jump_all": 0x88,
    "fade_rgb": 0x89,
    "fade_all": 0x8A,
    "fade_red": 0x8B,
    "fade_green": 0x8C,
    "fade_blue": 0x8D,
    "blink_all": 0x95,
    "blink_red": 0x96,
    "blink_green": 0x97,
    "blink_blue": 0x98,
}

EFFECT_LABELS = {
    "none": "Static",
    "jump_rgb": "Jump RGB",
    "jump_all": "Jump All",
    "fade_rgb": "Fade RGB",
    "fade_all": "Fade All",
    "fade_red": "Fade Red",
    "fade_green": "Fade Green",
    "fade_blue": "Fade Blue",
    "blink_all": "Blink All",
    "blink_red": "Blink Red",
    "blink_green": "Blink Green",
    "blink_blue": "Blink Blue",
}
