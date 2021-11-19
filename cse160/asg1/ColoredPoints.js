// ColoredPoint.js (c) 2012 matsuda
// Vertex shader program
var VSHADER_SOURCE = `
attribute vec4 a_Position;
uniform float u_Size;
void main() {
  gl_Position = a_Position;
  gl_PointSize = u_Size;
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

const POINT = 0;
const TRIANGLE = 1;
const CIRCLE = 2;

let g_selectedColor = [1, 1, 1, 1];
let g_selectedSize = 5;
let g_selectedType = POINT;
let g_selectedSeg = 6;

function setupWebGL() {
    // Retrieve <canvas> element
    canvas = document.getElementById('webgl');
    // Get the rendering context for WebGL
    gl = canvas.getContext('webgl', { preserveDrawingBuffer: true});

    if (!gl) {
        console.log('Failed to get the rendering context for WebGL');
        return;
    }
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

    u_Size = gl.getUniformLocation(gl.program, 'u_Size');
    if (!u_Size) {
        console.log('Failed to get the storage location of u_Size');
        return;
    }
}



function addActionsForHtmlUI() {

    document.getElementById('clearButton').onclick = function() {g_shapeList=[]; renderAllShapes();};

    document.getElementById('pointButton').onclick = function() {g_selectedType=POINT};
    document.getElementById('triangleButton').onclick = function() {g_selectedType=TRIANGLE};
    document.getElementById('circleButton').onclick = function() {g_selectedType=CIRCLE};

    document.getElementById('redSlide').addEventListener('mouseup', function() { g_selectedColor[0] = this.value/100; });
    document.getElementById('greenSlide').addEventListener('mouseup', function() { g_selectedColor[1] = this.value/100; });
    document.getElementById('blueSlide').addEventListener('mouseup', function() { g_selectedColor[2] = this.value/100; });

    document.getElementById('sizeSlide').addEventListener('mouseup', function() { g_selectedSize = this.value; });
    document.getElementById('segSlide').addEventListener('mouseup', function() { g_selectedSeg = this.value; });
    document.getElementById('alpSlide').addEventListener('mouseup', function() { g_selectedColor[3] = this.value/100; });


}

function main() {
    setupWebGL();
    connectVariablesToGLSL();

    addActionsForHtmlUI();


    // Register function (event handler) to be called on a mouse press
    canvas.onmousedown = click;

    canvas.onmousemove = function(ev) { if(ev.buttons == 1){ click(ev)}};

    // Specify the color for clearing <canvas>
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    // Clear <canvas>
    gl.clear(gl.COLOR_BUFFER_BIT);
}



var g_shapeList = [];

//var g_points = [];  // The array for the position of a mouse press
//var g_colors = [];  // The array to store the color of a point
//var g_sizes =  [];

function click(ev) {

    let [x,y] = convertCoordinatesEventToGL(ev);

    let point;
    if (g_selectedType==POINT){
        point = new Point();
    }
    else if (g_selectedType==TRIANGLE){
        point = new Triangle();
    }
    else{
        point = new Circle();
        point.segments = g_selectedSeg;
    }
    point.position=[x,y];
    point.color=g_selectedColor.slice();
    point.size=g_selectedSize;
    g_shapeList.push(point);
    
    // Store the coordinates to g_points array
    //g_points.push([x, y]);

    //g_colors.push(g_selectedColor.slice());

    //g_sizes.push(g_selectedSize);
    // Store the coordinates to g_points array
    //if (x >= 0.0 && y >= 0.0) {      // First quadrant
    //    g_colors.push([1.0, 0.0, 0.0, 1.0]);  // Red
    //} else if (x < 0.0 && y < 0.0) { // Third quadrant
    //    g_colors.push([0.0, 1.0, 0.0, 1.0]);  // Green
    //} else {                         // Others
    //    g_colors.push([1.0, 1.0, 1.0, 1.0]);  // White
    //}

    renderAllShapes();
}

function convertCoordinatesEventToGL(ev){
    var x = ev.clientX; // x coordinate of a mouse pointer
    var y = ev.clientY; // y coordinate of a mouse pointer
    var rect = ev.target.getBoundingClientRect();

    x = ((x - rect.left) - canvas.width/2)/(canvas.width/2);
    y = (canvas.height/2 - (y - rect.top))/(canvas.height/2);

    return ([x,y]);
}

function renderAllShapes(){
    // Clear <canvas>
    gl.clear(gl.COLOR_BUFFER_BIT);

    var len = g_shapeList.length;

    for(var i = 0; i < len; i++) {

        g_shapeList[i].render();
        if (i!=0){

            var rgba = g_shapeList[i].color;
            var size = g_shapeList[i].size;

            var vertices = ([g_shapeList[i-1].position[0], g_shapeList[i-1].position[1], g_shapeList[i].position[0], g_shapeList[i].position[1]]);

            gl.uniform4f(u_FragColor, rgba[0], rgba[1], rgba[2], rgba[3]);
        
            gl.uniform1f(u_Size, size)

            var vertexBuffer = gl.createBuffer();
            if (!vertexBuffer) {
             console.log('Failed to create the buffer object');
                 return -1;
            }
    
            // Bind the buffer object to target
            gl.bindBuffer(gl.ARRAY_BUFFER, vertexBuffer);
            // Write date into the buffer object
            gl.bufferData(gl.ARRAY_BUFFER,  new Float32Array(vertices), gl.DYNAMIC_DRAW);
            // Assign the buffer object to a_Position variable
            gl.vertexAttribPointer(a_Position, 2, gl.FLOAT, false, 0, 0);
    
            // Enable the assignment to a_Position variable
            gl.enableVertexAttribArray(a_Position);
    
            gl.drawArrays(gl.LINES, 0, 2);
        }
    }
}