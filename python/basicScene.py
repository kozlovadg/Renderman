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

  ri.Translate(0,0,3)
  ri.Rotate(-30,1,0,0)

  #######################################################################
  #World Begin
  #######################################################################
  ri.WorldBegin()

  ###
  # Lighting Begin
  ###
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)
  ri.Rotate(180,0,0,1)
  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'vatican_road_2k.tex'
   })
  ri.TransformEnd()
  ###
  # Lighting End
  ###


  ###
  # Model Part 1 Begin
  ###
  ri.AttributeBegin()
  ri.Attribute( 'user' , {'string __materialid' : ['metal'] })
  ri.Attribute( 'Ri', {'int Sides' : [2] })
  ri.Bxdf('PxrSurface', 'metal', {
          'float diffuseGain' : [0],
          'int specularFresnelMode' : [1],
          'color specularEdgeColor' : [1 ,1 ,1],
          'color specularIor' : [4.3696842, 2.916713, 1.654698],
          'color specularExtinctionCoeff' : [5.20643, 4.2313662, 3.7549689],
          'float specularRoughness' : [0.1], 
          'integer specularModelType' : [1] ,
          'string __materialid' : ['metal']
  })
  """ri.Bxdf('PxrDisney','metal',
  {
    'color baseColor' : [.25,.25,.25], 
    'float metallic' : [1], 
    'float specular' : [1], 
    'float roughness' : [0.2], 
    'string __materialid' : ['metal']
  })"""
  ri.TransformBegin()
  widthBig = 1.25
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
  ri.Disk(-0.125,1.05,360)
  ri.Hyperboloid([ 1.05,0.0,-0.075],[1.05,0.0,-0.125],360)
  ri.TransformBegin()
  ri.Translate(0,0,-0.2)
  ri.Rotate(-90,1,0,0)
  ri.Scale(0.1,0.1,0.1)
  ri.ReadArchive('buddha.rib')
  ri.TransformEnd()
  ri.AttributeEnd()
  # ------------- Metal -------------
  ri.Hyperboloid([ 1.05,0.0,-0.075],[1.1,0.0,-0.1],360)
  ri.Hyperboloid([widthSmall,0.0,-0.1], [widthBig,0.0,0.0],360)
  ri.Translate(0.0, 0.0, hight/2)
  ri.Hyperboloid([widthBig,0.0,-hight/2], [widthBig,0.0,hight/2],360)
  #ri.Disk(-hight/2,widthBig,360)
  ri.TransformEnd()
  ri.AttributeEnd()
  ###
  # Model Part 1 End
  ###


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
