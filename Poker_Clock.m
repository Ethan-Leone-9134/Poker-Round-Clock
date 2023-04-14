
% Ethan Leone Poker clock

%#ok<*GVMIS>   % Globals should not be used
%#ok<*SAGROW>  % Loop increasing vector sizes 
%#ok<*DEFNU>   % Function not called
clc
clear
format compact
format short g
close all


global startTime clock duration valid size rounds titleText playButton minPerRnd backColor chips
backColor = [1,1,1];
makeRounds();           % Call round and chip variables
valid = 1;              % Loop condition (is clock running)
startTime = tic;        % Sets first value for starting time
size = [0,0];           % Dimensions of screen
% Clock                 % Main clock display
% titleText             % Title text box
duration = minPerRnd*60;% How many total seconds there are to go
% minPerRnd             % Minutes per round

createFigWin()          % Make figure window


%% FUNCTIONS

function makeRounds()
% Pull rounds and chips from storage file
global rounds chips minPerRnd
run PokerRoundsFile.m
% disp(chips)
end

function primaryCounter()
    % Function primaryCounter
    % While loop to tick the time down
    % Inputs  : None
    % Outputs : None
    % Globals : see main code setup
    global valid duration startTime clock titleText rounds
    totalSecLeft = duration; % Needed to prevent input error
    startingRound = titleText.String;
    while valid % While play is active
        currTime = tic; % Find current time
        runTime = (currTime - startTime)/1e7; % How far is current time from start tic
        totalSecLeft = duration - double(runTime); % Find total seconds left
        showTime(totalSecLeft) % Display new time to clock
        pause(0.001) % Give code time to display
    end
    if strcmpi(titleText.String, startingRound)
    % As long as it is the same round as the start of function
    duration = totalSecLeft; % Change remaining duration for further plays
    end
end


%% Create screen

function createFigWin()
    % Function primaryCounter
    % While loop to tick the time down
    % Inputs  : None
    % Outputs : None
    % Globals : size - size of screen in pixels
    global size backColor

    % Create figure window  
    set(0, 'Units', 'inches')
    scrSize = get(0, 'ScreenSize');
    set(0, 'Units', 'pixels')
    fig1 = figure('Units', 'inches', 'Position', [0,0, scrSize(3), scrSize(4)], 'color', backColor, 'WindowState','maximized');
    % Get dimensions of figure window
    set(fig1, 'Units', 'pixels')
    size(1) = fig1.Position(3);
    size(2) = fig1.Position(4);
    % Format figure properties
    fig1.Name = 'Clock';
    fig1.NumberTitle = 'off';
    fig1.ToolBar = 'none';
    set(fig1, 'CloseRequestFcn', @closeOut)
    % Axis manipulation
    axes('Units', 'pixels', 'Position',[850,10,400,600], ...
        'XLim', [0, 200], 'YLim', [0, 300])
    hold on
    axis off
%     axis equal
    axis manual
    pause(0.001)
    placeBoxes()
    pause(0.001)
    placeChips()

end

function placeBoxes()
    % Function placeBoxes
    % Lays the uicontrols to the screen
    % Inputs  : None
    % Outputs : None
    % Globals : see main code setup
    
    global startTime clock duration valid size rounds titleText playButton backColor subTitleText uib
    
    % Relatively centered position for the clock
    xPosClock = size(1)/2-300-200;
    yPosClock = size(2)/2-150-100;

