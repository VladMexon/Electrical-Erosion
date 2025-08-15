include <config.scad>

module joint1(){
    // Original: translate([-8.12797, 0, -10.0512 ])
    translate([-16.25594, 0, -20.1024])
    scale(20)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_011.stl");
}

module joint2(){
    rotate([-90,0,0])
    // Original: translate([-8.7, 0, -25.8848])
    translate([-17.4, 0, -51.7696])
    scale(20)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_003.stl");
}

module joint3(){
    rotate([-90,0,0])
    // Original: translate([-1.20411, 0, -37.8626])
    translate([-2.40822, 0, -75.7252])
    scale(20)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_004.stl");
}

module joint4(){
    rotate([-90,0,0])
    // Original: translate([-6.1, 0, -48.2])
    translate([-12.2, 0, -96.4])
    scale(20)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_005.stl");
}

module joint5(){
    rotate([0,-90,0])
    // Original: translate([-16.9858, 0, -48.9217])
    translate([-33.9716, 0, -97.8434])
    scale(20)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_002.stl");
}

module joint6(){
    rotate([-90,0,0])
    // Original: translate([-28.7982, 0, -48.7925])
    translate([-57.5964, 0, -97.585])
    scale(20)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_009.stl");
}

module joint7(){
    rotate([0,-180,0])
    // Original: translate([-39.1173, 0, -19.7])
    translate([-78.2346, 0, -39.4])
    scale(20)
    color("black")
        import("../3DModel/STL/manipulator-phobosCylinder_001.stl");
}
module myrotate(a, orig) {
  translate([0,0,20])
  translate(orig)
  rotate(a)
  children();
}
translate([50,-5,60])import("test1.stl");
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
$vpt = [200, -220, 220];
// Set camera orientation (roll, pitch, yaw)
$vpr = [62, 0, 35];
// Set camera distance
$vpd = 4;
color("goldenrod")
scale(20) translate([-5,-5,0]) cube([15,10,1]);//platform
color("firebrick")
scale(200) translate([0,0, 0.15]) cylinder(0.1, 0.14, 0.14, center=true, $fn=25);//base
color("firebrick")
scale(200) translate([0.2,-0.15,0.1]) cube([0.3,0.3,0.2]);//table 40/30/40
difference(){
    color("gray")
    translate([0.35,-0.05,0.3]) scale(0.1,0.1,0.1) cube([0.2,1,0.15]);
    for(i = cuts)
    translate(i) sphere(0.02, $fn=20);
}