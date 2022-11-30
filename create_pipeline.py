import argparse

DEFAULT_VIDEO="sync-test-60FPS.mp4"

parser = argparse.ArgumentParser(
    description = 'Write in stdout the gst pipeline to test intel and d3d11'
)

parser.add_argument('-n', '--num', type=int, help='number of concurrent decoders', default=10)
parser.add_argument('-d', '--debug-level', type=int, help='gst debug level', default=3)
parser.add_argument('-i', '--input-file', help='H.264/MP4 input file', default=DEFAULT_VIDEO)
parser.add_argument('-o', '--os', help='OS to test in Linux', choices=["win", "linux"], default='win')
parser.add_argument('-f', '--fake-sink', help='Use fakesink', action='store_true', default=False)
parser.add_argument('-l', '--gst-launch', help='gst-launch.exe binary path', default='gst-launch-1.0.exe')
args = parser.parse_args()

exe = args.gst_launch if args.gst_launch != 'gst-launch-1.0.exe' else 'gst-launch-1.0.exe' if args.os == 'win' else 'gst-launch-1.0'
sink = 'fakesink' if args.fake_sink else 'd3d11videosink' if args.os == 'win' else 'vaapisink'
dec = 'd3d11h264dec' if args.os == 'win' else 'vaapih264dec'

BINARY="{} --gst-debug={} ".format(exe, args.debug_level)
BODY="filesrc location=\"{}\" ! qtdemux ! h264parse ! queue ! {} ! queue ! {}  ".format(args.input_file, dec, sink)

print(BINARY, end='')
for i in range(args.num):
    print(BODY, end='')
print('')
