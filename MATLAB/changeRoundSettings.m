clc

global rounds oldRound
oldRound = rounds(1,2);
% close all

run PokerRoundsFile.m



global chipCount
[~, chipCount] = size(chips);

global roundSize
roundSize = size(rounds);


createFigWin()

function createFigWin()
    % Function primaryCounter
    % While loop to tick the time down
    % Inputs  : None
    % Outputs : None
    % Globals : size - size of screen in pixels
    global size 

    % Create figure window  
%     figure(5)
    set(0, 'Units', 'inches')
    scrSize = get(0, 'ScreenSize');
    set(0, 'Units', 'pixels')
    fig1 = figure('Units', 'inches', 'Position', [0,0, scrSize(3), scrSize(4)], 'color', 'w', 'WindowState','maximized');
    % Get dimensions of figure window
    set(fig1, 'Units', 'pixels')
    size(1) = fig1.Position(3);
    size(2) = fig1.Position(4);
    % Format figure properties
    fig1.Name = 'Clock Settings';
    fig1.NumberTitle = 'off';
    fig1.ToolBar = 'none';
%     set(fig1, 'CloseRequestFcn', @closeOut)
    % Axis manipulation

    hold on
    axis off
% %     axis equal
%     axis manual
    % Next funtions
    placeChipsBoxes()
    placeRoundBoxes()
    placeTimeBox()
    placeSaveButton()

end

function placeChipsBoxes()
global chipCount chips chipBoxes
uicontrol('Style','pushbutton','Position',[80,560,50,50],'String','<', 'FontSize', 30, 'Callback', @saveVariables)
uicontrol('Style','pushbutton','Position',[140,560,50,50],'String','>', 'FontSize', 30, 'Callback', @saveVariables)
for x = 1:chipCount
    chipBoxes(1,x) = uicontrol('Style','edit','Position',[20+x*60,510,50,40],'String',chips(1,x), 'FontSize', 10);
end
for x = 1:chipCount
    chipBoxes(2,x) = uicontrol('Style','edit','Position',[20+x*60,460,50,40],'String',chips(2,x), 'FontSize', 10);
end
distib = [20,20,10,5];
for x = 1:4
    uicontrol('Style','text','Position',[30+x*60,430,30,20],'String',distib(x), 'FontSize', 10, 'BackgroundColor', 'w');
end


end 

function placeRoundBoxes()
global chipCount rounds roundSize roundBoxes chips
baseX = 100;
baseY = 430;
uicontrol('Style','pushbutton','Position',[baseX-60,baseY-40,30,30],'String','+', 'FontSize', 20, 'Callback', @saveVariables)
uicontrol('Style','pushbutton','Position',[baseX-60,baseY-80,30,30],'String','-', 'FontSize', 20, 'Callback', @saveVariables)
for y = 1:roundSize(1)-1 % For each row
    for x = 1:roundSize(2) % For each column
        if baseY-y*40 < 10 % realign when it passes the x axis
            baseX = baseX + roundSize(2)*60 +30;
            baseY = baseY + 560;
        end
        switch x % Special settings for each type
            case 1 
                xFactor = 70;
                xOver = -20;
                Bstyle = 'listbox';
                switch char(rounds(y+1,x)) % Scan Types and set box values
                    case 'Round'
                        firstVal = 1;
                    case 'Break'
                        firstVal = 2;
                    case 'Color-Up'
                        firstVal = 3;
                    case 'Unlock'
                        firstVal = 4;
                end
                roundBoxes(y, x) = uicontrol('Style',Bstyle,'Position',[baseX+xOver,baseY-y*40,xFactor,30], ...
                    'FontSize', 9, 'String', {'Round', 'Break', "C-Up", "Unlock"}, 'Value', firstVal);
            case 2
                xFactor = 80;
                xOver = 60;
                Bstyle = 'edit';
                roundBoxes(y, x) = uicontrol('Style',Bstyle,'Position',[baseX+xOver,baseY-y*40,xFactor,30],'String',rounds(y+1,x), 'FontSize', 10);
            case num2cell(3:roundSize(2))
                xFactor = 30;
                xOver = x*45+15;
                Bstyle = 'togglebutton';
                roundBoxes(y, x) = uicontrol('Style',Bstyle,'Position',[baseX+xOver,baseY-y*40,xFactor,30],'String',chips(2, x-2), 'FontSize', 10);
                if cell2mat(rounds(y+1,x)) == 1 % Enable all true buttons
                    set(roundBoxes(y, x), 'Value', true)
                end

        end

%         if x == 1 % Fix first boxes
%             set(roundBoxes(y, x), 'Items', {'Round', 'Break', "Color-Up", "Unlock"})
%         end
%         if strcmpi({Bstyle}, {'togglebutton'}) % Fix Logical boxes
%             set(roundBoxes(y, x), 'String', chips(2, x-2)) % Correct String
% 
%         end
    end
end

 
end

function placeTimeBox()
global minPerRnd timeBox
timeBox = uicontrol('Style','edit','Position',[200,560,50,50],'String',minPerRnd, 'FontSize', 20);

end

function placeSaveButton()
uicontrol('Style','pushbutton','Position',[1100,300,100,50],'String','SAVE', 'FontSize', 12, 'Callback', @saveVariables)

end

