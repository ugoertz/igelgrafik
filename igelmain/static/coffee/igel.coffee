class Turtle
  constructor: (w, h, @canvas) ->
    @canvas.width = w
    @canvas.height = h
    @stage = new createjs.Stage($("#canvas")[0])
    @home.x = w/2
    @home.y = h/2
    @home.angle = 0
    createjs.Ticker.addListener(this)
    @queue = $({})
    @clear()

  update: ->
    @turtle.x = @x
    @turtle.y = @y
    @turtle.rotation = @angle

  forwardPos: (distance) ->
    x = (Math.sin(@angle / 180 * Math.PI) * distance) + @x
    y = (Math.cos(@angle / 180 * Math.PI) * (-distance)) + @y
    return {x: x, y: y }

  forward: (distance) =>
    @queue.queue 'move', (next) =>
      toPos = @forwardPos distance
      if @isPendown
        @g.lineTo(toPos.x, toPos.y)
      else
        @g.moveTo(toPos.x, toPos.y)
      @x = toPos.x
      @y = toPos.y
      @update()

  backward: (distance) =>
    @forward(-distance)

  left: (angle) =>
    @queue.queue 'move', (next) =>
      @angle -= angle
      @update()

  right: (angle) =>
    @left -angle

  setAngle: (angle) =>
    @queue.queue 'move', (next) =>
      @angle = angle
      @update()


  pendown: =>
    @queue.queue 'move', (next) =>
      @isPendown = true
      next()

  penup: =>
    @queue.queue 'move', (next) =>
      @isPendown = false
      next()


  pencolor: (color) =>
    @queue.queue 'move', (next) =>
      @penColor = color
      @g.beginStroke(@penColor)
      @g.moveTo @x, @y
      next()

  pensize: (x) =>
    @queue.queue 'move', (next) =>
      @g.setStrokeStyle x
      @g.moveTo @x, @y
      next()

  hideturtle: =>
    @queue.queue 'move', (next) =>
      @turtle.visible = false
      @update()

  showturtle: =>
    @queue.queue 'move', (next) =>
      @turtle.visible = true
      @update()

  fill: (color) =>
    @queue.queue 'move', (next) =>
      @g.beginFill(color)
      @g.moveTo @x, @y
      next()

  clear: =>
    @queue.queue 'move', (next) =>
      @x = @home.x
      @y = @home.y
      @angle = @home.angle
      @isPendown = true
      @penColor = 'black'
      @stage.clear()
      @stage.removeAllChildren()
      g = new createjs.Graphics()
      g.setStrokeStyle(2)
      g.beginStroke('black')
      g.beginFill('gray')
      g.moveTo(-8, 7)
      g.lineTo(0, -15)
      g.lineTo(8, 7)
      g.lineTo(-8, 7)
      @turtle = new createjs.Shape(g)
      @stage.addChild @turtle
      @newpath()

  newpath: =>
    @g = new createjs.Graphics()
    @g.beginStroke(@penColor)
    @g.moveTo @x, @y
    @g.setStrokeStyle(2)
    @stage.addChildAt new createjs.Shape(@g), 0

    @update()

  home: =>
    @queue.queue 'move', (next) =>
      @x = @home.x
      @y = @home.y
      @angle = @home.angle

  tick: =>
    if @queue.length
      @queue.dequeue('move')
      @stage.update()

  speed: (speed) =>
    @queue.queue 'move', (next) =>
      createjs.Ticker.setFPS(speed)
      next()

window.Turtle = Turtle



