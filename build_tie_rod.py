import bpy
import math
import mathutils

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Conversion: inches to meters
def in2m(inches):
    return inches * 0.0254

# --- DIMENSIONS ---
tube_od = in2m(1.20)
tube_wall = in2m(0.120)
tube_id = tube_od - 2 * tube_wall
tube_length = in2m(22.0)

insert_od = tube_id - in2m(0.002)
insert_id = in2m(0.75)
insert_length = in2m(1.5)

heim_body_od = in2m(1.25)
heim_body_length = in2m(1.125)
heim_shank_od = in2m(0.75)
heim_shank_length = in2m(1.0)
heim_ball_od = in2m(0.875)
heim_eye_id = in2m(0.75)

# --- MATERIALS ---
steel_mat = bpy.data.materials.new('DOM_Steel')
steel_mat.use_nodes = True
bsdf = steel_mat.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.35, 0.37, 0.40, 1.0)
bsdf.inputs['Metallic'].default_value = 1.0
bsdf.inputs['Roughness'].default_value = 0.3

insert_mat = bpy.data.materials.new('Insert_Steel')
insert_mat.use_nodes = True
bsdf2 = insert_mat.node_tree.nodes['Principled BSDF']
bsdf2.inputs['Base Color'].default_value = (0.25, 0.27, 0.30, 1.0)
bsdf2.inputs['Metallic'].default_value = 1.0
bsdf2.inputs['Roughness'].default_value = 0.4

heim_mat = bpy.data.materials.new('Heim_Chrome')
heim_mat.use_nodes = True
bsdf3 = heim_mat.node_tree.nodes['Principled BSDF']
bsdf3.inputs['Base Color'].default_value = (0.6, 0.62, 0.65, 1.0)
bsdf3.inputs['Metallic'].default_value = 1.0
bsdf3.inputs['Roughness'].default_value = 0.15

weld_mat = bpy.data.materials.new('Weld_Bead')
weld_mat.use_nodes = True
bsdf4 = weld_mat.node_tree.nodes['Principled BSDF']
bsdf4.inputs['Base Color'].default_value = (0.30, 0.28, 0.25, 1.0)
bsdf4.inputs['Metallic'].default_value = 0.9
bsdf4.inputs['Roughness'].default_value = 0.6

# --- MAIN TUBE (hollow) ---
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=tube_od/2, depth=tube_length, location=(0,0,0), rotation=(0, math.pi/2, 0))
tube_outer = bpy.context.active_object
tube_outer.name = 'Tube_Outer'

bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=tube_id/2, depth=tube_length + in2m(0.1), location=(0,0,0), rotation=(0, math.pi/2, 0))
tube_bore = bpy.context.active_object
tube_bore.name = 'Tube_Bore'

mod = tube_outer.modifiers.new('Hollow', 'BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = tube_bore
bpy.context.view_layer.objects.active = tube_outer
bpy.ops.object.modifier_apply(modifier='Hollow')
bpy.data.objects.remove(tube_bore, do_unlink=True)
tube_outer.data.materials.append(steel_mat)
tube_outer.name = 'DOM_Tube_1.20x.120'

# --- INSERTS + WELD BEADS ---
for side, x_pos in [('LH', -tube_length/2), ('RH', tube_length/2)]:
    offset = in2m(0.75) if side == 'RH' else in2m(-0.75)
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=insert_od/2, depth=insert_length, location=(x_pos + offset, 0, 0), rotation=(0, math.pi/2, 0))
    insert = bpy.context.active_object
    insert.name = f'Insert_{side}'
    
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=insert_id/2, depth=insert_length + in2m(0.1), location=(x_pos + offset, 0, 0), rotation=(0, math.pi/2, 0))
    bore = bpy.context.active_object
    mod = insert.modifiers.new('Bore', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = bore
    bpy.context.view_layer.objects.active = insert
    bpy.ops.object.modifier_apply(modifier='Bore')
    bpy.data.objects.remove(bore, do_unlink=True)
    insert.data.materials.append(insert_mat)
    
    weld_x = x_pos + (in2m(0.01) if side == 'RH' else in2m(-0.01))
    bpy.ops.mesh.primitive_torus_add(major_radius=tube_od/2 + in2m(0.02), minor_radius=in2m(0.06), location=(weld_x, 0, 0), rotation=(0, math.pi/2, 0), major_segments=64, minor_segments=16)
    weld = bpy.context.active_object
    weld.name = f'Weld_{side}'
    weld.data.materials.append(weld_mat)

# --- HEIM JOINTS ---
for side, x_sign in [('LH', -1), ('RH', 1)]:
    base_x = x_sign * (tube_length/2 + insert_length)
    
    # Shank
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_shank_od/2, depth=heim_shank_length, location=(base_x + x_sign * heim_shank_length/2, 0, 0), rotation=(0, math.pi/2, 0))
    shank = bpy.context.active_object
    shank.name = f'Heim_Shank_{side}'
    shank.data.materials.append(heim_mat)
    
    # Body
    body_x = base_x + x_sign * (heim_shank_length + heim_body_length/2)
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_body_od/2, depth=heim_body_length, location=(body_x, 0, 0), rotation=(0, math.pi/2, 0))
    body = bpy.context.active_object
    body.name = f'Heim_Body_{side}'
    body.data.materials.append(heim_mat)
    
    # Ball
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, radius=heim_ball_od/2, location=(body_x, 0, 0))
    ball = bpy.context.active_object
    ball.name = f'Heim_Ball_{side}'
    ball.data.materials.append(heim_mat)
    
    # Eye hole
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=heim_eye_id/2, depth=heim_body_od + in2m(0.2), location=(body_x, 0, 0), rotation=(0, 0, 0))
    eye_cut = bpy.context.active_object
    mod = ball.modifiers.new('Eye', 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object = eye_cut
    bpy.context.view_layer.objects.active = ball
    bpy.ops.object.modifier_apply(modifier='Eye')
    bpy.data.objects.remove(eye_cut, do_unlink=True)
    
    # Jam nut (hex)
    nut_x = base_x + x_sign * in2m(0.1)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=in2m(0.56), depth=in2m(0.45), location=(nut_x, 0, 0), rotation=(0, math.pi/2, 0))
    nut = bpy.context.active_object
    nut.name = f'Jam_Nut_{side}'
    nut.data.materials.append(insert_mat)

# --- CAMERA + LIGHTING ---
bpy.ops.object.camera_add(location=(in2m(12), in2m(-18), in2m(8)))
cam = bpy.context.active_object
cam.name = 'Camera'
cam.data.lens = 50
direction = mathutils.Vector((0, 0, 0)) - cam.location
rot_quat = direction.to_track_quat('-Z', 'Y')
cam.rotation_euler = rot_quat.to_euler()
bpy.context.scene.camera = cam

bpy.ops.object.light_add(type='AREA', location=(in2m(15), in2m(-10), in2m(12)))
key = bpy.context.active_object
key.name = 'Key_Light'
key.data.energy = 200
key.data.size = 2.0
direction = mathutils.Vector((0, 0, 0)) - key.location
rot_quat = direction.to_track_quat('-Z', 'Y')
key.rotation_euler = rot_quat.to_euler()

bpy.ops.object.light_add(type='AREA', location=(in2m(-10), in2m(8), in2m(6)))
fill = bpy.context.active_object
fill.name = 'Fill_Light'
fill.data.energy = 80
fill.data.size = 3.0

# Render settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 64
bpy.context.scene.cycles.device = 'CPU'
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True
bpy.context.scene.render.filepath = '/tmp/tie_rod_render.png'

print('DONE: Tie rod model built successfully')
