The ML inference flow of the EVEREST SDK requires the following arguments:
1. Setup:
    - The `action_name` of the corresponding IBM cloudFPGA service.
    - The `host_address` (host ip address) to be used to connect to the FPGAs.
    - Both are then submitted via `dosa_net.init_from_action(action_name, host_address)`
2. Execution:
    - One numpy.ndarray `x` as input, where the first axis are the batches. 
    - The output is returned in another array `y`.
    - The inference is then called via `y = dosa_net.infer_batch(x)`
