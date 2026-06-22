# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "CSVToMeshAuto",
    "author" : "Auto-detect fork",
    "description" : "将 RenderDoc 导出的 CSV 文件转换为网格（自动检测 UV 列）",
    "blender" : (2, 80, 0),
    "version" : (1, 0, 1),
    "location" : "View3D > Tool > CSVToMeshAuto",
    "warning" : "",
    "category" : "Add Mesh"
}
import bpy
from bpy.types import Context
from bpy.types import Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ImportHelper

import csv
import os


def detect_uv_index(filepath):
    """Scan CSV header to find UV-related columns, skipping position columns
    (index 2,3,4 which are hardcoded as vertex positions). Returns the index
    of the first matching column, or None if not found."""
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
    for i, col in enumerate(header):
        if i <= 4:
            continue
        col_lower = col.lower().strip()
        # Match TEXCOORD*.x / TEXCOORD*.u or uv*.x / uv*.u patterns
        if 'texcoord' in col_lower or col_lower.startswith('uv'):
            return i
    return None


def CreateMesh(data,uvindex,name):
    minId=65535
    maxId=0
    
    count=len(data)
    triangleCount=count/3

    for i in range(count):
        minId=min(minId,int(data[i][1]))
        maxId=max(maxId,int(data[i][1]))
    vertexCount=maxId-minId+1
    vertices=[(0,0,0) for _ in range(vertexCount)]
    uv_data=[(0,0) for _ in range(vertexCount)]
    triangles=[]
    
    k=0
    n=0
    while k<count:
        tri=[0,0,0]
        for i in range(3):
            IDX=int(data[k+i][1])
            realIDX=IDX-minId
            tri[i]=realIDX
            vertex=(float(data[k+i][2]),float(data[k+i][3]),float(data[k+i][4]))
            uv=(float(data[k+i][uvindex]),float(data[k+i][uvindex+1]))
            vertices[realIDX]=vertex
            uv_data[realIDX]=uv
        triangles.append((tri[0],tri[1],tri[2]))
        k=k+3
        n=n+1

    mesh_data=bpy.data.meshes.new(name)
    mesh_data.from_pydata(vertices,[],triangles)
    mesh_data.update()

    print("uv_layers",len(mesh_data.uv_layers))
    uv_layer=mesh_data.uv_layers.new()
    uv_layer.name="uv0"
    for loop in mesh_data.loops:
        uv_layer.data[loop.index].uv=uv_data[loop.vertex_index]
    
    
    return mesh_data


def readcsvfile(filepath):
    """Read CSV file, returning (header, data) tuple."""
    f=open(filepath,'r')
    reader=csv.reader(f)
    header=next(reader)
    l=[]
    for line in reader:
        l.append(line)
    return header,l

class CSVTOOL_Properties(bpy.types.PropertyGroup):
    auto_detect_uv: bpy.props.BoolProperty(
        name="自动检测 UV",
        default=True,
        description="根据 CSV 表头自动定位 UV 列（跳过位置列）"
    )
    uvindex: bpy.props.IntProperty(
        name="UV 起始列",
        default=13,
        description="UV 列的起始索引（关闭自动检测时生效）"
    )


class CSVTOOL_OT_import_csv(Operator,ImportHelper):
    bl_idname="csv_to_mesh_auto.import_csv"
    bl_label="导入 CSV"
    bl_options={'PRESET', 'UNDO'}

    filename_ext=".csv"
    filter_glob: StringProperty(default="*.csv",options={"HIDDEN"})


    def execute(self, context):
        print("import file: ",self.filepath)
        scene=bpy.context.scene
        
        header,data=readcsvfile(self.filepath)
        print("CSV header:", header)
        filename=os.path.basename(self.filepath)
        meshname=os.path.splitext(filename)[0]
        
        if scene.csv_to_mesh_auto_tool.auto_detect_uv:
            auto_uv=detect_uv_index(self.filepath)
            if auto_uv is not None:
                scene.csv_to_mesh_auto_tool.uvindex=auto_uv
                print(f"Auto-detected UV index: {auto_uv} (col: {header[auto_uv]})")
            else:
                print("Warning: Could not auto-detect UV index, using manual value")
        
        mesh_data=CreateMesh(data,scene.csv_to_mesh_auto_tool.uvindex,meshname)
        obj=bpy.data.objects.new(meshname,mesh_data)

        
        scene.collection.objects.link(obj)
        obj.select_set(True)
        bpy.context.view_layer.objects.active=obj

        return {"FINISHED"}

    

class CSVTOOL_PT_main(bpy.types.Panel):
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="CSVToMeshAuto"
    bl_label="CSV 转网格"
    def draw(self, context: Context):
        col=self.layout.column(align=True)
        scene=bpy.context.scene
        col.prop(scene.csv_to_mesh_auto_tool,"auto_detect_uv")
        col.prop(scene.csv_to_mesh_auto_tool,"uvindex")
        col=self.layout.column(align=True)
        props=col.operator("csv_to_mesh_auto.import_csv",text="导入 CSV",icon="WORDWRAP_ON")


classes=[CSVTOOL_OT_import_csv,CSVTOOL_PT_main,CSVTOOL_Properties]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.csv_to_mesh_auto_tool=bpy.props.PointerProperty(type=CSVTOOL_Properties)
    print("CSVToMeshAuto 已加载")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.csv_to_mesh_auto_tool
    print("CSVToMeshAuto 已卸载")

if __name__=='__main__':
    register()
