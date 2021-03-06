#!/usr/bin/env python3
"""Cooling block and lid.

All dimensions are in mm.
"""
import math
import pathlib
import warnings

import cadquery as cq
from cadquery import CQ

# create build folder if required
build_dir = pathlib.Path("build")
if not build_dir.is_dir():
    build_dir.mkdir()

# check if ref_dir available
ref_dir = pathlib.Path("ref")
if not ref_dir.is_dir():
    warnings.warn("Reference directory not found - cannot import step files.")

# block parameters
block_l = 350
block_w = 350

# led array parameters
led_array_cols = 11
led_array_rows = led_array_cols
led_repeat_footprint_l = block_l / led_array_cols
led_repeat_footprint_w = block_w / led_array_rows

# screw holes fixing led array to block
led_screw_tap_r = 2.5 / 2
led_screw_tap_h = 5

# regular grid of screws
led_screw_centers_along_x_axis = [
    -block_l / 2 + x * led_repeat_footprint_l for x in range(1, led_array_cols)
]
led_screw_centers_along_y_axis = [
    -block_w / 2 + y * led_repeat_footprint_w + (led_repeat_footprint_w / 2)
    for y in range(0, led_array_rows)
]

# irregular positioned screws along left and right sides
led_screw_side_offset = 3.5
led_screw_centers_along_left = [
    (-block_l / 2 + led_screw_side_offset, y) for y in led_screw_centers_along_y_axis
]
led_screw_centers_along_right = [
    (block_l / 2 - led_screw_side_offset, y) for y in led_screw_centers_along_y_axis
]

# all screw holes
led_screw_holes = set(
    [
        (x, y)
        for x in led_screw_centers_along_x_axis
        for y in led_screw_centers_along_y_axis
    ]
    + led_screw_centers_along_left
    + led_screw_centers_along_right
)

# heat sink parameters
base_h = led_screw_tap_h + 2
fin_h = 15
block_h = base_h + fin_h

# o-ring parameters
oring_inner_edge_gap = 7
oring_outer_edge_gap = 4

# form Apple Rubber ISO 3601 Metric Size O-Rings Quick Reference Chart
oring_cs = 3.53
oring_groove_h = 2.64
oring_groove_w = 4.57


# Aluminium extrusion
# Ooznest V-Slot Linear Rail – 20x20mm
extrusion_w = 20
extrusion_h = 270
if ref_dir.is_dir():
    try:
        extrusion = cq.importers.importStep(
            str(ref_dir.joinpath("Al-extrusion-270mm.step"))
        )
        extrusion = extrusion.rotate((0, 0, 0), (1, 0, 0), 90)
    except:
        warnings.warn("Couldn't load extrusion step file.")

# extrusion bracket
# Ooznest 90 Degree Angle Corner
bracket_l = 20
bracket_w = 20
bracket_h = 20
if ref_dir.is_dir():
    try:
        bracket = cq.importers.importStep(
            str(ref_dir.joinpath("black-angle-corner-connector.step"))
        )
        bracket = bracket.rotate((0, 0, 0), (1, 0, 0), 90)
    except:
        warnings.warn("Couldn't load bracket step file.")

# bracket screw
bracket_screw_offset_z = 3.5
if ref_dir.is_dir():
    try:
        bracket_screw = cq.importers.importStep(
            str(ref_dir.joinpath("freecad-hex-head-screw-M5x25.step"))
        )
    except:
        warnings.warn("Couldn't load bracket screw step file.")


# screw holes for fixing led array/heatsink assembly to support extrusion
extrusion_screw_clearance_r = 5.5 / 2
extrusion_screw_tap_r = 4.2 / 2
extrusion_screw_min_gap = 2

# passthrough holes for wires
pt_hole_clearance_r = 2.65
pt_hole_footprint_offset = 4
pt_hole_x_centers_along_top = []
for x in range(0, led_array_cols):
    pt_hole_x_centers_along_top.append(
        (
            -block_l / 2 + x * led_repeat_footprint_l + pt_hole_footprint_offset,
            block_w / 2 - pt_hole_footprint_offset,
        )
    )
