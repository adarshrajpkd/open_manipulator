TunedBlocks = {'PID1','PID2'};
STO=slTuner('DOF2_RRR_PD',TunedBlocks);

addPoint(STO,TunedBlocks)

addPoint(STO,'Robot/qm');

RefSignals={'DOF2_RRR_PD/Signal Builder/q1','DOF2_RRR_PD/Signal Builder/q2',};
addPoint(STO,RefSignals)
Controls =TunedBlocks;
Measurements='DOF2_RRR_PD/Robot/qm';
options=looptuneOptions('RandomStart',80,'UseParallel',false);
TR= TuningGoal.StepTracking(RefSignals,Measurements,0.05,0);
ST1=looptune(STO,Controls,Measurements,TR,options);

writeBlockValue(ST1)


