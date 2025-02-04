using System;
using System.Collections.Generic;

public class CPHInline
{
    public bool Execute()
    {
        CPH.TryGetArg("message", out string chatMessage);
        CPH.TryGetArg("userName", out string userName);
        CPH.TryGetArg("eventSource", out string eventSource);
        CPH.TryGetArg("bits", out int bits);

        if (chatMessage.Split(' ')[0].Equals("position", StringComparison.OrdinalIgnoreCase))
        {
//            CPH.LogInfo("The first word is 'position'.");

            // Retrieve the existing lists for both 'priority_order' and 'order'
            var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
            var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
//            CPH.SendMessage($"The first word is 'position' and the priorityOrder count is {priorityOrder.Count} and the commandOrder count is {commandOrder.Count}.");

            // Search for the user in the priorityOrder list
            int userIndex = -1; // -1 means not found
            for (int i = 0; i < priorityOrder.Count; i++)
            {
                if (priorityOrder[i][0] == userName)
                {
                    userIndex = i;
                    CPH.SendMessage($"{userName}, You are currently at position {i + 1} out of {priorityOrder.Count} in the priority list.");
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
                        CPH.SendMessage($" 1- {userName}, You are currently at position {i + 1} out of {commandOrder.Count} in the regular list.");
                        break;
                    }
                }
            }
//            CPH.SendMessage($"{userIndex}");

            // If the user was not found in either list
            if (userIndex == -1)
            {
//                CPH.LogInfo($"User {userName} not found in priority or regular order lists.");
                CPH.SendMessage($"User {userName} not found in priority or regular order lists.");
            }

            // Your main code goes here
            return true;
        }
        else {
        	return true;
        	}
    }
}