// ColoredPoint.js (c) 2012 matsuda
// Vertex shader program
var VSHADER_SOURCE = `
precision mediump float;
attribute vec4 a_Position;
attribute vec2 a_UV;
attribute vec3 a_Normal;
varying vec2 v_UV;
varying vec3 v_Normal;
varying vec4 v_VertPos;
uniform mat4 u_ModelMatrix;
uniform mat4 u_NormalMatrix;
uniform mat4 u_GlobalRotateMatrix;
uniform mat4 u_ViewMatrix;
uniform mat4 u_ProjectionMatrix;

void main() {
    gl_Position = u_ProjectionMatrix * u_ViewMatrix * u_GlobalRotateMatrix * u_ModelMatrix * a_Position;
    v_UV = a_UV;
    v_Normal = normalize(vec3(u_NormalMatrix * vec4(a_Normal, 1)));
    v_VertPos = u_ModelMatrix * a_Position;
}`


// Fragment shader program
var FSHADER_SOURCE = `
precision mediump float;
varying vec2 v_UV;
varying vec3 v_Normal;
uniform vec4 u_FragColor;
uniform sampler2D u_Sampler0; 
uniform sampler2D u_Sampler1;
uniform int u_whichTexture;
uniform vec3 u_lightPos;
uniform vec3 u_cameraPos;
varying vec4 v_VertPos;
uniform bool u_lightOn;
void main() {

  if (u_whichTexture == -3) {
      gl_FragColor = u_FragColor;
  } else if (u_whichTexture == -2) {
      gl_FragColor = u_FragColor;
  } else if (u_whichTexture == -1) {
      gl_FragColor = vec4(v_UV,1,1);
  } else if (u_whichTexture == 0) {
      gl_FragColor = texture2D(u_Sampler0, v_UV);
  } else if (u_whichTexture == 1) {
    gl_FragColor = texture2D(u_Sampler1, v_UV);
  } else if (u_whichTexture == 2){
    gl_FragColor = vec4((v_Normal+1.0)/2.0, 1.0);
  } else {
      gl_FragColor = vec4(1, .2, .2 , 1);
  }
  
  vec3 lightVector =u_lightPos - vec3(v_VertPos);
  float r = length(lightVector);
//   if (r<1.0){
//       gl_FragColor = vec4(1,0,0,1);
//   } else if (r<2.0) {
//       gl_FragColor = vec4(0,1,0,1);
//   }

//gl_FragColor = vec4(vec3(gl_FragColor)/(r*r),1);

vec3 L = normalize(lightVector);
vec3 N = normalize(v_Normal);
float nDotL = max(dot(N,L), 0.0);

vec3 R = reflect(-L,N);

vec3 E = normalize(u_cameraPos-vec3(v_VertPos));

float specular = pow(max(dot(E,R), 0.0),64.0) * .08;
if (u_whichTexture == -3){
    specular = 0.0;
}

if(u_lightOn){
  vec3 diffuse = vec3(1.0,1.0,.9) * vec3(gl_FragColor) * nDotL *.7;
  vec3 ambient = vec3(gl_FragColor) * .2;
  gl_FragColor = vec4(specular+diffuse+ambient, 1.0);
}

}`

//Global variables 
let canvas;
let gl;
let a_Position;
let u_FragColor;
let a_UV;
let a_Normal;
let u_Size;
let u_ModelMatrix;
let u_GlobalRotateMatrix;
let u_ProjectionMatrix
let u_ViewMatrix;
let u_Sampler0;
let u_Sampler1;
let u_whichTexture;
let u_lightPos;
let u_lightOn;

const POINT = 0;
const TRIANGLE = 1;
const CIRCLE = 2;

let g_normalOn = false;
let g_lightOn = false;
let g_selectedColor = [1, 1, 1, 1];
let g_selectedSize = 5;
let g_selectedType = POINT;
let g_selectedSeg = 6;
let g_globalAngle = 5;
let g_thighAngle = 0;
let g_shinAngle = 180;
let g_footAngle = 0;
let g_thighAngle2 = 0;
let g_shinAngle2 = 180;
let g_footAngle2 = 0;
let g_animation = false;
let g_arm = 0;
let g_tail = 0;
let g_lightPos=[0,1,-2];

