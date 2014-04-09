
`bvh+obj` File Format Specification
=================================

"Because there aren't enough 3D file formats already"

Overview
--------

`bvh+obj` is a file format for describing characters and their animations.  As the name suggests, it relies heavily on the `bvh` and `obj` file formats with a bit extra.

It was designed to fit a specific need in a specific problem, and thus is not universally aplicable.  Don't use it if you don't want to.

I am not the best person to be writing Blender scripts (not being a graphic designer at all), and so it is probable that my script is horrible and doesn't work in many cases.  If you edit it, please submit a pull request.

File Format 
-----------

The file is split into two parts: the `bvh` section and the `obj` section.  Each is slightly modified however.  

 * **Modifications to the `bvh` section**

In the `bvh` section a line will follow the `MOTION` line of the form
    
    Action Count: NUMBER_OF_ACTIONS

where `NUMBER_OF_ACTIONS` is the number of motion blocks to follow.  Each follows the same format as the usual `bvh` (a string of space separated values for the parameters detailed in the `HIERACHY` section, with the addition of a line

    Name: ACTION_NAME

before the frame count.  This name is arbitrary.

 * **Modifications to the `obj`section**

The major change in the `obj` section is a new command.  It is of the form

    vg BONE_NAME COUNT V_1/W_1 V_2/W_2 ... V_COUNT/W_COUNT

where `BONE_NAME` is the name of some joint defined in the `bvh` section, `COUNT` is the number of succeding pairs, and each of the `V_i/W_i` represent a vertex and its weight to that joint.

The weights should be complete, ie the sum of all the weights associated with some vertex should be very close to 1.

Things To Do
------------
 
 * Check the exporter extensively
 * Write an importer 