pt_hole_x_centers_along_bottom = []
for x in range(1, led_array_cols + 1):
    pt_hole_x_centers_along_bottom.append(
        (
            -block_l / 2 + x * led_repeat_footprint_l - pt_hole_footprint_offset,
            -block_w / 2 + pt_hole_footprint_offset,
        )
    )
pt_hole_centers = pt_hole_x_centers_along_top + pt_hole_x_centers_along_bottom

# passthrough cuts to turn wire holes in U's
pt_u_x = pt_hole_clearance_r * 2
pt_u_y = pt_hole_footprint_offset
pt_u_x_centers_along_top = []
for x in range(0, led_array_cols):
    pt_u_x_centers_along_top.append(
        (
            -block_l / 2 + x * led_repeat_footprint_l + pt_hole_footprint_offset,
            block_w / 2 - pt_u_y / 2,
        )
    )
pt_u_x_centers_along_bottom = []
for x in range(1, led_array_cols + 1):
    pt_u_x_centers_along_bottom.append(
        (
            -block_l / 2 + x * led_repeat_footprint_l - pt_hole_footprint_offset,
            -block_w / 2 + pt_u_y / 2,
        )
    )
pt_u_centers = pt_u_x_centers_along_top + pt_u_x_centers_along_bottom

# countersink screws for fixing lid to block
cs_screw_clearance_r = extrusion_screw_clearance_r
cs_screw_tap_r = 4.2 / 2
cs_screw_tread_h = fin_h
cs_screw_cap_r = 9.2 / 2
cs_screw_cap_h = 2.5
cs_screw_angle = 90
cs_screw_min_gap = extrusion_screw_min_gap
cs_delta_l = 2 * led_repeat_footprint_l
cs_delta_w = 2 * led_repeat_footprint_w
cs_number_l = math.floor(led_array_cols / 2)
cs_number_w = math.floor(led_array_rows / 2)

cs_centers_along_x_axis_1 = [
    -block_l / 2
    + pt_hole_footprint_offset
    + x * cs_delta_l
    + 3 * led_repeat_footprint_l / 2
    for x in range(cs_number_l)
]
cs_centers_along_x_axis_2 = [
    block_l / 2
    - pt_hole_footprint_offset
    - x * cs_delta_l
    - 3 * led_repeat_footprint_l / 2
    for x in range(cs_number_l)
]
cs_centers_along_y_axis_1 = [
    -block_w / 2
    + pt_hole_footprint_offset
    + y * cs_delta_w
    + 3 * led_repeat_footprint_w / 2
    for y in range(cs_number_w)
]
cs_centers_along_y_axis_2 = [
    block_w / 2
    - pt_hole_footprint_offset
    - y * cs_delta_w
    - 3 * led_repeat_footprint_w / 2
    for y in range(cs_number_w)
]

cs_holes1 = [(x, (block_w - extrusion_w) / 2) for x in cs_centers_along_x_axis_1]
cs_holes2 = [(x, -(block_w - extrusion_w) / 2) for x in cs_centers_along_x_axis_2]

cs_holes3 = [(-(block_l - extrusion_w) / 2, y) for y in cs_centers_along_y_axis_1]
cs_holes4 = [((block_l - extrusion_w) / 2, y) for y in cs_centers_along_y_axis_2]

cs_holes = cs_holes1 + cs_holes2 + cs_holes3 + cs_holes4

# countersink screw
cs_screw_h = 25
if ref_dir.is_dir():
    try:
        cs_screw = cq.importers.importStep(
            str(ref_dir.joinpath("freecad-countersink-screw-M5x25.step"))
        )
    except:
        warnings.warn("Couldn't load cs screw step file.")


# extrusion (extrusion) mounting holes
extrusion_screw_tread_h = fin_h

