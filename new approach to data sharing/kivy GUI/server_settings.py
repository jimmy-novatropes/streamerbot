def counter_color_values():
    return {
    "white": [1, 0],
    "red": [1750, 0],
    "yellow": [511, 0],
    "green": [767, 0],
    "cyan": [1023, 0],
    "blue": [1279, 1],
    "magenta": [1535, 0],
    "purple": [1535, 0],
}

def modes_2_rpm():
    return {
    #"-7": [820, "forward"],
    # "-6": [945, "backward"],
    # "-5": [265, "backward"],
    # "-4": [1375, "backward"], #same as 820
    "-3": [425, "forward"],
    "-2": [685, "backward"],
    "-1": [1118, "forward"],
    "1": [1118, "backward"],
    "2": [685, "forward"],
    "3": [425, "backward"],
    # "4": [1375, "forward"],
    # "5": [265, "forward"],
    # "6": [945, "forward"]
    #"7": [820, "backward"], #same as 1375 but rougher
}