'''
#def_app3a
  # use_ferret
# def_app4(nc_file='', outDir=''):

'''
import os
#os.environ['PROJ_LIB']='/opt/conda/lib/python2.7/site-packages/pyproj/data'

def help():
  '''
<br><a href=%s>%s</a>
'''
  port = 'localhost:5003'
  a0 = port
  a1 = '%s/app1?a=5&b=3'%port
  a2 = '%s/app2?nc_file="/app_dir/user/zos_AVISO_L4_199210-201012.nc"'%port
  a3 = '%s/app3?nc_file="/app_dir/user/zos_AVISO_L4_199210-201012.nc"&var_name="zos"'%port
  temp1 = '''
<html>
<body>
<br>== for this help message   j :
<br><a hrep='%s'>%s</a>
<br>
<br>== an app of adding two numbers:
<br><a hrep='%s'>%s</a>
<br>
<br>== check an online NetCDF file
<br><a hrep='%s'>%s</a>
<br>== plot an online NetCDF file
<br><a hrep='%s'>%s</a>
</body>
</html>
''' %(
a0,a0,
a1,a1,
a2,a2,
a3,a3,
)
  print(temp1)
  return temp1

def app1(a=1,b=2, outDir=''):
  mes='a=%f    b=%f    a+b = %f'%(float(a), float(b), float(a) + float(b))
  img=None
  data=None
  return mes, img, data

def app3z(nc_file='', var_name='tmn', k=1, l=1, outDir=''):
  # init_ferret
  import pyferret as pf
  pf.start(quiet=True, unmapped=True)
  pf.run('set memory/size=500')
  pf.run('cancel mode logo' )
  pf.run('cancel mode journal' )

  temp1 = 'use "%s"'%nc_file
  print(temp1)
  pf.run(temp1)

  temp1 = 'show data'
  print(temp1)
  pf.run(temp1)

  #temp1 = 'shade %s[k=%d,l=%d]\ngo land'%(var_name, k, l)
  temp1 = 'shade %s[l=%d]'%(var_name, l)
  print(temp1)
  pf.run(temp1)

  temp1 = 'go land'
  print(temp1)
  pf.run(temp1)

  t1 = outDir.find('static')
  outDir1 = outDir[t1:]
  figFile1 = '%s/plot.png'%outDir1
  print(figFile1)

  figFile0 = '%s/plot.png'%outDir
  temp1 = 'frame/file="%s"'%figFile0
  print(temp1)
  pf.run(temp1)

  
  mess = 'Plot var %s of file:\n%s'%(nc_file, var_name)
  figFile = 'http://ec2-13-56-153-11.us-west-1.compute.amazonaws.com:5003/%s'%figFile1
  return mess, figFile, None

def app2(nc_file='', outDir=''):
  import checkNc2
  
  dict1 = {}
  dict1['fileName'] = nc_file
  dict1['source'] = 'online'
  dict1['message'] = ''

  ok1 = checkNc2.checkNc(nc_file, dict1, allowOverwrite=0)
  return dict1['check']+dict1['message'], None, None

# def_app4(nc_file='', outDir=''):
def app4(nc_file='', outDir=''):
  import subprocess 
  import shlex 

  ncdumpBin = '/opt/conda/bin/ncdump'
  temp1a = '%s -c %s'%(ncdumpBin, nc_file)
  #temp1a = 'ls -la'
  temp1 = shlex.split(temp1a)
  print temp1
  sp = subprocess.Popen(temp1,stdout = subprocess.PIPE)
  sp.wait()
  stdOut1, err = sp.communicate()
  print(stdOut1)
  return stdOut1, None, None


