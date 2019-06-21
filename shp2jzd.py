# -*- encoding: utf-8 -*-
import arcpy 
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')
fields = ['DKMC','SHAPE@','SHAPE@AREA']
dataset = 'test1.shp'

#读取prj文件描述信息
spatial_ref = arcpy.Describe(dataset)
SR = spatial_ref.spatialReference
#取最后两位为带号
DH = format(SR.name[-2:])

#判断80还是2000
if SR.name[0:4]=='Xian':
    s_type = '80'
elif SR.name[0:4]=='CGCS':
    s_type = '2000'
else:
    s_type = ''
    
with arcpy.da.SearchCursor('test1.shp', fields) as cursor:
    for row in cursor:
        num = 0
        qh = 1
        list_rings = eval(format(row[1].JSON))["rings"]
        
        #因为首行要写入圈数、点数等信息，方便起见先记录，实际上这里重复工作了
        for fc in list_rings:
            num = num+len(fc)
            qh = qh+1
            
        #界址点数量
        jzd_num =  num
        #地块面积(公顷)
        dk_area = row[2]/10000
        #地块名称
        dkmc = row[0]
        
        
        with open(dkmc+'.txt', 'a') as f:
            f.writelines(' [属性描述]'+'\n')
            f.writelines('格式版本号=1.00版本'+'\n')
            f.writelines('数据产生单位=上海杰狮信息技术有限公司''\n')
            f.writelines('数据产生日期='+time.strftime('%Y-%m-%d')+'\n')
            f.writelines('坐标系='+s_type+'国家大地坐标系'+'\n')
            f.writelines('几度分带=3'+'\n')
            f.writelines('投影类型=高斯克吕格'+'\n')
            f.writelines('计量单位=米'+'\n')
            f.writelines('带号='+DH+'\n')
            f.writelines('精度='+'\n')
            f.writelines('转换参数='+'\n')
            f.writelines('[地块坐标]'+'\n')
            f.writelines(format(jzd_num+1)+','+format(dk_area)+',,'+format(dkmc)+',面,,,@'+'\n')
     
            qh = 1
            jzd_objectid = 1
            for ring in list_rings:
                #界址点最后一个点和第一个点相同，这里记录每圈第一个界址点的编号
                start_objectid = jzd_objectid
                for point in ring:
                    f.writelines(format(jzd_objectid)+','+format(qh)+','+format(point[0])+','+format(point[1])+'\n')
                    jzd_objectid = jzd_objectid+1
                #写入每圈的第一个点
                f.writelines(format(start_objectid)+','+format(qh)+','+format(ring[0][0])+','+format(ring[0][0])+'\n')

                qh =qh+1  
        
        print row[0]+'输出完毕！'
            
            
            
