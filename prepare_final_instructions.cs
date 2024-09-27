using System;
using System.Collections.Generic;  // Use non-generic collection

public class CPHInline
{
    public bool Execute()
    {
        // Retrieve the existing list of lists for both 'priority_order' and 'order'
        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();

        // Check if there are any items in the priorityOrder list first
        if (priorityOrder.Count > 0)
        {
            // Extract the first item (which is a list of strings)
            var firstCommand = priorityOrder[0];

            // Log and process the first command from priorityOrder
            CPH.LogInfo("Priority command: " + string.Join(", ", firstCommand));
            CPH.SendMessage($"[Priority] Now serving ~ frequency {firstCommand[2]} Hz with color {firstCommand[1]} for user {firstCommand[0]}.");
            CPH.SetGlobalVar("current_user", firstCommand[0]);
            CPH.SetGlobalVar("current_color", firstCommand[1]);
            CPH.SetGlobalVar("current_frequency", firstCommand[2]);
            CPH.SetGlobalVar("bits_donated", firstCommand[3]);
            // Remove the first item from the priorityOrder list
            priorityOrder.RemoveAt(0);

            // Update the global variable to reflect the modified priorityOrder list
            CPH.SetGlobalVar("priority_order", priorityOrder);
        }
        // If priorityOrder is empty, check the regular commandOrder list
        else if (commandOrder.Count > 0)
        {
            // Extract the first item (which is a list of strings)
            var firstCommand = commandOrder[0];

            // Log and process the first command from commandOrder
            CPH.LogInfo("Regular command: " + string.Join(", ", firstCommand));
            CPH.SendMessage($"Now serving ~ frequency {firstCommand[2]} Hz with color {firstCommand[1]} for user {firstCommand[0]}.");
            PH.SetGlobalVar("current_user", firstCommand[0]);
            CPH.SetGlobalVar("current_color", firstCommand[1]);
            CPH.SetGlobalVar("current_frequency", firstCommand[2]);
            // Remove the first item from the commandOrder list
            commandOrder.RemoveAt(0);

            // Update the global variable to reflect the modified commandOrder list
            CPH.SetGlobalVar("order", commandOrder);
        }
        else
        {
            CPH.LogInfo("Both priority order and regular command order lists are empty.");
        }

        // Your main code goes here
        return true;
    }
}