%     buttonColor = [1, 0.4, 0.4];
    buttonColor = 'w';

    % Main time box
    clock = uicontrol('Style','text','String','0:0', ...
        'Position', [xPosClock, yPosClock, 600, 300], ...
        'BackgroundColor', backColor, 'FontSize', 175);

    % Time controls
    uib(1) = uicontrol('Style','pushbutton','String','+', 'Position', ...
        [xPosClock-75, yPosClock+175, 50, 50], 'BackgroundColor', buttonColor, 'FontSize', 25, 'Callback', @mU);
    uib(2) = uicontrol('Style','pushbutton','String','-', 'Position', ...
        [xPosClock-75, yPosClock+75, 50, 50], 'BackgroundColor', buttonColor, 'FontSize', 25, 'Callback', @mD);
    uib(3) = uicontrol('Style','pushbutton','String','+', 'Position', ...
        [xPosClock+625, yPosClock+175, 50, 50], 'BackgroundColor', buttonColor, 'FontSize', 25, 'Callback', @sU);
    uib(4) = uicontrol('Style','pushbutton','String','-', 'Position', ...
        [xPosClock+625, yPosClock+75, 50, 50], 'BackgroundColor', buttonColor, 'FontSize', 25, 'Callback', @sD);
   
    % Title words
    titleText = uicontrol('Style','text','String','SB/BB', ...
        'Position', [xPosClock-100, yPosClock+350, 800, 200], ...
        'BackgroundColor', backColor, 'FontSize', 125);
    subTitleText = uicontrol('Style','text','String','Next: SB/BB', ...
        'Position', [titleText.Position(1), titleText.Position(2)-70, 800, 70], ...
        'BackgroundColor', backColor, 'ForegroundColor', [0.5,0.5,0.5],'FontSize', 50);

    % Pause/Play Button
    playButton = uicontrol('Style','pushbutton','String','⏵', ...
        'Position', [xPosClock+260, yPosClock-100, 80, 80], ...
        'BackgroundColor', buttonColor, 'FontSize', 50, 'Callback', @playOrPause);
    % Round change buttons
    uib(5) = uicontrol('Style','pushbutton','String','>', ...
        'Position', [10, titleText.Position(2)+30, 40, 40], ...
        'BackgroundColor', buttonColor, 'FontSize', 40, 'Callback', @nextRound);
    uib(6) = uicontrol('Style','pushbutton','String','<', ...
        'Position', [10, titleText.Position(2)+110, 40, 40], ...
        'BackgroundColor', buttonColor, 'FontSize', 40, 'Callback', @backRound, 'Enable', 'off');
    % Settings button
    uicontrol('Style','pushbutton','String','⚙', ...
        'Position', [10, 10, 50, 50], ...
        'BackgroundColor', buttonColor, 'FontSize', 30, 'Callback', @openSettings);
    
    titleText.String = rounds(2, 2);
    subTitleText.String = ['Next: ', cell2mat(rounds(3,2))];
    showTime(duration)
    

end

function placeChips()
    global rounds chips backColor
    
    clearOut = rectangle('Position',[0,0,200,350], 'EdgeColor', backColor, 'FaceColor',backColor);
    currRound = cell2mat(rounds(1,2));
    roundSize = size(rounds);
    logVec = cell2mat(rounds(currRound,3:roundSize(2))); % Logical vector of all needed chips
    currColList = flip(matchLogical(logVec, chips),2);
    
    if sum(logVec) < 3
        for currChip = 1:sum(logVec) % Small
            eachSize = 300/sum(logVec);
            minRise = (eachSize-100)/2;
            yVal = minRise+eachSize*(currChip-1);
            color = cell2mat(currColList(1, currChip));
            rectangle('Position',[50,yVal,100,100], 'Curvature', 1, 'EdgeColor', 'black', 'FaceColor', color);
            printChipValue(50, yVal, currColList(:, currChip))
        end
    else
    for currChip = 1:sum(logVec) % Other 
        switch sum(logVec)
            case 3
                yInc = 100;
            case 4
                yInc = 65;
        end
        if even(currChip) % If the number is even
            xVal = 100;
        else
            xVal = 0;
        end
        eachSize = 300/sum(logVec);
        minRise = (eachSize-75)/2;
        yVal = yInc*(currChip-1);
        color = cell2mat(currColList(1, currChip));
        rectangle('Position',[xVal,yVal,100,100], 'Curvature', 1, 'EdgeColor', 'black', 'FaceColor', color);
        printChipValue(xVal, yVal, currColList(:, currChip))

    end
    end
    pause(0.000001) % Print progress to screen
end

%% Change Screen

function showTime(secsLeft)
    % Function showTimes
    % Formats and prints the remaing time to the figure window
    % Inputs  : secsLeft - Number of seconds left in countdown
    % Outputs : None
    % Globals : see main code setup
    global clock valid playButton
    minsLeft = floor(secsLeft/60); % Find remaining minutes
    secLeft = secsLeft - minsLeft*60; % FInd remaining seconds
    if secLeft < 10 % Add leading zeros
        secLeft = "0" + secLeft;
    end
    clock.String = minsLeft + ":" + secLeft; % Set the display
    if secsLeft <= 0 % Timer ended
        valid = 0; % End loop
%         nextRound()
        playButton.String = '⏵';
    end
    if secsLeft == 60 || secsLeft == 0
        beat = load('train.mat');
        sound(beat.y, beat.Fs)
        pause(0.9)
    end
end

function backRound(~,~)
global rounds
oldRound = cell2mat(rounds(1,2));
newRound = oldRound-2;
if newRound > 0
    rounds(1,2) = {newRound};
else
    rounds(1,2) = {1};
end
nextRound()
end

function nextRound(~, ~)
global startTime clock duration valid size rounds titleText playButton minPerRnd subTitleText
oldRound = cell2mat(rounds(1,2));
newRound = oldRound+1;
rounds(1,2) = {newRound};
if duration ~= 0 && valid
    playButton.String = '⏵';
    valid = 0;
