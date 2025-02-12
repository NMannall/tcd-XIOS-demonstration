from typing import List
import netCDF4
import numpy as np
import numpy.testing as npt
import os

import xios_examples.shared_testing as xshared

this_path = os.path.realpath(__file__)
this_dir = os.path.dirname(this_path)

class TestSamplingOffsetTimeBounds(xshared._TestCase):
    test_dir = this_dir
    transient_outputs = ["daily_average.nc"]
    executable = "./timesteps.exe"
    axis_size = 10

    def test_sampling_offset_time_bounds(self):
        self.run_mpi_xios()

        # Check the expected output file exists
        outputfile = '{}/{}'.format(self.test_dir, self.transient_outputs[0])
        self.assertTrue(os.path.exists(outputfile))

        rootgrp = netCDF4.Dataset(outputfile, 'r')

        self.check_dataset(rootgrp['daily_average'], [24.5, 48.5, 72.5])

    def check_dataset(self, dataset: netCDF4.Dataset, expected_values: List[int]):
        # Read data
        result = dataset[:]

        # If 'result' has masked values, we want to remove the masked values to
        # correctly validate the shape of the data
        if result.mask.any():
            result = result.compressed()
            result = np.reshape(result, (-1, self.axis_size))

        # Check dataset has correct number of timesteps and axis size
        timesteps = len(expected_values)
        self.assertEqual(result.shape, (timesteps, self.axis_size))

        # Calculate expected value and diff
        expected = np.repeat([expected_values], self.axis_size, axis=0).T
        diff = result - expected

        # prepare message for failure
        msg = (
            f"{self.transient_outputs[0]}[{dataset.name}]: the expected result\n {expected}\n"
            f" differs from the actual result\n {result} \n"
            f" with diff \n {diff}\n"
        )

        npt.assert_allclose(result, expected, rtol=self.rtol, err_msg=msg)
