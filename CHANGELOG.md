# 0.15.7 (2022-09-28)

- Fix broken tests.

# 0.15.3 (2022-06-10)

- Removed `mujin_controllerclientpy_registerscene.py` script that is deprecated.
- Add `DeleteConfig` api.

# 0.15.2 (2022-05-10)

- Removed old functions and clients:
    - `itlplanningclient2.py` (`ITLPlanning2ControllerClient`) and `realtimeitlplanningclient.py` (`RealtimeITLPlanningControllerClient`) were removed. Use `realtimeitlplanning3client.py` (`RealtimeITLPlanning3ControllerClient`) instead.
    - `SendCurrentLayoutData` and `ResetCurrentLayoutData` were removed from `BinpickingControllerClient`.
    - `RunSceneTaskAsync` was removed from `PlanningControllerClient`. It is available via `ControllerClientBase`.

# 0.15.1 (2022-04-27)

- Moved `ResetCachedRobotConfigurationState` to realtimerobotclient.
