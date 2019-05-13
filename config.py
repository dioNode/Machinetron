configurationMap = {
    'handler': {
        'railSpeed': 100,
        'flipSpeed': 20,
        'spinSpeed': 500,
        'railDPR': 0.1,
        'flipDPR': 0.5,
        'spinDPR': 2,
        'id': 0x1A,
    }, 'drill': { # Location of lathe is measured relative to bottom
        'homeX': 100,
        'raiseSpeed': 1,
        'pushSpeed': 4,
        'spinSpeed': 500,
        'raiseDPR': 0.806,
        'pushDPR': 3.225,
        'spinDPR': 1,
        'diameter': 6,
        'depth': 80,
        'id': 0x1F,
        'detectionTolerance': 5,
    }, 'lathe': {
        'homeX': 300,
        'raiseSpeed': 1,
        'pushSpeed': 4,
        'spinSpeed': 0,
        'raiseDPR': 0.806,
        'pushDPR': 3.225,
        'spinDPR': 1,
        'length': 3,
        'depth': 60,
        'pushIncrement': 5,
        'id': 0x2A,
        'minDetectionRadius': 10,
        'maxDetectionRadius': 100,
    }, 'mill': {
        'homeX': 500,
        'raiseSpeed': 1,
        'pushSpeed': 4,
        'spinSpeed': 500,
        'raiseDPR': 0.806,
        'pushDPR': 3.225,
        'spinDPR': 1,
        'diameter': 10,
        'depth': 60,
        'id': 0x2F,
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
    }, 'instructions': {
        'NORM_INST': 0,

    }, 'other': {
        'infVal': 9999,
        'mmPerPixelRatio': 80/1200,
        'mmError': 1.0,
        'numRotationSteps': 200,
    }
}
