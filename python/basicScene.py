from __future__ import print_function
import sys,os.path,subprocess
import prman

import ProcessCommandLine as cl
import modeling_innerDetails as m_iD
import modeling_outDetails as m_oD

def main(filename,
        shadingrate=10,
        pixelvar=0.1,
        fov=45.0,
        width=1024,
        height=720,
        integrator='PxrPathTracer',
        integratorParams={}
        ) :
  print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
    
  ri = prman.Ri() # create an instance of the RenderMan interface

  ri.Begin(filename)

  ri.Option('searchpath', {'string archive':'../assets/:@'})
  ri.Option('searchpath', {'string texture':'../textures/:@'})

  ri.Display('watches.exr', 'it', 'rgba')
  ri.Format(width,height,1)

  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })

  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})

  ri.Translate(0,0.25,3.2)
  ri.Rotate(-30,1,0,0)
  ri.Rotate(-130,0,1,0)

  #######################################################################
  #World Begin
  #######################################################################
  ri.WorldBegin()

  ###
  # Lighting Begin
  ###
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)
  ri.Rotate(0,0,0,1)
  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'vatican_road_2k.tex'
   })
  ri.TransformEnd()
  ###
  # Lighting End
  ###


  ri.TransformBegin()

  widthBig = 1.2
  widthSmall = 1.1
  hight = 0.5
  diskPosition = 0.15

  ri.Rotate(90,1,0,0)

  # ------------- Glass -------------
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['glass'] })
  ri.Attribute( 'visibility',{ 'int transmission' : [1]})
  ri.Attribute( 'trace',
  { 
    'int maxdiffusedepth' : [1], 
    'int maxspeculardepth' : [8]
  })
  ri.Bxdf('PxrSurface', 'glass',{ 
    'float diffuseGain' : [0],
    'float refractionGain' : [1.0],
    'float reflectionGain' : [1.0],
    'float glassRoughness' : [0.01],
    'float glassIor' : [1.5],
  })
  #ri.ReadArchive('cylinder.rib')
  ri.AttributeEnd()

  # ------------- Metal In -------------
  ri.AttributeBegin()
  ri.Bxdf('PxrSurface', 'metal_in', {
          'int specularFresnelMode' : [1],
          'color specularEdgeColor' : [0.54 ,0.54 ,0.54],
          'color specularIor' : [2.5, 2.5, 2.5],
          'color specularExtinctionCoeff' : [2.9996, 2.9996, 2.9996],
          'float specularRoughness' : [0.3], 
          'integer specularModelType' : [1] ,
          'string __materialid' : ['metal_in']
  })
  m_iD.metalIn(ri, diskPosition, widthSmall)
  ri.AttributeEnd()

  # ------------- Hands In ------------
  ri.TransformBegin()
  ri.Translate(0,0,0.225)
  m_iD.handsWhite(ri)
  ri.AttributeBegin()
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.001147,0.06711,0.516743]
  })
  m_iD.handsBlue(ri)
  ri.AttributeEnd()
  ri.TransformEnd()

  # ------------- Paper In -------------
  ri.AttributeBegin()

  ri.Pattern('clockface_paper','clockface_paper', 
  { 
  })

  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'reference color diffuseColor' : ['clockface_paper:Cout']
  })
  ri.TransformBegin()
  #ri.Rotate(15, 0, 0, 1)
  ri.Disk(diskPosition-0.005,widthSmall-0.5,360)
  ri.TransformEnd()
  ri.AttributeEnd()

  # ------------- Plastic In -------------
  ri.AttributeBegin()
  ri.TransformBegin()
  ri.Rotate(-18, 0,0,1)
  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.8,0.8,0.8]
  })
  m_iD.plasticIn(ri, widthSmall, diskPosition)
  ri.TransformEnd()
  ri.AttributeEnd()

  # ------------- Metal Out -------------

  ## -------------- Blue Metal Out ------------
  ri.AttributeBegin()
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.001147,0.06711,0.516743]
  }) 
  m_oD.outBlueMetalDetails(ri)
  ri.AttributeEnd()

  ## -------------- Ordinary Metal Out ------------
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['metal'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDisney','metal',
  {
    'color baseColor' : [.25,.25,.25], 
    'float metallic' : [1], 
    'float specular' : [1], 
    'float roughness' : [0.2], 
    'string __materialid' : ['metal']
  })
  m_oD.outOrdinaryMetalDetails(ri, widthSmall, widthBig, hight)
  ri.AttributeEnd()
  ri.TransformEnd()

  ## -------------- Cylinders Metal Out ------------
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['metal'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDisney','metal',
  {
    'color baseColor' : [.25,.25,.25], 
    'float metallic' : [1], 
    'float specular' : [1], 
    'float roughness' : [0.2], 
    'string __materialid' : ['metal']
  })
  m_oD.outCylindersMetalDetails(ri)
  ri.AttributeEnd()

  ri.WorldEnd()
  #######################################################################
  #World End
  #######################################################################

  ri.End()

def checkAndCompileShader(shader) :
  if os.path.isfile(shader+'.oso') != True  or os.stat(shader+'.osl').st_mtime - os.stat(shader+'.oso').st_mtime > 0 :
    print( 'compiling shader {0}'.format(shader))
    try:
      subprocess.check_call(['oslc', shader+'.osl'])
    except subprocess.CalledProcessError :
      sys.exit('shader compilation failed')

if __name__ == '__main__':  
  shaderName='clockface_paper'
  checkAndCompileShader(shaderName)
  cl.ProcessCommandLine('testScenes.rib')
  main(cl.filename,
    cl.args.shadingrate,
    cl.args.pixelvar,
    cl.args.fov,cl.args.width,
    cl.args.height,
    cl.integrator,
    cl.integratorParams)
