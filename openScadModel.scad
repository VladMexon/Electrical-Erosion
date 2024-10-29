import("C:/STL_OPENSCAD/manipulatorCylinder.stl");


module joint9(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
            import("C:/STL_OPENSCAD/manipulatorCylinder.001.stl");
        }
    }
}
module joint8(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.009.stl");
        }
    }
}
module joint7(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorPlane.stl");
        }
    }
}
module joint6(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.007.stl");
        }
    }        
}
    
module joint5(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.002.stl");
        }
    }
}
module joint4(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.005.stl");
        }
    }
}
module joint3(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.004.stl");
        }
    }
}
module joint2(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.003.stl");
        }
    }
}
module joint1(rx, ry, rz, tx, ty, tz){
    rotate([rx,ry,rz]){
        translate([tx, ty,tz]){
           import("C:/STL_OPENSCAD/manipulatorCylinder.011.stl");
        }
    }
}

module draw(rx, ry, rz, tx, ty, tz){
     joint1(rx, ry, rz, tx, ty, tz);
     joint2(rx, ry, rz, tx, ty, tz);
     joint3(rx, ry, rz, tx, ty, tz);
     joint4(rx, ry, rz, tx, ty, tz);
     joint5(rx, ry, rz, tx, ty, tz);
     joint6(rx, ry, rz, tx, ty, tz);
     joint7(rx, ry, rz, tx, ty, tz);
     joint8(rx, ry, rz, tx, ty, tz);
     joint9(rx, ry, rz, tx, ty, tz); 
}
draw(0,0,90,0,0,0);