end
duration = 0;
if ismember('/', char(rounds(newRound, 2))) % If it is a blind round
    newDuration = minPerRnd*60;
    duration = newDuration;
    showTime(newDuration)
    clock.FontSize = 175;
    titleText.String = rounds(newRound, 2);
else % If it is a special round
    clockText = cell2mat(rounds(newRound, 2));
    clock.String = clockText;
    clock.FontSize = 800/length(char(clockText));
    titleText.String = rounds(newRound, 1);
    playButton.String = '⏵';
end
subText(newRound)
buttonTest(newRound)
placeChips()
% playButton.String = '⏵'; % Something needed for zero out
% valid = 0;

end

function subText(currentRound)
global subTitleText rounds
if size(rounds) < currentRound+1
    subTitleText.String = 'Final Round';
else
    subTitleText.String = ['Next: ', cell2mat(rounds(currentRound+1,2))];
end

end

function buttonTest(currentRound)
% Function buttonTest
% Tests if certain buttons should be disabled
global uib rounds

for but = 1:6
    set(uib(but), 'Enable', 'on');
end

if currentRound == 2
    set(uib(6), 'Enable', 'off');
elseif size(rounds, 1) == currentRound
    set(uib(5), 'Enable', 'off');
end

if not(strcmpi(rounds(currentRound,1), {'Round'}) || strcmpi(rounds(currentRound,1), {'Break'}))
    for num = 1:4
        set(uib(num), 'Enable', 'off');
    end
end

end

function printChipValue(xVal, yVal, chipColumn)
    number = string(cell2mat(chipColumn(2)));
    backColor = cell2mat(chipColumn(1));
    chipVal = text(xVal+50,yVal+50, number, 'FontSize', 80);
    chipVal.Position(1) = xVal+50-(chipVal.Extent(3)/2);
    chipVal.Color = fontColor(backColor);
end

%% COMMENT ABOVE

%% Passable Functions

function c = matchLogical(a, b)
    [~, aCol] = size(a);
    [~, bCol] = size(b);
    if aCol == bCol
        c = [];
            for i = 1:length(a)
                if a(i)
                    c = [c,b(:, i)];
                end
            end
    
    else
        disp('matchLogical: Vector size non-equal! ')
    end
end

function logical = even(input)
    logical = (input/2 == round(input/2));
end

function answer = valueLim(num, limit)
    % Function valueLim
    % Restricts a number's absolute value if needed
    % (Shrinks if goes over positive limit)
    % (Grows if under negative limit)
    % Inputs  : num - original number
    %           limit - largest possible absolute value (smallest if negative)
    % Outputs : answer - restricted number
    % Globals : none
    answer = num;
    if limit > 0
        sign = 1;
    else
        sign = -1;
    end
    if limit > 0
        if abs(num) > limit % If |num| exceeds limit
            if num < 0 % If num is negative
                answer = -limit;
            elseif num > 0 % If num is positive
                answer = limit;
            end
        end
    elseif limit < 0
        if abs(num) < abs(limit)% If |num| exceeds limit
            if num < 0 % If num is negative
                answer = limit;
            elseif num > 0 % If num is positive
                answer = -limit;
            end
        end
    end
end


%% Color Functions

function logic = validColor(color)
% Function valid color
% Returns a logical value for wether an input is an acceptable color
% Inputs  : color - The input to be checked for acceptability
% Outputs : logic - Logical value for acceptability of input
% Globals : None
    testFig = figure(100); % Create a dummy test window
    test = rectangle('Position', [0,0,1,1]);
    logic = true; % Sets the baseline value
    try test = rectangle('Position', [0,0,1,1], 'FaceColor', color); % Detects if the color would cause an error if used in normal code
    catch
        logic = false; % If improper, set to false
    end
    % Delete test figure
    delete(test) 
    delete(testFig)
end

function fontCol = fontColor(background)
    % Function fontColor
    % Determines wether a font should be white or black based on background
    % Inputs  : background - color of the background that the text would be layed on top of
    % Outputs : fontCol - white or black color for the font
    % Globals : None

    % Converts into rgb components
    type = convertStringsToChars(background);
    if ischar(type) 
        if background(1) == '#' % If input is a hexadecimal
            background = hex2rgb(background);
        else % If input is a matlab color
            background = name2rgb(background);
        end
    end

    % Splits up rgb values into their components
    red = background(1);
    green = background(2);
    blue = background(3);

    % Runs a found algorithm to examine color
    if (red*255*0.299 + green*255*0.587 + blue*255*0.114) > 186 % Code taken from https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
        fontCol = '#000000'; % Black
    else
        fontCol = '#ffffff'; % White
    end
end

