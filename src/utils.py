from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt


def compute_rssd(true_atoms: np.ndarray, predicted_atoms: np.ndarray) -> tuple[R, float]:
    """
    Compute the root sum square deviation between the true atoms and the predicted atoms

    Parameters
    ----------
    true_atoms:
        Atoms from the native structure
    predicted_atoms:
        Atoms from the predicted structure

    Returns
    -------
    rotation:
        Rotation matrix that minimizes the root sum square deviation
    rssd:
        Root sum square deviation between the true and predicted atoms
    """
    rotation, rssd = R.align_vectors(
        true_atoms, predicted_atoms, return_sensitivity=False
    )
    return rotation, rssd


def align_predicted_atoms(true_atoms: np.ndarray, predicted_atoms: np.ndarray, rotation: R) -> np.ndarray:
    """
    Align the predicted atoms to the true atoms

    Parameters
    ----------
    true_atoms:
        Atoms from the native structure
    predicted_atoms:
        Atoms from the predicted structure
    rotation:
        Output of R.align_vectors that contains the rotation matrix

    Returns
    -------
    translated_atoms:
        Atoms from the predicted structure aligned to the native structure

    """
    rotated_atoms = rotation.apply(predicted_atoms)
    # Compute translation
    translation = true_atoms.mean(axis=0) - rotated_atoms.mean(axis=0)
    # Add to the rotated atoms
    translated_atoms = rotated_atoms + translation
    return translated_atoms


def plot_points(true_atoms: np.ndarray, predicted_atoms: np.ndarray, rotation: R):
    """
    Plot the atoms from the true structure, the predicted one, the rotated atoms that
    minimize the root sum square deviation and the final superimposed atoms

    Parameters
    ----------
    true_atoms:
        Atoms from the native structure
    predicted_atoms:
        Atoms from the predictive structure
    rotation:
        Output of R.align_vectors that contains the rotation matrix
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
    ax.scatter(
        predicted_atoms[:, 0],
        predicted_atoms[:, 1],
        predicted_atoms[:, 2],
        label="Predicted atoms",
    )
    ax.scatter(
        rotated_atoms[:, 0],
        rotated_atoms[:, 1],
        rotated_atoms[:, 2],
        label="Rotated atoms",
    )
    ax.scatter(
        translated_atoms[:, 0],
        translated_atoms[:, 1],
        translated_atoms[:, 2],
        label="Translated atoms",
    )
    plt.legend()
    plt.show()


def main():
    points_A = np.array(
        [[4.267, -36.014, -5.602], [5.643, -34.581, -7.312], [7.753, -32.311, -6.707]]
    )
    points_B = np.array(
        [[-1.926, -18.243, -1.897], [-0.394, -18.282, -4.045], [0.418, -19.086, -7.040]]
    )
    rotation, rssd = compute_rssd(points_A, points_B)
    plot_points(points_A, points_B, rotation)


if __name__ == "__main__":
    main()
