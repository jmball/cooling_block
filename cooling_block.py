"""Cooling block and lid.

All dimensions are in mm.
"""
import math
import pathlib
import warnings

import cadquery as cq

# create build folder if required
build_dir = pathlib.Path("build")
if not build_dir.is_dir():
    build_dir.mkdir()

# check if ref_dir available
ref_dir = pathlib.Path("ref")
if not ref_dir.is_dir():
    warnings.warn("Reference directory not found - cannot import step files.")

# heat sink parameters
base_h = 10
fin_h = 15

# block parameters
block_l = 350
block_w = 350
block_h = base_h + fin_h

# led array parameters
led_array_cols = 11
led_array_rows = led_array_cols
led_repeat_footprint_l = block_l / led_array_cols
led_repeat_footprint_w = block_w / led_array_rows

# o-ring parameters
oring_edge_gap = 3
oring_cs = 2.62
oring_groove_h = 0.077 * 25.4
oring_groove_w = 0.1225 * 25.4

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

# more heat sink parameters
heatsink_cut_l = block_l - 2 * (extrusion_w + oring_edge_gap + oring_groove_w)
heatsink_cut_w = heatsink_cut_l
fin_gap = 10
approx_fin_t = 2
fin_number = int((heatsink_cut_w - fin_gap) / (approx_fin_t + fin_gap))
if fin_number % 2 == 0:
    fin_number += 1
fin_t = (heatsink_cut_w - (fin_number + 1) * fin_gap) / fin_number
if fin_t < 1:
    raise ValueError(f"Fin thickness must be greater than 1 mm to be machinable.")
fin_l = heatsink_cut_l - 2 * fin_gap - fin_t
cut_r = fin_gap - 1

# more o-ring parameters
oring_inner_l = heatsink_cut_l + 2 * oring_edge_gap
oring_inner_w = heatsink_cut_w + 2 * oring_edge_gap
oring_inner_r = cut_r + oring_edge_gap
heatsink_offset = (
    (oring_inner_l + 2 * oring_groove_w) / 2
    + extrusion_w / 2
    + extrusion_screw_clearance_r
    + extrusion_screw_min_gap
    + oring_edge_gap
)

# block height depends on heatsink parameters
block_h = base_h + fin_h

# lid paramters
lid_l = block_l
lid_w = block_w
lid_h = 10

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
water_port_spacing = 2 * water_port_thread_tap_r + 45
water_port_hole_centers = [
    (
        water_port_spacing / 2,
        block_w / 2 - extrusion_w - oring_groove_w - oring_edge_gap - fin_gap / 2,
    ),
    (
        -water_port_spacing / 2,
        block_w / 2 - extrusion_w - oring_groove_w - oring_edge_gap - fin_gap / 2,
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
    channel = channel.translate((0, -(fin_gap + fin_t), 0,))
    for x in range(1, fin_number - 1):
        if x % 2 == 0:
            gap = gap_down_right
        else:
            gap = gap_up_right
        gap = gap.translate(
            (0, width / 2 - fin_gap / 2 - (x + 1) * (fin_gap + fin_t), 0,)
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
    heatsink_cutout, oring_groove,
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
    heatsink_offset : float
        Offset from center of heatsink cutout to edge of block. Assumes 4 square
        cutouts from a square block.
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

    # create o-ring and heatsink cutouts
    oring_groove = oring_groove.translate((0, 0, (fin_h - oring_groove_h) / 2))

    heatsink_oring = oring_groove.union(heatsink_cutout)
    heatsink_oring = heatsink_oring.translate((0, 0, (block_h - fin_h) / 2,))
    heatsink_oring = heatsink_oring.rotate((0, 0, 0), (0, 0, 1), 90)

    # cut heatsink and oring grooves
    block = block.cut(heatsink_oring)

    return block


def lid():
    """Lid for cooling block."""
    lid = cq.Workplane("XY").box(lid_l, lid_w, lid_h)
    lid = lid.translate((0, 0, (block_h + lid_h) / 2))

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

    # add holes for water ports
    lid = lid.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    lid = lid.pushPoints(water_port_hole_centers)
    lid = lid.hole(2 * water_port_thread_tap_r)

    return lid


def window():
    """Window to protect pcb."""

    window = cq.Workplane("XY").box(window_l, window_w, window_h)
    window = window.translate((0, 0, -(block_h + window_h) / 2 - 10))

    # add holes for lid fasteners
    window = window.faces(">Z").workplane(centerOption="CenterOfBoundBox")
    window = window.pushPoints(window_screw_holes)
    window = window.hole(2 * cs_screw_clearance_r,)

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
