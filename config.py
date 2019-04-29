configurationMap = {
    'handler': {
        'railSpeed': 100,
        'flipSpeed': 20,
        'spinSpeed': 500,
        'railDPR': 0.1,
        'flipDPR': 0.5,
        'spinDPR': 2,
        'id': 0x01,
    }, 'drill': { # Location of lathe is measured relative to bottom
        'homeX': 100,
        'raiseSpeed': 20,
        'pushSpeed': 30,
        'spinSpeed': 500,
        'raiseDPR': 10,
        'pushDPR': 5,
        'spinDPR': 1,
        'diameter': 6,
        'depth': 80,
        'id': 0x02,
    }, 'lathe': {
        'homeX': 300,
        'raiseSpeed': 20,
        'pushSpeed': 30,
        'spinSpeed': 0,
        'raiseDPR': 10,
        'pushDPR': 5,
        'spinDPR': 1,
        'length': 3,
        'depth': 60,
        'pushIncrement': 5,
        'id': 0x03,
    }, 'mill': {
        'homeX': 500,
        'raiseSpeed': 20,
        'pushSpeed': 30,
        'spinSpeed': 500,
        'raiseDPR': 10,
        'pushDPR': 5,
        'spinDPR': 1,
        'diameter': 10,
        'depth': 60,
        'id': 0x04,
    }, 'offsets': {
        'cuttingBit2HandlerCenter': 70,
        'cuttingBit2HandlerFlipBase': 140,
    }, 'coordination': {
        'speed': 20,
    }, 'motorMap': {
        'spin': 2,
        'vert': 3,
        'pen': 1,
        'rail': 1,
        'flip': 3,
    }, 'other': {
        'infVal': 9999,
    }
}
