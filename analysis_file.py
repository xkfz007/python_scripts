#!/bin/python
import subprocess
import lib
class Codec_analysis:
  id=""
  fstr=""
  __format_strs=dict()
  __format_strs["ashevcd"]="Frm.*"
  __format_strs["as265"]="POC.*bits"
  __format_strs["x265"]="POC.*bits"
  __format_strs["x264"]="frame=.*bits"

  qp_idx=0
  __qp_idxs=dict()
  __qp_idxs["ashevcd"]=20
  __qp_idxs["as265"]=7
  __qp_idxs["x265"]=4
  __qp_idxs["x264"]=3

  bits_idx=0
  __bits_idxs=dict()
  __bits_idxs["ashevcd"]=3
  __bits_idxs["as265"]=8
  __bits_idxs["x265"]=5
  __bits_idxs["x264"]=10

  def __set_codec_prop(self):
    self.fstr=Codec_analysis.__format_strs[self.id]
    self.qp_idx=Codec_analysis.__qp_idxs[self.id]
    self.bits_idx=Codec_analysis.__bits_idxs[self.id]

  def __init__(self,id="as265"):
    self.id=id
    self.__set_codec_prop()

  def set_codec_id(self,id):
    self.id=id
    self.__set_codec_prop()


  def get_cl_ashevcd(self,input_file,idx=0):
    cl_list=[]
    cl_list.append('grep -o "'+self.fstr+'" '+input_file)
    cl_list.append("awk '{print $"+str(idx)+"}'")
    cl_list.append('tr -t "\\n" " "')
    return cl_list

  def get_cl_as265(self,input_file,idx=0):
    cl_list=[]
    cl_list.append('grep -o "'+self.fstr+'" '+input_file)
    cl_list.append("awk '{print $"+str(idx)+"}'")
    cl_list.append("awk -F\( '{print \$1}'")
    cl_list.append('tr -t "\\n" " "')
    return cl_list

  def get_cl_x265(self,input_file,idx=0):
    cl_list=[]
    cl_list.append('grep -o "'+self.fstr+'" '+input_file)
    cl_list.append("awk '{print $"+str(idx)+"}'")
    cl_list.append("awk -F\( '{print \$1}'")
    cl_list.append('tr -t "\\n" " "')
    return cl_list

  def get_cl_x264(self,input_file,idx=0):
    cl_list=[]
    cl_list.append('grep -o "'+self.fstr+'" '+input_file)
    cl_list.append("awk '{print $"+str(idx)+"}'")
    cl_list.append("awk -F\= '{print \$2}'")
    cl_list.append('tr -t "\\n" " "')
    return cl_list

  __func_list=dict()
  __func_list["ashevcd"]=get_cl_ashevcd
  __func_list["as265"]=get_cl_as265
  __func_list["x265"]=get_cl_x265
  __func_list["x264"]=get_cl_x264

  def get_col_vals(self,input_file,idx=0):
    #if lib.determin_sys()=="windows":
    #  return
    cl_list=Codec_analysis.__func_list[self.id](self,input_file,idx)
    full_cl="|".join(cl_list)
    print full_cl
    output=subprocess.check_output(full_cl,shell=True)
    return output

  def get_qp_vals(self,input_file):
    return self.get_col_vals(input_file,self.qp_idx)

  def get_bits_vals(self,input_file):
    return self.get_col_vals(input_file,self.bits_idx)



#def get_qp_ashevcd(input_file,idx):
#  if lib.determin_sys()=="windows":
#    return
#  format_string="Frm.*"
#  grep_cl="grep -o '"+format_string+"' "+input_file
#  awk_cl="awk '{print $"+str(idx)+"}'"
#  tr_cl="tr -t '\n' ' '"
#  full_cl=grep_cl+"|"+awk_cl+"|"+tr_cl
#  output=subprocess.check_output(full_cl,shell=True)
#  return output

cdc=Codec_analysis("ashevcd")

output_str=cdc.get_qp_vals(lib.format_file_path("F:\\tmp\\2015.04.13\\cons.log"))
print output_str


