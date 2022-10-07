import numpy as np


def _deposit_pic(
    cell_edges_x1,
    cell_edges_x2,
    cell_edges_x3,
    particles_x1,
    particles_x2,
    particles_x3,
    field,
    hci,
    out,
):
    for ipart in range(len(hci)):
        md_idx = tuple(hci[ipart])
        out[md_idx] += field[ipart]


def _deposit_cic(
    cell_edges_x1,
    cell_edges_x2,
    cell_edges_x3,
    particles_x1,
    particles_x2,
    particles_x3,
    field,
    hci,
    out,
):
    return NotImplementedError("Cloud-in-cell deposition method is not implemented yet")


def _deposit_tsc_1D(
    cell_edges_x1,
    cell_edges_x2,
    cell_edges_x3,
    particles_x1,
    particles_x2,
    particles_x3,
    field,
    hci,
    out,
):
    nparticles = hci.shape[0]

    # weight array
    w = np.zeros(3, dtype=field.dtype)

    for ipart in range(nparticles):
        x = particles_x1[ipart]

        ci = hci[ipart, 0]
        d = (x - cell_edges_x1[ci]) / (cell_edges_x1[ci + 1] - cell_edges_x1[ci])
        w[0] = 0.5 * (1 - d) ** 2
        w[1] = 0.75 - (d - 0.5) ** 2
        w[2] = 0.5 * d**2

        for k, j in enumerate((ci - 1, ci, ci + 1)):
            out[j] += w[k] * field[ipart]


def _deposit_tsc_2D(
    cell_edges_x1,
    cell_edges_x2,
    cell_edges_x3,
    particles_x1,
    particles_x2,
    particles_x3,
    field,
    hci,
    out,
):
    nparticles = hci.shape[0]

    # weight arrays
    w1 = np.zeros(3, dtype=field.dtype)
    w2 = np.zeros(3, dtype=field.dtype)

    w = np.zeros((3, 3), dtype=field.dtype)

    for ipart in range(nparticles):
        x = particles_x1[ipart]
        ci = hci[ipart, 0]
        d = (x - cell_edges_x1[ci]) / (cell_edges_x1[ci + 1] - cell_edges_x1[ci])
        assert d > 0
        w1[0] = 0.5 * (1 - d) ** 2
        w1[1] = 0.75 - (d - 0.5) ** 2
        w1[2] = 0.5 * d**2

        x = particles_x2[ipart]
        cj = hci[ipart, 1]
        d = (x - cell_edges_x2[cj]) / (cell_edges_x2[cj + 1] - cell_edges_x2[cj])
        assert d > 0
        w2[0] = 0.5 * (1 - d) ** 2
        w2[1] = 0.75 - (d - 0.5) ** 2
        w2[2] = 0.5 * d**2

        for i in range(3):
            for j in range(3):
                w[i, j] = w1[i] * w2[j]

        for i, oci in enumerate((ci - 1, ci, ci + 1)):
            for j, ocj in enumerate((cj - 1, cj, cj + 1)):
                out[oci, ocj] += w[i, j] * field[ipart]


def _deposit_tsc_3D(
    cell_edges_x1,
    cell_edges_x2,
    cell_edges_x3,
    particles_x1,
    particles_x2,
    particles_x3,
    field,
    hci,
    out,
):
    nparticles = hci.shape[0]

    # weight arrays
    w1 = np.zeros(3, dtype=field.dtype)
    w2 = np.zeros(3, dtype=field.dtype)
    w3 = np.zeros(3, dtype=field.dtype)

    w = np.zeros((3, 3, 3), dtype=field.dtype)

    for ipart in range(nparticles):
        x = particles_x1[ipart]
        ci = hci[ipart, 0]
        d = (x - cell_edges_x1[ci]) / (cell_edges_x1[ci + 1] - cell_edges_x1[ci])
        assert d > 0
        w1[0] = 0.5 * (1 - d) ** 2
        w1[1] = 0.75 - (d - 0.5) ** 2
        w1[2] = 0.5 * d**2

        x = particles_x2[ipart]
        cj = hci[ipart, 1]
        d = (x - cell_edges_x2[cj]) / (cell_edges_x2[cj + 1] - cell_edges_x2[cj])
        assert d > 0
        w2[0] = 0.5 * (1 - d) ** 2
        w2[1] = 0.75 - (d - 0.5) ** 2
        w2[2] = 0.5 * d**2

        x = particles_x3[ipart]
        ck = hci[ipart, 2]
        d = (x - cell_edges_x3[ck]) / (cell_edges_x3[ck + 1] - cell_edges_x3[ck])
        assert d > 0
        w3[0] = 0.5 * (1 - d) ** 2
        w3[1] = 0.75 - (d - 0.5) ** 2
        w3[2] = 0.5 * d**2

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    w[i, j, k] = w1[i] * w2[j] * w3[k]

        for i, oci in enumerate((ci - 1, ci, ci + 1)):
            for j, ocj in enumerate((cj - 1, cj, cj + 1)):
                for k, ock in enumerate((ck - 1, ck, ck + 1)):
                    out[oci, ocj, ock] += w[i, j, k] * field[ipart]
