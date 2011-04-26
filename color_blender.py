import bpy
from bpy.props import *

class mmProps(bpy.types.PropertyGroup):
    enabled = bpy.props.IntProperty(default=0)
    
    # Material custom Properties properties
    mmColors = bpy.props.EnumProperty(
        name="Colors",
        items=(("RANDOM", "Random", "Use random colors"),
                ("BW", "Black/White", "Use Black and White"),
                ("BRIGHT", "Bright Colors", "Use Bright colors"),
                ("EARTH", "Earth", "Use Earth colors"),
                ("GREENBLUE", "Green to Blue", "Use Green to Blue colors")),
        description="Choose which type of colors the materials uses",
        default="RANDOM")
        
    mmSkip = bpy.props.IntProperty(
        name="Keyframe every", 
        min=1, max=250, default=50, 
        description="Number of frames between keyframes")
        
    mmBoolRandom = bpy.props.BoolProperty(
        name="Random Order", 
        default=False, 
        description="Randomize the order of the colors")

    mmColor = bpy.props.FloatVectorProperty(
        attr="myColorValue", 
        min=0, max=1, default=0, 
        name="myColor", 
        description="Color Value", 
        subtype="COLOR")

# Draw Material changer panel in Toolbar
class mmPanel(bpy.types.Panel):
    bl_label = "Material Madness"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        
        Mad = bpy.context.window_manager.madness
        # Box for Material Madness
        box = self.layout.box()
        box.prop(Mad, 'mmColors')
        box.prop(Mad, 'mmSkip')
        box.prop(Mad, 'mmBoolRandom')
        box.prop(Mad, 'mmColor1')
        box.operator("object.madness", text="Color Madness")
        box.operator("object.madnessclear", text="Reset Keyframes")
        row = self.layout.row()


# This is the magical material changer!
class OBJECT_OT_materialChango(bpy.types.Operator):
    bl_idname = 'object.madness'
    bl_label = 'Material Madness'
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
        
        import bpy, random
        madProp = bpy.context.window_manager.madness # properties panel
        
        if bpy.context.object and bpy.context.object.type=='MESH':
            
            # Check to see if object has materials
            checkMaterials = len(bpy.context.object.data.materials)
            if checkMaterials == 0:
                # Add a material
                print('No materials, adding one now.')
                materialName = "MadMaterial"
                madMat = bpy.data.materials.new(materialName)
                bpy.context.object.data.materials.append(madMat)
            else:                
                pass # pass since we have what we need
            
        # assign the first material of the object to "mat"
        mat = bpy.context.object.data.materials[0] 
        
        # define frame start/end variables
        scn = bpy.context.scene       
        start = scn.frame_start
        end = scn.frame_end

        # Numbers of frames to skip between keyframes
        # Get property from panel
        skip = madProp.mmSkip

        # Random material function
        def madnessRandom():
            for crazyNumber in range(3):
                mat.diffuse_color[crazyNumber] = random.random()
                
        # Black and white color        
        def madnessBW():
            bwColors = [(0.0,0.0,0.0),(1.0,1.0,1.0)]
            mat.diffuse_color = random.choice(bwColors)
        
        # Bright colors
        def madnessBright():
            brightColors  = [(1.0, 0.0, 0.75), (0.0,1.0,1.0), (0.0,1.0,0.0), (1.0,1.0,0.0)]
            mat.diffuse_color = random.choice(brightColors)
            
        # Earth Tones
        def madnessEarth():
            earthColors = [(0.068, 0.019, 0.014), (0.089, 0.060, 0.047), (0.188, 0.168, 0.066), (0.445, 0.296, 0.065), (0.745, 0.332, 0.065)]
            mat.diffuse_color = random.choice(earthColors)
            
        # Green to Blue Tones
        def madnessGreenBlue():
            earthColors = [(0.296, 0.445, 0.074), (0.651, 1.0, 0.223), (0.037, 0.047, 0.084), (0.006, 0.012, 0.024)]
            mat.diffuse_color = random.choice(earthColors)
        
        # Go to each frame in iteration and add material
        while start<=(end+(skip-1)):
           
            bpy.ops.anim.change_frame(frame=start)
            
            # Check what colors setting is checked
            if madProp.mmColors=='RANDOM':
                madnessRandom()
            elif madProp.mmColors=='BW':
                madnessBW()
            elif madProp.mmColors=='BRIGHT':
                madnessBright()
            elif madProp.mmColors=='EARTH':
                madnessEarth()
            elif madProp.mmColors=='GREENBLUE':
                madnessGreenBlue()
            
            else:
                pass
            
            # Add keyframe to material
            mat.keyframe_insert('diffuse_color')
            
            # Increase frame number
            start += skip
        return{'FINISHED'}

###### This clears the keyframes ######
class OBJECT_OT_clearMadness(bpy.types.Operator):
    bl_idname = 'object.madnessclear'
    bl_label = 'Clear Madness'
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
        
        import bpy, random
        mMad = context.window_manager.madness_operator # properties panel
        
        # assign the first material of the object to "mat"
        mat = bpy.context.object.data.materials[0] 
        
        # define frame start/end variables
        scn = bpy.context.scene       
        start = scn.frame_start
        end = scn.frame_end

        # Remove all keyframes from diffuse_color, super sloppy need to find better way
        while start<=(end*2):
            bpy.ops.anim.change_frame(frame=start)
            mat.keyframe_delete('diffuse_color')
            start += 1
            
        return{'FINISHED'} 
 
classes = [OBJECT_OT_materialChango, 
                OBJECT_OT_clearMadness,
                mmPanel, 
                mmProps]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.madness = bpy.props.PointerProperty(type=mmProps)
    bpy.types.WindowManager.madness_operator = bpy.props.PointerProperty(type=mmProps)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.madness
    del bpy.types.WindowManager.madness_operator
    
if __name__ == "__main__":
    register()