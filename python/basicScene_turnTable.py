from __future__ import print_function
import sys,os.path,subprocess
import prman

import ProcessCommandLine as cl
import modeling_innerDetails as m_iD
import modeling_outDetails as m_oD

def main(filename,
        shadingrate=10,
        pixelvar=0.01,
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

  ri.DisplayChannel("color Ci", {"string source" : ["Ci"]})
  ri.DisplayChannel("float a", {"string source" : ["a"]})
  ri.DisplayChannel("color directDiffuse",{"string source" : ["color lpe:C<RD>[<L.>O]"]})
  ri.DisplayChannel("color directSpecular",{"string source" : ["color lpe:C<RS>[<L.>O]"]})
  ri.DisplayChannel("color __depth",{"string source" : ["__depth"]})
  ri.DisplayChannel("color indirectDiffuse",{"string source": ["color lpe:C<RD>[DS]+[<L.>O]"]})
  ri.DisplayChannel("color indirectSpecular", {"string source" :["color lpe:C<RS>[DS]+[<L.>O]"]})
  ri.DisplayChannel("color albedo", {"string source" : ["color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)"]})
  ri.DisplayChannel("color refraction", {"string source" : ["color lpe:(C<T[S]>[DS]+<L.>)|(C<T[S]>[DS]*O)"]})

  ri.Display('/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches.THETA.exr', 'openexr', 'Ci,a')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches_DirectDiffuse.THETA.exr', 'openexr', 'directDiffuse')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches_DirectSpecular.THETA.exr', 'openexr', 'directSpecular')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches___depth.THETA.exr', 'openexr', '__depth')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches_indirectDiffuse.THETA.exr', 'openexr', 'indirectDiffuse')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches_indirectSpecular.THETA.exr', 'openexr', 'indirectSpecular')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches_albedo.THETA.exr', 'openexr', 'albedo')
  ri.Display('+/home/s5101972/Desktop/RENDERING/Renderman/turntable/watches_refraction.THETA.exr', 'openexr', 'refraction')
  ri.Format(2048,872,1)

  ri.Hider('raytrace' ,{
    'int incremental' :[1], 
  })
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })

  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})
  
  ri.Translate(0,0.5,3.2)
  ri.Rotate(-50,1,0,0)

  if (THETA <= 360):
    ri.MotionBegin([ 0, 1 ])
    ri.Rotate(THETA, 0, 1, 0)
    ri.Rotate(NEXT, 0, 1, 0)
    ri.MotionEnd()

  #######################################################################
  #World Begin
  #######################################################################
  ri.WorldBegin()

  ###
  # Lighting Begin
  ###
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)

  if (THETA > 360):
    ri.MotionBegin([ 0, 1 ])
    ri.Rotate(THETA, 0, 1, 0)
    ri.Rotate(NEXT, 0, 1, 0)
    ri.MotionEnd()

  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'vatican_road_2k.tx'
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
  ri.AttributeBegin()
  ri.TransformBegin()
  ri.Translate(0,0,0.4)
  ri.Scale(4,4,4)
  ri.Attribute ('displacementbound', {'float sphere' : [0.2], 'string coordinatesystem' : ['shader']})
  ri.Pattern ("PxrTexture", "PxrTexture1", {
    "string filename" : ["woodTexture.tx"],
  })
  ri.Pattern ("PxrTexture", "PxrTexture2", {
    "string filename" : ["dirt.tx"],
  })
  ri.Pattern('PxrMix','mix_colour',
  {
    'color color1' : [0.6,0.6,0.6], 
    'color color2' : [0.45,0.45,0.45], 
    'reference float mix' : ['PxrTexture1:resultA'], 
  })
  ri.Pattern('PxrMix','mix_colour_dirt',
  {
    'color color2' : [0.425,0.415,0.415], 
    'reference color color1' : ['mix_colour:resultRGB'], 
    'reference float mix' : ['PxrTexture2:resultA'], 
  })
  ri.Pattern('PxrMix','mix_spec',
  {
    'color color1' : [0.3,0.0,0.0], 
    'color color2' : [0.35,0.0,0.0], 
    'reference float mix' : ['PxrTexture1:resultA'], 
  })
  ri.Pattern('PxrMix','mix_rough',
  {
    'color color1' : [0.3,0.0,0.0], 
    'color color2' : [0.6,0.0,0.0], 
    'reference float mix' : ['PxrTexture1:resultA'], 
  })
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [0.001],
    'reference float dispScalar' : ['PxrTexture1:resultA'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["wood_displace"]
  })
  ri.Bxdf("PxrDisney","PxrDisney1", {
    "reference color baseColor" : ["mix_colour_dirt:resultRGB"],
    'reference float specular' : ['mix_spec:resultR'],
    'reference float roughness' : ['mix_rough:resultR'], 
  })
  face=[1.5,-1.5,0,
            1.5,1.5,0,
            -1.5,-1.5,0,
            -1.5,1.5,0]
  ri.Patch("bilinear",{'P':face})
  ri.TransformEnd()
  ri.AttributeEnd()

  # ------------- Glass -------------
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['glass'] })
  ri.Attribute( 'visibility',{ 'int transmission' : [1]})
  ri.Attribute( 'trace',
  { 
    'int maxdiffusedepth' : [1], 
    'int maxspeculardepth' : [8]
  })
  ri.Pattern('dirt','dirt', 
  { 
      'float minus' : [0.3],
      'float freq' : [5],
  })
  ri.Pattern('PxrMix','mix_dirt_glass',
  {
    'color color1' : [0.25,0.25,0.25], 
    'color color2' : [0.175,0.15,0.15], 
    'reference float mix' : ['dirt:dirtDots'], 
  })
  ri.Bxdf('PxrSurface', 'glass',{ 
    'reference float diffuseGain' : ['dirt:dirtDots'],
    'color diffuseColor' : [0.15,0.15,0.15],
    'float refractionGain' : [1.0],
    'float reflectionGain' : [1.0],
    'float glassRoughness' : [0.01],
    'float glassIor' : [1.5],
  })
  ri.ReadArchive('cylinder.rib')
  ri.AttributeEnd()

  # ------------- Metal In -------------
  ri.AttributeBegin()

  ri.Attribute ('displacementbound', {'float sphere' : [0.2], 'string coordinatesystem' : ['shader']})

  ri.Pattern('clockface','clockface', 
  { 
    'float angle' : [16.0],
    'string textureName' : ['blue_numbers.tx'],
    'float scale1' : [0.48],
    'float scale2' : [0.48],
    'float translate1' : [0.53],
    'float translate2' : [0.51],
  })
  ri.Pattern('clockface','nine', 
  { 
    'float angle' : [16.0],
    'string textureName' : ['blue_numbers_nine.tx'],
    'float scale1' : [0.48],
    'float scale2' : [0.48],
    'float translate1' : [0.53],
    'float translate2' : [0.51],
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
  ri.Pattern('PxrMix','displace_numbers',
  {
    'color color1' : [0.01,0.0,0.0], 
    'color color2' : [0,0.0,0.0], 
    'reference float mix' : ['clockface:Calphainvert'], 
  })
  ri.Pattern('PxrMix','displace_numbers_nine',
  {
    'reference color color1' : ['displace_numbers:resultRGB'], 
    'color color2' : [0.05,0.0,0.0], 
    'reference float mix' : ['nine:Calpha'], 
  })
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'reference float dispAmount' : ['displace_numbers_nine:resultR'],
    'reference float dispScalar' : ['clockface:Calpha'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["blue_numbers_displace"]
  })
  ri.Pattern('radialMetalLines','radialMetalLines', 
  { 
  })
  ri.Pattern('PxrMix','radialMetalLines_mix_roughness',
  {
    'color color1' : [0.5,0.0,0.0], 
    'color color2' : [0.3,0.0,0.0], 
    'reference float mix' : ['radialMetalLines:resultStripes'], 
  })
  ri.Bxdf('PxrSurface', 'metal_in', {
          'reference color diffuseColor' : ['mix_blue_numbers:resultRGB'], 
          'reference float diffuseGain' : ['clockface:Calpha'],
          'int specularFresnelMode' : [1],
          'reference color specularEdgeColor' : ['mix_blue_numbers_EdgeColor:resultRGB'],
          'reference color specularIor' : ['mix_blue_numbers_ior:resultRGB'],
          'color specularExtinctionCoeff' : [3.9996, 3.9996, 3.9996],
          'reference float specularRoughness' : ['radialMetalLines_mix_roughness:resultR'], 
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
  ri.Attribute ('displacementbound', {'float sphere' : [0.2], 'string coordinatesystem' : ['shader']})
  ri.Pattern('rectangle','rectangle', 
  { 
      'color blue' : [0.000147,0.05711,0.216743],
  })
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [-0.01],
    'reference float dispScalar' : ['rectangle:alpha'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["hands_minute_displace"]
  })
  ri.Bxdf('PxrDisney', 'smooth', { 
          'reference color baseColor' : ['rectangle:Cout'],
          'float metallic' :  [0.2] 
  })
  m_iD.handsBlue_minute(ri)
  ri.AttributeEnd()
  ri.AttributeBegin()
  ri.Attribute ('displacementbound', {'float sphere' : [0.2], 'string coordinatesystem' : ['shader']})
  ri.Pattern('rectangle','rectangle', 
  { 
        'color blue' : [0.000147,0.05711,0.216743],
        'float mindistance' : [0.45],
        'float maxdistance' : [0.64],
  })
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [-0.01],
    'reference float dispScalar' : ['rectangle:alpha'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["hands_hours_displace"]
  })
  ri.Bxdf('PxrDisney', 'smooth', { 
          'reference color baseColor' : ['rectangle:Cout'],
          'float metallic' :  [0.2] 
  })
  m_iD.handsBlue_hour(ri)
  ri.AttributeEnd()
  ri.TransformEnd()

  # ------------- White Metal In -------------
  ri.AttributeBegin()

  ri.Pattern('clockface','clockface', 
  { 
    'float angle' : [16.0],
    'string textureName' : ['black_numbers.tx'],
    'float scale1' : [0.8],
    'float scale2' : [0.8],
    'float translate1' : [0.49],
  })
  ri.Pattern('PxrMix','mix_black_numbers',
  {
    'color color1' : [0.05,0.05,0.05], 
    'color color2' : [0.8,0.8,0.8], 
    'reference float mix' : ['clockface:Calphainvert'], 
  })
  ri.Pattern('metalLines','metalLines', 
  { 
  })
  ri.Pattern('PxrMix','mix_stripes_roughness',
  {
    'color color1' : [0.1, 0.0,0.0], 
    'color color2' : [0.311376,0.0,0.0], 
    'reference float mix' : ['metalLines:resultStripes'], 
  })
  ri.Pattern('PxrMix','mix_stripes_spec',
  {
    'color color1' : [0.7,0.0,0.0], 
    'color color2' : [0.5,0.0,0.0], 
    'reference float mix' : ['metalLines:resultStripes'], 
  })
  ri.Pattern('PxrMix','mix_stripes_metalness',
  {
    'color color1' : [0.1,0.0,0.0], 
    'color color2' : [0.3,0.0,0.0], 
    'reference float mix' : ['metalLines:resultStripes'], 
  })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDisney', 'white_metal_in',{ 
    'reference color baseColor' : ['mix_black_numbers:resultRGB'],
    'reference float specular' : ['mix_stripes_spec:resultR'],
    'reference float metallic' : ['mix_stripes_metalness:resultR'],
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
    'float angle' : [-75.0],
    'string textureName' : ['plastic_circle.tx'],
    'float scale1' : [0.475],
    'float scale2' : [0.475],
    'float translate1' : [0.49],
  })
  ri.Pattern('PxrMix','mix_circle',
  {
    'color color1' : [0.8,0.8,0.8], 
    'color color2' : [0.2,0.2,0.2], 
    'reference float mix' : ['circle:Calpha'], 
  })
  ri.Pattern('PxrMix','mix_circle_roughness',
  {
    'color color1' : [0.3,0.0,0.0], 
    'color color2' : [0.9,0.0,0.0], 
    'reference float mix' : ['circle:Calpha'], 
  })
  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDisney', 'plastic', { 
      'reference color baseColor' : ['mix_circle:resultRGB'], 
      'reference float roughness' : ['mix_circle_roughness:resultR'], 
  })
  m_iD.plasticIn(ri, widthSmall, diskPosition)
  ri.TransformEnd()
  ri.AttributeEnd()

  # ------------- Metal Out -------------

  ## -------------- Blue Metal Out ------------
  ri.AttributeBegin()
  ri.Bxdf('PxrDisney', 'smooth', { 
          'color baseColor' : [0.000147,0.05711,0.216743]
  })  
  m_oD.outBlueMetalDetails(ri)
  ri.AttributeEnd()

  ## -------------- Ordinary Metal Out ------------
  ri.AttributeBegin()
  ri.Attribute ('displacementbound', {'float sphere' : [0.2], 'string coordinatesystem' : ['shader']})
  ri.Attribute( 'user' , {'string __materialid' : ['metal'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Pattern('scratches','scratches', 
  { 
  })
  ri.Pattern('PxrMix','mix_scratches_roughness',
  {
    'color color1' : [0.01,0.0,0.0], 
    'color color2' : [0.2,0.0,0.0], 
    'reference float mix' : ['scratches:resultStripes'], 
  })
  ri.Pattern('PxrMix','mix_scratches_anisotropic',
  {
    'color color1' : [0.0,0.0,0.0], 
    'color color2' : [0.6,0.0,0.0], 
    'reference float mix' : ['scratches:resultStripes'], 
  })
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [-0.00025],
    'reference float dispScalar' : ['scratches:resultStripes'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["netal_out_displace"]
  })
  ri.Pattern('dirt','dirt', 
  { 
  })
  ri.Pattern('PxrMix','mix_dirt',
  {
    'color color1' : [0.25,0.25,0.25], 
    'color color2' : [0.175,0.15,0.15], 
    'reference float mix' : ['dirt:dirtDots'], 
  })
  ri.Bxdf('PxrDisney','metal',
  {
    'reference color baseColor' : ['mix_dirt:resultRGB'], 
    'float metallic' : [0.9], 
    'float specular' : [0.9], 
    'reference float roughness' : ['mix_scratches_roughness:resultR'], 
    'reference float anisotropic' : ['mix_scratches_anisotropic:resultR'], 
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
  shaderName='radialMetalLines'
  checkAndCompileShader(shaderName)
  shaderName='rectangle'
  checkAndCompileShader(shaderName)
  shaderName='scratches'
  checkAndCompileShader(shaderName)
  shaderName='dirt'
  checkAndCompileShader(shaderName)
  cl.ProcessCommandLine('testScenes.rib')
  main(cl.filename,
    cl.args.shadingrate,
    cl.args.pixelvar,
    cl.args.fov,cl.args.width,
    cl.args.height,
    cl.integrator,
    cl.integratorParams)
