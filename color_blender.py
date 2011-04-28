import bpy
from bpy.props import *

class mmProps(bpy.types.PropertyGroup):
    enabled = bpy.props.IntProperty(default=0)
    
    # Material custom Properties properties
    mmColors = bpy.props.EnumProperty(
        name="Colors",
        items=(("RANDOM", "Random", "Use random colors"),
                ("CUSTOM", "Custom", "Use custom colors"),
                ("BW", "Black/White", "Use Black and White"),
                ("BRIGHT", "Bright Colors", "Use Bright colors"),
                ("EARTH", "Earth", "Use Earth colors"),
                ("GREENBLUE", "Green to Blue", "Use Green to Blue colors")),
        description="Choose which type of colors the materials uses",
        default="RANDOM")
        
    mmSkip = bpy.props.IntProperty(name="Keyframe every", min=1, max=250, default=50, description="Number of frames between keyframes")
    mmBoolRandom = bpy.props.BoolProperty(name="Random Order", default=False, description="Randomize the order of the colors")
    
    # Custom Color properties
    mmColor1 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.8, 0.8, 0.8), description="Custom Color 1", subtype="COLOR")
    mmColor2 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.8, 0.8, 0.3), description="Custom Color 2", subtype="COLOR")
    mmColor3 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.8, 0.5, 0.6), description="Custom Color 3", subtype="COLOR")
    mmColor4 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.2, 0.8, 0.289), description="Custom Color 4", subtype="COLOR")
    mmColor5 = bpy.props.FloatVectorProperty(min=0, max=1, default=(1.0, 0.348, 0.8), description="Custom Color 5", subtype="COLOR")
    mmColor6 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.4, 0.67, 0.8), description="Custom Color 6", subtype="COLOR")
    mmColor7 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.66, 0.88, 0.8), description="Custom Color 7", subtype="COLOR")
    mmColor8 = bpy.props.FloatVectorProperty(min=0, max=1, default=(0.8, 0.38, 0.22), description="Custom Color 8", subtype="COLOR")

# Draw Material changer panel in Toolbar
class mmPanel(bpy.types.Panel):
    bl_label = "Color Blender"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    
    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout
        objects = bpy.context.selected_objects
        colorProp = bpy.context.window_manager.colorblender
        
        # Don't show menu if no objects are selected
        if not objects:
            box = self.layout.box()
            box.label(text='No object(s) selected', icon='COLOR')
            return
        
        # Box for Color Blender
        box = self.layout.box()
        box.prop(colorProp, 'mmColors')
        if colorProp.mmColors == 'CUSTOM':
            box.label("Set Custom Colors")
            box.prop(colorProp, 'mmColor1')
            box.prop(colorProp, 'mmColor2')
            box.prop(colorProp, 'mmColor3')
            box.prop(colorProp, 'mmColor4')
            box.prop(colorProp, 'mmColor5')
            box.prop(colorProp, 'mmColor6')
            box.prop(colorProp, 'mmColor7')
            box.prop(colorProp, 'mmColor8')
        box.prop(colorProp, 'mmSkip')
        box.prop(colorProp, 'mmBoolRandom')
        box.operator("object.colorblender", text="Run Color Blender", icon="COLOR")
        box.operator("object.colorblenderclear", text="Reset Keyframes", icon="KEY_DEHLT")
        row = self.layout.row()


