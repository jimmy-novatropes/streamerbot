using System;
using System.Collections.Generic;  // Use non-generic collection

public class CPHInline
{
    public bool Execute()
    {
        // Try to get the userName argument
        if (!CPH.TryGetArg("userName", out string userName))
        {
            CPH.LogInfo("userName argument not found.");
            return false;  // Exit if the userName argument is not provided
        }

        CPH.LogInfo($"Searching for user: {userName}");

        // Retrieve the existing lists for both 'priority_order' and 'order'
        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();

        // Search for the user in the priorityOrder list
        int userIndex = -1; // -1 means not found
        for (int i = 0; i < priorityOrder.Count; i++)
        {
            if (priorityOrder[i][0] == userName)
            {
                userIndex = i;
                CPH.SendMessage($"{userName}, You are currently at position {i+1} out of {priorityOrder.Count} in the priority list.");
                break;
            }
        }

        // If not found in the priorityOrder list, search in the commandOrder list
        if (userIndex == -1)
        {
            for (int i = 0; i < commandOrder.Count; i++)
            {
                if (commandOrder[i][0] == userName)
                {
                    userIndex = i;
                    CPH.SendMessage($"{userName}, You are currently at position {i+1} out of {commandOrder.Count} in the regular list.");
                    break;
                }
            }
        }

        // If the user was not found in either list
        if (userIndex == -1)
        {
            CPH.LogInfo($"User {userName} not found in priority or regular order lists.");
        }

        // Your main code goes here
        return true;
    }
}
