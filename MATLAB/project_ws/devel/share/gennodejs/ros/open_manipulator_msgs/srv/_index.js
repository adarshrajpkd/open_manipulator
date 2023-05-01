
"use strict";

let GetJointPosition = require('./GetJointPosition.js')
let SetDrawingTrajectory = require('./SetDrawingTrajectory.js')
let SetKinematicsPose = require('./SetKinematicsPose.js')
let GetKinematicsPose = require('./GetKinematicsPose.js')
let SetJointPosition = require('./SetJointPosition.js')
let SetActuatorState = require('./SetActuatorState.js')

module.exports = {
  GetJointPosition: GetJointPosition,
  SetDrawingTrajectory: SetDrawingTrajectory,
  SetKinematicsPose: SetKinematicsPose,
  GetKinematicsPose: GetKinematicsPose,
  SetJointPosition: SetJointPosition,
  SetActuatorState: SetActuatorState,
};