function setupWebGL() {
    // Retrieve <canvas> element
    canvas = document.getElementById('webgl');
    // Get the rendering context for WebGL
    gl = canvas.getContext('webgl', { preserveDrawingBuffer: true});

    if (!gl) {
        console.log('Failed to get the rendering context for WebGL');
        return;
    }
    gl.enable(gl.DEPTH_TEST);
}

function connectVariablesToGLSL() {
    //Initialize Shaders
    if (!initShaders(gl, VSHADER_SOURCE, FSHADER_SOURCE)) {
        console.log('Failed to intialize shaders.');
        return;
    }

    // Get the storage location of a_Position
    a_Position = gl.getAttribLocation(gl.program, 'a_Position');
    if (a_Position < 0) {
        console.log('Failed to get the storage location of a_Position');
        return;
    }

    a_UV = gl.getAttribLocation(gl.program, 'a_UV');
    if (a_UV < 0) {
        console.log('Failed to get the storage location of a_UV');
        return;
    }

    a_Normal = gl.getAttribLocation(gl.program, 'a_Normal');
    if (a_Normal < 0) {
        console.log('Failed to get the storage location of a_Normal');
        return;
    }

    // Get the storage location of u_FragColor
    u_FragColor = gl.getUniformLocation(gl.program, 'u_FragColor');
    if (!u_FragColor) {
        console.log('Failed to get the storage location of u_FragColor');
        return;
    }

    // u_Size = gl.getUniformLocation(gl.program, 'u_Size');
    // if (!u_Size) {
    //     console.log('Failed to get the storage location of u_Size');
    //     return;
    // }

    u_ModelMatrix = gl.getUniformLocation(gl.program, 'u_ModelMatrix');
    if (!u_ModelMatrix) {
        console.log('Failed to get the storage location of u_ModelMatrix');
        return;
    }

    u_NormalMatrix = gl.getUniformLocation(gl.program, 'u_NormalMatrix');
    if (!u_NormalMatrix) {
        console.log('Failed to get the storage location of u_NormalMatrix');
        return;
    }

    u_GlobalRotateMatrix = gl.getUniformLocation(gl.program, 'u_GlobalRotateMatrix');
    if (!u_GlobalRotateMatrix) {
        console.log('Failed to get the storage location of u_GlobalRotateMatrix');
        return;
    }

    u_ViewMatrix = gl.getUniformLocation(gl.program, 'u_ViewMatrix');
    if (!u_ViewMatrix) {
        console.log('Failed to get the storage location of u_GlobalRotateMatrix');
        return;
    }

    u_ProjectionMatrix = gl.getUniformLocation(gl.program, 'u_ProjectionMatrix');
    if (!u_ProjectionMatrix) {
        console.log('Failed to get the storage location of u_ProjectionMatrix');
        return;
    }

    u_Sampler0 = gl.getUniformLocation(gl.program, 'u_Sampler0');
    if (!u_Sampler0) {
      console.log('Failed to get the storage location of u_Sampler0');
      return false;
    }

    u_Sampler1 = gl.getUniformLocation(gl.program, 'u_Sampler1');
    if (!u_Sampler1) {
      console.log('Failed to get the storage location of u_Sampler1');
      return false;
    }

    u_whichTexture = gl.getUniformLocation(gl.program, 'u_whichTexture');
    if (!u_whichTexture) {
      console.log('Failed to get the storage location of u_whichTexture');
      return false;
    }

    u_lightPos = gl.getUniformLocation(gl.program, 'u_lightPos');
    if (!u_lightPos) {
      console.log('Failed to get the storage location of u_lightPos');
      return false;
    }

    u_cameraPos = gl.getUniformLocation(gl.program, 'u_cameraPos');
    if (!u_cameraPos) {
      console.log('Failed to get the storage location of u_cameraPos');
      return false;
    }

    u_lightOn = gl.getUniformLocation(gl.program, 'u_lightOn');
    if (!u_lightOn) {
      console.log('Failed to get the storage location of u_lightOn');
      return false;
    }

    var identityM = new Matrix4();
    gl.uniformMatrix4fv(u_ModelMatrix, false, identityM.elements);
}