extrusion_holes = [
    (-(block_l - extrusion_w) / 2, -block_w / 2 + extrusion_w + bracket_w / 2),
    (-(block_l - extrusion_w) / 2, block_w / 2 - extrusion_w - bracket_w / 2),
    ((block_l - extrusion_w) / 2, -block_w / 2 + extrusion_w + bracket_w / 2),
    ((block_l - extrusion_w) / 2, block_w / 2 - extrusion_w - bracket_w / 2),
]

# more o-ring parameters
oring_inner_l = (
    block_l
    - extrusion_w
    - 2 * cs_screw_clearance_r
    - 2 * oring_outer_edge_gap
    - 2 * oring_groove_w
)
oring_inner_w = (
    block_w
    - extrusion_w
    - 2 * cs_screw_clearance_r
    - 2 * oring_outer_edge_gap
    - 2 * oring_groove_w
)

# more heat sink parameters
heatsink_cut_l = oring_inner_l - 2 * oring_inner_edge_gap
heatsink_cut_w = oring_inner_l - 2 * oring_inner_edge_gap
fin_gap = 10
approx_fin_t = 4
fin_number = int((heatsink_cut_w - fin_gap) / (approx_fin_t + fin_gap))
if fin_number % 2 == 0:
    fin_number += 1
fin_t = (heatsink_cut_w - (fin_number + 1) * fin_gap) / fin_number
if fin_t < 1:
    raise ValueError(f"Fin thickness must be greater than 1 mm to be machinable.")
fin_l = heatsink_cut_l - 2 * fin_gap - fin_t
cut_r = fin_gap - 1

oring_inner_r = cut_r + oring_inner_edge_gap

# o-ring dimenstions
oring_outer_perimeter = (
    2 * (oring_inner_l - 2 * oring_inner_r)
    + 2 * (oring_inner_w - 2 * oring_inner_r)
    + 2 * math.pi * (oring_inner_r + oring_groove_w)
)
oring_od = oring_outer_perimeter / math.pi
oring_id = oring_od - 2 * oring_cs
print(f"O-ring ID = {oring_id}, O-ring OD = {oring_od}")


# lid paramters
lid_l = block_l
lid_w = block_w
lid_h = 10
lid_recess_depth = 5
lid_recess_xy = 310
lid_water_thread_length = 20  # total length of the threads for the water hose connections
lid_threadblock_xy = [90, 35]  # xy dims for the hose connection updent
lid_chamfer_clearance = 10  # to make sure there's room to get the chamfer tool in
lid_fillet_r = 5  # general purpose fillet radius

# screw holes for standoffs for attaching a window/diffuser
standoff_screw_tap_r = 2.5 / 2
standoff_screw_tap_h = 5
standoff_screw_offset = 5
standoff_screw_holes = [
    (block_l / 2 - standoff_screw_offset, block_w / 2 - standoff_screw_offset),
    (-(block_l / 2 - standoff_screw_offset), block_w / 2 - standoff_screw_offset),
    (block_l / 2 - standoff_screw_offset, -(block_w / 2 - standoff_screw_offset)),
    (-(block_l / 2 - standoff_screw_offset), -(block_w / 2 - standoff_screw_offset)),
]

# protective window
window_l = block_l
window_w = block_w
window_h = 3
window_screw_clearance_r = 3.4 / 2
window_screw_offset_x = 3.5
window_screw_offset_y = block_l / led_array_cols / 2
window_screw_holes = [
    (-window_l / 2 + window_screw_offset_x, -window_w / 2 + window_screw_offset_y),
    (window_l / 2 - window_screw_offset_x, -window_w / 2 + window_screw_offset_y),
    (-window_l / 2 + window_screw_offset_x, window_w / 2 - window_screw_offset_y),
    (window_l / 2 - window_screw_offset_x, window_w / 2 - window_screw_offset_y),
]

