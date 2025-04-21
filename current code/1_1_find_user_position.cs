/*
 * Code to check a user's position in either the priority list or regular command list
 * This script responds to the "position" command in chat
 */

using System;
using System.Collections.Generic;

public class CPHInline
{
    // Constants for repeated strings
    private const string POSITION_COMMAND = "position";
    private const string PRIORITY_LIST_VAR = "priority_order";
    private const string COMMAND_LIST_VAR = "order";
    
    public bool Execute()
    {
        // Get arguments from the event
        CPH.TryGetArg("message", out string chatMessage);
        CPH.TryGetArg("userName", out string userName);
        CPH.TryGetArg("eventSource", out string eventSource);
        CPH.TryGetArg("bits", out int bits);

        // Check if the command is "position"
        if (IsPositionCommand(chatMessage))
        {
            // Get the lists from global variables
            var priorityList = CPH.GetGlobalVar<List<List<string>>>(PRIORITY_LIST_VAR) ?? new List<List<string>>();
            var commandList = CPH.GetGlobalVar<List<List<string>>>(COMMAND_LIST_VAR) ?? new List<List<string>>();

            // Check user position in both lists
            CheckUserPosition(userName, priorityList, commandList);
            
            return true;
        }
        
        return true;
    }
    
    /// <summary>
    /// Checks if the message starts with the position command
    /// </summary>
    private bool IsPositionCommand(string message)
    {
        if (string.IsNullOrEmpty(message))
            return false;
            
        return message.Split(' ')[0].Equals(POSITION_COMMAND, StringComparison.OrdinalIgnoreCase);
    }
    
    /// <summary>
    /// Checks the user's position in both lists and sends appropriate messages
    /// </summary>
    private void CheckUserPosition(string userName, List<List<string>> priorityList, List<List<string>> commandList)
    {
        // Check in priority list first
        int position = FindUserInList(userName, priorityList);
        CPH.TryGetArg("eventSource", out string eventSource);
        
        if (position >= 0)
        {
            if (eventSource == "Twitch")
            {
                CPH.SendMessage($"{userName}, You are currently at position {position + 1} out of {priorityList.Count} in the priority list.");
            }
            else if (eventSource == "YouTube")
            {
                CPH.SendYouTubeMessage($"{userName}, You are currently at position {position + 1} out of {priorityList.Count} in the priority list.");
            }
//            CPH.SendMessage($"{userName}, You are currently at position {position + 1} out of {priorityList.Count} in the priority list.");
            return;
        }
        
        // If not in priority list, check in command list
        position = FindUserInList(userName, commandList);
        
        if (position >= 0)
        {
            if (eventSource == "Twitch")
            {
                CPH.SendMessage($"{userName}, You are currently at position {position + 1} out of {commandList.Count} in the regular list.");
            }
            else if (eventSource == "YouTube")
            {
                CPH.SendYouTubeMessage($"{userName}, You are currently at position {position + 1} out of {commandList.Count} in the regular list.");
            }
//            CPH.SendMessage($"{userName}, You are currently at position {position + 1} out of {commandList.Count} in the regular list.");
            return;
        }
        
        // User not found in either list
        if (eventSource == "Twitch")
        {
            CPH.SendMessage($"User {userName} not found in priority or regular order lists.");
        }
        else if (eventSource == "YouTube")
        {
            CPH.SendYouTubeMessage($"User {userName} not found in priority or regular order lists.");
        }
//        CPH.SendMessage($"User {userName} not found in priority or regular order lists.");
    }
    
    /// <summary>
    /// Finds a user in a list and returns their index, or -1 if not found
    /// </summary>
    private int FindUserInList(string userName, List<List<string>> list)
    {
        for (int i = 0; i < list.Count; i++)
        {
            if (list[i][0] == userName)
            {
                return i;
            }
        }
        
        return -1;
    }
}