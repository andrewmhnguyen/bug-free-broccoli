class Cube {
    constructor() {
        this.type = 'cube';
        // this.position = [0.0, 0.0, 0.0];
        this.color = [1.0, 1.0, 1.0, 1.0];
        // this.segments = 6;
        this.matrix = new Matrix4();
        this.normalMatrix = new Matrix4();
        this.textureNum=-2;
    }

    render() {
        //var xy = this.position;
        var rgba = this.color;
        //var size = this.size;
        //var segments = this.segments;
        gl.uniform1i(u_whichTexture, this.textureNum);
        // Pass the position of a point to a_Position variable
        //gl.vertexAttrib3f(a_Position, xy[0], xy[1], 0.0);
        // Pass the color of a point to u_FragColor variable
        gl.uniform4f(u_FragColor, rgba[0], rgba[1], rgba[2], rgba[3]);
        
        gl.uniformMatrix4fv(u_ModelMatrix, false, this.matrix.elements);
        gl.uniformMatrix4fv(u_NormalMatrix, false, this.normalMatrix.elements);
        // // Draw
        // var d = this.size/200.0;
        // let angleStep=360/segments;
        // for (var angle = 0; angle < 360; angle=angle+=angleStep){
        //     let centerPt = [xy[0], xy[1]];
        //     let angle1 = angle;
        //     let angle2 = angle+angleStep;
        //     let vec1=[Math.cos(angle1*Math.PI/180)*d, Math.sin(angle1*Math.PI/180)*d];
        //     let vec2=[Math.cos(angle2*Math.PI/180)*d, Math.sin(angle2*Math.PI/180)*d];
        //     let pt1 = [centerPt[0]+vec1[0], centerPt[1]+vec1[1]];
        //     let pt2 = [centerPt[0]+vec2[0], centerPt[1]+vec2[1]];

        //     drawTriangle( [xy[0], xy[1], pt1[0], pt1[1], pt2[0], pt2[1]]);

        // }
        
        //front side of cube
        drawTriangle3DUVNormal([0,0,0 , 1,1,0 , 1,0,0], [0,0, 1,1, 1,0], [0,0,-1, 0,0,-1, 0,0,-1]);
        drawTriangle3DUVNormal([0,0,0 , 0,1,0 , 1,1,0], [0,0, 0,1, 1,1], [0,0,-1, 0,0,-1, 0,0,-1]);

        // drawTriangle3D([0.0,0.0,0.0, 1.0,1.0,0.0, 1.0,0.0,0.0]);
        // drawTriangle3D([0.0,0.0,0.0, 0.0,1.0,0.0, 1.0,1.0,0.0]);

        //back side of the cube
        drawTriangle3DUVNormal([0,0,1 , 1,1,1 , 1,0,1], [1,0, 1,1, 0,1], [0,0,1, 0,0,1, 0,0,1]);
        drawTriangle3DUVNormal([0,0,1 , 0,1,1 , 1,1,1], [1,0, 0,1, 0,0], [0,0,1, 0,0,1, 0,0,1]);

        // drawTriangle3D([0,0,1, 0,1,1, 1,1,1]);
        // drawTriangle3D([0,0,1, 1,1,1, 1,0,1]);
        //gl.uniform4f(u_FragColor, rgba[0]*.7, rgba[1]*.7, rgba[2]*.7, rgba[3]);
        //left side of the cube
        drawTriangle3DUVNormal([0,0,0 , 0,1,0 , 0,1,1], [1,0, 1,1, 0,1], [-1,0,0, -1,0,0, -1,0,0]);
        drawTriangle3DUVNormal([0,0,0 , 0,1,1 , 0,0,1], [1,0, 0,1, 0,0], [-1,0,0, -1,0,0, -1,0,0]);

        // drawTriangle3D([0,0,0, 0,1,0, 0,1,1]);
        // drawTriangle3D([0,0,0, 0,1,1, 0,0,1]);

        //right side of the cube
        drawTriangle3DUVNormal([1,0,0 , 1,1,0 , 1,1,1], [0,0, 0,1, 1,1], [1,0,0, 1,0,0, 1,0,0]);
        drawTriangle3DUVNormal([1,0,0 , 1,1,1 , 1,0,1], [0,0, 1,1, 1,0], [1,0,0, 1,0,0, 1,0,0]);

        // drawTriangle3D([1,0,0, 1,1,0, 1,1,1]);
        // drawTriangle3D([1,0,0, 1,1,1, 1,0,1]);

        //gl.uniform4f(u_FragColor, rgba[0]*.8, rgba[1]*.8, rgba[2]*.8, rgba[3]);
        //top side of the cube 
        drawTriangle3DUVNormal([0,1,0 , 0,1,1 , 1,1,1], [0,0, 0,1, 1,1], [0,1,0, 0,1,0, 0,1,0]);
        drawTriangle3DUVNormal([0,1,0 , 1,1,1 , 1,1,0], [0,0, 1,1, 1,0], [0,1,0, 0,1,0, 0,1,0]);

        // drawTriangle3D([0,1,0, 0,1,1, 1,1,1]);
        // drawTriangle3D([0,1,0, 1,1,1, 1,1,0]);

        //bottom side of the cube
        drawTriangle3DUVNormal([0,0,0 , 0,0,1 , 1,0,1], [1,0, 1,1, 0,1], [0,-1,0, 0,-1,0, 0,-1,0]);
        drawTriangle3DUVNormal([0,0,0 , 1,0,1 , 1,0,0], [1,0, 0,1, 0,0], [0,-1,0, 0,-1,0, 0,-1,0]);

        // drawTriangle3D([0,0,0, 0,0,1, 1,0,1]);
        // drawTriangle3D([0,0,0, 1,0,1, 1,0,0]);
        
    }

    renderfast(){
        var rgba = this.color;

        gl.uniform1i(u_whichTexture, this.textureNum);
        // Pass the position of a point to a_Position variable
        //gl.vertexAttrib3f(a_Position, xy[0], xy[1], 0.0);
        // Pass the color of a point to u_FragColor variable
        gl.uniform4f(u_FragColor, rgba[0], rgba[1], rgba[2], rgba[3]);
        
        gl.uniformMatrix4fv(u_ModelMatrix, false, this.matrix.elements);

        var allverts = [];
        var allvertsUV = [];
        var allvertsNormal = [];
        allverts = allverts.concat([0,0,0 , 1,1,0 , 1,0,0]);
        allverts = allverts.concat([0,0,0 , 0,1,0 , 1,1,0]);
        allvertsUV = allvertsUV.concat([0,0, 1,1, 1,0]);
        allvertsUV = allvertsUV.concat([0,0, 0,1, 1,1]);

        allverts = allverts.concat([0,0,1 , 0,1,1 , 1,1,1]);
        allverts = allverts.concat([0,0,1 , 1,1,1 , 1,0,1]);
        allvertsUV = allvertsUV.concat([1,0, 1,1, 0,1]);
        allvertsUV = allvertsUV.concat([1,0, 0,1, 0,0]);

        allverts = allverts.concat([0,0,0 , 0,1,0 , 0,1,1]);
        allverts = allverts.concat([0,0,0 , 0,1,1 , 0,0,1]);
        allvertsUV = allvertsUV.concat([1,0, 1,1, 0,1]);
        allvertsUV = allvertsUV.concat([1,0, 0,1, 0,0]);

        allverts = allverts.concat([1,0,0 , 1,1,0 , 1,1,1]);
        allverts = allverts.concat([1,0,0 , 1,1,1 , 1,0,1]);
        allvertsUV = allvertsUV.concat([0,0, 0,1, 1,1]);
        allvertsUV = allvertsUV.concat([0,0, 1,1, 1,0]);

        allverts = allverts.concat([0,1,0 , 0,1,1 , 1,1,1]);
        allverts = allverts.concat([0,1,0 , 1,1,1 , 1,1,0]);
        allvertsUV = allvertsUV.concat([0,0, 0,1, 1,1]);
        allvertsUV = allvertsUV.concat([0,0, 1,1, 1,0]);

        allverts = allverts.concat([0,0,0 , 0,0,1 , 1,0,1]);
        allverts = allverts.concat([0,0,0 , 1,0,1 , 1,0,0]);
        allvertsUV = allvertsUV.concat([1,0, 1,1, 0,1]);
        allvertsUV = allvertsUV.concat([1,0, 0,1, 0,0]);

        drawTriangle3DUV(allverts, allvertsUV);
    }
}
