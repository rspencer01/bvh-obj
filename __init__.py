# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# Script copyright (C) Robert Spencer

bl_info = {
    "name":         "BVH+OBJ Object Format",
    "author":       "Robert Spencer",
    "blender":      (2,6,2),
    "version":      (0,0,1),
    "location":     "File > Import-Export",
    "description":  "Export PMIII Object Fomat",
    "category":     "Import-Export"
}
        
import bpy;
from bpy_extras.io_utils import ExportHelper


class Exporter(bpy.types.Operator, ExportHelper):
    bl_idname       = "untitled.bbj";
    bl_label        = "BVH+OBJ Format";
    bl_options      = {'PRESET'};
    
    filename_ext    = ".bvh+obj";

    def doBVH(self,context,filename):
        frame_start = context.scene.frame_start
        frame_end = context.scene.frame_end
        from . import export_bvh
        return export_bvh.save(self, context,filepath=filename, frame_start=frame_start,frame_end=frame_end)
      
    def execute(self, context):
        # Select the object.  BTW this needs to be the mesh, not the armature.  The armature is selected as the parent of the mesh
        bpy.ops.object.mode_set(mode='OBJECT');
        # We open the file, and write a header
        file = open(self.filepath, 'w');
        file.write("#BVH+OBJ File\n");
        file.close()
        # Now, we do the BVH part.  As this is heavily cribbed from the origional bvh code, 
        self.doBVH(context,self.filepath)
        # Reopen the file
        file = open(self.filepath, 'a');
        # Now, given the mesh data,
        mesh = context.object.data
        # For each vertex, write its position and vertex normal as per obj standards.  Just to keep things neat, we will have exactly
        # one vertex normal per vertex
        for vertex in mesh.vertices:
          file.write('v '+' '.join(map(str,[vertex.co.x,vertex.co.y,vertex.co.z]))+'\n')
          file.write('vn '+' '.join(map(str,[vertex.normal.x,vertex.normal.y,vertex.normal.z]))+'\n')
        # A helper function for texture less vertices of obj faces
        makeStandard = lambda f1: ' '.join(map(lambda x:x+'//'+x,map(str,f1)))
        # For each set of vertices (ie a polygon)
        for verts in mesh.polygons:
          # split up quads into two triangles
          if (len(verts.vertices)==4):
            f1 = verts.vertices[:3]
            f2 = [verts.vertices[0]]+list(verts.vertices[2:])
            file.write('f ' + makeStandard(f1)+'\n')
            file.write('f ' + makeStandard(f2)+'\n')
          # or just write the triangles
          else:
            file.write('f ' + makeStandard(verts.vertices)+'\n')
        # Create a dictionary of vertex groups
        vgroups = {}
        # For each vertex, find all the groups it belongs to
        for vertex in mesh.vertices:
          for group in vertex.groups:
            # Insert this group id into vgroups, if it is not there already
            if (group.group not in vgroups):
              vgroups[group.group] = []
            # Add this vertex to that group
            groupO = context.object.vertex_groups[group.group]
            weight = groupO.weight(vertex.index)
            # Then, if the weight is sufficient, add it
            if (weight>0.0001):
              vgroups[group.group].append((vertex.index,weight))
        # Now, for each group, print its name, the number of items in it and the nice formatted v_i/w_i
        for g in vgroups:
          file.write('vg '+context.object.vertex_groups[g].name+' '+str(len(vgroups[g]))+' '+' '.join(map(lambda x:"{0}/{1:.5f}".format(x[0],x[1]),vgroups[g]))+'\n')
        
        # Close the file
        file.close();
    
        return {"FINISHED"}; 


def menu_func(self, context):
    self.layout.operator(Exporter.bl_idname, text="BVH+OBJ Format(.bvh+obj)");

def register():
    bpy.utils.register_module(__name__);
    bpy.types.INFO_MT_file_export.append(menu_func);
    
def unregister():
    bpy.utils.unregister_module(__name__);
    bpy.types.INFO_MT_file_export.remove(menu_func);

if __name__ == "__main__":
    register() 
