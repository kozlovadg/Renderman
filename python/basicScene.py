from __future__ import print_function
import prman
import ProcessCommandLine as cl

def sideDetailsNearMechanism(ri):
      # Detail 1
      ri.TransformBegin()
      ri.Rotate(-5, 0,0,1)

      face=[0,1.325,-0.175,
            0.15,1.24,-0.22,
            0,1.325,-0.175,
            0,1.25,-0.225,
            ]	
      ri.Patch("bilinear",{'P':face})

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

      face=[0,1.325,-0.175,
            -0.15,1.24,-0.22,
            0,1.325,-0.175,
            0,1.25,-0.225,
            ]	
      ri.Patch("bilinear",{'P':face})

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

def detailAroundMechanism(ri):
      index = 0
      while index < 2:
            ri.TransformBegin()
            ri.Translate(0,0,-0.1*index)
            angle = 0
            while angle<360:
                  
                  ri.TransformBegin()
                  ri.Rotate(angle-5,0,0,1)
                  face=[0,-0.175,-1.25,
                        0,-0.1,-1.25,
                        0,-0.175,-1.325,
                        0,-0.1,-1.325]	
                  ri.Patch("bilinear",{'P':face})
                  ri.TransformEnd()

                  ri.TransformBegin()
                  ri.Rotate(angle,0,0,1)
                  face=[0,-0.175,-1.25,
                        0,-0.1,-1.25,
                        0,-0.175,-1.325,
                        0,-0.1,-1.325]	
                  ri.Patch("bilinear",{'P':face})

                  face=[0,-0.175,-1.25,
                        0,-0.175,-1.325,
                        0.075,-0.16,-1.25,
                        0.075,-0.16,-1.325]	
                  ri.Patch("bilinear",{'P':face})

                  face=[0,-0.175,-1.325,
                        0.075,-0.16,-1.325,
                        0,-0.1,-1.325,
                        0.05,-0.1,-1.325]	
                  ri.Patch("bilinear",{'P':face})
                  ri.TransformEnd()

                  angle += 30
            ri.TransformEnd()
            index += 1

