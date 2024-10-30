import("C:/STL2/manipulator-phobosCylinder.stl");

module joint1(){
    translate([-0.812797, 0, -1.00512 ])
           import("C:/STL2/manipulator-phobosCylinder_011.stl");
}
module joint2(){
    rotate([-90,0,0])
    translate([-0.87, 0, -2.58848])
           import("C:/STL2/manipulator-phobosCylinder_003.stl");
}
module joint3(){
    rotate([-90,0,0])
    translate([0, 0, -3.78626])
           import("C:/STL2/manipulator-phobosCylinder_004.stl");
}
module joint4(){
    rotate([-90,0,0])
    translate([-0.61, 0, -4.82])
           import("C:/STL2/manipulator-phobosCylinder_005.stl");
}
module joint5(){
    rotate([0,-90,0])
    translate([-1.69858, 0, -4.89217])
           import("C:/STL2/manipulator-phobosCylinder_002.stl");
}
module joint6(){
    rotate([-90,0,0])
    translate([-2.87982, 0, -4.87925])
           import("C:/STL2/manipulator-phobosCylinder_009.stl");
}
module joint7(){
    rotate([0,180,0])
    translate([-3.91173, 0, -2.56752])
           import("C:/STL2/manipulator-phobosCylinder_001.stl");
}


module myrotate(a, orig) {
  translate(orig)
  rotate([a[0],a[1], a[2]])
    
  children();
}
//module myrotate1(a, orig) {
//  translate(orig)
//  rotate([a[0],a[1], a[2]])
//  children();
//}
//module myrotate5(a, orig) {
//  translate(orig)
//  rotate([a[0]+30,a[1]-85, a[2]+43])
//  children();
//}
//module myrotate7(a, orig) {
//  translate(orig)
//  rotate([a[0],a[1]+90, a[2]])
//  children();
//}
myrotate([0,0,-19], [0.8128,0,1.00512 ]) {
  joint1();
}
myrotate([90, -24.52792448, -18.0415467], [0.86718763,0,2.58848]) {
  joint2();
}
myrotate([90,-26.84916641,-18.0415572], [-0.25390281,0.34784277,3.36697979]) {
  joint3();
}
myrotate([90,-12.07797207,-18.0414957], [-0.28261668,0.35678086, 4.51040121]) {
  joint4();
}
myrotate([-42,73,-61], [0.71529039,0.03215188,4.80875098]) {
  joint5();
}
myrotate([79,11,-23], [1.81523657,-0.32905807,5.04357174]) {
  joint6();
}
myrotate([-170,-12,157], [2,-1,2]) {
  joint7();
}