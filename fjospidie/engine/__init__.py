engines = ['PcapEngine', "SuricataEngine"]


def start():
    for engine in engines:
        m = __import__(engine)
        c = getattr(m, engine)
        engine_obj = c()
        engine_obj.start()
