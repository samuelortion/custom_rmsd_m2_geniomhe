import utils
import metrics
import inputs


class CustomCGRMSD:
  def __init__(self, *args, **kwargs):
      pass

  def predict(self, native_path: str, predicted_path: str) -> float:
    """
    Function that predicts CG-RMSD.

    Args
    ----
        native_path: path to a `.pdb` native file
        predicted_path: path to a `.pdb` predicted file

    Returns
    -------
        A custom Coarse Grained - RMSD metric
    """
    print(native_path, predicted_path)
    selected_atoms = ["C3'"]
    native_atoms: np.ndarray = inputs.load_atoms(native_path, selected_atoms=selected_atoms)
    predicted_atoms: np.ndarray = inputs.load_atoms(predicted_path, selected_atoms=selected_atoms)
    assert native_atoms.shape == predicted_atoms.shape, f"Not the same number of atoms in {native_path} compared to {predicted_path}"
    rotation, _ = utils.compute_rssd(native_atoms, predicted_atoms)
    aligned_predicted_atoms: np.ndarray = utils.align_predicted_atoms(native_atoms, predicted_atoms, rotation)
    score: float = metrics.rmsd(native_atoms, aligned_predicted_atoms)
    return score
