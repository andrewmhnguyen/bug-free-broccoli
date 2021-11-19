'use strict';

// DrawRectangle.js
function main() {
    // Retrieve <canvas> element <- (1)

    var canvas = document.getElementById('example');
    if (!canvas) {
        console.log('Failed to retrieve the <canvas> element');
        return;
    }
 
    // Get the rendering context for 2DCG <- (2)
    var ctx = canvas.getContext('2d');

    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, 400, 400); // Fill a rectangle with the color

    var v1 = new Vector3([2.25, 2.25, 0.0]);

    drawVector(v1, "red");

    document.getElementById("draw").onclick = handleDrawEvent
    document.getElementById("draw2").onclick = handleDrawOperationEvent

    function drawVector(v, color) {
        ctx.strokeStyle = color;
        ctx.beginPath();
        ctx.moveTo(200, 200);
        ctx.lineTo(v.elements[0]*20+200, -v.elements[1]*20+200);
        ctx.stroke();
    }

    function handleDrawEvent() {
        ctx.clearRect(0, 0, 400, 400);
        ctx.fillRect(0, 0, 400, 400);
        var x = document.getElementById("x-coord").value;
        var y = document.getElementById("y-coord").value;
        var v1 = new Vector3([x, y, 0]);
        drawVector(v1, "red");
        var x2 = document.getElementById("x-coord2").value;
        var y2 = document.getElementById("y-coord2").value;
        var v2 = new Vector3([x2, y2, 0]);
        drawVector(v2, "blue");
    }

    function angleBetween(v1,v2) {
        var dotp = Vector3.dot(v1, v2);
        var mag1 = v1.magnitude();
        var mag2 = v2.magnitude();
        var dotp = dotp/(mag1 * mag2);
        var angle = Math.acos(dotp);
        return angle;
    }

    function areaTriangle(v1,v2) {
        var tri = Vector3.cross(v1,v2);
        var area = tri.elements[2]/2;
        return area;
    }

    function handleDrawOperationEvent() {
        ctx.clearRect(0, 0, 400, 400);
        ctx.fillRect(0, 0, 400, 400);
        var x = document.getElementById("x-coord").value;
        var y = document.getElementById("y-coord").value;
        var v1 = new Vector3([x, y, 0]);
        drawVector(v1, "red");
        var x2 = document.getElementById("x-coord2").value;
        var y2 = document.getElementById("y-coord2").value;
        var v2 = new Vector3([x2, y2, 0]);
        drawVector(v2, "blue");
        var val = document.getElementById("operation").value;
        var scalar = document.getElementById("scalar").value;
        if (val == "add") {
            var v3 = v1.add(v2);
            drawVector(v3, "green");
        }
        else if (val == "sub") {
            var v3 = v1.sub(v2);
            drawVector(v3, "green");
        }
        else if (val == "mul") {
            var v3 = v1.mul(scalar);
            var v4 = v2.mul(scalar);
            drawVector(v3, "green");
            drawVector(v4, "green");
        }
        else if (val == "div") {
            var v3 = v1.div(scalar);
            var v4 = v2.div(scalar);
            drawVector(v3, "green");
            drawVector(v4, "green");
        }
        else if (val == "mag") {
            var mag1 = v1.magnitude();
            var mag2 = v2.magnitude();
            console.log("Magnitude v1: " + mag1);
            console.log("Magnitude v2: " + mag2);
        }
        else if (val == "nor") {
            var v3 = v1.normalize();
            var v4 = v2.normalize();
            drawVector(v3, "green");
            drawVector(v4, "green");
        }
        else if (val == "ang") {
            var angle = angleBetween(v1, v2);
            angle = angle*180/Math.PI;
            console.log("Angle: " + angle);
        }
        else if (val == "are") {
            var area = areaTriangle(v1, v2);
            console.log("Area of the triangle: " + Math.abs(area));
        }
        
    }
    
} 

