# import__
#== providers_models
# def_checkNc_w(nc, fn, dict1):
# def_checkNc(fn, dict1):
  # loop_vars
    # find_units
    # find_longname
    # collect_dims
  # loop_dim_vars
    # if_hasUnits
      # replace_ref_time_of 0000
    # dim_range
  # collect_vars
  # construct_dim2

# import__
from netCDF4 import Dataset
from netCDF4 import MFDataset
import netCDF4 
import os
import cfunits as cf1
import copy
import glob
import traceback

vb = 0

#== providers_models
sources = {
'staged',
'online',
'uploaded',
}

providers = {
'tkubar': 'T. Kubar',
'fli': 'F. Li',
'noaa': 'NOAA',
'inm': 'INM',
'wcrp': 'WCRP',
'wrf': 'WRF',
'ecmwf': 'ECMWF',
'fub-dwd': 'FUB-DWD',
'bcc': 'BCC',
'nasa': 'NASA',
'uoe': 'UOE',
'ukmo': 'UKMO',
'iap': 'IAP',
'giss': 'GISS',
'mpi': 'MPI',
'argo': 'ARGO',
'ncc': 'NCC',
'cnrm': 'CNRM',
'ipsl': 'IPSL',
'cccma': 'CCCMA',
'miroc': 'MIROC',
'mri': 'MRI',
'ncar': 'NCAR',
'csiro': 'CSIRO',
'cmcc': 'CMCC',
'gfdl': 'GFDL',
}

models = [
'TRMM-L3',
'IPSL-CM5A-LR',
'ECMWF_interim',
'ERA_interim',
'GFDL-ESM2G',
'SSMI-MERIS',
'GFDL-CM3',
'GISS-E2-H',
'GISS-E2-R',
'FGOALS-s2',
'PSL-CM5A-LR',
'MIROC5',
'MIROC4h',
'MPI-ESM-LR',
'MRI-CGCM3',
'MODIS',
'TRMM',
'CESM1-CAM5',
'NorESM1-ME',
'NorESM1-M',
'NOAA',
'HadGEM2-A',
'HadGEM2-ES',
'ATSR',
'ISCCP',
'ARGO',
'CanESM2',
'CanAM4',
'CNRM-CM5',
'CSIRO-MK3-6-0',
'CMCC-CM',
'NCC-NORESM',
'bbc-csm1-1',
'inmcm4',
'CM3',
'CM5A-LR',
'MIROC5',
'HadGEM2-A',
'CM5',
'SSMI-MERIS',
'ESM-LR',
'CGCM3',
'GRACE',
'AMSRE',
'MLS',
'AIRS',
'GPCP-SG',
'CERES-SG',
'CERES-EBAF',
'QuikSCAT',
'AVISO',
'cloudSat-CALIPSO',
'MISR',
'2C-ICE',
'TES',
'CALIOP',
'CALIOP-GOCCP-v2.1',
'CESM1-CAM5',
'ARGO',
#
'wrf_st',
'wrf_ra-cam',
'wrf_pbl-ysu',
'wrf_pbl-nn2',
'wrf_mp-wdm',
'wrf_mp-mor',
'wrf_co-kf',
'wrf_co-tie',
'wrf_st',
#
'bcc-csm1-1',
'inmcm4',
]

models2 = {}
for mod1 in models:
  #models2[mod1] =  ['-' + mod1.lower() + '_', '_' + mod1.lower() + '_']
  models2[mod1] =  '_' + mod1.lower() + '_'

experiments = [
'historical',
'esmHistorical',
'historicalExt',
'amip',
'amip4XCO2',
'obs4MIPs',
]

experiments2 = {}
for exp1 in experiments:
  experiments2[exp1] =  '_' + exp1.lower() + '_' 

runs = [
'r1i1p1',
]

runs2 = {}
for rr in runs:
  runs2[rr] =  '_' + rr.lower() + '_' 


