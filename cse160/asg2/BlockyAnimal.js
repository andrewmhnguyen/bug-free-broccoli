// ColoredPoint.js (c) 2012 matsuda
// Vertex shader program
var VSHADER_SOURCE = `
attribute vec4 a_Position;
uniform mat4 u_ModelMatrix;
uniform mat4 u_GlobalRotateMatrix;
void main() {
  gl_Position = u_GlobalRotateMatrix * u_ModelMatrix * a_Position;
}`

// Fragment shader program
var FSHADER_SOURCE = `
precision mediump float;
uniform vec4 u_FragColor;
void main() {
  gl_FragColor = u_FragColor;
}`

//Global variables 
let canvas;
let gl;
let a_Position;
let u_FragColor;
let u_Size;
let u_ModelMatrix;
let u_GlobalRotateMatrix;

const POINT = 0;
const TRIANGLE = 1;
const CIRCLE = 2;

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

    u_GlobalRotateMatrix = gl.getUniformLocation(gl.program, 'u_GlobalRotateMatrix');
    if (!u_GlobalRotateMatrix) {
        console.log('Failed to get the storage location of u_GlobalRotateMatrix');
        return;
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


    document.getElementById('angleSlide').addEventListener('mousemove', function() { g_globalAngle = this.value; renderScene(); });
    document.getElementById('thighSlide').addEventListener('mousemove', function() { g_thighAngle = this.value; renderScene(); });
    document.getElementById('shinSlide').addEventListener('mousemove', function() { g_shinAngle = this.value; renderScene(); });
    document.getElementById('footSlide').addEventListener('mousemove', function() { g_footAngle = this.value; renderScene(); });

    document.getElementById('thighSlide2').addEventListener('mousemove', function() { g_thighAngle2 = this.value; renderScene(); });
    document.getElementById('shinSlide2').addEventListener('mousemove', function() { g_shinAngle2 = this.value; renderScene(); });
    document.getElementById('footSlide2').addEventListener('mousemove', function() { g_footAngle2 = this.value; renderScene(); });


}

function main() {
    setupWebGL();
    connectVariablesToGLSL();

    addActionsForHtmlUI();


    // Register function (event handler) to be called on a mouse press
    //canvas.onmousedown = click;

    //canvas.onmousemove = function(ev) { if(ev.buttons == 1){ click(ev)}};

    // Specify the color for clearing <canvas>
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    // Clear <canvas>
    //gl.clear(gl.COLOR_BUFFER_BIT);
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
    console.log(g_seconds);
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
    
    }
}


function renderScene(){

    var globalRotMat = new Matrix4().rotate(g_globalAngle, 0, 1, 0);
    gl.uniformMatrix4fv(u_GlobalRotateMatrix, false, globalRotMat.elements);

    // Clear <canvas>
    // gl.clear(gl.COLOR_BUFFER_BIT);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    var body = new Cube();
    body.color = [0, 0, .8, .8];
    body.matrix.scale(.75,.5,.5);
    body.matrix.translate(-.5,0,-.5);
    body.render();

    var tail = new Cube();
    tail.color = [0,0,.5,.4];
    tail.matrix.rotate(g_tail, 0, 1, 0);
    tail.matrix.scale(.125,.125,.5);
    tail.matrix.translate(-.5,0,.5);
    tail.render();

    var leftEye = new Cube();
    leftEye.color = [1, 1, 0, 1];
    leftEye.matrix.scale(.1,.1,.1);
    leftEye.matrix.translate(1.75,3,-3);
    leftEye.render();

    var rightEye = new Cube();
    rightEye.color = [1, 1, 0, 1];
    rightEye.matrix.scale(.1,.1,.1);
    rightEye.matrix.translate(-2.5,3,-3);
    rightEye.render();

    var mouth = new Cube();
    mouth.color = [1, 1, 0, 1];
    mouth.matrix.scale(.5,.05,.5);
    mouth.matrix.translate(-.5,3,-1);
    mouth.render();

    var rightArm = new Cube();
    rightArm.color = [0, .1, .5, .5];
    rightArm.matrix.rotate(g_arm, 0, 1, 0);
    rightArm.matrix.rotate(45,0,0);
    rightArm.matrix.scale(.25,.5,.25);
    rightArm.matrix.translate(1.3,-.9,-.5);
    rightArm.render();

    var leftArm = new Cube();
    leftArm.color = [0, .1, .5, .5];
    leftArm.matrix.rotate(g_arm, 0, 1, 0);
    leftArm.matrix.rotate(-45,0,0);
    leftArm.matrix.scale(.25, .5, .25);
    leftArm.matrix.translate(-2.3, -.9, -.5);
    leftArm.render();



    var rightThigh = new Cube();
    rightThigh.color = [0, 0, 1, .7];
    rightThigh.matrix.rotate(g_thighAngle, 1, 0, 0);
    var rightThighMat = new Matrix4(rightThigh.matrix);
    rightThigh.matrix.scale(.15, .4, .15);
    rightThigh.matrix.translate(1,-.8,-.5001);
    rightThigh.render();

    var rightShin = new Cube();
    rightShin.color = [0, 0, 1, .4];
    rightShin.matrix = rightThighMat;
    rightShin.matrix.translate(0.0001, -.26, 0);
    rightShin.matrix.rotate(g_shinAngle, 1, 0, 0);
    var rightShinMat = new Matrix4(rightShin.matrix);
    rightShin.matrix.scale(.15, .4, .15);
    rightShin.matrix.translate(1,0,-.5);
    rightShin.render();

    var rightFoot = new Cube();
    rightFoot.color = [0, 0, 1, .2];
    rightFoot.matrix = rightShinMat;
    rightFoot.matrix.translate(0.0001, .4, 0);
    rightFoot.matrix.rotate(g_footAngle, 1, 0, 0);
    rightFoot.matrix.scale(.15, .1, .3);
    rightFoot.matrix.translate(1.000001,-.2,-.2);
    rightFoot.render();

    var leftThigh = new Cube();
    leftThigh.color = [0, 0, 1, .7];
    leftThigh.matrix.rotate(g_thighAngle2, 1, 0, 0);
    var leftThighMat = new Matrix4(leftThigh.matrix);
    leftThigh.matrix.scale(.15, .4, .15);
    leftThigh.matrix.translate(-2,-.8,-.5001);
    leftThigh.render();

    var leftShin = new Cube();
    leftShin.color = [0, 0, 1, .4];
    leftShin.matrix = leftThighMat;
    leftShin.matrix.translate(0.0001, -.26, 0);
    leftShin.matrix.rotate(g_shinAngle2, 1, 0, 0);
    var leftShinMat = new Matrix4(leftShin.matrix);
    leftShin.matrix.scale(.15, .4, .15);
    leftShin.matrix.translate(-2,0,-.5);
    leftShin.render();

    var leftFoot = new Cube();
    leftFoot.color = [0, 0, 1, .2];
    leftFoot.matrix = leftShinMat;
    leftFoot.matrix.translate(0.0001, .4, 0);
    leftFoot.matrix.rotate(g_footAngle2, 1, 0, 0);
    leftFoot.matrix.scale(.15, .1, .3);
    leftFoot.matrix.translate(-2, -.2 ,-.2);
    leftFoot.render();

    


    var rightArm2 = new Cube();

    var leftArm2 = new Cube();


    


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