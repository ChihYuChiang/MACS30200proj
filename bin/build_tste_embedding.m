%--Setting up
%Get the functions to use
addpath('tste/');

%Disable the pause after each loop
pause('off');


%--Read in survey result
M = csvread('../data/triplets_survey.csv');
% M = [1,2,3; 1,2,4; 2,1,3; 4,2,3];


%--Perform embedding
%TSTE t-Distributed Stochastic Triplet Embedding
%
%   X = tste(triplets, no_dims, lambda, alpha, use_log)
% 
% The function implements t-distributed stochastic triplet embedding (t-STE) 
% based on the specified triplets, to construct an embedding with no_dims 
% dimensions. The parameter lambda specifies the amount of L2-
% regularization (default = 0), whereas alpha sets the number of degrees of
% freedom of the Student-t distribution (default = 1). The variable use_log
% determines whether the sum of the log-probabilities or the sum of the
% probabilities is maximized (default = true).
%
% Note: This function directly learns the embedding X.
embedding = tste(M, 25, 0, 2665);


%--Save result in csv
csvwrite('../data/process/tste.csv', embedding);


%--Keyboard shortcut used in MATLAB
%C-R comment; C-T uncomment