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