function codifyRounds()
% Put rounds data to file
global chipCount rounds roundSize roundBoxes chips
rounds = num2cell(zeros(roundSize));
% rounds(1,1:2) = {'Curr', oldRound}
rounds(1,1:2) = {'Curr', 2};
for y = 1:roundSize(1)-1 % For each row
    for x = 1:roundSize(2) % For each column
        switch x % Special settings for each type
            case 1 % Main type
                val = get(roundBoxes(y,x), 'Value');
                switch val     % {'Round', 'Break', 'C-Up', "Unlock"}
                    case 1
                        val = 'Round';
                    case 2
                        val = 'Break';
                    case 3
                        val = 'Color-Up';
                    case 4
                        val = 'Unlock';
                end
                rounds(y+1, x) = {char(val)}; %%%%%%%%
            case 2 % Description
                rounds(y+1, x) = {char(get(roundBoxes(y,x), 'String'))};
            case num2cell(3:roundSize(2)) % Logical buttons
                rounds(y+1, x) = num2cell(get(roundBoxes(y,x), 'Value'));
        end
    end
    
end
end

function codifyChips()
% put chips data to file
global chipCount chipBoxes chips timeBox minPerRnd
disp(chips)
chipCount = size(chips);
chips = num2cell(zeros(chipCount));
for y = 1:chipCount(1) % For each row %%%%%%%%%%%REARRANGE
    for x = 1:chipCount(2) % For each column
        switch y
            case 1 % Description
                chips(y, x) = (get(chipBoxes(y,x), 'String'));
            case 2 % Logical buttons
                chips(y, x) = (get(chipBoxes(y,x), 'String'));
        end
    end
    
end

minPerRnd = str2double(timeBox.String);

chips
end

function saveVariables(src,event)
global chipCount rounds roundSize roundBoxes chips minPerRnd oldRound
codifyRounds()
codifyChips()
% pause(3)
switch src.String
    case '<' % Remove last
        % Add to chips
        chips(:, end) = [];
        % Add to rounds
        rounds(:,end) = [];
    case '>' % Add another
        % Add to chips
        chips(1, chipCount(2)+1) = {'__'};
        chips(2, chipCount(2)+1) = {'__'};
        % Add to rounds
        rounds = [rounds, num2cell(zeros(roundSize(1),1))];
    case '+'
        rounds(end+1, :) = {0};
        rounds(end,1) = {'Round'};
        rounds(end,2) = {'___'};
    case '-'
        rounds(end,:) = [];
end

%%% Insert Save to file code here %%%
delete('PokerRoundsFile.m')
diary('PokerRoundsFile.m')
diary on
disp('global rounds chips minPerRnd')
printArray(chips, 0, 'chips', 0) % Chips
disp(['minPerRnd = ', num2str((minPerRnd)), ';'])
printArray(rounds, 3, 'rounds', 0) % Rounds
diary off
%%% End save file %%%
% yui= char({4})
clc
rounds(1,2) = oldRound;
if strcmp(src.String, 'SAVE')
    closereq
else

    run changeRoundSettings.m
    pause(2)
    closereq
end
end

function printArray(array, indSpace, name, comms)
    % Function printArray
    % Prints an array assignment to the command window
    % Inputs  : array - the array that will be printed (array)
    %           indSpace - the minimum amount of characters between commas (number) !!! Gets weird above 8
    %           name - the variable that the array will be assigned to (string)
    %           comms - a value of 1 will cause comments for r and c numbers (number 0 or 1)
    % Outputs : None (Command Window)

    if class(indSpace) ~= 'double'
        disp('!!!indSpace must be a double!!!')
        return
    end
    if class(name) ~= 'char'
        disp('!!!name must be a char!!!')
        return
    end
    if (class(comms) ~= "double") || not((comms==1)||(comms==0))
        disp('!!!comms must be a double of either 1 or 0!!!')
        return
    end

    
    [rows, cols] = size(array);  % Finds array dimensions    
    %     format = ['%' num2str(indSpace) '.0f,'];  % Creates the formating style for the values
    %     rhFormat = ['%' num2str(indSpace) '.0f;'];  % Creates the formating style for the higher rightmost values
    %     rbFormat = ['%' num2str(indSpace) '.0f];\n'];  % Creates the formating style for the final value
    indent = repmat(' ', 1, length(name)+4);  % Finds the indentation used for following lines
    for x = 1:comms  % Print top comment line % For statement for collapsability
        fprintf('%s', ['%', repmat(' ', 1, length(name)+2)])
        for c = 1:cols
            fprintf(['%' num2str(indSpace)+1 '.0f'], c)
        end
        fprintf('\n')
    end
    
    fprintf('%s = {', name)  % Prints the declaration variable
    for r = 1:rows % Repeat for each row
        for c = 1:cols % Repeat for all but the last column
            if strcmp(class(cell2mat(array(r,c))),'double')
                fprintf(['%' num2str(indSpace) 's'], num2str(cell2mat(array(r,c))))  % Displays most values
            else
                fprintf([char(39), '%', num2str(indSpace), 's', char(39)], char(array(r,c)))  % Displays most values
            end
        if c ~= cols
            fprintf(',')
        else
            if r ~= rows % Prints the ending column values
                fprintf(';')  % Displays nonlast right values
                if comms == 1 % Higher Right side comment
                    fprintf(['%' num2str(indSpace)+1 's %0.0f\n'], '%',r)
                else
                    fprintf('\n')
                end
                fprintf('%s', indent) % Start next line
            else % Prints the final array value
                fprintf('};')  % Displays final value
                if comms == 1 % Final right side comment
                    fprintf(['%' num2str(indSpace) 's %0.0f\n'], '%',r)
                end
            end
        end
        end
    
    
    end
    
    fprintf('\n')  % Extra white space


end


