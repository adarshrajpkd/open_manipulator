% PID controller parameters
Kp = 1.0; % Proportional gain
Ki = 0.5; % Integral gain
Kd = 0.2; % Derivative gain

% Sample time
dt = 0.01; % 100 Hz

% Setpoint and initial process variable
setpoint = 50;
pv = 0;

% Initialize variables
integral = 0;
previous_error = 0;

% Simulation time
t = 0:dt:10;

% Loop through each time step
for i = 1:length(t)
    % Error calculation
    error = setpoint - pv;
    
    % Proportional term
    P = Kp * error;
    
    % Integral term
    integral = integral + Ki * error * dt;
    
    % Derivative term
    derivative = Kd * (error - previous_error) / dt;
    
    % PID output
    output = P + integral + derivative;
    
    % Update previous error
    previous_error = error;
    
    % Update process variable
    pv = pv + output * dt;
    
    % Display results
    disp(['Time: ' num2str(t(i)) ' seconds - PV: ' num2str(pv) ' - Output: ' num2str(output)]);

   
end
