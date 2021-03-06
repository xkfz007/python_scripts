# classA=('Traffic_2560x1600_30_crop','PeopleOnStreet_2560x1600_30_crop')
# classB=('Kimono1_1920x1080_24','ParkScene_1920x1080_24','Cactus_1920x1080_50','BasketballDrive_1920x1080_50','BQTerrace_1920x1080_60')
#classC=('BasketballDrill_832x480_50','BQMall_832x480_60','PartyScene_832x480_50','RaceHorses_832x480_30')
#classD=('BasketballPass_416x240_50','BQSquare_416x240_60','BlowingBubbles_416x240_50','RaceHorses_416x240_30')
#classE=('FourPeople_1280x720_60','Johnny_1280x720_60','KristenAndSara_1280x720_60')
#classF=('BasketballDrillText_832x480_50','SlideEditing_1280x720_30','SlideShow_1280x720_20')

import logging
import os.path

class_a = ('Apeopleonstreet_2560x1600_8_30_150', 'Atraffic_2560x1600_8_30_150')
class_b = ('Bbasketballdrive_1920x1080_8_50_500', 'Bbqterrace_1920x1080_8_60_600',
           'Bcactus_1920x1080_8_50_500', 'Bkimono_1920x1080_8_24_240', 'Bparkscene_1920x1080_8_24_240')
class_c = ('Cbasketballdrill_832x480_8_50_500', 'Cbqmall_832x480_8_60_600',
           'Cpartyscene_832x480_8_50_500', 'Cracehorses_832x480_8_30_300')
class_d = ('Dbasketballpass_416x240_8_50_500', 'Dblowingbubbles_416x240_8_50_500',
           'Dbqsquare_416x240_8_60_600', 'Dracehorses_416x240_8_30_300')
class_e = ('Efourpeople_1280x720_8_60_600', 'Ejohnny_1280x720_8_60_600', 'Ekristenandsara_1280x720_8_60_600')
class_f = ('Fbasketballdrilltext_832x480_8_50_500', 'Fchinaspeed_1024x768_8_30_500',
           'Fslideediting_1280x720_8_30_300', 'Fslideshow_1280x720_8_20_500')
class_h=('Hforeman_176x144_8_25_300','Hforeman_352x288_8_25_300')
class_i = ('Iduckstakeoff_1280x720_8_25_500', 'Ifcwr_1920x1080_8_25_6987',
           'Iflowervase_832x480_8_25_300', 'Iintotree_1280x720_8_25_500', 'Ikeiba_832x480_8_25_300',
           'Imobcalter_1280x720_8_25_500', 'Imobisode2_832x480_8_25_300', 'Imonkey_1280x720_8_25_79',
           'Inavyflight_1920x1080_8_30_2973', 'Iparkjoy_1280x720_8_25_500', 'Istockholmter_1280x720_8_25_600',
           'Itennis_1920x1080_8_25_240', 'Ividyo1_1280x720_8_25_600', 'Ividyo3_1280x720_8_25_600',
           'Ividyo4_1280x720_8_25_600',
           'Ixtslf_1920x1080_8_25_1854')
class_special = ('Ifcwr_1920x1080_8_25_6987', 'Ixtslf_1920x1080_8_25_1854', 'Inavyflight_1920x1080_8_30_2973','kldby_1920x1080_25')
class_special2 = ('ztv_720x576_25',)
class_x = ('Xclownlogoed_3840x2160_8_25_640', 'Xsnake_3840x2160_8_25_353', 'Xsusielogoed_3840x2160_8_25_588')
class_m=('ClassAmerge_2560x1600_30','ClassBMerge_1920x1080_24','ClassEMerge_1280x720_60','ClassFMerge_1280x720_30')

class_std2 = class_b + class_c + class_d + class_e + class_f
class_std = class_a + class_b + class_c + class_d + class_e + class_f


def guess_seqname(name):
    if name.lower().endswith('.yuv'):
        name,ext=os.path.splitext(name)
        return name
    seq_list = class_a + class_b + class_c + class_d + class_e + class_f + class_special + class_x + class_special2+class_m+class_h
    for i in seq_list:
        if i.upper().find(name.upper().split('_')[0]) >= 0:
            return i

    return name

import sys

def get_reso_info(seq_name):
    common_reso_list = ('176x144', '352x288', '416x240', '832x480', '1024x768',
                        '1280x720', '1920x1080', '2560x1600', '3840x2160',
                        '640x480', '448x336', '720x576')
    common_fps_list = (15, 20, 23, 24, 25, 30, 50, 60)
    #seq_name format: name_widthxheight_fps or
    #                 name_widthxheight_bitdepth_fps_totalframes
    print "seq_name=%s"%seq_name
    import os.path
    tmp_list = seq_name.split('_')
    print tmp_list
    width=0
    height=0
    fps=0
    if tmp_list[1] not in common_reso_list:
        logging.warning("maybe the resolution is invalid, please check")
    else:
        reso = tmp_list[1].split('x')
        if type(reso[0])==int:
            width = int(reso[0])
        if type(reso[1])==int:
           height = int(reso[1])

    if len(tmp_list)>2 and type(tmp_list[2])==int:
        fps = int(tmp_list[2])
        if fps < 15:
            if len(tmp_list) == 5:
                fps = int(tmp_list[3])
            else:
                fps = 30  #default fps
        if fps not in common_fps_list:
            logging.error("maybe the fps is invalid, please check")
    return (width, height, fps)

