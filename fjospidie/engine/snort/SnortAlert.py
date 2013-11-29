import re
class SnortAlert:
    def __init__(self, alert):
        text_parts = alert.split("[**]")
        self.alarm_text = (re.compile("\[\d+:\d+:\d+\]").split(text_parts[1]))[1].strip()
        space_parts = alert.split(" ")
        self.classification = ((text_parts[2].split("["))[1]).split("]")[0]
        pri = (re.compile("\s+").split((((text_parts[2].split("["))[2]).split("]")[0])))[1]
        self.priority = int(pri)
        self.time = space_parts[0]
        self.dst = (((text_parts[2].split("} "))[1]).split("->"))[0]
        self.src = (((text_parts[2].split("} "))[1]).split("-> "))[1].strip()
