"""Cooling block and lid.

All dimensions are in mm.
"""

import pathlib

import cadquery as cq

# create build folder if required
build_dir = pathlib.Path("build")
if not build_dir.is_dir():
    build_dir.mkdir()

# block parameters
block_l = 350
block_w = 350

# o-ring parameters
oring_edge_gap = 2
oring_cs = 2.62
oring_groove_h = 0.077 * 25.4
oring_groove_w = 0.1225 * 25.4

# extrusion
extrusion_w = 20

# screw holes for fixing led array/heatsink assembly to support extrusion
extrusion_screw_clearance_r = 5.5 / 2
extrusion_screw_min_gap = 2

# countersink screws for fixing lid to block
cs_screw_clearance_r = extrusion_screw_clearance_r
cs_screw_tap_r = 4.2 / 2
cs_screw_tread_h = 10
cs_screw_cap_r = 9.2 / 2
cs_screw_cap_h = 2.5
cs_screw_angle = 90
cs_screw_min_gap = extrusion_screw_min_gap
cs_number = 7
cs_delta = (block_l - extrusion_w) / (cs_number - 1)
cs_centers_along_axis = [
    -(block_l - extrusion_w) / 2 + x * cs_delta for x in range(cs_number)
]
cs_holes1 = [(0, x) for x in cs_centers_along_axis]
cs_holes2 = [((block_l - extrusion_w) / 2, x) for x in cs_centers_along_axis]
cs_holes3 = [(-(block_l - extrusion_w) / 2, x) for x in cs_centers_along_axis]
cs_holes4 = [(x, 0) for x in cs_centers_along_axis]
cs_holes5 = [(x, (block_w - extrusion_w) / 2) for x in cs_centers_along_axis]
cs_holes6 = [(x, -(block_w - extrusion_w) / 2) for x in cs_centers_along_axis]
cs_holes = set(cs_holes1 + cs_holes2 + cs_holes3 + cs_holes4 + cs_holes5 + cs_holes6)

# extrusion holes
extrusion_screw_number = cs_number - 1
extrusion_screw_delta = (block_l - extrusion_w - cs_delta) / (
    extrusion_screw_number - 1
)
extrusion_screw_centers_along_axis = [
    -(block_l - extrusion_w - cs_delta) / 2 + x * extrusion_screw_delta
    for x in range(extrusion_screw_number)
]
extrusion_holes1 = [
    (x, (block_w - extrusion_w) / 2) for x in extrusion_screw_centers_along_axis
]
extrusion_holes2 = [
    (x, -(block_l - extrusion_w) / 2) for x in extrusion_screw_centers_along_axis
]
extrusion_holes = set(extrusion_holes1 + extrusion_holes2)