function addActionsForHtmlUI() {

    // document.getElementById('clearButton').onclick = function() {g_shapeList=[]; renderScene();};

    // document.getElementById('pointButton').onclick = function() {g_selectedType=POINT};
    // document.getElementById('triangleButton').onclick = function() {g_selectedType=TRIANGLE};
    // document.getElementById('circleButton').onclick = function() {g_selectedType=CIRCLE};

    // document.getElementById('redSlide').addEventListener('mouseup', function() { g_selectedColor[0] = this.value/100; });
    // document.getElementById('greenSlide').addEventListener('mouseup', function() { g_selectedColor[1] = this.value/100; });
    // document.getElementById('blueSlide').addEventListener('mouseup', function() { g_selectedColor[2] = this.value/100; });

    // document.getElementById('sizeSlide').addEventListener('mouseup', function() { g_selectedSize = this.value; });
    // document.getElementById('segSlide').addEventListener('mouseup', function() { g_selectedSeg = this.value; });

    document.getElementById('onButton').onclick = function() {g_animation=true};
    document.getElementById('offButton').onclick = function() {g_animation=false};

    document.getElementById('normalOnButton').onclick = function() {g_normalOn=true};
    document.getElementById('normalOffButton').onclick = function() {g_normalOn=false};

    document.getElementById('lightOnButton').onclick = function() {g_lightOn=true};
    document.getElementById('lightOffButton').onclick = function() {g_lightOn=false};

    document.getElementById('lightSlideX').addEventListener('mousemove', function(ev) {if(ev.buttons ==1) { g_lightPos[0] = this.value/100; renderScene(); }});
    document.getElementById('lightSlideY').addEventListener('mousemove', function(ev) {if(ev.buttons ==1) { g_lightPos[1] = this.value/100; renderScene(); }});
    document.getElementById('lightSlideZ').addEventListener('mousemove', function(ev) {if(ev.buttons ==1) { g_lightPos[2] = this.value/100; renderScene(); }});

    document.getElementById('angleSlide').addEventListener('mousemove', function() { g_globalAngle = this.value; renderScene(); });
    document.getElementById('thighSlide').addEventListener('mousemove', function() { g_thighAngle = this.value; renderScene(); });
    document.getElementById('shinSlide').addEventListener('mousemove', function() { g_shinAngle = this.value; renderScene(); });
    document.getElementById('footSlide').addEventListener('mousemove', function() { g_footAngle = this.value; renderScene(); });

    document.getElementById('thighSlide2').addEventListener('mousemove', function() { g_thighAngle2 = this.value; renderScene(); });
    document.getElementById('shinSlide2').addEventListener('mousemove', function() { g_shinAngle2 = this.value; renderScene(); });
    document.getElementById('footSlide2').addEventListener('mousemove', function() { g_footAngle2 = this.value; renderScene(); });

}

function initTextures() {
    // Get the storage location of u_Sampler
    var image = new Image();  // Create the image object
    if (!image) {
      console.log('Failed to create the image object');
      return false;
    }
    // Register the event handler to be called on loading an image
    image.onload = function(){ sendTextureTOGLSL(u_Sampler0, image, 0); };
    // Tell the browser to load an image
    image.src = 'dirt.jpg';

    var image1 = new Image();  // Create the image object
    if (!image1) {
      console.log('Failed to create the image object');
      return false;
    }
    // Register the event handler to be called on loading an image
    image1.onload = function(){ sendTextureTOGLSL(u_Sampler1, image1, 1); };
    // Tell the browser to load an image
    image1.src = 'sky2.jpg';
    
    return true;
}
  