#def_app3a(nc_file='', var_name=None, k=1, l=1, outDir=''):
def app3(nc_file='', var_name=None, k=1, l=1, outDir=''):
  # checkNc
  import checkNc2
  
  dict1 = {}
  dict1['fileName'] = nc_file
  dict1['source'] = 'online'
  dict1['message'] = ''

  ok1 = checkNc2.checkNc(nc_file, dict1, allowOverwrite=0)

  mes1 = dict1['message']
  mes1 += '\n\n' + dict1['check']

  print(ok1)
  print('dict1.key:')
  for kk in dict1.keys():
    print(kk)

  varList = dict1['varList']
  var_name1 = None
  if var_name is None:
    for v in varList:
        d2 = dict1['varDict'][v]['dim2']
        if (len(d2)>1) and (len(d2)<5):
          if (d2[-1] == 'lon') and (d2[-2] == 'lat'):
            var_name1 = v
            nD = len(d2)
  else:
    var_name1 = var_name
    try:
      d2 = dict1['varDict'][var_name]['dim2']
      nD = len(d2)
    except:
      text1 = 'Variable %s does not exist in the file.'%var_name
      print(text1)
      mes1 += '\n%s'%text1
    
  if var_name1 is None:
    mes1 += '\n\n## Cannot figure out which variable to plot.##'

  # plotting
  k = int(k)
  l = int(l)


  # use_ferret
  if 1: 
    # init_ferret
    import pyferret as pf
    pf.start(quiet=True, unmapped=True)
    pf.run('set memory/size=1000')
    pf.run('cancel mode logo' )
    pf.run('cancel mode journal' )

    temp1 = 'use "%s"'%nc_file
    print(temp1)
    pf.run(temp1)

    temp1 = 'show data'
    print(temp1)
    pf.run(temp1)

    if nD==2:
        temp1 = 'shade %s'%(var_name1)
    elif nD==3:
        temp1 = 'shade %s[l=%d]'%(var_name1, l)
    elif nD==4:
        temp1 = 'shade %s[k=%d, l=%d]'%(var_name1, k, l)
    print(temp1)
    pf.run(temp1)

    temp1 = 'go land'
    print(temp1)
    pf.run(temp1)

    t1 = outDir.find('static')
    outDir1 = outDir[t1:]
    figFile1 = '%s/plot.png'%outDir1
    print(figFile1)

    figFile0 = '%s/plot.png'%outDir
    temp1 = 'frame/file="%s"'%figFile0
    print(temp1)
    pf.run(temp1)


  if 0: # use basemap
    from netCDF4 import Dataset
    import matplotlib as mpl
    mpl.use('Agg')  # for interactive. Work on svm3 
    import matplotlib.pylab as Mat
    from mpl_toolkits.basemap import Basemap

    mpl.rcParams['image.cmap'] = 'jet'

    nc = Dataset(nc_file)
    ncVar =  nc.variables[var_name1]
    dims1 = ncVar.dimensions
    print(dims1)
    print(ncVar.shape)

    if 0:
        if len(dims1)==3:
            data1 = ncVar[k-1, ::-1,:]
        elif len(dims1)==4:
            data1 = ncVar[k-1,l-1,::-1,:]
        elif len(dims1)==2:
            data1 = ncVar[::-1,:]
    if 1: 
        if len(dims1)==3:
            data1 = ncVar[k-1, :,:]
        elif len(dims1)==4:
            data1 = ncVar[k-1,l-1,:,:]
        elif len(dims1)==2:
            data1 = ncVar[:,:]


    lon2 = nc.variables[dims1[-1]][:]
    lat2 = nc.variables[dims1[-2]][:]

    m = Basemap(lon2[0], lat2[0], lon2[-1], lat2[-1], resolution='c', suppress_ticks=False)


    #m.pcolor(lon2, lat2, pattern1[i, ::-1, :], vmin=min2, vmax=max2, shading='flat')
    #data1 = data1[::-1, :]
    m.pcolor(lon2, lat2, data1)
    m.drawcoastlines(color=(.7,.7,.7))

    m.colorbar()

    #Mat.title('EOF %d'%(i+1))
    figFile0 = '%s/plot.png'%outDir
    Mat.savefig(figFile0, dpi=100)
    #figFile = 'http://localhost:5003/%s'%figFile0
    #figFile = 'http://ec2-13-56-67-192.us-west-1.compute.amazonaws.com:8080/%s'%figFile0
    # for ec20

  t1 = outDir.find('static')
  outDir1 = outDir[t1:]
  figFile1 = '%s/plot.png'%outDir1
  print(figFile1)

  figFile = 'http://ec2-13-56-153-11.us-west-1.compute.amazonaws.com:5003/%s'%figFile1
  return mes1, figFile, None



