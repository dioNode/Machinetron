#!/usr/bin/python

# also runs with pypy
import sys, re
from optparse import OptionParser
from STL.trianglezslice import TriZSlice

def generateSlices(filename, throughFace, sliceNum):
    parser = OptionParser()
    parser.add_option("-s", "--stl",        dest="stlfiles",     action="append",metavar="FILE",   help="Input STL file")
    parser.add_option("-o", "--output",     dest="outputfile",   default=None,metavar="FILE",      help="Output image name (can contain %d or %f) for multiple names")
    parser.add_option("-t", "--transform",  dest="transform",    default="unit",                   help="Transformation to apply to STL file")
    parser.add_option("-q", "--quiet",      dest="verbose",      default=True,action="store_false",help="Verbose")
    parser.add_option("-w", "--width",      dest="widthpixels",  default=1200,type="int",          help="Bitmap width")
    parser.add_option("",   "--height",     dest="heightpixels", default=0,type="int",             help="Bitmap height")
    parser.add_option("",   "--extra",      dest="extra",        default="5%",                     help="Extra space to leave around the model")
    parser.add_option("-p", "--position",   dest="position",     default="mid",                    help="Position")
    parser.add_option("-n", "--nslices",    dest="nslices",      default=0,type="int",             help="Number of slices to make")
    parser.add_option("-z", "--zlevel",     dest="zlevels",      action="append",                  help="Zlevel values to slice at")
    parser.add_option("-i", "--inputs",     dest="cinputs",      default=False,action="store_true",help="Wait for lines from input stream of form 'zvalue [pngfile]\\n'")
    parser.description = "Slices STL files into black and white PNG bitmaps as a batch or on demand"
    parser.epilog = "For more speed try running with pypy"

    options, args = parser.parse_args()
    #options, args = parser.parse_args(args=[])  # to run within debugger
    print('args', args)
    args = []
    options.stlfiles = [filename]
    options.nslices = sliceNum
    #, 'outputfile': None, 'transform': 'unit', 'verbose': True, 'widthpixels': 1200, 'heightpixels': 0, 'extra': '5%', 'position': 'mid', 'nslices': 10, 'zlevels': None, 'cinputs': False}


    if not options.stlfiles:
        parser.print_help()
        exit(1)

    if not options.outputfile:
        rfile = re.sub("\.stl$(?i)", "", options.stlfiles[0])
        if options.nslices != 0:
            options.outputfile = rfile+"_%04d.png"
        elif options.zlevels:
            options.outputfile = rfile+"_%010f.png"
        else:
            options.outputfile = rfile+".png"

    # load the stl files into trianglebarmeshes
    transmaps = { "unit":lambda t: t, "swapyz": lambda t: (t[0], -t[2], t[1]) }

    tzs = TriZSlice(options.verbose)
    for stlfile in options.stlfiles:
        tzs.LoadSTLfile(stlfile, transmaps[options.transform])

    tzs.LoadSTLfile(stlfile, transmaps['unit'])

    # Determin the ranges from the loaded files
    tzs.SetExtents(options.extra)
    tzs.BuildPixelGridStructures(options.widthpixels, options.heightpixels)

    def pngname(optionoutputfile, i, z):
        if re.search("%.*?d(?i)", optionoutputfile):
            return optionoutputfile % i
        if re.search("%.*?f(?i)", optionoutputfile):
            return optionoutputfile % z
        return optionoutputfile

    if options.nslices != 0:
        for i in range(options.nslices):
            z = tzs.zlo + (tzs.zhi - tzs.zlo)*(i + 0.5)/options.nslices
            print('zloose', z, tzs.zlo, tzs.zhi, i, options.nslices)
            tzs.SliceToPNG(z, pngname(options.outputfile, i, z), throughFace)

    i = options.nslices
    for sz in options.zlevels or []:
        z = float(z)
        tzs.SliceToPNG(z, pngname(options.outputfile, i, z), throughFace)
        i += 1

    if options.cinputs:
        if options.verbose:
            print("Give zvalue within [%.3f,%.3f] and optionally pngfile name followed by linefeed" % (tzs.zlo, tzs.zhi))
        while True:
            cl = sys.stdin.readline().strip()
            if cl == "":
                break
            lcl = cl.split(None, 1)
            z = float(lcl[0])
            tzs.SliceToPNG(z, pngname(lcl[1] if len(lcl) == 2 else options.outputfile, i, z), throughFace)
            i += 1