# window spacers
# e.g. Accu HPS-6-3.4-10-N
spacer_inner_r = 3.4 / 2
spacer_outer_r = 6 / 2
spacer_h = 10

# water inlet/outlet ports
# SMC KQ2L12-G04A
water_port_thread_tap_r = 19 / 2
water_port_thread_h = 9.05
water_port_spacing = 53
water_port_hole_centers = [
    (
        water_port_spacing / 2,
        block_w / 2
        - extrusion_w / 2
        - cs_screw_clearance_r
        - oring_outer_edge_gap
        - oring_groove_w
        - oring_inner_edge_gap
        - fin_gap / 2,
    ),
    (
        -water_port_spacing / 2,
        block_w / 2
        - extrusion_w / 2
        - cs_screw_clearance_r
        - oring_outer_edge_gap
        - oring_groove_w
        - oring_inner_edge_gap
        - fin_gap / 2,
    ),
]

if ref_dir.is_dir():
    try:
        water_port = cq.importers.importStep(str(ref_dir.joinpath("KQ2L12-G04A.stp")))
        water_port = water_port.rotate((0, 0, 0), (1, 0, 0), 90)
        water_port = water_port.rotate((0, 0, 0), (0, 0, 1), 90)
        water_port_h = (
            water_port.vertices(">Z").val().Center().z
            - water_port.vertices("<Z").val().Center().z
        )
    except:
        warnings.warn("Couldn't load water port step file.")


# ground screw
# Accu Product Code (APC): SIP-M3-5-A2
ground_screw_tap_r = 2.5 / 2
ground_screw_tap_h = 5
ground_screw_cap_r = 3
ground_screw_cap_clearance = 1

ground_screw_x_y = [
    (
        -block_l / 2 + ground_screw_cap_r + ground_screw_cap_clearance,
        -block_w / 2 + ground_screw_cap_r + ground_screw_cap_clearance,
    )
]

# ground ring terminal
# https://uk.rs-online.com/web/p/ring-terminals/1787255/
# RS components 178-7255
ground_ring_l = 10  # length from wire inlet to center of ring
ground_ring_w = 5
ground_ring_clearance = 5

ground_ring_lid_cut_w = 2 * (ground_screw_cap_r + ground_screw_cap_clearance)
ground_ring_lid_cut_l = (
    ground_screw_cap_clearance
    + ground_screw_cap_r
    + ground_ring_l
    + ground_ring_clearance
)
ground_screw_lid_cut_r = 3


def oring_groove(inner_length, inner_width, groove_h, groove_w, inner_radius):
    """Groove for o-ring in the base.

    Parameters
    ----------
    inner_length : float or int
        internal length
    inner_width : float or int
        internal width
    groove_h : float or int
        depth of groove
    groove_w : float or int
        width of groove
    inner_radius : float or int
        internal radius

    Returns
    -------
    groove : Shape
        o-ring groove
    """
    # define outer perimeter
    outer = (
        cq.Workplane("XY")
        .box(inner_length + 2 * groove_w, inner_width + 2 * groove_w, groove_h)
        .edges("|Z")
        .fillet(inner_radius + groove_w)
    )

    # # define inner perimeter
    inner = (
        cq.Workplane("XY")
        .box(inner_length, inner_width, groove_h)
        .edges("|Z")
        .fillet(inner_radius)
    )

    # cut the inner from the outer
    groove = outer.cut(inner)

    return groove