def fastenerDetail(ri):
  # Detail 3
  ri.TransformBegin()

  ri.Rotate(-110, 0,0,1)

  face=[0,1.55,-0.05,
        0.1,1.325,-0.175,
        0,1.55,0.185,
        0.1,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.55,-0.05,
        0.5,1.22,-0.175,
        0.25,1.55,0.185,
        0.5,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.55,-0.05,
        0.5,1.22,-0.175,
        0,1.55,-0.05,
        0.1,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.55,0.185,
        0.5,1.22,0.125,
        0,1.55,0.185,
        0.1,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  # Second part of Detail 3
  face=[0,1.55,-0.05,
        0,1.55,0.185,
        -0.1,1.7,0.1,
        -0.1,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  face=[0.25,1.55,-0.05,
        0.25,1.55,0.185,
        0.125,1.7,0.1,
        0.125,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  face=[-0.1,1.7,0.1,
        -0.1,1.7,0.235,
        0.125,1.7,0.1,
        0.125,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  face=[0,1.55,-0.05,
        -0.1,1.7,0.1,
        0.25,1.55,-0.05,
        0.125,1.7,0.1]	
  ri.Patch("bilinear",{'P':face})

  face=[0,1.55,0.185,
        -0.1,1.7,0.235,
        0.25,1.55,0.185,
        0.125,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()

  # Detail 4
  ri.TransformBegin()

  ri.Rotate(-65, 0,0,1)

  face=[0,1.55,-0.05,
        -0.1,1.325,-0.175,
        0,1.55,0.185,
        -0.1,1.35,0.125]	
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.55,-0.05,
        -0.5,1.22,-0.175,
        -0.25,1.55,0.185,
        -0.5,1.22,0.125]
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.55,-0.05,
        -0.5,1.22,-0.175,
        0,1.55,-0.05,
        -0.1,1.325,-0.175]
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.55,0.185,
        -0.5,1.22,0.125,
        0,1.55,0.185,
        -0.1,1.35,0.125]
  ri.Patch("bilinear",{'P':face})

  # Second part of Detail 4
  face=[0,1.55,-0.05,
        0,1.55,0.185,
        0.1,1.7,0.1,
        0.1,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  face=[-0.25,1.55,-0.05,
        -0.25,1.55,0.185,
        -0.125,1.7,0.1,
        -0.125,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  face=[0.1,1.7,0.1,
        0.1,1.7,0.235,
        -0.125,1.7,0.1,
        -0.125,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  face=[0,1.55,-0.05,
        0.1,1.7,0.1,
        -0.25,1.55,-0.05,
        -0.125,1.7,0.1]	
  ri.Patch("bilinear",{'P':face})

  face=[0,1.55,0.185,
        0.1,1.7,0.235,
        -0.25,1.55,0.185,
        -0.125,1.7,0.235]	
  ri.Patch("bilinear",{'P':face})

  ri.TransformEnd()

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

  ri.Translate(0,0.25,3.2)
  ri.Rotate(-30,1,0,0)
  ri.Rotate(-230,0,1,0)

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
  ri.Pattern('PxrTexture','PxrTexture1',
  {
        'string filename' : ["/Users/daria/Desktop/texture.tx"],
  })
  ri.Pattern('PxrMix','PxrMix1',
  {
        'reference color color2' : ["PxrTexture1:missingColor"],
        'reference float mix' : ["PxrTexture1:resultA"],
        'color color1' : [1,0,0]
  })
  ri.Attribute( 'user' , {'string __materialid' : ['metal_in'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrSurface', 'metal_in', {
          'reference color diffuseColor' : ["PxrMix1:resultRGB"],
          'reference float diffuseGain' : ["PxrTexture1:resultA"],
          'int specularFresnelMode' : [1],
          'color specularEdgeColor' : [0.54 ,0.54 ,0.54],
          'color specularIor' : [2.5, 2.5, 2.5],
          'color specularExtinctionCoeff' : [2.9996, 2.9996, 2.9996],
          'float specularRoughness' : [0.3], 
          'integer specularModelType' : [1] ,
          'string __materialid' : ['metal_in']
  })
  ri.Disk(diskPosition,widthSmall,-360)
  ri.Hyperboloid([ widthSmall,0.0,diskPosition],[widthSmall,0.0,diskPosition-0.2],360)
  ri.AttributeEnd()
  # ------------- Hands In ------------
  ri.TransformBegin()

  ri.Translate(0,0,0.225)

  ri.TransformBegin()
  ri.Rotate(25, 0,0,1)
  ri.Disk(-0.15,0.07,360)
  face=[-0.9,-0.01,-0.15,
        -0.9,0.01,-0.15,
        0.15,-0.03,-0.15,
        0.15,0.03,-0.15]
  ri.Patch("bilinear",{'P':face})
  ri.TransformEnd()

  ri.AttributeBegin()
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.001147,0.06711,0.516743]
  })

  ri.Disk(-0.155,0.0125,360)

  face=[-0.9,-0.03,-0.125,
        -0.9,0.03,-0.125,
        0.15,-0.03,-0.125,
        0.15,0.03,-0.125]
  ri.Disk(-0.125,0.07,360)
  ri.Patch("bilinear",{'P':face})

  ri.TransformBegin()
  ri.Rotate(-120, 0,0,1)
  ri.Disk(-0.1,0.07,360)
  face=[-0.65,-0.03,-0.1,
        -0.65,0.03,-0.1,
        0.15,-0.03,-0.1,
        0.15,0.03,-0.1]
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
  face=[0.285,-1.05,-0.06,
        0.285,-1.05,-0.06,
        0.285,-1.05,0.175,
        0.23,-0.875,0.175]
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

  # Side details near mechanism
  sideDetailsNearMechanism(ri)

  ri.TransformBegin()
  ri.Rotate(-20, 0,0,1)
  ri.Rotate(90, 1,0,0)
  ri.Translate(0,-0.025,0)
  ri.Cylinder(0.15,-1.45,-1.1,360)
  ri.Hyperboloid([0.15,0.0,-1.45],[0.125,0.0,-1.45],360)
  
  ri.AttributeBegin()
  ri.Bxdf('PxrDiffuse', 'smooth', { 
          'color diffuseColor' : [0.001147,0.06711,0.516743]
  }) 
  ri.Disk(-1.45,0.125,360)
  ri.AttributeEnd()

  
  # Small details around mechanism
  detailAroundMechanism(ri)
  
  ri.TransformEnd()

  ri.Hyperboloid([ widthBig + 0.05,0.0,-0.225],[widthBig + 0.05,0.0,0.125],330)

  ri.TransformBegin()
  ri.Rotate(85, 0,0,1)
  ri.Hyperboloid([ widthBig + 0.05,0.0,-0.225],[widthBig + 0.125,0.0,-0.175],330)
  ri.Hyperboloid([ widthBig + 0.125,0.0,-0.175],[widthBig + 0.15,0.0,0.125],330)
  ri.TransformEnd()

  ri.Disk(0.125, widthBig + 0.15, 360)
  ri.Hyperboloid([ widthBig-0.1,0.0,0.125],[widthBig-0.1,0.0,0.14],360)
  ri.Hyperboloid([ widthBig-0.1,0.0,0.14],[widthBig-0.2,0.0,0.16],360)
  ri.Disk(0.16, widthBig-0.2, 360)

  # Detail 3 and Detail 4
  ri.TransformBegin()
  ri.Rotate(-20, 0,0,1)
  fastenerDetail(ri)
  ri.TransformEnd()

  # Detail 5 and Detail 6
  ri.TransformBegin()
  ri.Rotate(-200, 0,0,1)
  fastenerDetail(ri)
  ri.TransformEnd()

  ri.AttributeEnd()
  ri.TransformEnd()

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
  # Cylinder between details
  ri.TransformBegin()
  ri.Translate(1.55,-0.3,0)
  ri.Rotate(15, 0,1,0)
  ri.Cylinder(0.04,-1.05,0.25,360)
  ri.TransformEnd()

  ri.TransformBegin()
  ri.Translate(-1.55,-0.3,0)
  ri.Rotate(15, 0,1,0)
  ri.Cylinder(0.04,-0.25,1.05,360)
  ri.TransformEnd()

  ri.AttributeEnd()


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
