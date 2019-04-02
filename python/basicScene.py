from __future__ import print_function
import sys,os.path,subprocess
import prman

sys.path.insert(0, '../modeling')

import ProcessCommandLine as cl
import modeling_innerDetails as m_iD
import modeling_outDetails as m_oD

def main(filename,
        shadingrate=10,
        pixelvar=0.001,
        fov=45.0,
        width=2048,
        height=1548,
        integrator='PxrPathTracer',
        integratorParams={}
        ) :
  print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,0.01,integrator,integratorParams))
    
  ri = prman.Ri() # create an instance of the RenderMan interface

  ri.Begin(filename)

  ri.Option('searchpath', {'string archive':'../assets/:@'})
  ri.Option('searchpath', {'string texture':'../textures/:@'})
  ri.Option('searchpath', {'string shader':'../shaders/:@'})

  ri.DisplayChannel("color Ci", {"string source" : ["Ci"]})
  ri.DisplayChannel("float a", {"string source" : ["a"]})
  ri.DisplayChannel("color directDiffuse",{"string source" : ["color lpe:C<RD>[<L.>O]"]})
  ri.DisplayChannel("color directSpecular",{"string source" : ["color lpe:C<RS>[<L.>O]"]})
  ri.DisplayChannel("color __depth",{"string source" : ["__depth"]})
  ri.DisplayChannel("color indirectDiffuse",{"string source": ["color lpe:C<RD>[DS]+[<L.>O]"]})
  ri.DisplayChannel("color indirectSpecular", {"string source" :["color lpe:C<RS>[DS]+[<L.>O]"]})
  ri.DisplayChannel("color albedo", {"string source" : ["color lpe:nothruput;noinfinitecheck;noclamp;unoccluded;overwrite;C<.S'passthru'>*((U2L)|O)"]})
  ri.DisplayChannel("color refraction", {"string source" : ["color lpe:(C<T[S]>[DS]+<L.>)|(C<T[S]>[DS]*O)"]})

  ri.Display('../rendering/oneframe/watches.exr', 'openexr', 'Ci,a,directDiffuse,directSpecular,__depth,indirectDiffuse,indirectSpecular,albedo,refraction')
  
  ri.Format(2048,1548,1)

  ri.Hider('raytrace' ,{
    'int incremental' :[1], 
    'int maxsamples' : [1024],
  })
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (0.001)
  ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })

  #ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})

  ri.Projection('PxrCamera',{
                ri.FOV:fov,
                'float fStop' : [1.0],
                'float focalLength' : [0.12],
                'float focalDistance' : [3.25],
                'color transverse' : [1,1.0005, 1.001], 
                'float natural' : [0.25],
  })
  
  ri.Translate(0,0.5,3.2)
  ri.Rotate(-50,1,0,0)
  ri.Rotate(30,0,1,0)

  #######################################################################
  #World Begin
  #######################################################################
  ri.WorldBegin()

  ###
  # Lighting Begin
  ###
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)
  ri.Rotate(290,0,0,1)
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
  ri.Translate(-0.75,0.5,0.4)
  ri.Scale(2.2,2.2,2.2)
  ri.Attribute ('displacementbound', 
  {
    'float sphere' : [0.2], 
    'string coordinatesystem' : ['shader']
  })
  ri.Pattern ("PxrTexture", "PxrTexture_wood_plane", 
  {
    "string filename" : ["woodTexture.tx"],
  })
  ri.Pattern ("PxrTexture", "PxrTexture_dirt_plane", 
  {
    "string filename" : ["dirt.tx"],
  })
  ri.Pattern('PxrMix','mix_colour_wood_plane',
  {
    'color color1' : [0.6,0.6,0.6], 
    'color color2' : [0.45,0.45,0.45], 
    'reference float mix' : ['PxrTexture_wood_plane:resultA'], 
  })
  ri.Pattern('PxrMix','mix_colour_dirt_plane',
  {
    'color color2' : [0.425,0.415,0.415], 
    'reference color color1' : ['mix_colour_wood_plane:resultRGB'], 
    'reference float mix' : ['PxrTexture_dirt_plane:resultA'], 
  })
  ri.Pattern('PxrMix','mix_spec_plane',
  {
    'color color1' : [0.3,0.0,0.0], 
    'color color2' : [0.35,0.0,0.0], 
    'reference float mix' : ['PxrTexture_wood_plane:resultA'], 
  })
  ri.Pattern('PxrMix','mix_rough_plane',
  {
    'color color1' : [0.3,0.0,0.0], 
    'color color2' : [0.6,0.0,0.0], 
    'reference float mix' : ['PxrTexture_wood_plane:resultA'], 
  })
  ri.Displace( 'PxrDisplace' ,'displacement' ,
  {
    'int enabled' : [1],
    'float dispAmount' : [0.001],
    'reference float dispScalar' : ['PxrTexture_wood_plane:resultA'] ,
    'vector dispVector' : [0, 0 ,0],
    'vector modelDispVector' : [0, 0 ,0],
    'string __materialid' : ["displace_wood_plane"]
  })
  ri.Bxdf("PxrDisney","PxrDisney_plane", {
    "reference color baseColor" : ["mix_colour_dirt_plane:resultRGB"],
    'reference float specular' : ['mix_spec_plane:resultR'],
    'reference float roughness' : ['mix_rough_plane:resultR'], 
    'string __materialid' : ['material_wood_plane']
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
  ri.Attribute( 'visibility',
  { 
    'int transmission' : [1]
  })
  ri.Attribute( 'trace',
  { 
    'int maxdiffusedepth' : [1], 
    'int maxspeculardepth' : [8]
  })
  ri.Pattern ("PxrTexture", "PxrTexture_glassdirt", 
  {
    "string filename" : ["smudges.tx"],
  })
  ri.Pattern('PxrMix','mix_dirt_glass',
  {
    'color color1' : [0.25,0,0], 
    'color color2' : [0,0,0], 
    'reference float mix' : ['PxrTexture_glassdirt:resultA'], 
  })
  ri.Bxdf('PxrSurface', 'glass',
  { 
    'reference float diffuseGain' : ['mix_dirt_glass:resultR'],
    'color diffuseColor' : [0.15,0.15,0.15],
    'float refractionGain' : [1.0],
    'float reflectionGain' : [1.0],
    'float glassRoughness' : [0.01],
    'float glassIor' : [1.5],
    'string __materialid' : ['material_glass'] 
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
  ri.Pattern("PxrDirt", "PxrDirt1",
  {
    "int direction": [2],
    "int numSamples" : [16], 
  })
  ri.Pattern("PxrRemap", "PxrRemap1", 
  {
    "reference color inputRGB" : ["PxrDirt1:resultRGB"],
    "float inputMin" : [0.6], 
    "float inputMax" : [0.7],
    "float outputMin" : [1], 
    "float outputMax" : [0],
  })
  ri.Pattern('PxrMix','mix_dirt_general',
  {
    'color color2' : [0.25,0.25,0.25], 
    'color color1' : [0.2,0.2,0.2], 
    'reference float mix' : ['PxrRemap1:resultR'], 
  })
  ri.Pattern('PxrMix','mix_dirt_general_metallic',
  {
    'color color2' : [0.9,0.0,0.0], 
    'color color1' : [0.75,0.0,0.0], 
    'reference float mix' : ['PxrRemap1:resultR'], 
  })
  ri.Pattern ("PxrTexture", "Texture_dust", {
    "string filename" : ["dust.tx"],
  })
  ri.Pattern('PxrMix','mix_dirt_general_plus_dust',
  {
    'reference color color1' : ['mix_dirt_general:resultRGB'], 
    'color color2' : [0.175,0.175,0.175], 
    'reference float mix' : ['Texture_dust:resultR'], 
  })
  ri.Pattern('PxrMix','mix_dirt_general_metallic_plus_dust',
  {
    'reference color color1' : ['mix_dirt_general_metallic:resultRGB'], 
    'color color2' : [0.6,0,0], 
    'reference float mix' : ['Texture_dust:resultR'], 
  })
  ri.Bxdf('PxrDisney','metal',
  {
    'reference color baseColor' : ['mix_dirt_general_plus_dust:resultRGB'], 
    'reference float metallic' : ['mix_dirt_general_metallic_plus_dust:resultR'], 
    'float specular' : [0.9], 
    'reference float roughness' : ['mix_scratches_roughness:resultR'], 
    'reference float anisotropic' : ['mix_scratches_anisotropic:resultR'], 
    'string __materialid' : ['metal']
  })
  m_oD.outOrdinaryMetalDetails(ri, widthSmall, widthBig, hight)
  ri.AttributeEnd()
  ri.AttributeBegin()
  ri.Translate(0.0, 0.0, hight/2-0.05)
  ri.Pattern('dirt','dirt', 
  { 
  })
  ri.Pattern('PxrMix','mix_dirt_roughness',
  {
    'color color1' : [0.4,0.0,0.0], 
    'color color2' : [0.7,0.0,0.0], 
    'reference float mix' : ['dirt:dirtDots'], 
  })
  ri.Pattern('PxrMix','mix_dirt',
  {
    'color color1' : [0.25,0.25,0.25], 
    'color color2' : [0.225,0.21,0.21], 
    'reference float mix' : ['dirt:dirtDots'], 
  })
  ri.Bxdf('PxrDisney','metal_dirt',
  {
    'reference color baseColor' : ['mix_dirt:resultRGB'], 
    'float metallic' : [0.9], 
    'float specular' : [0.9], 
    'reference float roughness' : ['mix_dirt_roughness:resultR'], 
    'string __materialid' : ['metal_dirt']
  })
  ri.Hyperboloid([ widthBig,0.0,-0.2],[widthBig + 0.05,0.0,-0.2],360)
  ri.AttributeEnd()
  ri.TransformEnd()

  ri.WorldEnd()
  #######################################################################
  #World End
  #######################################################################

  ri.End()

def checkAndCompileShader(shader) :
  path = os.path.join(os.pardir, 'shaders')
  print(path)
  if os.path.isfile(os.path.join(path, shader+'.oso')) != True  or os.stat(os.path.join(path, shader+'.osl')).st_mtime - os.stat(os.path.join(path, shader+'.oso')).st_mtime > 0 :
    print( 'compiling shader {0}'.format(shader))
    try:
      subprocess.check_call(['oslc', os.path.join(path,shader+'.osl')], cwd=path)
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
  
