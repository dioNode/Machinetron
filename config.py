configurationMap = {
    'handler': {
        'railSpeed': 10,
        'flipSpeed': 12,
        'spinSpeed': 100,
        'rapidRailSpeed': 50,
        'rapidSpinSpeed': 360*2,
        'initialRampUpSpeed': 100,
        'maxRailSpeed': 80,
        'maxFlipSpeed': 20,
        'maxSpinSpeed': 500,
        'railDPR': 39.23809524,
        'flipDPR': 25.7142857,
        'spinDPR': 360,
        'maxRail': 239.5,
        'maxFlip': 90,
        'id': 0x1A,
    }, 'drill': { # Location of lathe is measured relative to bottom
        'homeX': 205,
        'raiseSpeed': 10,
        'pushSpeed': 5,
        'spinSpeed': 500,
        'rapidRaiseSpeed': 25,
        'rapidPushSpeed': 50,
        'rapidSpinSpeed': 500,
        'maxRaiseSpeed': 30,
        'maxPushSpeed': 80,
        'maxSpinSpeed': 500,
        'raiseDPR': 8.06115358,
        'pushDPR': 31.643,
        'spinDPR': 1,
        'maxRaise': 140 - 5,
        'maxPush': 190,
        'diameter': 6,
        'depth': 80,
        'pushIncrement': 5,
        'id': 0x1F,
        'detectionTolerance': 10,
        'offsets': {
            'cuttingBit2HandlerCenter': 187 - 10 + 6,
            'cuttingBit2HandlerFlipBase': 152 - 3 + 1,
            'cuttingBitHeightOffset': 22,
            'cuttingBitHeightOffsetFlipped': 15 - 3 + 5,
            'motorStartDepthOffset': 30, # The amount of distance before the drill should start spinning
        },
    }, 'lathe': {
        'homeX': 91,
        'raiseSpeed': 2,
        'pushSpeed': 2,
        'spinSpeed': 0,
        'rapidRaiseSpeed': 25,
        'rapidPushSpeed': 50,
        'rapidSpinSpeed': 0,
        'maxRaiseSpeed': 30,
        'maxPushSpeed': 80,
        'maxSpinSpeed': 500,
        'raiseDPR': 8.06115358,
        'pushDPR': 31.643,
        'spinDPR': 1,
        'maxRaise': 145 - 10,
        'maxPush': 189,
        'length': 3,
        'depth': 60,
        'pushIncrement': 2,
        'id': 0x2A,
        'minDetectionRadius': 10,
        'maxDetectionRadius': 100,
        'offsets': {
            'cuttingBit2HandlerCenter': 189,
            'cuttingBit2HandlerFlipBase': 157,
            'cuttingBitHeightOffset': 26 - 6 - 1,
            'cuttingBitHeightOffsetFlipped': 11,
            'motorStartDepthOffset': 40 - 10 - 5 - 4, # The amount of distance before the handler should start spinning
        },
    }, 'mill': {
        'homeX': 46,
        'raiseSpeed': 10,
        'pushSpeed': 10,
        'spinSpeed': 500,
        'rapidRaiseSpeed': 25,
        'rapidPushSpeed': 50,
        'rapidSpinSpeed': 500,
        'maxRaiseSpeed': 40,
        'maxPushSpeed': 80,
        'maxSpinSpeed': 500,
        'raiseDPR': 8.06115358,
        'pushDPR': 31.643,
        'spinDPR': 1,
        'maxRaise': 131 - 2,
        'maxPush': 185,
        'diameter': 10,
        'depth': 60,
        'pushIncrement': 20,
        'id': 0x2F,
        'offsets': {
            'cuttingBit2HandlerCenter': 175 - 3,
            'cuttingBit2HandlerFlipBase': 144 - 5 - 3,
            'cuttingBitHeightOffset': 17 - 3,
            'cuttingBitHeightOffsetFlipped': 16 - 2 - 6 - 1,
            'motorStartDepthOffset': 30, # The amount of distance before the mill should start spinning
        },
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
        'speedMultiplier': 10,
        'numRotationSteps': 200,
        'syncSpeed': 15,
        'gripperHeight': 30,
    }
}
