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

  ri.Translate(0,0.5,3.2)
  ri.Rotate(-50,1,0,0)
  ri.Rotate(40,0,1,0)

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

  # ------------- Plane -------------
  ri.TransformBegin()
  ri.Translate(0,0,0.4)
  ri.Scale(3,3,3)
  face=[1.5,-1.5,0,
            1.5,1.5,0,
            -1.5,-1.5,0,
            -1.5,1.5,0]
  ri.Patch("bilinear",{'P':face})
  ri.TransformEnd()

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

  ri.Attribute ('displacementbound', {'float sphere' : [0.2], 'string coordinatesystem' : ['shader']})

  ri.Pattern('clockface','clockface', 
  { 
    'float angle' : [75.0],
    'string textureName' : ['blue_numbers.tx'],
    'float scale1' : [0.5],
    'float scale2' : [1.35],
    'float translate1' : [1.075],
    'float translate2' : [-0.12],
  })
  ri.Pattern('clockface','nine', 
  { 
    'float angle' : [75.0],
    'string textureName' : ['blue_numbers_nine.tx'],
    'float scale1' : [0.5],
    'float scale2' : [1.35],
    'float translate1' : [1.075],
    'float translate2' : [-0.12],
  })
  ri.Pattern('PxrMix','mix_blue_numbers',
  {
    'color color1' : [0.000147,0.05711,0.216743], 
    'color color2' : [0.0,0.0,0.0], 
    'reference float mix' : ['clockface:Calphainvert'], 
  })
  ri.Pattern('PxrMix','mix_blue_numbers_EdgeColor',
  {
    'color color1' : [0.025,0.025,0.025], 
    'color color2' : [0.64,0.64,0.64], 
    'reference float mix' : ['clockface:Calphainvert'], 
  })
  ri.Pattern('PxrMix','mix_blue_numbers_ior',
  {
    'color color1' : [1.45,1.45,1.45], 
    'color color2' : [2.5,2.5,2.5], 
    'reference float mix' : ['clockface:Calphainvert'], 
  })
  # Does not work Begin
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [1.0],
    'reference float dispScalar' : ['nine:Calpha'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["mainplate"]
  })
  # Does not work End
  ri.Bxdf('PxrSurface', 'metal_in', {
          'reference color diffuseColor' : ['mix_blue_numbers:resultRGB'], 
          'reference float diffuseGain' : ['clockface:Calpha'],
          'int specularFresnelMode' : [1],
          'reference color specularEdgeColor' : ['mix_blue_numbers_EdgeColor:resultRGB'],
          'reference color specularIor' : ['mix_blue_numbers_ior:resultRGB'],
          'color specularExtinctionCoeff' : [3.9996, 3.9996, 3.9996],
          'float specularRoughness' : [0.4], 
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
  ri.Bxdf('PxrDisney', 'smooth', { 
          'color baseColor' : [0.000147,0.05711,0.216743],
          'float metallic' :  [0.2] 
  })
  m_iD.handsBlue(ri)
  ri.AttributeEnd()
  ri.TransformEnd()

  # ------------- White Metal In -------------
  ri.AttributeBegin()

  ri.Pattern('clockface','clockface', 
  { 
    'float angle' : [75.0],
    'string textureName' : ['black_numbers.tx'],
    'float scale1' : [0.825],
    'float scale2' : [2.35],
    'float translate1' : [0.6],
    'float translate2' : [-0.288],
  })
  ri.Pattern('metalLines','metalLines', 
  { 
    'float angle' : [75.0],
    'float scale' : [20.0],
  })
  ri.Pattern('PxrVoronoise','voronoi_noise',
  {
    'float frequency' : [20.0],  
  })
  ri.Pattern('PxrMix','mix_stripes_roughness',
  {
    'reference color color1' : ['voronoi_noise:resultRGB'], 
    'color color2' : [0.311376,0.0,0.0], 
    'reference float mix' : ['metalLines:resultStripes'], 
  })
  ri.Pattern('PxrMix','mix_stripes_spec',
  {
    'reference color color1' : ['voronoi_noise:resultRGB'], 
    'color color2' : [0.5,0.0,0.0], 
    'reference float mix' : ['metalLines:resultStripes'], 
  })
  ri.Pattern('PxrMix','mix_black_numbers',
  {
    'color color1' : [0.05,0.05,0.05], 
    'color color2' : [0.8,0.8,0.8], 
    'reference float mix' : ['clockface:Calphainvert'], 
  })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDisney', 'white_metal_in',{ 
    'reference color baseColor' : ['mix_black_numbers:resultRGB'],
    'reference float specular' : ['mix_stripes_spec:resultR'],
    'reference float metallic' : ['metalLines:resultStripes'],
    'reference float roughness' : ['mix_stripes_roughness:resultR'],
    'float anisotropic' : [0.6] 
  })
  ri.Disk(diskPosition-0.005,widthSmall-0.5,-360)
  ri.AttributeEnd()

  # ------------- Plastic In -------------
  ri.AttributeBegin()
  ri.TransformBegin()
  ri.Rotate(-18, 0,0,1)
  ri.Pattern('clockface','circle', 
  { 
    'float angle' : [75.0],
    'string textureName' : ['plastic_circle.tx'],
    'float scale1' : [0.48],
    'float scale2' : [1.15],
    'float translate1' : [1.025],
    'float translate2' : [-0.055],
  })
  ri.Pattern('PxrMix','mix_circle',
  {
    'color color1' : [0.8,0.8,0.8], 
    'color color2' : [0.4,0.4,0.4], 
    'reference float mix' : ['circle:Calpha'], 
  })
  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDisney', 'plastic', { 
      'color baseColor' : [0.8,0.8,0.8], 
      'float roughness' : [.5], 
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
  ri.Pattern('metalLines','metalLines', 
  { 
    'float scale' : [20.0],
  })
  ri.Bxdf('PxrDisney','metal',
  {
    'color baseColor' : [.25,.25,.25], 
    'reference float metallic' : ['metalLines:resultRound'], 
    'reference float specular' : ['metalLines:resultRound'], 
    'float roughness' : [0.2], 
    'float anisotropic' : [0.6], 
    'string __materialid' : ['metal']
  })
  m_oD.outOrdinaryMetalDetails(ri, widthSmall, widthBig, hight)
  ri.AttributeEnd()
  ri.TransformEnd()

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
  shaderName='clockface'
  checkAndCompileShader(shaderName)
  shaderName='metalLines'
  checkAndCompileShader(shaderName)
  cl.ProcessCommandLine('testScenes.rib')
  main(cl.filename,
    cl.args.shadingrate,
    cl.args.pixelvar,
    cl.args.fov,cl.args.width,
    cl.args.height,
    cl.integrator,
    cl.integratorParams)
