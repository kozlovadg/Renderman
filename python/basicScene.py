from __future__ import print_function
import prman
import ProcessCommandLine as cl

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
  ri.Option('searchpath', {'string texture':'../hdri/:@'})

  ri.Display('watches.exr', 'it', 'rgba')
  ri.Format(width,height,1)

  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  ri.Integrator (integrator ,'integrator',integratorParams)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })

  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})

  ri.Translate(0,0.25,4)
  ri.Rotate(-90,1,0,0)
  ri.Rotate(-290,0,1,0)

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
  diskPosition = 0.15
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrSurface', 'metal_in', {
          'float diffuseGain' : [0],
          'int specularFresnelMode' : [1],
          'color specularEdgeColor' : [1 ,1 ,1],
          'color specularIor' : [4.3696842, 2.916713, 1.654698],
          'float specularAnisotropy' : [1.0],
          'color specularExtinctionCoeff' : [5.20643, 4.2313662, 3.7549689],
          'float specularRoughness' : [0.5], 
          'integer specularModelType' : [1] ,
          'string __materialid' : ['metal_in']
  })
  ri.Disk(diskPosition,widthSmall,-360)
  ri.Hyperboloid([ widthSmall,0.0,diskPosition],[widthSmall,0.0,diskPosition-0.2],360)
  ri.AttributeEnd()
  # ------------- Hands In ------------
  ri.TransformBegin()

  ri.Translate(0,0,0.225)

  w = 0.9
  d = 0.15
  h = 0.03
  face=[-w,-h+0.02,-d,-w,h-0.02,-d,0.15,-h,-d,0.15,h,-d]
  ri.TransformBegin()
  ri.Rotate(25, 0,0,1)
  ri.Disk(-0.15,-0.07,360)
  ri.Patch("bilinear",{'P':face})
  ri.TransformEnd()

  ri.AttributeBegin()
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.001147,0.06711,0.516743]
  })

  w = 0.9
  d = 0.125
  h = 0.03
  face=[-w,-h,-d,-w,h,-d,0.15,-h,-d,0.15,h,-d]
  ri.Disk(-0.125,-0.07,360)
  ri.Patch("bilinear",{'P':face})

  w = 0.65
  d = 0.1
  h = 0.03
  face=[-w,-h,-d,-w,h,-d,0.15,-h,-d,0.15,h,-d]
  ri.TransformBegin()
  ri.Rotate(-120, 0,0,1)
  ri.Disk(-0.1,-0.07,360)
  ri.Patch("bilinear",{'P':face})
  ri.TransformEnd()
  ri.AttributeEnd()
  ri.TransformEnd()
  # ------------- Paper In -------------
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.8,0.8,0.8]
  })
  ri.Disk(diskPosition-0.005,widthSmall-0.5,360)
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
  # Triangles
  face=[0.285,-1.05,-0.06,0.285,-1.05,-0.06,0.285,-1.05,0.175,0.23,-0.875,0.175]
  ri.Patch("bilinear",{'P':face})	
  ri.TransformBegin()
  ri.Rotate(-30,0,0,1)
  ri.Patch("bilinear",{'P':face})	
  ri.TransformEnd()

  ri.TransformBegin()
  ri.Rotate(-75, 0,0,1)
  ri.Hyperboloid([ widthSmall-0.175,0.0,diskPosition],[widthSmall,0.0,diskPosition-0.2],330)
  ri.TransformEnd()
  ri.TransformEnd()
  ri.AttributeEnd()
  # ------------- Metal Out -------------
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['metal'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  """
  ri.Bxdf('PxrSurface', 'metal', {
          'float diffuseGain' : [0],
          'int specularFresnelMode' : [1],
          'color specularEdgeColor' : [1 ,1 ,1],
          'color specularIor' : [4.3696842, 2.916713, 1.654698],
          'color specularExtinctionCoeff' : [5.20643, 4.2313662, 3.7549689],
          'float specularRoughness' : [0.1], 
          'integer specularModelType' : [1] ,
          'string __materialid' : ['metal']
  })"""
  ri.Bxdf('PxrDisney','metal',
  {
    'color baseColor' : [.25,.25,.25], 
    'float metallic' : [1], 
    'float specular' : [1], 
    'float roughness' : [0.2], 
    'string __materialid' : ['metal']
  })
  ri.Hyperboloid([ widthSmall-0.05,0.0,-0.075],[widthSmall,0.0,-0.1],360)
  ri.Hyperboloid([widthSmall,0.0,-0.1], [widthBig,0.0,-0.05],360)
  ri.Translate(0.0, 0.0, hight/2-0.05)
  ri.Hyperboloid([widthBig,0.0,-hight/2], [widthBig,0.0,-0.2],360)
  ri.Hyperboloid([ widthBig,0.0,-0.2],[widthBig + 0.05,0.0,-0.2],360)
  ri.Hyperboloid([ widthBig + 0.05,0.0,-0.2],[widthBig + 0.05,0.0,-0.225],360)

  # Detail 1
  ri.TransformBegin()
  ri.Rotate(-5, 0,0,1)

  face=[0.05,1.5,-0.05,
        0,1.325,-0.175,
        0.05,1.5,0.085,
        0,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[0.15,1.5,-0.05,
        0.15,1.24,-0.22,
        0.175,1.5,0.085,
        0.15,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[0.175,1.5,-0.05,
        0.15,1.24,-0.22,
        0.05,1.5,-0.05,
        0,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[0.175,1.5,0.085,
        0.15,1.22,0.125,
        0.05,1.5,0.085,
        0,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[0.175,1.5,-0.05,
        0.175,1.5,0.085,
        0.05,1.5,-0.05,
        0.05,1.5,0.085]
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()

  # Detail 2
  ri.TransformBegin()
  ri.Rotate(-35, 0,0,1)

  face=[-0.05,1.5,-0.05,
        0,1.325,-0.175,
        -0.05,1.5,0.085,
        0,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[-0.175,1.5,-0.05,
        -0.15,1.24,-0.22,
        -0.175,1.5,0.085,
        -0.15,1.22,0.125]
  ri.Patch("bilinear",{'P':face})
  
  face=[-0.175,1.5,-0.05,
        -0.15,1.24,-0.22,
        -0.05,1.5,-0.05,
        0,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[-0.175,1.5,0.085,
        -0.15,1.22,0.125,
        -0.05,1.5,0.085,
        0,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[-0.175,1.5,-0.05,
        -0.175,1.5,0.085,
        -0.05,1.5,-0.05,
        -0.05,1.5,0.085]
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()

  ri.TransformBegin()
  ri.Rotate(-20, 0,0,1)
  ri.Rotate(90, 1,0,0)
  ri.Translate(0,-0.025,0)
  ri.Cylinder(0.15,-1.45,-1.1,360)
  
  ri.AttributeBegin()
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.001147,0.06711,0.516743]
  }) 
  ri.Disk(-1.45,0.15,360)
  ri.AttributeEnd()
  
  ri.TransformEnd()

  ri.Hyperboloid([ widthBig + 0.05,0.0,-0.225],[widthBig + 0.05,0.0,0.125],330)

  ri.TransformBegin()
  ri.Rotate(85, 0,0,1)
  ri.Hyperboloid([ widthBig + 0.05,0.0,-0.225],[widthBig + 0.125,0.0,-0.175],330)
  ri.Hyperboloid([ widthBig + 0.125,0.0,-0.175],[widthBig + 0.15,0.0,0.125],330)
  ri.TransformEnd()

  # Detail 3 and Detail 4
  ri.TransformBegin()
  ri.Rotate(-20, 0,0,1)

  # Detail 3
  ri.TransformBegin()

  ri.Rotate(-110, 0,0,1)

  face=[0,1.65,0.05,
        0.1,1.325,-0.175,
        0,1.65,0.185,
        0.1,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.65,0.05,
        0.5,1.22,-0.175,
        0.25,1.65,0.185,
        0.5,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.65,0.05,
        0.5,1.22,-0.175,
        0,1.65,0.05,
        0.1,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.65,0.185,
        0.5,1.22,0.125,
        0,1.65,0.185,
        0.1,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()

  # Detail 4
  ri.TransformBegin()

  ri.Rotate(-65, 0,0,1)

  face=[0,1.65,0.05,
        -0.1,1.325,-0.175,
        0,1.65,0.185,
        -0.1,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.65,0.05,
        -0.5,1.22,-0.175,
        -0.25,1.65,0.185,
        -0.5,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.65,0.05,
        -0.5,1.22,-0.175,
        0,1.65,0.05,
        -0.1,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.65,0.185,
        -0.5,1.22,0.125,
        0,1.65,0.185,
        -0.1,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()
  ri.TransformEnd()

  # Detail 5 and Detail 6
  ri.TransformBegin()
  ri.Rotate(-200, 0,0,1)

  # Detail 5
  ri.TransformBegin()

  ri.Rotate(-110, 0,0,1)

  face=[0,1.65,0.05,
        0.1,1.325,-0.175,
        0,1.65,0.185,
        0.1,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.65,0.05,
        0.5,1.22,-0.175,
        0.25,1.65,0.185,
        0.5,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.65,0.05,
        0.5,1.22,-0.175,
        0,1.65,0.05,
        0.1,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.65,0.185,
        0.5,1.22,0.125,
        0,1.65,0.185,
        0.1,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()

  # Detail 6
  ri.TransformBegin()

  ri.Rotate(-65, 0,0,1)

  face=[0,1.65,0.05,
        -0.1,1.325,-0.175,
        0,1.65,0.185,
        -0.1,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.65,0.05,
        -0.5,1.22,-0.175,
        -0.25,1.65,0.185,
        -0.5,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.65,0.05,
        -0.5,1.22,-0.175,
        0,1.65,0.05,
        -0.1,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.65,0.185,
        -0.5,1.22,0.125,
        0,1.65,0.185,
        -0.1,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()
  ri.TransformEnd()

  ri.AttributeEnd()
  ri.TransformEnd()


  ri.WorldEnd()
  #######################################################################
  #World End
  #######################################################################

  ri.End()


if __name__ == '__main__':  
  cl.ProcessCommandLine('testScenes.rib')
  main(cl.filename,
    cl.args.shadingrate,
    cl.args.pixelvar,
    cl.args.fov,cl.args.width,
    cl.args.height,
    cl.integrator,
    cl.integratorParams)
