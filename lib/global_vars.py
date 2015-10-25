x265_ver = "v1.6"

# RC modes, enum type simple implementation
HEVC_RC_FIXQUANT = 0
HEVC_RC_CBR = 1
HEVC_RC_QUALITY_RANK = 2
HEVC_RC_VBR = 3
HEVC_RC_CONFERENCE = 4
HEVC_RC_ABR_TWOPASS_ANAlYSE = 5
HEVC_RC_ABR_TWOPASS_ENC = 6
HEVC_RC_VBR_Q = 7
HEVC_RC_ABR = 8
HEVC_RC_CQP = 9
HEVC_RC_CRF = 10
HEVC_RC_VBR_TWOPASS_ANAlYSE = 11
HEVC_RC_VBR_TWOPASS_ENC = 12

RC_STRING = ( 'HEVC_RC_FIXQUANT', 'HEVC_RC_CBR', 'HEVC_RC_QUALITY_RANK', 'HEVC_RC_VBR',
              'HEVC_RC_CONFERENCE', 'HEVC_RC_ABR_TWOPASS_ANAlYSE', 'HEVC_RC_ABR_TWOPASS_ENC', 'HEVC_RC_VBR_Q',
              'HEVC_RC_ABR', 'HEVC_RC_CQP', 'HEVC_RC_CRF', 'HEVC_RC_VBR_TWOPASS_ANAlYSE', 'HEVC_RC_VBR_TWOPASS_ENC'  )
RC_DICT = {'CQP': HEVC_RC_CQP,
           'CQ': HEVC_RC_FIXQUANT,
           'ABR': HEVC_RC_ABR,
           'CBR': HEVC_RC_CBR,
           'VBR': HEVC_RC_VBR,
           'ABR-2': HEVC_RC_ABR_TWOPASS_ANAlYSE,
           'VBR-2': HEVC_RC_VBR_TWOPASS_ANAlYSE,
           'CRF': HEVC_RC_CRF,
}

h264_extension = ('.264', '.avc', '.h264')
h265_extension = ('.265', '.hevc', '.h265')

ashevcd_name_list = ('ashevcd', 'ashevc', 'as265d')
jmd_name_list = ('jmd',)
hmd_name_list = ('hmd',)

h264_decoder_list = (jmd_name_list[0],)
h265_decoder_list = (ashevcd_name_list[0], hmd_name_list[0])

as265_name_list=('as265','a265')
jm_name_list=('jm',)
hm_name_list=('hm',)
x264_name_list=('x264',)
x265_name_list=('x265',)

h264_encoder_list=(x264_name_list[0],jmd_name_list[0])
h265_encoder_list=(as265_name_list[0],x265_name_list[0],hm_name_list[0])

import logging
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]:%(message)s')
