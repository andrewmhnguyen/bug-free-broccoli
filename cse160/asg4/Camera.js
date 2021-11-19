class Camera {

    constructor(){
        this.fov = 60;
        this.eye = new Vector3([0,0,-3]);
        this.at = new Vector3([0,0,0]);
        this.up = new Vector3([0,1,0]);
        this.viewMatrix = new Matrix4();
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
        this.projectionMatrix = new Matrix4();
        this.projectionMatrix.setPerspective(90, 1, 0.1, 1000);
    }

    moveForward(){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        f.normalize();
        this.eye.add(f);
        this.at.add(f);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    moveBackwards(){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        f.normalize();
        this.eye.sub(f);
        this.at.sub(f);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    moveLeft(){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        var s = Vector3.cross(this.up, f);
        s.normalize();
        this.eye.add(s);
        this.at.add(s);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    moveRight(){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        f.mul(-1);
        var s = Vector3.cross(this.up, f);
        s.normalize();
        this.eye.add(s);
        this.at.add(s);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    panLeft(){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        var rotationMatrix = new Matrix4();
        rotationMatrix.setRotate(5, this.up.elements[0], this.up.elements[1], this.up.elements[2]);
        var f_prime = new Vector3();
        f_prime = rotationMatrix.multiplyVector3(f);
        var eye2 = new Vector3();
        eye2.set(this.eye);
        this.at = eye2.add(f_prime);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    panRight(){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        var rotationMatrix = new Matrix4();
        rotationMatrix.setRotate(-5, this.up.elements[0], this.up.elements[1], this.up.elements[2]);
        var f_prime = new Vector3();
        f_prime = rotationMatrix.multiplyVector3(f);
        var eye2 = new Vector3();
        eye2.set(this.eye);
        this.at = eye2.add(f_prime);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    panLeftMouse(x){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        var rotationMatrix = new Matrix4();
        rotationMatrix.setRotate(1*Math.abs(x), this.up.elements[0], this.up.elements[1], this.up.elements[2]);
        var f_prime = new Vector3();
        f_prime = rotationMatrix.multiplyVector3(f);
        var eye2 = new Vector3();
        eye2.set(this.eye);
        this.at = eye2.add(f_prime);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }

    panRightMouse(x){
        var f = new Vector3();
        f = f.set(this.at);
        f.sub(this.eye);
        var rotationMatrix = new Matrix4();
        rotationMatrix.setRotate(-1*Math.abs(x), this.up.elements[0], this.up.elements[1], this.up.elements[2]);
        var f_prime = new Vector3();
        f_prime = rotationMatrix.multiplyVector3(f);
        var eye2 = new Vector3();
        eye2.set(this.eye);
        this.at = eye2.add(f_prime);
        this.viewMatrix.setLookAt(this.eye.elements[0], this.eye.elements[1], this.eye.elements[2], this.at.elements[0], this.at.elements[1], this.at.elements[2], this.up.elements[0], this.up.elements[1], this.up.elements[2]);
    }
}