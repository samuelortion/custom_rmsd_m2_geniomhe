from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt


def compute_rssd(true_atoms, predicted_atoms) -> float:
    """
    Compute the root sum square deviation between the true atoms and the predicted atoms
    :param true_atoms: atoms from the native structure
    :param predicted_atoms: atoms from the predicted structure
    :return: (float) root sum square deviation
    """
    rotation, rssd = R.align_vectors(true_atoms, predicted_atoms, return_sensitivity=False)
    return rotation, rssd


def align_predicted_atoms(true_atoms, predicted_atoms, rotation):
    """
    Align the predicted atoms to the true atoms
    :param true_atoms: atoms from the native structure
    :param predicted_atoms: atoms from the predicted structure
    :param rotation: output or R.align_vectors that contains the rotation matrix
    :return: (np.array) the predicted atoms aligned to true atoms
    """
    rotated_atoms = rotation.apply(predicted_atoms)
    # Compute translation
    translation = true_atoms.mean(axis=0) - rotated_atoms.mean(axis=0)
    # Add to the rotated atoms
    translated_atoms = rotated_atoms + translation
    return translated_atoms


def plot_points(true_atoms, predicted_atoms, rotation):
    """
    Plot the atoms from the true structure, the predicted one, the rotated atoms that
    minimize the root sum square deviation and the final superimposed atoms
    :param true_atoms: atoms from the native structure
    :param predicted_atoms: atoms from the predictive structure
    :param rotation: output of R.align_vectors that contains the rotation matrix
    """

    rotated_atoms = rotation.apply(predicted_atoms)
    # Compute translation
    translation = true_atoms.mean(axis=0) - rotated_atoms.mean(axis=0)
    # Add to the rotated atoms
    translated_atoms = rotated_atoms + translation
    # Plot the atoms
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(true_atoms[:, 0], true_atoms[:, 1], true_atoms[:, 2], label="True atoms")
    ax.scatter(predicted_atoms[:, 0], predicted_atoms[:, 1], predicted_atoms[:, 2], label="Predicted atoms")
    ax.scatter(rotated_atoms[:, 0], rotated_atoms[:, 1], rotated_atoms[:, 2], label="Rotated atoms")
    ax.scatter(
        translated_atoms[:, 0],
        translated_atoms[:, 1],
        translated_atoms[:, 2],
        label="Translated atoms",
    )
    plt.legend()
    plt.show()


if __name__ == "__main__":
    points_A = np.array(
        [[4.267, -36.014, -5.602], [5.643, -34.581, -7.312], [7.753, -32.311, -6.707]]
    )
    points_B = np.array(
        [[-1.926, -18.243, -1.897], [-0.394, -18.282, -4.045], [0.418, -19.086, -7.040]]
    )
    rotation, rssd = compute_rssd(points_A, points_B)
    plot_points(points_A, points_B, rotation)
