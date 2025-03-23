from dataGeneration.data_generation import moivre_pmf, poisson_pmf, binom_pmf
import numpy as np


# TODO:
# 1. почему ошибка муавра так странное себя ведет, при больших количествах испытаний?


def _find_crossover_point(n=100, k_values=np.arange(0, 100), start_p=0.2, step=0.001):
    """
    Находит точку пересечения ошибок аппроксимаций Пуассона и Муавра-Лапласа.

    Args:
        n (int): Количество испытаний.
        k_values (array-like): Значения k (количество успехов) для вычисления ошибок.
        start_p (float): Начальное значение вероятности успеха.
        step (float): Шаг уменьшения вероятности успеха.

    Returns:
        float or None: Значение p, при котором ошибка Муавра-Лапласа становится
                       меньше ошибки Пуассона, или None, если такая точка не найдена.
    """
    p = start_p
    error_poisson = float("inf")  # Инициализируем бесконечностью
    error_moivre = 0

    while p > 0 and error_poisson > error_moivre:
        binom_probs = binom_pmf(k_values, n, p)
        poisson_probs = poisson_pmf(k_values, n * p)
        moivre_probs = moivre_pmf(k_values, n, p)

        error_poisson = np.mean(np.abs(binom_probs - poisson_probs))
        error_moivre = np.mean(np.abs(binom_probs - moivre_probs))

        p -= step

    if error_poisson <= error_moivre:
        return p + step  # Возвращаем предыдущее значение p
    else:
        return None  # Точка пересечения не найдена


def plot_approximation_errors(
    n=100, k_values=np.arange(0, 100), start_p=0.2, end_p=0.0001, step=0.001
):
    """
    Строит график ошибок аппроксимаций и отмечает точку пересечения (если найдена)
    """

    error_poisson_array = []
    error_moivre_array = []
    p_values = []

    p = start_p
    while p >= end_p:  # идем до end_p
        binom_probs = binom_pmf(k_values, n, p)
        poisson_probs = poisson_pmf(k_values, n * p)
        moivre_probs = moivre_pmf(k_values, n, p)

        error_poisson = np.mean(np.abs(binom_probs - poisson_probs))
        error_moivre = np.mean(np.abs(binom_probs - moivre_probs))

        error_poisson_array.append(error_poisson)
        error_moivre_array.append(error_moivre)
        p_values.append(p)

        p -= step

    crossover_p = _find_crossover_point(n, k_values, start_p, step)

    return p_values, error_moivre_array, error_poisson_array, crossover_p