def heatsink_cutout(fin_h, fin_l, fin_t, fin_gap, fin_number, cut_r):
    """Shape to cut from a block to define a heatsink.

    Parameters
    ----------
    fin_h : float or int
        Height of fins.
    fin_l : float or int
        Length of fins.
    fin_t : float or int
        Thickness of fins.
    fin_gap : float or int.
        Gap between fins.
    fin_number : int
        Number of fins.
    cut_r : float or int
        Radius of the tool used to make the cut.
    """
    # if fin number is not odd raise value error
    if fin_number % 2 == 0:
        raise ValueError(f"Fin number must be odd.")

    # vertical gap
    gap_v = cq.Workplane("XY").box(fin_l + fin_gap, fin_gap, fin_h)

    # horizontal gap
    gap_h = cq.Workplane("XY").box(fin_gap, 2 * fin_gap + fin_t, fin_h)
    gap_h = gap_h.translate(
        (
            (fin_l + fin_gap) / 2 - fin_gap / 2,
            (2 * fin_gap + fin_t) / 2 - fin_gap / 2,
            0,
        )
    )

    # create repeat units (L-shape)
    gap_up_right = gap_v.union(gap_h)
    gap_up_left = gap_up_right.rotate((0, 0, 0), (1, 0, 0), 180)
    gap_down_right = gap_up_left.rotate((0, 0, 0), (0, 0, 1), 180)
    gap_down_left = gap_down_right.rotate((0, 0, 0), (1, 0, 0), 180)

    # calculate total width of cut
    width = fin_number * (fin_gap + fin_t) + fin_gap

    # build channel from L-shapes
    channel = gap_down_right.translate((0, width / 2 - fin_gap / 2, 0))
    channel = channel.translate(
        (
            0,
            -(fin_gap + fin_t),
            0,
        )
    )
    for x in range(1, fin_number - 1):
        if x % 2 == 0:
            gap = gap_down_right
        else:
            gap = gap_up_right
        gap = gap.translate(
            (
                0,
                width / 2 - fin_gap / 2 - (x + 1) * (fin_gap + fin_t),
                0,
            )
        )
        channel = channel.union(gap)

    # overlay oposite side L for last gap to make it symmetrical
    last_gap = gap_down_left.translate(
        (0, (width - fin_gap) / 2 - (fin_number - 1) * (fin_gap + fin_t), 0)
    )
    channel = channel.union(last_gap)

    # fillet the serpentine channel
    channel = channel.edges(">X and |Z").fillet(cut_r)
    channel = channel.edges("<X and |Z").fillet(cut_r)

    # extra path to close channel
    close_gap = water_port_spacing
    close_w = (width - close_gap) / 2

    # horizontal parts
    close_h = cq.Workplane("XY").box(fin_gap, close_w, fin_h)
    close_end = cq.Workplane("XY").circle(fin_gap / 2).extrude(fin_h)

    close_end_1 = close_end.translate((0, -close_w / 2, -fin_h / 2))
    close_h1 = close_h.union(close_end_1)
    close_h1 = close_h1.translate(
        (fin_l / 2 + fin_t + fin_gap, (width - close_w) / 2, 0)
    )

    close_end_2 = close_end.translate((0, close_w / 2, -fin_h / 2))
    close_h2 = close_h.union(close_end_2)
    close_h2 = close_h2.translate(
        (fin_l / 2 + fin_t + fin_gap, -(width - close_w) / 2, 0)
    )

    # vertical parts
    close_gap_v = cq.Workplane("XY").box(fin_l + fin_gap + fin_t, fin_gap, fin_h)
    close_v1 = close_gap_v.translate(
        (fin_t + fin_gap - fin_t / 2, (width - fin_gap) / 2, 0)
    )
    close_v2 = close_gap_v.translate(
        (fin_t + fin_gap - fin_t / 2, -(width - fin_gap) / 2, 0)
    )

    # join horizontal and vertical sections
    close_1 = close_h1.union(close_v1)
    close_2 = close_h2.union(close_v2)

    close_1 = (
        close_1.edges("|Z").edges("not(>Y or <Y or >X or <X)").fillet(cut_r + fin_t)
    )
    close_1 = (
        close_1.edges("|Z")
        .edges("not(not(>Y or <Y or >X or <X))")
        .edges(">X and >Y")
        .fillet(cut_r + fin_t + fin_gap)
    )

    close_2 = (
        close_2.edges("|Z").edges("not(>Y or <Y or >X or <X)").fillet(cut_r + fin_t)
    )
    close_2 = (
        close_2.edges("|Z")
        .edges("not(not(>Y or <Y or >X or <X))")
        .edges(">X and <Y")
        .fillet(cut_r + fin_t + fin_gap)
    )

    # union closing sections with main serpent
    channel = channel.union(close_1)
    channel = channel.union(close_2)

    # re-center
    channel = channel.translate((-(fin_gap + fin_t) / 2, 0, 0))

    return channel


