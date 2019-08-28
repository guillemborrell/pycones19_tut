from streamz import Stream
import pandas as pd
from flappystream.analysis import flatten_record
import ujson
from operator import methodcaller


data = b'[{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":223.08000000000004,"radius":9,"speed":5.04,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":96,"score":{"best":34,"value":8},"timestamp":1566846826562},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":299.0600000000001,"radius":9,"speed":6.439999999999999,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":154,"score":{"best":34,"value":8},"timestamp":1566846827532},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":328.56000000000023,"radius":9,"speed":5.000000000000001,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":204,"score":{"best":34,"value":8},"timestamp":1566846828357},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":304.44000000000034,"radius":9,"speed":2.4800000000000013,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":240,"score":{"best":34,"value":8},"timestamp":1566846828959},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":285.82000000000045,"radius":9,"speed":2.8400000000000016,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":278,"score":{"best":34,"value":8},"timestamp":1566846829592},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":288.0200000000005,"radius":9,"speed":3.9200000000000026,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":322,"score":{"best":34,"value":8},"timestamp":1566846830329},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":286.3000000000006,"radius":9,"speed":3.7400000000000024,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":365,"score":{"best":34,"value":8},"timestamp":1566846831042},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":301.34000000000066,"radius":9,"speed":4.460000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":412,"score":{"best":34,"value":8},"timestamp":1566846831821},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":282.72000000000077,"radius":9,"speed":2.8400000000000016,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":450,"score":{"best":34,"value":8},"timestamp":1566846832463},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":241.2200000000008,"radius":9,"speed":0.5000000000000012,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":475,"score":{"best":34,"value":8},"timestamp":1566846832871},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":228.82000000000085,"radius":9,"speed":3.200000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":515,"score":{"best":34,"value":8},"timestamp":1566846833537},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":187.02000000000086,"radius":9,"speed":-0.5799999999999987,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":534,"score":{"best":34,"value":8},"timestamp":1566846833864},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":197.60000000000093,"radius":9,"speed":4.280000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":580,"score":{"best":34,"value":8},"timestamp":1566846834621},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":212.640000000001,"radius":9,"speed":4.460000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":627,"score":{"best":34,"value":8},"timestamp":1566846835415},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":232.3200000000011,"radius":9,"speed":4.6400000000000015,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":675,"score":{"best":34,"value":8},"timestamp":1566846836217},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":234.52000000000118,"radius":9,"speed":3.9200000000000026,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":719,"score":{"best":34,"value":8},"timestamp":1566846836947},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":222.12000000000123,"radius":9,"speed":3.200000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":759,"score":{"best":34,"value":8},"timestamp":1566846837604},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":311.52000000000135,"radius":9,"speed":6.799999999999998,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":819,"score":{"best":34,"value":8},"timestamp":1566846838607},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":292.90000000000146,"radius":9,"speed":2.8400000000000016,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":857,"score":{"best":34,"value":8},"timestamp":1566846839247},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":262.8000000000015,"radius":9,"speed":-2.1999999999999984,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":867,"score":{"best":34,"value":8},"timestamp":1566846839415},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":228.8400000000015,"radius":9,"speed":-1.8399999999999983,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":879,"score":{"best":34,"value":8},"timestamp":1566846839609},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":189.92000000000155,"radius":9,"speed":1.0400000000000011,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":907,"score":{"best":34,"value":8},"timestamp":1566846840073},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":165.8000000000016,"radius":9,"speed":2.4800000000000013,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":943,"score":{"best":34,"value":8},"timestamp":1566846840674},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":true,"bird":{"x":50,"y":180.8400000000017,"radius":9,"speed":4.460000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":990,"score":{"best":34,"value":8},"timestamp":1566846841468},{"player":"","uuid":"635cf93d-5a4c-4573-9698-a7967482ac43","alive":false,"bird":{"x":50,"y":191.42000000000178,"radius":9,"speed":4.280000000000002,"gravity":0.18},"pipes":{"position":[{"x":52,"y":-287.45929773374957},{"x":250,"y":-197.1858726040121}],"h":400,"gap":85,"w":53},"frames":1035,"score":{"best":34,"value":8},"timestamp":1566846842218}]'


def test_save_to_database():
    stream = Stream()

    (
        stream.map(ujson.loads)
        .flatten()
        .map(flatten_record)
        .partition(10)
        .map(pd.DataFrame)
        .map(methodcaller("to_csv", header=False, sep="\t", na_rep='\\N'))
        .sink(print)
    )

    stream.emit(data)

    assert False
