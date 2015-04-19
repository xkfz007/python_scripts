
#classA=('Traffic_2560x1600_30_crop','PeopleOnStreet_2560x1600_30_crop')
#classB=('Kimono1_1920x1080_24','ParkScene_1920x1080_24','Cactus_1920x1080_50','BasketballDrive_1920x1080_50','BQTerrace_1920x1080_60')
#classC=('BasketballDrill_832x480_50','BQMall_832x480_60','PartyScene_832x480_50','RaceHorses_832x480_30')
#classD=('BasketballPass_416x240_50','BQSquare_416x240_60','BlowingBubbles_416x240_50','RaceHorses_416x240_30')
#classE=('FourPeople_1280x720_60','Johnny_1280x720_60','KristenAndSara_1280x720_60')
#classF=('BasketballDrillText_832x480_50','SlideEditing_1280x720_30','SlideShow_1280x720_20')

class_a=('Apeopleonstreet_2560x1600_8_30_150', 'Atraffic_2560x1600_8_30_150')
class_b=('Bbasketballdrive_1920x1080_8_50_500', 'Bbqterrace_1920x1080_8_60_600',
 'Bcactus_1920x1080_8_50_500', 'Bkimono_1920x1080_8_24_240', 'Bparkscene_1920x1080_8_24_240')
class_c=('Cbasketballdrill_832x480_8_50_500', 'Cbqmall_832x480_8_60_600',
'Cpartyscene_832x480_8_50_500', 'Cracehorses_832x480_8_30_300')
class_d=('Dbasketballpass_416x240_8_50_500', 'Dblowingbubbles_416x240_8_50_500',
'Dbqsquare_416x240_8_60_600', 'Dracehorses_416x240_8_30_300')
class_e=('Efourpeople_1280x720_8_60_600', 'Ejohnny_1280x720_8_60_600', 'Ekristenandsara_1280x720_8_60_600')
class_f=('Fbasketballdrilltext_832x480_8_50_500', 'Fchinaspeed_1024x768_8_30_500',
'Fslideediting_1280x720_8_30_300', 'Fslideshow_1280x720_8_20_500')
class_i=('Iduckstakeoff_1280x720_8_25_500', 'Ifcwr_1920x1080_8_25_6987',
'Iflowervase_832x480_8_25_300', 'Iintotree_1280x720_8_25_500', 'Ikeiba_832x480_8_25_300',
'Imobcalter_1280x720_8_25_500', 'Imobisode2_832x480_8_25_300', 'Imonkey_1280x720_8_25_79',
'Inavyflight_1920x1080_8_30_2973', 'Iparkjoy_1280x720_8_25_500', 'Istockholmter_1280x720_8_25_600',
'Itennis_1920x1080_8_25_240', 'Ividyo1_1280x720_8_25_600', 'Ividyo3_1280x720_8_25_600', 'Ividyo4_1280x720_8_25_600',
'Ixtslf_1920x1080_8_25_1854')
class_special=('Ifcwr_1920x1080_8_25_6987','Ixtslf_1920x1080_8_25_1854','Inavyflight_1920x1080_8_30_2973')
class_x=('Xclownlogoed_3840x2160_8_25_640', 'Xsnake_3840x2160_8_25_353', 'Xsusielogoed_3840x2160_8_25_588')

class_std2=class_b+class_c+class_d+class_e+class_f
class_std=class_a+class_b+class_c+class_d+class_e+class_f

def get_seqname(name):
  seq_list=class_a+class_b+class_c+class_d+class_e+class_f+class_special+class_x
  for i in seq_list:
    if i.upper().find(name.upper().split('_')[0])>=0:
      return i

  return name

