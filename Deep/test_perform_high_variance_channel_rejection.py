import numpy as np
import pytest
from pyautomagic.preprocessing.perform_high_variance_channel_rejection import perform_high_variance_channel_rejection


def test_basic_input():
    data = np.array([[0, 2, 4],
                  [0, 35, 70]])
    removed_mask = np.array([0, 0], dtype=bool)
    expected_data_out = np.array([[0, 2, 4],
                               [0, 0, 0]])
    expected_bad_channels = np.array([1])
    expected_updated_removed_mask = np.array([False, True])
    data_out, bad_channels, updated_removed_mask = perform_high_variance_channel_rejection(data, removed_mask)
    assert(np.allclose(data_out, expected_data_out))
    assert(np.allclose(bad_channels, expected_bad_channels))
    assert(np.allclose(updated_removed_mask, expected_updated_removed_mask))


def test_no_input():
    with pytest.raises(TypeError):
        data_out, bad_channels, updated_removed_mask = perform_high_variance_channel_rejection()


def test_params():
    data = np.array([[0, 2, 4],
                     [0, 5, 10]])
    removed_mask = np.array([0, 0], dtype=bool)
    sd_threshold = 4
    expected_data_out = np.array([[0, 2, 4],
                                  [0, 0, 0]])
    expected_bad_channels = np.array([1])
    expected_updated_removed_mask = np.array([False, True])
    data_out, bad_channels, updated_removed_mask = perform_high_variance_channel_rejection(data, removed_mask, sd_threshold)
    assert (np.allclose(data_out, expected_data_out))
    assert (np.allclose(bad_channels, expected_bad_channels))
    assert (np.allclose(updated_removed_mask, expected_updated_removed_mask))