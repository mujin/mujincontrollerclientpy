# 0.16.8 (2022-11-10)

- Regenerate graph client.


# 0.16.7 (2022-11-08)

- Regenerate graph client.


# 0.16.6 (2022-11-01)

- Add `GetPackItemPoseInWorld` to support manual order processing.


# 0.16.5 (2022-11-01)

- Add `UploadFiles` to support multi-file upload.


# 0.16.3 (2022-11-07)

- Regenerate graph client.


# 0.16.2 (2022-11-07)

- Regenerate graph client.

# 0.16.1 (2022-10-07)

- Remove `ExecuteTrajectory` method, to avoid dangerous usage. Instead, an ITL program (e.g. with `Move`) should be executed to ensure that the trajectory is collision-free.


# 0.16 (2022-10-06)

- Remove `GetInertiaChildJointStartValues`


# 0.15.9 (2022-09-30)

- Regenerate graph client.


# 0.15.8 (2022-08-19)

- Allow controller client user to supply additional headers to be included in http requests.


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