function sendTextureTOGLSL(u_Sampler, image, texUnit) {

    var texture = gl.createTexture();   // Create a texture object
    var texture1 = gl.createTexture();

    if (!texture || !texture1) {
      console.log('Failed to create the texture object');
      return false;
    }

    var g_texUnit0 = false, g_texUnit1 = false; 

    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, 1); // Flip the image's y axis
    // Enable texture unit0
    if (texUnit == 0) {
        gl.activeTexture(gl.TEXTURE0);
        g_texUnit0 = true;
      } else {
        gl.activeTexture(gl.TEXTURE1);
        g_texUnit1 = true;
    }

    // Bind the texture object to the target
    gl.bindTexture(gl.TEXTURE_2D, texture);

    // Set the texture parameters
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    // Set the texture image
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, image);
    
    // Set the texture unit 0 to the sampler
    gl.uniform1i(u_Sampler, texUnit);


    console.log('finished sendTextureToGLSL');
    
}



function main() {
    setupWebGL();

    connectVariablesToGLSL();

    addActionsForHtmlUI();
    camera = new Camera();
    document.onkeydown = keydown;
    
    initTextures();
    // Register function (event handler) to be called on a mouse press
    //canvas.onmousedown = click;

    // Specify the color for clearing <canvas>
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    // Clear <canvas>
    //gl.clear(gl.COLOR_BUFFER_BIT);
    canvas.onmousemove = mousemove;
    requestAnimationFrame(tick);
    //renderScene();
}
var g_shapeList = [];
//var g_points = [];  // The array for the position of a mouse press
//var g_colors = [];  // The array to store the color of a point
//var g_sizes =  [];

// function click(ev) {

//     let [x,y] = convertCoordinatesEventToGL(ev);

//     let point;
//     if (g_selectedType==POINT){
//         point = new Point();
//     }
//     else if (g_selectedType==TRIANGLE){
//         point = new Triangle();
//     }
//     else{
//         point = new Circle();
//         point.segments = g_selectedSeg;
//     }
//     point.position=[x,y];
//     point.color=g_selectedColor.slice();
//     point.size=g_selectedSize;
//     g_shapeList.push(point);
    
//     // Store the coordinates to g_points array
//     //g_points.push([x, y]);

//     //g_colors.push(g_selectedColor.slice());

//     //g_sizes.push(g_selectedSize);
//     // Store the coordinates to g_points array
//     //if (x >= 0.0 && y >= 0.0) {      // First quadrant
//     //    g_colors.push([1.0, 0.0, 0.0, 1.0]);  // Red
//     //} else if (x < 0.0 && y < 0.0) { // Third quadrant
//     //    g_colors.push([0.0, 1.0, 0.0, 1.0]);  // Green
//     //} else {                         // Others
//     //    g_colors.push([1.0, 1.0, 1.0, 1.0]);  // White
//     //}   
// }

function convertCoordinatesEventToGL(ev){
    var x = ev.clientX; // x coordinate of a mouse pointer
    var y = ev.clientY; // y coordinate of a mouse pointer
    var rect = ev.target.getBoundingClientRect();

    x = ((x - rect.left) - canvas.width/2)/(canvas.width/2);
    y = (canvas.height/2 - (y - rect.top))/(canvas.height/2);

    return ([x,y]);
}

var g_startTime=performance.now()/1000.0;
var g_seconds=performance.now()/1000.0-g_startTime;

function tick() {
    //console.log(g_seconds);
    g_seconds=performance.now()/1000.0-g_startTime;
    updateAnimationAngles();
    renderScene();
    requestAnimationFrame(tick);
}

function updateAnimationAngles(){
    if (g_animation){
        g_thighAngle = (30*Math.sin(g_seconds));
        g_thighAngle2 = (-30*Math.sin(g_seconds));
        g_shinAngle = (45*Math.sin(g_seconds) + 135);
        g_shinAngle2 = (-45*Math.sin(g_seconds) + 135);
        g_footAngle = (-20*Math.sin(g_seconds));
        g_footAngle2 = (20*Math.sin(g_seconds));
        g_arm = (-15*Math.sin(g_seconds));
        g_tail = (30*Math.sin(g_seconds));
        g_lightPos[0]=2*Math.cos(g_seconds);
    
    }
}


