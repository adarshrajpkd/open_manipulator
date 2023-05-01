TunedBlocks = {'PID1','PID2'};
STO=slTuner('sine',TunedBlocks);

addPoint(STO,TunedBlocks)

addPoint(STO,'Robot/qm');

RefSignals={'sine/Signal Builder/q1','sine/Signal Builder/q2',};
addPoint(STO,RefSignals)
Controls =TunedBlocks;
Measurements='sine/Robot/qm';
options=looptuneOptions('RandomStart',80,'UseParallel',false);
TR= TuningGoal.StepTracking(RefSignals,Measurements,0.05,0);
ST1=looptune(STO,Controls,Measurements,TR,options);

writeBlockValue(ST1)