def block(
    heatsink_cutout,
    oring_groove,
):
    """Cooling block.

    Parameters
    ----------
    block_l : float or int
        Block length.
    block_w : float or int
        Block width.
    base_h : float or int
        Height of heatsink base.
    fin_h : float or int
        Height of heatsink fins.
    heatsink_cutout : Shape
        Shape to cut from block to define heatsink.
    oring_groove : Shape
        Shape to cut from block to define o-ring groove.
    oring_groove_h : Shape
        Depth of cut for o-ring groove.
    cs_centres_along_axis : list
        List of centers for screws that fasten list to base along an axis.
    extrusion_w : float
        Width of extrusion. Used here to reference fastener positions.
    """
    block_h = base_h + fin_h
    block = cq.Workplane("XY").box(block_l, block_w, block_h)

    # add holes for lid fasteners
    block = block.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(cs_holes)
    block = block.hole(2 * cs_screw_tap_r, depth=cs_screw_tread_h)

    # add holes for extrusion screws
    block = block.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(extrusion_holes)
    block = block.hole(2 * extrusion_screw_tap_r, depth=extrusion_screw_tread_h)

    # add holes for wire passthroughs
    block = block.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(pt_hole_centers)
    block = block.hole(2 * pt_hole_clearance_r)

    # add holes for led screws
    block = block.faces("<Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(led_screw_holes)
    block = block.hole(2 * led_screw_tap_r, depth=led_screw_tap_h)

    # add hole for ground screw
    block = block.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(ground_screw_x_y)
    block = block.hole(2 * ground_screw_tap_r, depth=ground_screw_tap_h)

    # create o-ring and heatsink cutouts
    oring_groove = oring_groove.translate((0, 0, (fin_h - oring_groove_h) / 2))

    heatsink_oring = oring_groove.union(heatsink_cutout)
    heatsink_oring = heatsink_oring.translate(
        (
            0,
            0,
            (block_h - fin_h) / 2,
        )
    )
    heatsink_oring = heatsink_oring.rotate((0, 0, 0), (0, 0, 1), 90)

    # cut heatsink and oring grooves
    block = block.cut(heatsink_oring)

    return block


def lid():
    """Lid for cooling block."""
    lid = cq.Workplane("XY").box(lid_l, lid_w, lid_h)
    lid = lid.translate((0, 0, (block_h + lid_h) / 2))

    # add cut for ground ring
    ground_ring_cut = cq.Workplane("XY").box(
        ground_ring_lid_cut_l, ground_ring_lid_cut_w, lid_h
    )
    ground_ring_cut = ground_ring_cut.translate(
        (
            -(lid_l - ground_ring_lid_cut_l) / 2,
            -(lid_w - ground_ring_lid_cut_w) / 2,
            (block_h + lid_h) / 2,
        )
    )
    ground_ring_cut = ground_ring_cut.edges(">X and >Y and |Z").fillet(
        ground_screw_lid_cut_r
    )
    lid = lid.cut(ground_ring_cut)

    # add holes for lid fasteners
    lid = lid.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    lid = lid.pushPoints(cs_holes)
    lid = lid.cskHole(
        2 * cs_screw_clearance_r, 2 * cs_screw_cap_r, cs_screw_angle, cs_screw_tread_h
    )

    # add holes for extrusion screws
    lid = lid.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    lid = lid.pushPoints(extrusion_holes)
    lid = lid.hole(2 * extrusion_screw_clearance_r)

    # add holes for wire passthroughs
    lid = lid.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    lid = lid.pushPoints(pt_hole_centers)
    lid = lid.hole(2 * pt_hole_clearance_r)

    # add cuts to turn wire passthroughs into U-shapes
    u_cut = cq.Workplane("XY").box(pt_u_x, pt_u_y, lid_h)
    for x, y in pt_u_centers:
        _u_cut = u_cut
        _u_cut = _u_cut.translate((x, y, (block_h + lid_h) / 2))
        lid = lid.cut(_u_cut)

    # for making ure the chamfer cutting tool can get down to where it needs to be
    chamfer_allowance = (
        CQ().copyWorkplane(lid.faces(">Z").workplane(centerOption="CenterOfBoundBox"))
        .pushPoints(cs_holes)
        .circle(lid_chamfer_clearance).extrude(lid_water_thread_length - lid_h)
    )

    # for a pocket in the middle to reduce weight
    recess = (
        CQ().copyWorkplane(lid.faces(">Z").workplane(centerOption="CenterOfBoundBox", invert=True))
        .box(lid_recess_xy, lid_recess_xy, lid_recess_depth, centered=(True, True, False))
    )

    # for a block around the hose connections to add more connector thread purchase
    thread_block = (
        CQ().copyWorkplane(lid.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True))
        .center(0, water_port_hole_centers[0][1])
        .box(lid_threadblock_xy[0], lid_threadblock_xy[1], lid_water_thread_length, centered=(True, True, False))
        .cut(chamfer_allowance)
        .edges('|Z').fillet(lid_fillet_r)
    )

    # cut the thread block from the recess negative and then fillet that
    # this allows the result to have fillets that are manufacturable
    recess = recess.cut(thread_block).edges('|Z').fillet(lid_fillet_r)

    # cut out the recess then add the thread block
    lid = lid.cut(recess).union(thread_block)

    # add holes for water ports (drill holes up form bottom)
    lid = lid.faces("<Z").workplane(centerOption="CenterOfBoundBox", invert=True)
    lid = lid.pushPoints(water_port_hole_centers)
    lid = lid.circle(water_port_thread_tap_r).cutThruAll()

    return lid


