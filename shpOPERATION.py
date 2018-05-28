# -*- coding: utf-8 -*-
import shapefile
import math
def nettoline():#单shp转多shp
    sf=shapefile.Reader(r"G:\SUTPC-DZ\bus\foshancoordbusline.shp")
    dir1=r"G:\SUTPC-DZ\bus\1"
    shapes = sf.shapes()
    print len(shapes)
    print shapes[3].points[7]
    fields = sf.fields
    records = sf.records()
    print fields,records[3][0:2]
    i=0
    for line in shapes:
        #len(shapes[3].points)
        print records[i][0]
        w = shapefile.Writer(shapefile.POINT)
        w.field('FIRST_FLD','C','40')
        w.field('SECOND_FLD', 'C', '40')
        j=0
        lastpoint=(520000,2500000)
        for point in line.points:
            #print point,line.bbox
            #print lastpoint,point
            #dis=(lastpoint[0]-point[0])*(lastpoint[0]-point[0])+(lastpoint[1]-point[1])*(lastpoint[1]-point[1])
            print len(line.points)
            if (j%20==0) or (j==0) or( j==(len(line.points)-1)):#dis>10000:
                w.point(point[0], point[1])
                w.record(records[i][0],'point')
            j=j+1
            #lastpoint = point
           # shpname=records[i][0][0:5]
        filename=str(i)+'.shp'
        w.save(filename)
        i = i + 1
        print 'success',i
def linetonet():#多shp转为单shp
    w = shapefile.Writer(shapefile.POLYLINE)
    w.field('lineinfo', 'C', '200')
    for i in range(1,1178):
        dir1 = 'G:/SUTPC-DZ/bus/20/%d.shp'%i
        sfor = shapefile.Reader(r"G:\SUTPC-DZ\bus\foshancoordbusline.shp")
        recordsor = sfor.records()
        sf = shapefile.Reader(dir1)
        shapes = sf.shapes()
        for line in shapes:
            #print line.points
            points=line.points
            #B = list(set(points))
           # B.sort(key=points.index)
            w.line([points], shapeType=shapefile.POLYLINE)
            #print line
            w.record( recordsor[i][0])
    w.save('G:/SUTPC-DZ/bus/0527/newbusline20.shp')
def multipointTOpoint():#多点shp保存一点
    sf = shapefile.Reader(r"G:/LAJI/1.shp")
    shapes = sf.shapes()
    record=sf.records()
    i=0
    w = shapefile.Writer(shapefile.POINT)
    w.field('name','C','100')
    for Apoints in shapes:
        print Apoints.points[0]
        w.point(Apoints.points[0][0],Apoints.points[0][1])
        w.record(record[i][1])
        print str(record[i][1])
        i=i+1
    w.save("G:/LAJI/2.shp")
def whatispolylineM():#解析polylineM
    sf = shapefile.Reader(r"G:/SUTPC-DZ/bus/single/1.shp")
    w = shapefile.Writer(shapefile.POLYLINE)
    w.field('lineinfo', 'C', '200')
    shapes = sf.shapes()
    print len(shapes)
    for things in shapes:
        print things.bbox
        print len(things.points)
        print things.parts
        w.poly([things.points], shapeType=shapefile.POLYLINE)
        w.record('1')
    w.save("G:/LAJI/4.shp")
def caldis(x1,y1,x2,y2):#计算距离
    return math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))
def keepdis50():
    sf = shapefile.Reader(r"G:/SUTPC-DZ/bus/0527/busunq.shp")
    w = shapefile.Writer(shapefile.POINT)
    w.field('name', 'C', '100')
    shapes = sf.shapes()
    pointli=[]
    for stop in shapes:
        #print stop.points
        #print pointli
        count=0
        try:
            for stop2 in pointli:
               # print stop2.points
                if(caldis(stop.points[0][0],stop.points[0][1],stop2.points[0][0],stop2.points[0][1]))<100:
                    break
                else:
                    count=count+1
        except Exception as e:
            import traceback, sys
            tb = sys.exc_info()[2]
            print "An error occured on line %i" % tb.tb_lineno
            print str(e)
        if len(pointli)==0: pointli.append(stop)
        if count==len(pointli):
            pointli.append(stop)
            w.point(stop.points[0][0],stop.points[0][1], shapeType=shapefile.POINT)
            w.record('point')
            print 'a'
    w.save(r'G:/SUTPC-DZ/bus/0527/100.shp')
