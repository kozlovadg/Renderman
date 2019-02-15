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
  #print ('shading rate {} pivel variance {} using {} {}'.format(shadingrate,pixelvar,integrator,integratorParams))
    
  ri = prman.Ri() # create an instance of the RenderMan interface

  ri.Begin(filename)

  ri.Option('searchpath', {'string archive':'./assets/:@'})
  ri.Option('searchpath', {'string texture':'../hdri/:@'})

  ri.Display('watches.exr', 'it', 'rgba')
  ri.Format(width,height,1)

  ri.Hider('raytrace' ,{'int incremental' :[1]})
  ri.ShadingRate(shadingrate)
  ri.PixelVariance (pixelvar)
  ri.Option( 'statistics', {'filename'  : [ 'stats.txt' ] } )
  ri.Option( 'statistics', {'endofframe' : [ 1 ] })
  ri.Projection(ri.PERSPECTIVE,{ri.FOV:fov})

  #######################################################################
  #World Begin
  #######################################################################
  ri.WorldBegin()

  #######################################################################
  #Lighting Begin
  #######################################################################
  ri.TransformBegin()
  ri.Rotate(-90,1,0,0)
  ri.Rotate(180,0,0,1)
  ri.Light( 'PxrDomeLight', 'domeLight', { 
            'string lightColorMap'  : 'vatican_road_2k.tx'
   })
  ri.TransformEnd()
  #######################################################################
  # Lighting End
  #######################################################################

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