def window():
    """Window to protect pcb."""
    window = cq.Workplane("XY").box(window_l, window_w, window_h)
    window = window.translate((0, 0, -(block_h + window_h) / 2 - 10))

    # add holes for lid fasteners
    window = window.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    window = window.pushPoints(window_screw_holes)
    window = window.hole(
        2 * cs_screw_clearance_r,
    )

    return window


def cylindrical_spacer(inner_r, outer_r, height):
    """Cylindrical spacer for window."""
    inner = cq.Workplane("XY").circle(inner_r).extrude(height)
    outer = cq.Workplane("XY").circle(outer_r).extrude(height)
    spacer = outer.cut(inner)

    return spacer


cut = heatsink_cutout(fin_h, fin_l, fin_t, fin_gap, fin_number, cut_r)
oring = oring_groove(
    oring_inner_l, oring_inner_w, oring_groove_h, oring_groove_w, oring_inner_r
)
cooling_block = block(cut, oring)
block_lid = lid()
pcb_window = window()

assembly = []
assembly.extend(cooling_block.vals())
assembly.extend(block_lid.vals())
assembly.extend(pcb_window.vals())

for x, y in window_screw_holes:
    _spacer = cylindrical_spacer(spacer_inner_r, spacer_outer_r, spacer_h).translate(
        (x, y, -block_h / 2 - spacer_h)
    )
    assembly.extend(_spacer.vals())

try:
    water_inlet = water_port.translate(
        (
            water_port_hole_centers[0][0],
            water_port_hole_centers[0][1],
            block_h / 2 + lid_h,
        )
    )
    water_outlet = water_port.translate(
        (
            water_port_hole_centers[1][0],
            water_port_hole_centers[1][1],
            block_h / 2 + lid_h,
        )
    )

    assembly.extend(water_inlet.vals())
    assembly.extend(water_outlet.vals())
