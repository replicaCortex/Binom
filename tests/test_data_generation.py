from dataGeneration.data_generation import moivre_pmf, binom
import numpy as np
import pytest


@pytest.mark.parametrize(
    "k, n, p",
    [
        (50, 100, 0.5),
        ([40, 50, 60], 100, 0.5),
        (50, 100, 0.2),
        (25, 50, 0.5),
    ],
)
def test_moivre_laplace_pmf_specific_values(k, n, p):
    """Тестирование для конкретных значений k, n, p."""

    approx_prob = moivre_pmf(k, n, p)
    exact_prob = binom.pmf(k, n, p)

    assert np.allclose(approx_prob, exact_prob, atol=0.001)