function keydown(ev) {    
    if (ev.keyCode==87){
        camera.moveForward();
    } else if (ev.keyCode == 83){
        camera.moveBackwards();
    } else if (ev.keyCode == 65){
        camera.moveLeft();
    } else if (ev.keyCode == 68){
        camera.moveRight();
    } else if (ev.keyCode == 81){
        camera.panLeft();
    } else if (ev.keyCode == 69){
        camera.panRight();
    } else if (ev.keyCode == 67){
        var x = camera.at.elements[0];
        var y = camera.at.elements[1];
        var z = camera.at.elements[2];
        var body = new Cube();
        body.color = [0, 0, .8, 1];
        body.textureNum=0;
        body.matrix.translate(x,y,z);
        g_shapeList = g_shapeList.concat(body);
    } else if (ev.keyCode == 86) {
        var x = camera.at.elements[0];
        var y = camera.at.elements[1];
        var z = camera.at.elements[2];

        for(var i = 0; i < g_shapeList.length; i++) {
            width = g_shapeList[i].matrix.elements[0]/2;
            height = g_shapeList[i].matrix.elements[5]/2;
            length = g_shapeList[i].matrix.elements[10]/2;
            cubex = g_shapeList[i].matrix.elements[12];
            cubey = g_shapeList[i].matrix.elements[13];
            cubez = g_shapeList[i].matrix.elements[14];

            

            maxcubex = cubex + width;
            mincubex = cubex - width;
            maxcubey = cubey + height;
            mincubey = cubey - height;

            maxcubez = cubez + length;
            mincubez = cubez - length;

            if (x < maxcubex && x > mincubex){
                if (y < maxcubey && y > mincubey){
                    if (z < maxcubez && z > mincubez){
                        g_shapeList.splice(i, 1);
                        i--;
                    }
                }
            }
        }
    }

    renderScene();
    console.log(ev.keyCode);
}

function mousemove(ev){
    let [x,y] = convertCoordinatesEventToGL(ev);
    if (x > 0){
        camera.panRightMouse(x);
    } else if (x < 0) {
        camera.panLeftMouse(x);
    }
}

function drawMap(){
    for (x=0; x<32; x++){
        for (y=0; y<32; y++){
            var limit = Math.random()*10;
            if (x == 0 || y == 0 || x == 31 || y == 31){
                var body = new Cube();
                body.color = [.5, .15, 1, 1];
                body.textureNum=0;
                body.matrix.translate(x-15, -.75, y-15);
                g_shapeList = g_shapeList.concat(body);
            } else if (limit < .5){
                var body = new Cube();
                var height = Math.random()*3;
                var width = Math.random()*3;
                var length = Math.random()*3;
                body.color = [165, 42, 42, 1];
                body.textureNum=0;
                body.matrix.translate(x-15, -.75, y-15);
                body.matrix.scale(width, height, length);
                body.width = width;
                body.height = height;
                body.length = length;
                g_shapeList = g_shapeList.concat(body);
            }
        }
    }
}