# This is the magical material changer!
class OBJECT_OT_materialChango(bpy.types.Operator):
    bl_idname = 'object.colorblender'
    bl_label = 'Color Blender'
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
        
        import bpy, random
        colorProp = bpy.context.window_manager.colorblender # properties panel
        colorObjects = bpy.context.selected_objects
        
        # Go through each selected object and run the operator
        for i in colorObjects:
            theObj = i
            # Check to see if object has materials
            checkMaterials = len(theObj.data.materials)
            if checkMaterials == 0:
                # Add a material
                print('No materials, adding one now.')
                materialName = "colorblendMaterial"
                madMat = bpy.data.materials.new(materialName)
                theObj.data.materials.append(madMat)
            else:                
                pass # pass since we have what we need
                
            # assign the first material of the object to "mat"
            mat = theObj.data.materials[0] 

            # Numbers of frames to skip between keyframes
            # Get property from panel
            skip = colorProp.mmSkip

            # Random material function
            def colorblenderRandom():
                for crazyNumber in range(3):
                    mat.diffuse_color[crazyNumber] = random.random()
            
            def colorblenderCustom():
                customColors = [colorProp.mmColor1, colorProp.mmColor2, colorProp.mmColor3, colorProp.mmColor4, colorProp.mmColor5, colorProp.mmColor6, colorProp.mmColor7, colorProp.mmColor8]
                mat.diffuse_color = random.choice(customColors)
                
            # Black and white color        
            def colorblenderBW():
                bwColors = [(0.0,0.0,0.0),(1.0,1.0,1.0)]
                mat.diffuse_color = random.choice(bwColors)
            
            # Bright colors
            def colorblenderBright():
                brightColors  = [(1.0, 0.0, 0.75), (0.0,1.0,1.0), (0.0,1.0,0.0), (1.0,1.0,0.0)]
                mat.diffuse_color = random.choice(brightColors)
                
            # Earth Tones
            def colorblenderEarth():
                earthColors = [(0.068, 0.019, 0.014), (0.089, 0.060, 0.047), (0.188, 0.168, 0.066), (0.445, 0.296, 0.065), (0.745, 0.332, 0.065)]
                mat.diffuse_color = random.choice(earthColors)
                
            # Green to Blue Tones
            def colorblenderGreenBlue():
                earthColors = [(0.296, 0.445, 0.074), (0.651, 1.0, 0.223), (0.037, 0.047, 0.084), (0.006, 0.012, 0.024)]
                mat.diffuse_color = random.choice(earthColors)
             
            # define frame start/end variables
            scn = bpy.context.scene       
            start = scn.frame_start
            end = scn.frame_end           
            # Go to each frame in iteration and add material
            while start<=(end+(skip-1)):
               
                bpy.ops.anim.change_frame(frame=start)
                
                # Check what colors setting is checked and run the appropriate function
                if colorProp.mmColors=='RANDOM':
                    colorblenderRandom()
                elif colorProp.mmColors=='CUSTOM':
                    colorblenderCustom()
                elif colorProp.mmColors=='BW':
                    colorblenderBW()
                elif colorProp.mmColors=='BRIGHT':
                    colorblenderBright()
                elif colorProp.mmColors=='EARTH':
                    colorblenderEarth()
                elif colorProp.mmColors=='GREENBLUE':
                    colorblenderGreenBlue()
                else:
                    pass
                
                # Add keyframe to material
                mat.keyframe_insert('diffuse_color')
                
                # Increase frame number
                start += skip
        return{'FINISHED'}
    
###### This clears the keyframes ######
class OBJECT_OT_clearColorblender(bpy.types.Operator):
    bl_idname = 'object.colorblenderclear'
    bl_label = 'Clear colorblendness'
    bl_options = {'REGISTER', 'UNDO'}
    
    def invoke(self, context, event):
        
        import bpy, random
        mcolorblend = context.window_manager.colorblender_operator # properties panel
        colorObjects = bpy.context.selected_objects
        
        # Go through each selected object and run the operator
        for i in colorObjects:
            theObj = i    
            # assign the first material of the object to "mat"
            matCl = theObj.data.materials[0] 
            
            # define frame start/end variables
            scn = bpy.context.scene       
            start = scn.frame_start
            end = scn.frame_end

            # Remove all keyframes from diffuse_color, super sloppy need to find better way
            while start<=(end*2):
                bpy.ops.anim.change_frame(frame=start)
                matCl.keyframe_delete('diffuse_color')
                start += 1
            
        return{'FINISHED'} 
 
classes = [OBJECT_OT_materialChango, 
                OBJECT_OT_clearColorblender,
                mmPanel, 
                mmProps]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.colorblender = bpy.props.PointerProperty(type=mmProps)
    bpy.types.WindowManager.colorblender_operator = bpy.props.PointerProperty(type=mmProps)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.colorblender
    del bpy.types.WindowManager.colorblender_operator
    
if __name__ == "__main__":
    register()