except:
    pass

try:
    bracket_1 = bracket.translate(
        (
            extrusion_holes[0][0],
            extrusion_holes[0][1],
            (bracket_h + block_h) / 2 + lid_h,
        )
    )

    bracket_2 = bracket.rotate((0, 0, 0), (0, 0, 1), 180)
    bracket_2 = bracket_2.translate(
        (
            extrusion_holes[1][0],
            extrusion_holes[1][1],
            (bracket_h + block_h) / 2 + lid_h,
        )
    )

    bracket_3 = bracket.translate(
        (
            extrusion_holes[2][0],
            extrusion_holes[2][1],
            (bracket_h + block_h) / 2 + lid_h,
        )
    )

    bracket_4 = bracket.rotate((0, 0, 0), (0, 0, 1), 180)
    bracket_4 = bracket_4.translate(
        (
            extrusion_holes[3][0],
            extrusion_holes[3][1],
            (bracket_h + block_h) / 2 + lid_h,
        )
    )

    assembly.extend(bracket_1.vals())
    assembly.extend(bracket_2.vals())
    assembly.extend(bracket_3.vals())
    assembly.extend(bracket_4.vals())
except:
    pass

try:
    bracket_screw_1 = bracket_screw.translate(
        (
            extrusion_holes[0][0],
            extrusion_holes[0][1],
            block_h / 2 + lid_h + bracket_screw_offset_z,
        )
    )

    bracket_screw_2 = bracket_screw.translate(
        (
            extrusion_holes[1][0],
            extrusion_holes[1][1],
            block_h / 2 + lid_h + bracket_screw_offset_z,
        )
    )

    bracket_screw_3 = bracket_screw.translate(
        (
            extrusion_holes[2][0],
            extrusion_holes[2][1],
            block_h / 2 + lid_h + bracket_screw_offset_z,
        )
    )

    bracket_screw_4 = bracket_screw.translate(
        (
            extrusion_holes[3][0],
            extrusion_holes[3][1],
            block_h / 2 + lid_h + bracket_screw_offset_z,
        )
    )

    assembly.extend(bracket_screw_1.vals())
    assembly.extend(bracket_screw_2.vals())
    assembly.extend(bracket_screw_3.vals())
    assembly.extend(bracket_screw_4.vals())
except:
    pass

try:
    extrusion = extrusion.rotate((0, 0, 0), (1, 0, 0), 90)

    extrusion_1 = extrusion.translate(
        (
            -(block_l - extrusion_w) / 2,
            -extrusion_h / 2,
            (block_h + extrusion_w) / 2 + lid_h,
        )
    )

    extrusion_2 = extrusion.translate(
        (
            (block_l - extrusion_w) / 2,
            -extrusion_h / 2,
            (block_h + extrusion_w) / 2 + lid_h,
        )
    )

    assembly.extend(extrusion_1.vals())
    assembly.extend(extrusion_2.vals())
except:
    pass

try:
    for x, y in cs_holes:
        _cs_screw = cs_screw.translate((x, y, block_h / 2 + lid_h))
        assembly.extend(_cs_screw.vals())
except:
    pass

compound = cq.Compound.makeCompound(assembly)

# check to see if we can/should use the "show_object" function
if "show_object" in locals():
    # show in CadQuery Editor
    for thing in assembly:
        show_object(thing)
else:
    # export everything as step (this can take a while)
    with open(build_dir.joinpath("assembly.step"), "w") as fh:
        cq.exporters.exportShape(compound, cq.exporters.ExportTypes.STEP, fh)

    with open(build_dir.joinpath("block.step"), "w") as fh:
        cq.exporters.exportShape(cooling_block, cq.exporters.ExportTypes.STEP, fh)

    with open(build_dir.joinpath("lid.step"), "w") as fh:
        cq.exporters.exportShape(block_lid, cq.exporters.ExportTypes.STEP, fh)
