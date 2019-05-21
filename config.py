configurationMap = {
    'handler': {
        'railSpeed': 25,
        'flipSpeed': 12,
        'spinSpeed': 400,
        'maxRailSpeed': 80,
        'maxFlipSpeed': 20,
        'maxSpinSpeed': 500,
        'railDPR': 40,
        'flipDPR': 24.8276,
        'spinDPR': 360,
        'maxRail': 200,
        'maxFlip': 100,
        'id': 0x1A,
    }, 'drill': { # Location of lathe is measured relative to bottom
        'homeX': 35,
        'raiseSpeed': 25,
        'pushSpeed': 50,
        'spinSpeed': 500,
        'maxRaiseSpeed': 30,
        'maxPushSpeed': 80,
        'maxSpinSpeed': 500,
        'raiseDPR': 8.06,
        'pushDPR': 32.25,
        'spinDPR': 1,
        'maxRaise': 110,
        'maxPush': 70,
        'diameter': 6,
        'depth': 80,
        'id': 0x1F,
        'detectionTolerance': 10,
    }, 'lathe': {
        'homeX': 70,
        'raiseSpeed': 25,
        'pushSpeed': 50,
        'spinSpeed': 0,
        'maxRaiseSpeed': 30,
        'maxPushSpeed': 80,
        'maxSpinSpeed': 500,
        'raiseDPR': 8.06,
        'pushDPR': 32.25,
        'spinDPR': 1,
        'maxRaise': 110,
        'maxPush': 70,
        'length': 3,
        'depth': 60,
        'pushIncrement': 5,
        'id': 0x2A,
        'minDetectionRadius': 10,
        'maxDetectionRadius': 100,
    }, 'mill': {
        'homeX': 40,
        'raiseSpeed': 25,
        'pushSpeed': 50,
        'spinSpeed': 500,
        'maxRaiseSpeed': 40,
        'maxPushSpeed': 80,
        'maxSpinSpeed': 500,
        'raiseDPR': 8.06,
        'pushDPR': 32.25,
        'spinDPR': 1,
        'maxRaise': 110,
        'maxPush': 70,
        'diameter': 10,
        'depth': 60,
        'id': 0x2F,
    }, 'offsets': {
        'cuttingBit2HandlerCenter': 40,
        'cuttingBit2HandlerFlipBase': 90,
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
        'START_INST': 1,
        'PAUSE_INST': 2,
        'STOP_INST': 3,
    }, 'other': {
        'infVal': 9999,
        'homeVal': -10,
        'mmPerPixelRatio': 0.1, # Using the y direction
        'mmError': 1.0,
        'speedMultiplier': 3,
        'numRotationSteps': 200,
        'syncSpeed': 15,
    }
}
