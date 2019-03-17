import modeling_sideDetails as m_sD

def outBlueMetalDetails(ri):
    ri.TransformBegin()
    ri.Rotate(-20, 0,0,1)
    ri.Rotate(90, 1,0,0)
    ri.Translate(0,0.175,0)
    ri.Disk(-1.45,0.125,360)
    ri.TransformEnd()

def outOrdinaryMetalDetails(ri, widthSmall, widthBig, hight):
    ri.Hyperboloid([ widthSmall-0.05,0.0,-0.075],[widthSmall,0.0,-0.1],360)
    ri.Hyperboloid([widthSmall,0.0,-0.1], [widthBig,0.0,-0.05],360)
    ri.Translate(0.0, 0.0, hight/2-0.05)
    ri.Hyperboloid([widthBig,0.0,-hight/2], [widthBig,0.0,-0.2],360)
    ri.Hyperboloid([ widthBig,0.0,-0.2],[widthBig + 0.05,0.0,-0.2],360)
    ri.Hyperboloid([ widthBig + 0.05,0.0,-0.2],[widthBig + 0.05,0.0,-0.225],360)

    # Side details near mechanism
    m_sD.sideDetailsNearMechanism(ri)

    ri.TransformBegin()
    ri.Rotate(-20, 0,0,1)
    ri.Rotate(90, 1,0,0)
    ri.Translate(0,-0.025,0)
    ri.Cylinder(0.15,-1.45,-1.1,360)
    ri.Hyperboloid([0.15,0.0,-1.45],[0.125,0.0,-1.45],360)
    
    # Small details around mechanism
    m_sD.detailAroundMechanism(ri)
    
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
    m_sD.fastenerDetail(ri)
    ri.TransformEnd()

    # Detail 5 and Detail 6
    ri.TransformBegin()
    ri.Rotate(-200, 0,0,1)
    m_sD.fastenerDetail(ri)
    ri.TransformEnd()

def outCylindersMetalDetails(ri):
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