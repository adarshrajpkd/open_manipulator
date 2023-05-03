
"use strict";

let GetKinematicsPose = require('./GetKinematicsPose.js')
let SetActuatorState = require('./SetActuatorState.js')
let SetKinematicsPose = require('./SetKinematicsPose.js')
let SetJointPosition = require('./SetJointPosition.js')
let SetDrawingTrajectory = require('./SetDrawingTrajectory.js')
let GetJointPosition = require('./GetJointPosition.js')

module.exports = {
  GetKinematicsPose: GetKinematicsPose,
  SetActuatorState: SetActuatorState,
  SetKinematicsPose: SetKinematicsPose,
  SetJointPosition: SetJointPosition,
  SetDrawingTrajectory: SetDrawingTrajectory,
  GetJointPosition: GetJointPosition,
};
