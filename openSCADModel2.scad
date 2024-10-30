include <config.scad>
import("3DModel/STL/manipulator-phobosCylinder.stl");
module joint1(){
    translate([-0.812797, 0, -1.00512 ])
           import("3DModel/STL/manipulator-phobosCylinder_011.stl");
}
module joint2(){
    rotate([-90,0,0])
    translate([-0.87, 0, -2.58848])
           import("3DModel/STL/manipulator-phobosCylinder_003.stl");
}
module joint3(){
    rotate([-90,0,0])
    translate([-0.120411, 0, -3.78626])
           import("3DModel/STL/manipulator-phobosCylinder_004.stl");
}
module joint4(){
    rotate([-90,0,0])
    translate([-0.61, 0, -4.82])
           import("3DModel/STL/manipulator-phobosCylinder_005.stl");
}
module joint5(){
    rotate([0,-90,0])
    translate([-1.69858, 0, -4.89217])
           import("3DModel/STL/manipulator-phobosCylinder_002.stl");
}
module joint6(){
    rotate([-90,0,0])
    translate([-2.87982, 0, -4.87925])
           import("3DModel/STL/manipulator-phobosCylinder_009.stl");
}
module joint7(){
    rotate([0,-180,0])
    translate([-3.91173, 0, -1.97])
           import("3DModel/STL/manipulator-phobosCylinder_001.stl");
}
module myrotate(a, orig) {
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