#stopcode=[]
def busstationMATCHcode():
    sfstation = shapefile.Reader(r"G:/SUTPC-DZ/bus/0527/100.shp")
    sfroad=shapefile.Reader(r"G:/SUTPC-DZ/bus/0527/fsroad2017splitatpoint.shp")
    stations=sfstation.shapeRecords()
   # roads=sfroad.shapes()
    roadsREC=sfroad.shapeRecords()
    w = shapefile.Writer()
    #w.field('name', 'C', '100')
    w.field('code', 'C', '10')
    #print roadsREC
    #stopcode=[]
    for busstop in stations:
       # print busstop.points[0][0],busstop.points[0][1]
       #i=0
       for line in roadsREC:
            #print line.points[0],line.points[-1]
           # print i
           # print line.shape.points
           # w.point(busstop.shape.points[0][0],busstop.shape.points[0][1])
            try:
                if caldis(busstop.shape.points[0][0],busstop.shape.points[0][1],line.shape.points[0][0],line.shape.points[0][1])<51:

                    print (line.record)
                   # w.record(line.record[2])
                    stopcode.append(int(line.record[2]))
                    print 'start'
                    break
                if  caldis(busstop.shape.points[0][0], busstop.shape.points[0][1], line.shape.points[-1][0], line.shape.points[-1][1]) < 51:

                    print (line.record)
                  #  w.record(line.record[3])
                    stopcode.append(int(line.record[3]))
                    print 'end'
                    break
            except:
                #print i
                continue
           # i=i+1
    #w.save(r"G:/SUTPC-DZ/bus/bustationmatchnm/codematched.shp")
    print len(stopcode)
    file = open(r"G:/SUTPC-DZ/bus/bustationmatchnm/roadwithab.txt", 'w')
    file.write(str(stopcode));
    file.close()
def editorlinfile():#将非节点编号变负
    fpcode=open(r"G:/SUTPC-DZ/bus/bustationmatchnm/roadwithab.txt", 'r')
    codes=fpcode.readlines()
    stopcode=codes[0].split(',')
    print stopcode
    list2 = []
    for codenum in stopcode:
        try:
            list2.append(int(codenum))
        except:
            print 'error'
    print list2
    fp  = open(r"G:/SUTPC-DZ/bus/0527/200528.lin", 'r')
    lines = open(r"G:/SUTPC-DZ/bus/0527/200528.lin").readlines()  # 打开文件，读入每一行
    coordlist = []
    fp2 = open(r"G:/SUTPC-DZ/bus/bustationmatchnm/editor2.lin", 'w')
    for s in lines:
        #for code in stopcode:
        #print s
        l=s.split(',')
        if  'LINE NAME' in l[0]:
            coordlist=[]
            fp2.write("\n")
        flag=0
        for a in l:
           # print l
            #print a
            try:
                #print float(a)
              #  print coordlist
                print a
                if abs(int(a)) in coordlist:#删除重复项
                    if int(a)>0: tems1='-'+str(int(a))+', '
                    if int(a)<0: tems1 =str(int(a)) + ', '
                    s=s.replace(tems1,'',1)
                    #s = s.replace(tems2, '', -1)
            #        print '重复'
                    continue
                if (abs(int(a)) not in list2) :#替换不含在code中的
            #        print 'not in'
                    if int(a)>0:
                        minas= ', '+str(-1*int(a))
                        orin=', '+str(int(a))
                        #print minas
                        s=s.replace(orin,minas)
             #           print 'e'
                    #print  a
                else:
                    print 'in'
                    if int(a)<0:
                        minas=', '+str(abs(int(a)))
                        orin=', '+str(int(a))
                        s=s.replace(orin,minas)
                    #    print 'f'
                   # print 'not in code'
                   # print a
                coordlist.append(abs(int(a)))
                if (int(l[0]) not in list2 )and (flag==0) and (int(l[0])>0):#stopcode:#首行改变
                    s=s.replace(str(l[0]),'       '+str(-1*int(l[0])))
                    flag=1
                  #  print 'a'
            except Exception as e:
               # print str(e)
                import traceback, sys
                tb = sys.exc_info()[2]
                print "An error occured on line %i" % tb.tb_lineno
                print str(e)
                continue
        print str(s)
        fp2.write(s)
    fp2.close()
    fp.close()  # 关闭文件
if __name__ == '__main__':
   #nettoline()
   #multipointTOpoint()
   #whatispolylineM()
   #busstationMATCHcode()
   editorlinfile()
   #linetonet()
   # keepdis50()