function renderScene(){

    var projMat = camera.projectionMatrix;
    gl.uniformMatrix4fv(u_ProjectionMatrix, false, projMat.elements);

    var viewMat = camera.viewMatrix;
    gl.uniformMatrix4fv(u_ViewMatrix, false, viewMat.elements);

    var globalRotMat = new Matrix4().rotate(g_globalAngle, 0, 1, 0);
    gl.uniformMatrix4fv(u_GlobalRotateMatrix, false, globalRotMat.elements);

    // Clear <canvas>
    // gl.clear(gl.COLOR_BUFFER_BIT);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // var len = g_shapeList.length;
    // for(var i = 0; i < len; i++) {
    //     g_shapeList[i].renderfast();
    // }


    gl.uniform3f(u_cameraPos, camera.eye.elements[0], camera.eye.elements[1], camera.eye.elements[2],)
    gl.uniform3f(u_lightPos, g_lightPos[0], g_lightPos[1], g_lightPos[2]);
    gl.uniform1i(u_lightOn, g_lightOn);

    var light = new Cube();
    light.color = [2,2,0,1];
    light.matrix.translate(g_lightPos[0], g_lightPos[1], g_lightPos[2]);
    light.matrix.scale(-.1,-.1,-.1);
    light.matrix.translate(-.5,-.5,-.5);
    light.render();

    var floor = new Cube();
    floor.color = [.6, 1, .6, 1];
    floor.textureNum=-3;
    if (g_normalOn) floor.textureNum=2;
    floor.matrix.translate(0, -1, 0);
    floor.matrix.scale(7, 0, 7);
    floor.matrix.translate(-.5, 0, -.5);
    floor.render();

    var circle = new Sphere();
    if (g_normalOn) circle.textureNum=2;
    circle.matrix.translate(-2, 0, 0);
    circle.render();

    var sky = new Cube();
    sky.color = [.5, .5, .5, 1];
    sky.textureNum=-3;
    if (g_normalOn) sky.textureNum=2;
    sky.matrix.scale(-7,-7,-7);
    sky.matrix.translate(-.5, -.5, -.5);
    sky.render();

    var body = new Cube();
    body.color = [0, 0, .8, 1];
    if (g_normalOn) body.textureNum=2;
    body.matrix.scale(.75,.5,.5);
    body.matrix.translate(-.5,0,-.5);
    //body.normalMatrix.setInverseOf(body.matrix).transpose();
    body.render();

    var tail = new Cube();
    tail.color = [0,0,.8,.4];
    if (g_normalOn) tail.textureNum=2;
    tail.matrix.rotate(g_tail, 0, 1, 0);
    tail.matrix.scale(.125,.125,.5);
    tail.matrix.translate(-.5,0,.5);
    //tail.normalMatrix.setInverseOf(tail.matrix).transpose();
    tail.render();

    var leftEye = new Cube();
    leftEye.color = [1, 1, 0, 1];
    if (g_normalOn) leftEye.textureNum=2;
    leftEye.matrix.scale(.1,.1,.1);
    leftEye.matrix.translate(1.75,3,-3);
    leftEye.render();

    var rightEye = new Cube();
    rightEye.color = [1, 1, 0, 1];
    if (g_normalOn) rightEye.textureNum=2;
    rightEye.matrix.scale(.1,.1,.1);
    rightEye.matrix.translate(-2.5,3,-3);
    rightEye.render();

    var mouth = new Cube();
    mouth.color = [1, 1, 0, 1];
    if (g_normalOn) mouth.textureNum=2;
    mouth.matrix.scale(.5,.05,.5);
    mouth.matrix.translate(-.5,3,-1);
    mouth.render();

    var rightArm = new Cube();
    rightArm.color = [0, 0, .8, 1];
    if (g_normalOn) rightArm.textureNum=2;
    rightArm.matrix.rotate(g_arm, 0, 1, 0);
    rightArm.matrix.rotate(45,0,0);
    rightArm.matrix.scale(.25,.5,.25);
    rightArm.matrix.translate(1.3,-.9,-.5);
    rightArm.normalMatrix.setInverseOf(rightArm.matrix).transpose();
    rightArm.render();

    var leftArm = new Cube();
    leftArm.color = [0, 0, .8, 1];
    if (g_normalOn) leftArm.textureNum=2;
    leftArm.matrix.rotate(g_arm, 0, 1, 0);
    leftArm.matrix.rotate(-45,0,0);
    leftArm.matrix.scale(.25, .5, .25);
    leftArm.matrix.translate(-2.3, -.9, -.5);
    leftArm.normalMatrix.setInverseOf(leftArm.matrix).transpose();
    leftArm.render();

    var rightThigh = new Cube();
    rightThigh.color = [0, 0, .8, 1];
    if (g_normalOn) rightThigh.textureNum=2;
    rightThigh.matrix.rotate(g_thighAngle, 1, 0, 0);
    var rightThighMat = new Matrix4(rightThigh.matrix);
    rightThigh.matrix.scale(.15, .4, .15);
    rightThigh.matrix.translate(1,-.8,-.5001);
    rightThigh.normalMatrix.setInverseOf(rightThigh.matrix).transpose();
    rightThigh.render();

    var rightShin = new Cube();
    rightShin.color = [0, 0, .8, 1];
    if (g_normalOn) rightShin.textureNum=2;
    rightShin.matrix = rightThighMat;
    rightShin.matrix.translate(0.0001, -.26, 0);
    rightShin.matrix.rotate(g_shinAngle, 1, 0, 0);
    var rightShinMat = new Matrix4(rightShin.matrix);
    rightShin.matrix.scale(.15, .4, -.15);
    rightShin.matrix.translate(1,0,-.5);
    rightShin.normalMatrix.setInverseOf(rightShin.matrix).transpose();
    rightShin.render();

    var rightFoot = new Cube();
    rightFoot.color = [0, 0, .8, 1];
    if (g_normalOn) rightFoot.textureNum=2;
    rightFoot.matrix = rightShinMat;
    rightFoot.matrix.translate(0.0001, .4, 0);
    rightFoot.matrix.rotate(g_footAngle, 1, 0, 0);
    rightFoot.matrix.scale(.15, -.1, -.3);
    rightFoot.matrix.translate(1.000001,-.2,-.8);
    rightFoot.normalMatrix.setInverseOf(rightFoot.matrix).transpose();
    rightFoot.render();

    var leftThigh = new Cube();
    leftThigh.color = [0, 0, .8, 1];
    if (g_normalOn) leftThigh.textureNum=2;
    leftThigh.matrix.rotate(g_thighAngle2, 1, 0, 0);
    var leftThighMat = new Matrix4(leftThigh.matrix);
    leftThigh.matrix.scale(.15, .4, .15);
    leftThigh.matrix.translate(-2,-.8,-.5001);
    leftThigh.normalMatrix.setInverseOf(leftThigh.matrix).transpose();
    leftThigh.render();

    var leftShin = new Cube();
    leftShin.color = [0, 0, .8, 1];
    if (g_normalOn) leftShin.textureNum=2;
    leftShin.matrix = leftThighMat;
    leftShin.matrix.translate(0.0001, -.26, 0);
    leftShin.matrix.rotate(g_shinAngle2, 1, 0, 0);
    var leftShinMat = new Matrix4(leftShin.matrix);
    leftShin.matrix.scale(.15, .4, -.15);
    leftShin.matrix.translate(-2,0,-.5);
    leftShin.normalMatrix.setInverseOf(leftShin.matrix).transpose();
    leftShin.render();

    var leftFoot = new Cube();
    leftFoot.color = [0, 0, .8, 1];
    if (g_normalOn) leftFoot.textureNum=2;
    leftFoot.matrix = leftShinMat;
    leftFoot.matrix.translate(0.0001, .4, 0);
    leftFoot.matrix.rotate(g_footAngle2, 1, 0, 0);
    leftFoot.matrix.scale(.15, -.1, -.3);
    leftFoot.matrix.translate(-2, -.2 ,-.8);
    leftFoot.normalMatrix.setInverseOf(leftFoot.matrix).transpose();
    leftFoot.render();

    // var len = g_shapeList.length;

    // for(var i = 0; i < len; i++) {

    //     g_shapeList[i].render();
    //     if (i!=0){

    //         var rgba = g_shapeList[i].color;
    //         var size = g_shapeList[i].size;

    //         var vertices = ([g_shapeList[i-1].position[0], g_shapeList[i-1].position[1], g_shapeList[i].position[0], g_shapeList[i].position[1]]);

    //         gl.uniform4f(u_FragColor, rgba[0], rgba[1], rgba[2], rgba[3]);
        
    //         gl.uniform1f(u_Size, size)

    //         var vertexBuffer = gl.createBuffer();
    //         if (!vertexBuffer) {
    //          console.log('Failed to create the buffer object');
    //              return -1;
    //         }
    
    //         // Bind the buffer object to target
    //         gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
    //         // Write date into the buffer object
    //         gl.bufferData(gl.ARRAY_BUFFER,  new Float32Array(vertices), gl.DYNAMIC_DRAW);
    //         // Assign the buffer object to a_Position variable
    //         gl.vertexAttribPointer(a_Position, 2, gl.FLOAT, false, 0, 0);
    
    //         // Enable the assignment to a_Position variable
    //         gl.enableVertexAttribArray(a_Position);
    
    //         gl.drawArrays(gl.LINES, 0, 2);
    //     }
    // }
}