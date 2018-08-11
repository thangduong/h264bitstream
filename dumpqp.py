#! dump QP from an H264 ES
# python3 dumpqp.py <filename>
#
# output is csv of the form
#
# <frame-num>, <min_qp>, <max_qp>, <average_qp>, <all-slices-data>
#
# thang@quantee.com
#
import subprocess
import sys

result = subprocess.run(['./h264_analyze', sys.argv[1]], stdout=subprocess.PIPE)
lines = result.stdout.decode('utf-8').split('\n')
baseqp = -1
fnum = -1
frame_qp = []
for line in lines:
	params = line.split(': ')
	if "->pic_init_qp_minus26" in line:
		num = int(params[-1])
		baseqp = 26+num
	elif "->slice_qp_delta" in line:
		num = int(params[-1])
		qp = baseqp + num
		frame_qp.append(qp)
	elif "->frame_num" in line:
		num = int(params[-1])
		if num == fnum:
			None
		else:
			if fnum >= 0:
				print("%s, %s, %s, %s, \"%s\"" %(fnum, min(frame_qp), max(frame_qp), sum(frame_qp)/len(frame_qp), frame_qp))
			fnum = num
			frame_qp = []