function rgb = hex2rgb(hexadec)
% Function hex2rgb
% Converts the hexadecimal to rgb triplet ( MAX [1,1,1] )
% Inputs  : hexadec - Initial hexadecimal value
% Outputs : rgb - converted rgb triplet 
% Globals : None

    if hexadec(1) == '#' % Eliminates # from input if needed
        hexadec = hexadec(1,2:7);
    end

    forNums = []; % Formatted numbers for each of the 6 characters
    for x = 1:6 % Formats the numbers from the character codes
        charCode = double(hexadec(x)); 
        if (charCode < 58)  && (charCode > 47) % Numbers
            forNums(x) = charCode-48;
        end
        if (charCode < 71)  && (charCode > 64) % Letters
            forNums(x) = charCode-64+10-1;
        end
    end

    for val = 1:3 % Creates the rgb vector
        rgb(val) = forNums(1+((val-1)*2))*16 + forNums(2+((val-1)*2));
    end

    rgb = rgb./255; % 255 max to 1 max

end

function rgb = name2rgb(colName)
    % Function name2rgb
    % Converts a color name to rgb triplet ( MAX [1,1,1] )
    % Inputs  : colName - Initial color name
    % Outputs : rgb - converted rgb triplet 
    % Globals : None

    testFig = figure(100); % Creates a dummy test figure
    mainTest = rectangle('Position', [0,0,1,1], 'EdgeColor', colName); % Creates a box using the input
    mainTrips = [1,0,0; % Holds the main matlab name color triplets
                 0,1,0;
                 0,0,1;
                 0,1,1;
                 1,0,1;
                 1,1,0;
                 0,0,0;
                 1,1,1];
    % Basically test the 8 default colors to match the input
    for x = 1:8 % Go through the 8 named colors
        test = rectangle('Position', [0,0,1,1], 'EdgeColor', mainTrips(x,:)); % Makes a box using each of the default colors
        if test.EdgeColor == mainTest.EdgeColor % If the input matches the current "test color"
            rgb = mainTrips(x,:); % Set rgb to the current value if correct
        end
    end

    % Delete all graphical objects
    delete(mainTest)
    delete(test)
    delete(testFig)

end


%% Pushbutton Callbacks

function mU(~, ~)
    % Function mU
    % Increments the clock up one minute
    % Inputs  : src - ID of keypress source
    %           event - handle of keypress event
    % Outputs : None
    % Globals : duration - How many total seconds there are to go
    global duration
    duration  = duration  + 60;
    showTime(duration)
end

function mD(~, ~)
    % Function mD
    % Increments the clock down one minute
    % Inputs  : src - ID of keypress source
    %           event - handle of keypress event
    % Outputs : None
    % Globals : duration - How many total seconds there are to go
    global duration 
    duration  = duration  - 60;
    showTime(duration)
end

function sU(~, ~)
    % Function sU
    % Increments the clock up one second
    % Inputs  : src - ID of keypress source
    %           event - handle of keypress event
    % Outputs : None
    % Globals : duration - How many total seconds there are to go
    global duration 
    duration  = duration  + 1;
    showTime(duration)
end

function sD(~, ~)
    % Function sD
    % Increments the clock down one second
    % Inputs  : src - ID of keypress source
    %           event - handle of keypress event
    % Outputs : None
    % Globals : duration - How many total seconds there are to go
    global duration 
    duration  = duration  - 1;
    showTime(duration)
end

function openSettings(~,~)
% Function openSettings
% Opens the settings screen and saves to workplace with "SAVE"
global rounds chips
run changeRoundSettings.m
% createFigWin()
end

function playOrPause(src, event)
    % Function playOrPause
    % Either plays or pauses the clock
    % Inputs  : src - ID of keypress source
    %           event - handle of keypress event
    % Outputs : None
    % Globals : see main code setup
    global startTime clock duration valid rounds

    if src.String == '⏵' % If the button was set to play
        valid = 1; % Let loop run
        if duration == 0
            nextRound()
        end
        startTime = tic; % Restart reference time
        
        if contains(rounds(cell2mat(rounds(1,2)),2), "/" )
            src.String = '⏸'; % Change button
            primaryCounter() % Main loop
        end
    elseif src.String == '⏸' % If the button was set to pause
        valid = 0; % End loop
        src.String = '⏵'; % Change button
    else
        disp('ERROR')
    end
end

function closeOut(src, event)
    % Function closeOut
    % Set a global to false when the figure window is closed
    % Inputs  : src - ID of keypress source
    %           event - handle of keypress event
    % Outputs : None
    % Globals : valid - Loop condition
    global valid
    valid = false; % Falsify logical global 
    pause(0.2)
    closereq % Normal MATLAB close window function
end


