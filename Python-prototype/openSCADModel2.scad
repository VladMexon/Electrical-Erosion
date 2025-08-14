include <config.scad>
module joint1(){
    translate([-0.0812797, 0, -0.100512 ])
    scale(0.1)
    color("blue")
           import("../3DModel/STL/manipulator-phobosCylinder_011.stl");
}
module joint2(){
    rotate([-90,0,0])
    translate([-0.087, 0, -0.258848])
    scale(0.1)
    color("blue")
           import("../3DModel/STL/manipulator-phobosCylinder_003.stl");
}
module joint3(){
    
    rotate([-90,0,0])
    translate([-0.0120411, 0, -0.378626])
    scale(0.1)
    color("blue")
           import("../3DModel/STL/manipulator-phobosCylinder_004.stl");
}
module joint4(){
    rotate([-90,0,0])
    translate([-0.061, 0, -0.482])
    scale(0.1)
    color("blue")
           import("../3DModel/STL/manipulator-phobosCylinder_005.stl");
}
module joint5(){
    rotate([0,-90,0])
    translate([-0.169858, 0, -0.489217])
    scale(0.1)
    color("blue")
           import("../3DModel/STL/manipulator-phobosCylinder_002.stl");
}
module joint6(){
    rotate([-90,0,0])
    translate([-0.287982, 0, -0.487925])
    scale(0.1)
    color("blue")
           import("../3DModel/STL/manipulator-phobosCylinder_009.stl");
}
module joint7(){
    rotate([0,-180,0])
    translate([-0.391173, 0, -0.197])
    scale(0.1)
    color("black")
           import("../3DModel/STL/manipulator-phobosCylinder_001.stl");
}
module myrotate(a, orig) {
  translate([0,0,0.1])
  translate(orig)
  rotate(a)
  children();
}
myrotate(rot1, pos1) {
  joint1();
}
myrotate(rot2, pos2) {
  joint2();
}
myrotate(rot3, pos3) {
  joint3();
}
myrotate(rot4, pos4) {
  joint4();
}
myrotate(rot5, pos5) {
  joint5();
}
myrotate(rot6, pos6) {
  joint6();
}
myrotate(rot7, pos7) {
  joint7();
}
// Set camera position (x, y, z)
$vpt = [3, 0, 3];
// Set camera orientation (roll, pitch, yaw)
$vpr = [45, 0, 45];
// Set camera distance
$vpd = 4;
//color("goldenrod")
//scale(0.1,0.1,0.1) translate([-5,-5,0]) cube([15,10,1]);//platform
color("firebrick")
translate([0,0, 0.15]) cylinder(0.1, 0.14, 0.14, center=true, $fn=25);//base
color("firebrick")
translate([0.2,-0.15,0.1]) cube([0.3,0.3,0.2]);//table
difference(){
    color("gray")
    translate([3,-0.5,3]) scale(0.1,0.1,0.1) cube([0.2,1,0.15]);
    for(i = cuts)
    translate(i) sphere(0.02, $fn=20);
}