# heat sink parameters
base_h = 10
fin_h = 15
heatsink_cut_l = (
    (
        block_l
        - extrusion_w
        - 2
        * (
            extrusion_screw_clearance_r
            + extrusion_screw_min_gap
            + cs_screw_clearance_r
            + cs_screw_min_gap
            + 2 * oring_edge_gap
        )
    )
    / 2
    - 2 * oring_groove_w
    - 2 * oring_edge_gap
)
heatsink_cut_w = heatsink_cut_l
fin_gap = 6
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
led_array_rows_cols = 12
led_repeat_footprint_l = (block_l - 2 * extrusion_w) / led_array_rows_cols
led_screw_centers_along_axis = [
    -block_l / 2 + extrusion_w + x * led_repeat_footprint_l
    for x in range(led_array_rows_cols + 1)
]
led_screw_holes = set(
    [(y, x) for x in led_screw_centers_along_axis for y in led_screw_centers_along_axis]
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

    # repeat units (L-shape)
    gap_up_right = gap_v.union(gap_h)
    gap_up_left = gap_up_right.rotate((0, 0, 0), (1, 0, 0), 180)
    gap_down_right = gap_up_left.rotate((0, 0, 0), (0, 0, 1), 180)

    width = fin_number * (fin_gap + fin_t) + fin_gap

    channel = gap_v.translate((0, width / 2 - fin_gap / 2, 0))
    for x in range(fin_number):
        if x % 2 == 0:
            gap = gap_down_right
        else:
            gap = gap_up_right
        gap = gap.translate(
            (0, width / 2 - fin_gap / 2 - (x + 1) * (fin_gap + fin_t), 0,)
        )
        channel = channel.union(gap)

    # TODO: figure out how to deselect outermost channels from filleting
    # fillets
    channel = channel.edges(">X and |Z").edges("not(>Y)").edges("not(<Y)").fillet(cut_r)
    channel = channel.edges("<X and |Z").fillet(cut_r)

    # extra path to close channel
    close_h = cq.Workplane("XY").box(fin_gap, width, fin_h)
    close_h = close_h.translate((fin_l / 2 + fin_t + fin_gap, 0, 0))
    close_v1 = gap_v.translate((fin_t + fin_gap, width / 2 - fin_gap / 2, 0))
    close_v2 = gap_v.translate((fin_t + fin_gap, -width / 2 + fin_gap / 2, 0))
    close = close_h.union(close_v1)
    close = close.union(close_v2)
    close = close.edges(">X and |Z").fillet(cut_r)

    channel = channel.union(close)

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
    block = block.hole(2 * extrusion_screw_clearance_r)

    # add holes for led screws
    block = block.faces("<Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(led_screw_holes)
    block = block.hole(2 * led_screw_tap_r, depth=led_screw_tap_h)

    # add holes for standoffs
    block = block.faces("<Z").workplane(centerOption="CenterOfBoundBox")
    block = block.pushPoints(standoff_screw_holes)
    block = block.hole(2 * standoff_screw_tap_r, depth=standoff_screw_tap_h)

    # create o-ring and heatsink cutouts
    oring_groove = oring_groove.translate((0, 0, (fin_h - oring_groove_h) / 2))

    heatsink_oring1 = oring_groove.union(heatsink_cutout)
    heatsink_oring1 = heatsink_oring1.translate(
        (
            block_l / 2 - heatsink_offset,
            block_w / 2 - heatsink_offset,
            (block_h - fin_h) / 2,
        )
    )

    heatsink_oring2 = oring_groove.union(heatsink_cutout)
    heatsink_oring2 = heatsink_oring2.translate(
        (
            -block_l / 2 + heatsink_offset,
            block_w / 2 - heatsink_offset,
            (block_h - fin_h) / 2,
        )
    )

    heatsink_oring3 = oring_groove.union(heatsink_cutout)
    heatsink_oring3 = heatsink_oring3.translate(
        (
            block_l / 2 - heatsink_offset,
            -block_w / 2 + heatsink_offset,
            (block_h - fin_h) / 2,
        )
    )

    heatsink_oring4 = oring_groove.union(heatsink_cutout)
    heatsink_oring4 = heatsink_oring4.translate(
        (
            -block_l / 2 + heatsink_offset,
            -block_w / 2 + heatsink_offset,
            (block_h - fin_h) / 2,
        )
    )

    # cut heatsink and oring grooves
    block = block.cut(heatsink_oring1)
    block = block.cut(heatsink_oring2)
    block = block.cut(heatsink_oring3)
    block = block.cut(heatsink_oring4)

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

    return lid


cut = heatsink_cutout(fin_h, fin_l, fin_t, fin_gap, fin_number, cut_r)
oring = oring_groove(
    oring_inner_l, oring_inner_w, oring_groove_h, oring_groove_w, oring_inner_r
)
cooling_block = block(cut, oring)
block_lid = lid()

assembly = []
assembly.extend(cooling_block.vals())
assembly.extend(block_lid.vals())

compound = cq.Compound.makeCompound(assembly)

with open(build_dir.joinpath("assembly.step"), "w") as fh:
    cq.exporters.exportShape(compound, cq.exporters.ExportTypes.STEP, fh)

with open(build_dir.joinpath("block.step"), "w") as fh:
    cq.exporters.exportShape(cooling_block, cq.exporters.ExportTypes.STEP, fh)

with open(build_dir.joinpath("lid.step"), "w") as fh:
    cq.exporters.exportShape(block_lid, cq.exporters.ExportTypes.STEP, fh)
