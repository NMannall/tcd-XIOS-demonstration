Sampling Offset - Time Bounds
------

This example writes the average of single field over a 24 hour time period to a
file at a 12 hour offset. The field values are simply the current timestep to
more easily show the behaviour.

Despite providing an offset, nothing in the generated file shows this. The
`time_counter` and `time_centred` datasets specify the time origin as
`2024-01-01 00:00:00` and the units as `seconds since 2024-01-01 00:00:00`
despite the bounds starting at zero (not 43,200 as a 12 hour offset would
imply).

For a demonstration of starting sampling at user specified points in a
simulation, see the [Sampling Offset](../sampling_offset) example.

