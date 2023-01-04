

# 0.1.0 (Migrating from mujincontrollerclientpy)

The package `mujincontrollerclient` was split into `mujinwebstackclient` and `mujinplanningclient`. To migrate, determine which methods are used by your controllerclient instance, and convert to the correct class from either package (or use both).

Classes:
- `BinpickingControllerClient` → `BinpickingPlanningClient`
- `HandEyeCalibrationControllerClient` → `HandEyeCalibrationPlanningClient`
- `RealtimeRobotControllerClient` → `RealtimeRobotPlanningClient`
- `RealtimeITLPlanning3ControllerClient` → `RealtimeITL3PlanningClient`
- `ControllerClientError` → `WebstackClientError`
- `UseControllerClientDecorator` → `UsePlanningClientDecorator` AND/OR `UseWebstackClientDecorator`

Imports/Packages:
- `mujincontrollerclient` → `mujinwebstackclient` AND/OR `mujinplanningclient`
- `controllerclientbase` → `webstackclient`
- `controllerclientraw` → `controllerwebclientraw`
- `binpickingcontrollerclient` → `binpickingplanningclient`
- `planningclient` → `planningclient`
- `realtimerobotclient` → `realtimerobotplanningclient`
- `realtimeitlplanning3client` → `realtimeitl3planningclient`
- `handeyecalibrationcontrollerclient` → `handeyecalibrationplanningclient`

In addition:

- `CheckITLProgramExists` has been removed from `realtimeitlplanning3client`. Use webstackclient's `GetProgram` instead.