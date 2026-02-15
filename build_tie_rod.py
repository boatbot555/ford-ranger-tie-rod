import bpy
import math
import mathutils

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Conversion
def in2m(inches):
    return inches * 0.0254

# ============================================
# 2001 Ford Ranger Tie Rod — V2
# 1.25" OD x 0.120" wall DOM tube
# Weld-in inserts, 3/4-16 heim joints
# ============================================

# --- DIMENSIONS ---
tube_od = in2m(1.25)
tube_wall = in2m(0.120)
tube_id = tube_od - 2 * tube_wall  # 1.01"
tube_length = in2m(22.0)

# Inserts: turned to slip fit inside tube bore
insert_od = tube_id - in2m(0.002)  # ~1.008"
insert_id = in2m(0.750)  # 3/4" bore for heim thread
insert_length = in2m(1.5)
insert_shoulder_od = tube_od  # flush shoulder at tube end face
insert_shoulder_length = in2m(0.125)  # 1/8" lip

# Heim joint (3/4-16)
heim_body_od = in2m(1.25)
heim_body_length = in2m(1.125)
heim_shank_od = in2m(0.750)
heim_shank_length = in2m(1.0)
heim_ball_od = in2m(0.875)
heim_eye_id = in2m(0.750)

# Jam nut
nut_af = in2m(1.125)  # 1-1/8" across flats for 3/4-16
nut_thickness = in2m(0.453)

# --- MATERIALS ---
steel_mat = bpy.data.materials.new('DOM_Steel')
steel_mat.use_nodes = True
bsdf = steel_mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.32, 0.34, 0.37, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.28

insert_mat = bpy.data.materials.new('Insert_Steel')
insert_mat.use_nodes = True
bsdf2 = insert_mat.node_tree.nodes['Principled BSDF']
bsdf2.inputs['Base Color'].default_value = (0.22, 0.24, 0.27, 1.0)
bsdf2.inputs['Metallic'].default_value = 1.0
bsdf2.inputs['Roughness'].default_value = 0.35

heim_mat = bpy.data.materials.new('Heim_Chrome')
heim_mat.use_nodes = True
bsdf3 = heim_mat.node_tree.nodes['Principled BSDF']
bsdf3.inputs['Base Color'].default_value = (0.55, 0.57, 0.60, 1.0)
bsdf3.inputs['Metallic'].default_value = 1.0
bsdf3.inputs['Roughness'].default_value = 0.12

weld_mat = bpy.data.materials.new('Weld_Bead')
weld_mat.use_nodes = True
bsdf4 = weld_mat.node_tree.nodes['Principled BSDF']
bsdf4.inputs['Base Color'].default_value = (0.28, 0.26, 0.23, 1.0)
bsdf4.inputs['Metallic'].default_value = 0.85
bsdf4.inputs['Roughness'].default_value = 0.65

nut_mat = bpy.data.materials.new('Jam_Nut_Steel')
nut_mat.use_nodes = True
bsdf5 = nut_mat.node_tree.nodes['Principled BSDF']
bsdf5.inputs['Base Color'].default_value = (0.20, 0.22, 0.25, 1.0)
bsdf5.inputs['Metallic'].default_value = 1.0
bsdf5.inputs['Roughness'].default_value = 0.4

# --- MAIN TUBE (hollow) ---
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=tube_od/2, depth=tube_length, location=(0,0,0), rotation=(0, math.pi/2, 0))
tube = bpy.context.active_object
tube.name = 'DOM_Tube_1.25x.120'

bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=tube_id/2, depth=tube_length + in2m(0.5), location=(0,0,0), rotation=(0, math.pi/2, 0))
bore = bpy.context.active_object
mod = tube.modifiers.new('Hollow', 'BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = bore
bpy.context.view_layer.objects.active = tube
bpy.ops.object.modifier_apply(modifier='Hollow')
bpy.data.objects.remove(bore, do_unlink=True)
tube.data.materials.append(steel_mat)

# --- INSERTS (both ends) ---
for side, x_sign in [('LH', -1), ('RH', 1)]:
    tube_end_x = x_sign * tube_length / 2
    # Insert body sits inside tube
    insert_center_x = tube_end_x + x_sign * (insert_length / 2 - in2m(0.25))
    
    # Main insert body (flush inside tube bore)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=insert_od/2, depth=insert_length, location=(insert_center_x, 0, 0), rotation=(0, math.pi/2, 0))
    ins = bpy.context.active_object
    ins.name = f'Insert_{side}'
    
    # Bore through insert for heim thread
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=insert_id/2, depth=insert_length + in2m(0.2), location=(insert_center_x, 0, 0), rotation=(0, math.pi/2, 0))
    ins_bore = bpy.context.active_object
    mod = ins.modifiers.new('Bore', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = ins_bore
    bpy.context.view_layer.objects.active = ins
    bpy.ops.object.modifier_apply(modifier='Bore')
    bpy.data.objects.remove(ins_bore, do_unlink=True)
    ins.data.materials.append(insert_mat)
    
    # Shoulder/lip flush with tube OD at tube end face
    shoulder_x = tube_end_x + x_sign * (insert_shoulder_length / 2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=insert_shoulder_od/2, depth=insert_shoulder_length, location=(shoulder_x, 0, 0), rotation=(0, math.pi/2, 0))
    shoulder = bpy.context.active_object
    shoulder.name = f'Insert_Shoulder_{side}'
    # Bore the shoulder too
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=insert_id/2, depth=insert_shoulder_length + in2m(0.1), location=(shoulder_x, 0, 0), rotation=(0, math.pi/2, 0))
    sh_bore = bpy.context.active_object
    mod = shoulder.modifiers.new('Bore', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = sh_bore
    bpy.context.view_layer.objects.active = shoulder
    bpy.ops.object.modifier_apply(modifier='Bore')
    bpy.data.objects.remove(sh_bore, do_unlink=True)
    shoulder.data.materials.append(insert_mat)
    
    # Weld bead at tube end (fillet weld around insert shoulder)
    weld_x = tube_end_x + x_sign * insert_shoulder_length
    bpy.ops.mesh.primitive_torus_add(
        major_radius=tube_od/2,
        minor_radius=in2m(0.05),
        location=(weld_x, 0, 0),
        rotation=(0, math.pi/2, 0),
        major_segments=64, minor_segments=12
    )
    weld = bpy.context.active_object
    weld.name = f'Weld_{side}'
    weld.data.materials.append(weld_mat)

# --- HEIM JOINTS (both ends) ---
for side, x_sign in [('LH', -1), ('RH', 1)]:
    tube_end_x = x_sign * tube_length / 2
    
    # Threaded shank emerges from insert
    shank_start = tube_end_x + x_sign * insert_shoulder_length
    shank_center = shank_start + x_sign * heim_shank_length / 2
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_shank_od/2, depth=heim_shank_length, location=(shank_center, 0, 0), rotation=(0, math.pi/2, 0))
    shank = bpy.context.active_object
    shank.name = f'Heim_Shank_{side}'
    shank.data.materials.append(heim_mat)
    
    # Heim body (housing)
    body_start = shank_start + x_sign * heim_shank_length
    body_center = body_start + x_sign * heim_body_length / 2
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_body_od/2, depth=heim_body_length, location=(body_center, 0, 0), rotation=(0, math.pi/2, 0))
    body = bpy.context.active_object
    body.name = f'Heim_Body_{side}'
    body.data.materials.append(heim_mat)
    
    # Spherical ball bearing
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=heim_ball_od/2, location=(body_center, 0, 0))
    ball = bpy.context.active_object
    ball.name = f'Heim_Ball_{side}'
    ball.data.materials.append(heim_mat)
    
    # Eye bore through ball (vertical, for mounting bolt)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_eye_id/2, depth=heim_body_od + in2m(0.3), location=(body_center, 0, 0), rotation=(0, 0, 0))
    eye_cut = bpy.context.active_object
    mod = ball.modifiers.new('Eye', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = eye_cut
    bpy.context.view_layer.objects.active = ball
    bpy.ops.object.modifier_apply(modifier='Eye')
    bpy.data.objects.remove(eye_cut, do_unlink=True)
    
    # Jam nut (hex, on shank between tube end and heim body)
    nut_center = shank_start + x_sign * in2m(0.25)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=nut_af/2, depth=nut_thickness, location=(nut_center, 0, 0), rotation=(0, math.pi/2, 0))
    nut = bpy.context.active_object
    nut.name = f'Jam_Nut_{side}'
    # Bore through nut
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_shank_od/2 + in2m(0.005), depth=nut_thickness + in2m(0.1), location=(nut_center, 0, 0), rotation=(0, math.pi/2, 0))
    nut_bore = bpy.context.active_object
    mod = nut.modifiers.new('Bore', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = nut_bore
    bpy.context.view_layer.objects.active = nut
    bpy.ops.object.modifier_apply(modifier='Bore')
    bpy.data.objects.remove(nut_bore, do_unlink=True)
    nut.data.materials.append(nut_mat)

# --- CAMERA (3/4 view showing full assembly) ---
bpy.ops.object.camera_add(location=(in2m(8), in2m(-35), in2m(10)))
cam = bpy.context.active_object
cam.name = 'Camera'
cam.data.lens = 40
direction = mathutils.Vector((0, 0, 0)) - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam

# --- LIGHTING ---
# Key light (warm, above right)
bpy.ops.object.light_add(type='AREA', location=(in2m(15), in2m(-12), in2m(15)))
key = bpy.context.active_object
key.name = 'Key_Light'
key.data.energy = 250
key.data.size = 2.5
key.data.color = (1.0, 0.95, 0.9)
direction = mathutils.Vector((0, 0, 0)) - key.location
rot_quat = direction.to_track_quat('-Z', 'Y')
key.rotation_euler = rot_quat.to_euler()

# Fill light (cool, left side)
bpy.ops.object.light_add(type='AREA', location=(in2m(-12), in2m(8), in2m(6)))
fill = bpy.context.active_object
fill.name = 'Fill_Light'
fill.data.energy = 100
fill.data.size = 3.0
fill.data.color = (0.9, 0.93, 1.0)

# Rim light (behind, above)
bpy.ops.object.light_add(type='AREA', location=(in2m(-5), in2m(15), in2m(10)))
rim = bpy.context.active_object
rim.name = 'Rim_Light'
rim.data.energy = 150
rim.data.size = 1.5

# --- WORLD ---
world = bpy.data.worlds.new('Studio')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs['Color'].default_value = (0.10, 0.11, 0.13, 1.0)
bg.inputs['Strength'].default_value = 0.3

# --- RENDER SETTINGS ---
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 96
bpy.context.scene.cycles.use_denoising = False
bpy.context.scene.cycles.device = 'CPU'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = False

# Render main view
bpy.context.scene.render.filepath = '/tmp/tie_rod_v2_main.png'
bpy.ops.render.render(write_still=True)

# Close-up of heim end
for obj in list(bpy.data.objects):
    if obj.type == 'CAMERA':
        bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.object.camera_add(location=(in2m(16), in2m(-8), in2m(4)))
cam2 = bpy.context.active_object
cam2.name = 'Camera_Closeup'
cam2.data.lens = 65
target = mathutils.Vector((in2m(14), 0, 0))
direction = target - cam2.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam2.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam2

bpy.context.scene.render.filepath = '/tmp/tie_rod_v2_closeup.png'
bpy.ops.render.render(write_still=True)

# Save blend
bpy.ops.wm.save_as_mainfile(filepath='/tmp/ford_ranger_tie_rod_v2.blend')
print('V2 COMPLETE')