# def_checkNc_w(nc, fn, dict1):
def checkNc_w(nc, fn, dict1):
  print 'in checkNc_w'
  nc.close()
  # call checkNc(overwrite=1)
  ok1 = checkNc(fn, dict1, overwrite=1)
  return ok1

# def_checkNc(fn, dict1):
def checkNc(fn, dict1, overwrite=0, allowOverwrite=1):
  '''
return:
0 -- good
2 -- dimension has no units
3 -- dimension units not recognized
4 -- ref time is 0000
5 -- cannot open file
'''
  ok1 = 0
  dict9 = copy.deepcopy(dict1)

  varDict = {}
  varList = []
  dimList = []
  varListLong = []
  dim2 = []

  dict1['varDict'] = varDict
  dict1['varList'] = varList
  dict1['varListLong'] = varListLong
  dict1['dimList'] = dimList
  dict1['dim2'] = dim2 

  dict1['check'] = ''
  dict1['warning'] = ''

  pp = '_'
  dict1['source'] = pp
  dict1['provider'] = pp
  dict1['model'] = pp
  dict1['experiment'] = pp
  dict1['run'] = pp

  dict1['message'] = ''
  dict1['success'] = True
  dict1['ok'] = 0

  if fn.find('*')>-1:
    fn2 = glob.glob(fn)
  else:
    fn2 = [fn,]

  if 0:
    temp2 = os.path.split(fn2[0])
    dict1['filename'] = temp2[1]
    dict1['filepath'] = fn2[0]

  dict1['nFile'] = len(fn2)

  # used as a fn facet 
  #fn3 = fn2[0]
  fn3a = fn.lower()

  #zzzz 
  if 1:
    pp = '_'
    if fn3a.find('/mnt/')>-1:
      pp = 'staged'

    if fn3a.find('/home/svc/upload')>-1:
      pp = 'uploaded'

    if fn3a.find('http')>-1:
      pp = 'online'
    dict1['source'] = pp

  pp = '_'
  for prov in providers:
    if fn3a.find('cmip5/%s'%prov)>-1:
      pp = providers[prov]

  dict1['provider'] = pp
  
  pp = '_'
  for mod1 in models2:
    if fn3a.find(models2[mod1])>-1:
      pp = mod1
  dict1['model'] = pp

  pp = '_'
  for exp1 in experiments2:
    if fn3a.find(experiments2[exp1])>-1:
      pp = exp1
  dict1['experiment'] = pp

  pp = '_'
  for rr in runs2:
    if fn3a.find(runs2[rr])>-1:
      pp = rr
  dict1['run'] = pp

  if vb>=2: print "in checkNc: ", fn

  try:
    if len(fn2)>1:
      nc = MFDataset(fn2)
      nc1 = Dataset(fn2[0])
      nc2 = Dataset(fn2[-1])

    else:
      if overwrite:
        nc = Dataset(fn2[0], 'r+')
      else:
        nc = Dataset(fn2[0])

  except Exception as e :
    dict1['message'] += "File on server is not found: %s \n\n%s"%(fn, repr(e))
    dict1['success'] = False
    ok1 = 5
    dict1['ok'] = ok1
    return ok1

  # loop_vars
  varListAll = nc.variables.keys()
  
  str1 = ''
  dimList0 = []
  for var in varListAll:

    # find_units
    units1 = ''
    d1 = nc.variables[var]
    try:
      units1 = d1.units 
    except:
      temp1 = var.find('_bnds')
      if temp1==-1:
        dict1['check'] += var + ': need the units attribute.\n'

    # find_longname
    if vb==1: print 'here 1'
    longName = '_'

    try:
      longName = d1.long_name 
    except: pass

    try:
      longName = d1.longname 
    except: pass
      
    # collect_dims
    if vb==1: print 'here 2'
    # to remove u' (unicode thing)
    dim1 = list(d1.dimensions)
    for i in range(len(dim1)):
      dim1[i] = str(dim1[i])
    dim1 = tuple(dim1)
 
    if var.find('_bnds')==-1:
      str1 += '%s: %s\n'%(var, str(dim1))
      dimList0 += list(dim1)

    varDict[var] = {'dim':  dim1, 
                    'units': units1,
                    'longName': longName,
                   }

  # loop_dim_vars
  if vb==1: print 'here 3'
  str1 += '\nDimension Variables\n'
  dimList0 = list(set(dimList0))

  dimList2 = []
  for d in dimList0:
    if d in varListAll:
      dimList2.append(d)
  if vb==1: print 'dimList2: ', dimList2
  dimList0 = dimList2

  for dimVar in dimList0:
    if vb==1: print 'here 4a'
    dimWhat = ''
    d2 = nc.variables[dimVar]
    if len(fn2)>1:
      d2a1 = nc1.variables[dimVar]
      d2a2 = nc2.variables[dimVar]
      units1a1 = d2a1.units
      units1a2 = d2a2.units
    try:
      units1 = d2.units
      hasUnits = 1
      print 'units1: ', units1
    except Exception as e :
      traceback.print_exc()
      hasUnits = 0
      if overwrite==0 and allowOverwrite==1:
        return checkNc_w(nc, fn, dict9)
      else:
        dict1['message'] += "this dim has no unit: %s \n\n%s"%(dimVar, repr(e))
        print 'ok1=2'
        ok1 = 2
        dict1['ok'] = ok1
        return ok1
      
    # if_hasUnits
    if hasUnits:
      try:
        cfUnits = cf1.Units(units1)
        #cfUnits = units1
      except Exception as e :
        traceback.print_exc()
        dict1['message'] += "this dim's unit does not conform: %s(%s) \n\n%s"%(dimVar, units1, repr(e))
        print 'ok1=3'
        ok1 = 3
        dict1['ok'] = ok1
        return ok1

      if cfUnits.islongitude:
        dimWhat = 'lon'
      elif cfUnits.islatitude:
        dimWhat = 'lat'
      elif cfUnits.isreftime:
        dimWhat = 'time'
      elif cfUnits.ispressure:
        dimWhat = 'z'
      else:
        dimWhat = 'i'

      # replace_ref_time_of 0000
      if 0:
        if vb==1: print 'here 4b'
        if dimWhat=='time':
          if vb==1: print 'here 4ba'
          if str(cfUnits.reftime)[:4]=='0000':
            if overwrite==0 and allowOverwrite==1:
              return checkNc_w(nc, fn, dict9)
            else:
              #dict1['message'] += "this dim's unit does not conform: %s(%s) \n\n%s"%(dimVar, units1, repr(e))
              ok1 = 4
              print 'ok1=4'
              dict1['ok'] = ok1
              return ok1
            
            if 1:
              units2 = units1.replace( '0000', '1800' ) 
              cfUnits1 = cf1.Units( units1 )
              cfUnits2 = cf1.Units( units2 )
              d2[:] = cf1.conform( d2[:], cfUnits1, cfUnits2 )
              d2.units = units2

    else:  # no units
      if vb==1: print 'here 4c'
      if dimVar.lower().find('lon')>-1: 
        dimWhat = 'lon'
        units1 = 'degrees_east'

      elif dimVar.lower().find('lat')>-1: 
        dimWhat = 'lat'
        units1 = 'degrees_north'

      elif dimVar.lower().find('time')>-1: 
        dimWhat = 'time'
        units1 = 'days since 1800-01-01'
        dict1['warning'] += '!!! made up time units: %s !!! \n'%(units1)
        dict1['check'] += '!!! made up time units: %s !!! \n'%(units1)

      elif (dimVar.lower().find('z')>-1) \
         or (dimVar.lower().find('plev')>-1)  \
         or (dimVar.lower().find('depth')>-1)  \
         or (dimVar.lower().find('height')>-1)  \
         or (dimVar.lower().find('vert')>-1) :
        if vb==1: print 'here 4d'
        dimWhat = 'z'
        units1 = 'm'
        dict1['warning'] += '!!! made up vertical units: %s !!! \n'%(units1)
        dict1['check'] += '!!! made up vertical units: %s !!! \n'%(units1)

      else:
        if vb==1: print 'here 4e'
        dimWhat = 'i'
        units1 = 'count'
        dict1['warning'] += '!!! made up i units: %s !!! \n'%(units1)
        dict1['check'] += '!!! made up i units: %s !!! \n'%(units1)

      d2.units = units1

    # dim_range
    if vb==1: print 'd2: ', d2
    if vb==1: print 'here 5'
    #   a1 = '00000101'
    #   a2 = '29991231'

    
    if dimWhat=='time':
      if vb==1: print 'here 3aa'
      if len(fn2)>1:
        time1 = netCDF4.num2date(d2[0], units1a1).timetuple()
      else:
        time1 = netCDF4.num2date(d2[0], d2.units).timetuple()

      if vb==1: print 'time1: ', time1
      a1 = '%04d%02d%02d %02d:%02d:%02d'%(time1[0], time1[1], time1[2], time1[3], time1[4], time1[5])

      if len(fn2)>1:
        time2 = netCDF4.num2date(d2[-1], units1a2).timetuple()
      else:
        time2 = netCDF4.num2date(d2[-1], d2.units).timetuple()
      a2 = '%04d%02d%02d %02d:%02d:%02d'%(time2[0], time2[1], time2[2], time2[3], time2[4], time2[5])

      a1 = a1[:8]
      a2 = a2[:8]

    else:  # not time
      try:
        d2a = d2[:]
        a1 = str(d2a.min())
        a2 = str(d2a.max())      
        if vb==1: print 'here 3ab'
      except:
        a1 = '0'
        a2 = '0'
        if vb==1: print 'here 3ac'
    if vb==1: print 'here 3ad'
    str1 += '%s: %s to %s (%s)\n'%(dimVar, a1, a2, units1)
    varDict[dimVar]['min'] = a1
    varDict[dimVar]['max'] = a2
    varDict[dimVar]['units'] = units1
    varDict[dimVar]['what'] = dimWhat
    if vb==1: print varDict[dimVar]
    if vb==1: print 'here 3b'

  # collect_vars
  if vb==1: print 'here 4'
  varList = []
  for k in varListAll:
    if k not in dimList0 and k.find('_bnds')==-1 \
       and k not in (
        'month', 
        'year',
        'height',
        'model_lat',
        'model_lon'): 
      varList.append(k)
      varListLong.append(varDict[k]['longName'])

  # construct_dim2
  if 1:
    if vb==1: print 'calc dim2'
    if vb==1: print ' varDict.keys(): ',
    if vb==1: print varDict.keys()
    for var1 in varList:
    #for var1 in varDict.keys():
      if k.find('_bnds')>-1: continue

      if vb==1: print 'var1: ', var1
      dim2a = []
      if vb==1: print "varDict[var1]['dim']: ",
      if vb==1: print varDict[var1]['dim']
      for i in varDict[var1]['dim']:
        try:
          dim2a.append( varDict[i]['what'] )
        except:
          dim2a.append( 'unknown' )
      if vb==1: print 'dim2a: ', dim2a
      varDict[var1]['dim2a'] = dim2a

  # construct_global_dim2
  for d in dimList0:
    try:
      dim2.append( varDict[d]['what'] ) 
    except:
      dim2.append( 'unknown' )
  

  if vb==1: print 'here 7'
  nc.close()
  if vb==1: print 'here 7a'
  dict1['check'] += '\nThe netCDF file has %d variables:\n%s'%(len(varList), str1) 

  dimList[:] = dimList0

  #dict1['varDict'] = varDict 
  #dict1['varList'] = varList
  #dict1['varListLong'] = varListLong
  #dict1['dimList'] = dimList 
  #dict1['dim2'] = dim2 
  #dict1['check'] = check1
  #dict1['warning'] = warning
  #dict1['ok'] = 0

  return 0


