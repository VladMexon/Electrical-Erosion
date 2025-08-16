include <config.scad>

module joint1(){
    translate([-81.2797, 0, -100.512])
    scale(100)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_011.stl");
}

module joint2(){
    rotate([-90,0,0])
    translate([-87, 0, -258.848])
    scale(100)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_003.stl");
}

module joint3(){
    rotate([-90,0,0])
    translate([-12.0411, 0, -378.626])
    scale(100)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_004.stl");
}

module joint4(){
    rotate([-90,0,0])
    translate([-61, 0, -482])
    scale(100)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_005.stl");
}

module joint5(){
    rotate([0,-90,0])
    translate([-169.858, 0, -489.217])
    scale(100)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_002.stl");
}

module joint6(){
    rotate([-90,0,0])
    // Original: translate([-28.7982, 0, -48.7925])
    translate([-287.982, 0, -487.925])
    scale(100)
    color("blue")
        import("../3DModel/STL/manipulator-phobosCylinder_009.stl");
}

module joint7(){
    rotate([0,-180,0])
    // Original: translate([-39.1173, 0, -19.7])
    translate([-391.173, 0, -197])
    scale(100)
    color("black")
        import("../3DModel/STL/manipulator-phobosCylinder_001.stl");
}
module myrotate(a, orig) {
  //translate([0,0,100])
  translate(orig)
  rotate(a)
  children();
}
translate([250,-5,300])import("test1.stl");
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
$vpt = [550, -450, 600];
// Set camera orientation (roll, pitch, yaw)
$vpr = [62, 0, 35];
// Set camera distance
$vpd = 1000;
color("goldenrod")
scale(100) translate([-5,-5,0]) cube([15,10,1]);//platform
//color("firebrick")
//scale(1000) translate([0,0, 0.15]) cylinder(0.1, 0.14, 0.14, center=true, $fn=25);//base
color("firebrick")
scale(1000) translate([0.2,-0.15,0.1]) cube([0.3,0.3,0.2]);//table 200/-150/300
difference(){
    color("gray")
    translate([260,-65,300]) cube([100,50,1]);
    for(i = cuts)
    translate(i) cylinder(depth, radius, radius, $fn=10);
}