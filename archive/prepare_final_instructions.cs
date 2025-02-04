using System;
using System.Collections.Generic;  // Use non-generic collection

public class CPHInline
{
    public bool Execute()
    {
        // Retrieve the existing list of lists for both 'priority_order' and 'order'
        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();

        // Set the variable for the number of people in the queues
        CPH.SetGlobalVar("priority_queue_count", priorityOrder.Count);
        CPH.SetGlobalVar("regular_queue_count", commandOrder.Count);

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

            // Check if there is a next user in the queue
            if (priorityOrder.Count > 1)
            {
                var nextCommand = priorityOrder[1];
                CPH.SetGlobalVar("next_user", nextCommand[0]);
                CPH.SetGlobalVar("next_color", nextCommand[1]);
                CPH.SetGlobalVar("next_frequency", nextCommand[2]);
            }
            else if (commandOrder.Count > 0)
            {
                // If no more priority commands, check the regular order for the next user
                var nextCommand = commandOrder[0];
                CPH.SetGlobalVar("next_user", nextCommand[0]);
                CPH.SetGlobalVar("next_color", nextCommand[1]);
                CPH.SetGlobalVar("next_frequency", nextCommand[2]);
            }
            else
            {
                // Clear next variables if no users are available
                CPH.SetGlobalVar("next_user", null);
                CPH.SetGlobalVar("next_color", null);
                CPH.SetGlobalVar("next_frequency", null);
            }

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
            CPH.SetGlobalVar("current_user", firstCommand[0]);
            CPH.SetGlobalVar("current_color", firstCommand[1]);
            CPH.SetGlobalVar("current_frequency", firstCommand[2]);

            // Check if there is a next user in the regular order queue
            if (commandOrder.Count > 1)
            {
                var nextCommand = commandOrder[1];
                CPH.SetGlobalVar("next_user", nextCommand[0]);
                CPH.SetGlobalVar("next_color", nextCommand[1]);
                CPH.SetGlobalVar("next_frequency", nextCommand[2]);
            }
            else
            {
                // Clear next variables if no users are available
                CPH.SetGlobalVar("next_user", null);
                CPH.SetGlobalVar("next_color", null);
                CPH.SetGlobalVar("next_frequency", null);
            }

            // Remove the first item from the commandOrder list
            commandOrder.RemoveAt(0);

            // Update the global variable to reflect the modified commandOrder list
            CPH.SetGlobalVar("order", commandOrder);
        }
        else
        {
            CPH.LogInfo("Both priority order and regular command order lists are empty.");
            // Clear next variables if no users are available
            CPH.SetGlobalVar("next_user", null);
            CPH.SetGlobalVar("next_color", null);
            CPH.SetGlobalVar("next_frequency", null);
        }

        // Your main code goes here
        return true;
    }
}
