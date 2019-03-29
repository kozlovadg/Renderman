def metalIn(ri, diskPosition, widthSmall):
    ri.Disk(diskPosition,widthSmall,-360)
    ri.Hyperboloid([ widthSmall,0.0,diskPosition],[widthSmall,0.0,diskPosition-0.2],360)

def handsWhite(ri):
    ri.TransformBegin()
    ri.Rotate(25, 0,0,1)
    ri.Disk(-0.15,0.07,360)
    face=[-0.9,-0.01,-0.15,
            -0.9,0.01,-0.15,
            0.15,-0.03,-0.15,
            0.15,0.03,-0.15]
    ri.Patch("bilinear",{'P':face})
    ri.TransformEnd()

def handsBlue_minute(ri):
    ri.Disk(-0.155,0.0125,360)

    face=[-0.9,-0.03,-0.125,
            -0.9,0.03,-0.125,
            0.15,-0.03,-0.125,
            0.15,0.03,-0.125]
    ri.Disk(-0.125,0.07,360)
    ri.Patch("bilinear",{'P':face})

def handsBlue_hour(ri):
    ri.TransformBegin()
    ri.Rotate(-120, 0,0,1)
    ri.Disk(-0.1,0.07,360)
    face=[-0.65,-0.03,-0.1,
            -0.65,0.03,-0.1,
            0.15,-0.03,-0.1,
            0.15,0.03,-0.1]
    ri.Patch("bilinear",{'P':face})
    ri.TransformEnd()

def plasticIn(ri, widthSmall, diskPosition):
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