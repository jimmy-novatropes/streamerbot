/*
This C# code defines a command handler that processes chat commands, primarily focused on identifying a user’s position in
priority or regular queues, and parsing mode and color information. The `Execute` method first verifies input arguments
(`message`, `userName`, `eventSource`, and `bits`). If the chat command starts with "position," the handler checks both
`priorityOrder` and `commandOrder` queues for the user and provides a position update. It also handles custom commands involving
mode and color, where valid data is extracted and stored or updated in the appropriate queue (`priorityOrder` if bits are used).
The code includes helper functions for mode and color validation, logs the updated queue lists, sets the next user,
and dynamically updates queue counts.
*/

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
//        int bits = 0;

        //CPH.SendMessage($"Received message: {chatMessage} from @{userName} (source: {eventSource}) with bits: {bits}");

        if (chatMessage.IndexOf("Adding ", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("Now Serving ~", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("found in", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("position", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("does not match the expected format", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("Updating data for", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("is the timer active?", StringComparison.OrdinalIgnoreCase) >= 0
//            eventSource != "twitch"
            )
        {
            return true;
        }

        if (string.IsNullOrEmpty(chatMessage) || string.IsNullOrEmpty(userName))
        {
            CPH.LogWarn("Root: The required variables 'message' or 'userName' are missing.");
            return false;
        }

//        if (TryParseModeAndColor(chatMessage, out int mode, out string color, out string direction))
        if (TryParseModeAndColor(chatMessage, out int mode, out string color))
        {
//            if (!ProcessModeAndColor(mode, color, direction, userName))
            if (!ProcessModeAndColor(mode, color, userName))
            {
                return false;
            }

            CPH.LogInfo($"Root: Extracted mode: {mode} , color: {color}");
            string stringMode = mode.ToString();

            // Retrieve the existing list of lists for both 'priority_order' and 'order'
            var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
            var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();

            // Variable to check if the user is already in the list
            bool userFound = false;

            // Decide whether to work with priorityOrder or commandOrder based on the bits
            var targetOrder = bits > 0 ? priorityOrder : commandOrder;

            // Iterate through the selected list to check if the user is already present
            for (int i = 0; i < targetOrder.Count; i++)
            {
                if (targetOrder[i][0] == userName)
                {
                    // Update the existing entry if the user is found
                    targetOrder[i][1] = color;
                    targetOrder[i][2] = stringMode;
//                    targetOrder[i][3] = direction;
                    if (bits > 0)
                    {
                        targetOrder[i][4] = bits.ToString();
                    }

                    // Send an update message since the user is being updated
//                    CPH.SendMessage($"Updating data for @{userName} Mode:{mode}, color:{color}, direction: {direction}.");
                    CPH.SendMessage($"Updating data for @{userName} Mode:{mode}, color:{color}.");

                    userFound = true;
                    break;
                }
            }

            // If the user was not found, add a new entry to the target list
            if (!userFound)
            {
//                var newCommand = new List<string> { userName, color, stringMode, direction };
//                targetOrder.Add(newCommand);

                // If the user was not found, add a new entry ONLY to the appropriate list
                if (bits != 0)
                {
//                    priorityOrder.Add(new List<string> { userName, color, stringMode, direction, bits.ToString() });
//                    CPH.SendMessage($"[Priority] Adding @{userName} to queue with mode {mode}, color {color}, direction {direction} (bits: {bits}).");
                    priorityOrder.Add(new List<string> { userName, color, stringMode, bits.ToString() });
                    CPH.SendMessage($"[Priority] Adding @{userName} to queue with mode {mode}, color {color} (bits: {bits}).");
                }
                else if (bits == 0)
                {
//                    commandOrder.Add(new List<string> { userName, color, stringMode, direction});
//                    CPH.SendMessage($"Adding @{userName} to queue with mode {mode}, color {color}, direction {direction}.");
                    commandOrder.Add(new List<string> { userName, color, stringMode});
                    CPH.SendMessage($"Adding @{userName} to queue with mode {mode}, color {color}.");
                }
            }

            // Log the updated lists for debugging purposes
            CPH.LogInfo("Priority Order:");
            foreach (var command in priorityOrder)
            {
                CPH.LogInfo($"User: {command[0]}, Color: {command[1]}, Mode: {command[2]}");
            }

            CPH.LogInfo("Regular Order:");
            foreach (var command in commandOrder)
            {
                CPH.LogInfo($"User: {command[0]}, Color: {command[1]}, Mode: {command[2]}");
            }

            // Update the global variables for both lists
            CPH.SetGlobalVar("priority_order", priorityOrder);
            CPH.SetGlobalVar("order", commandOrder);

            // Call the method to only set the next user if necessary
            SetNextUserIfAvailable(priorityOrder, commandOrder);

            // Update the count of users in both queues
            CPH.SetGlobalVar("priority_queue_count", priorityOrder.Count);
            CPH.SetGlobalVar("regular_queue_count", commandOrder.Count);

            CPH.Wait(2000);
        }
        else
        {
//            CPH.SendMessage($"Sorry @{userName}, the message '{chatMessage}' does not match the expected format.");
            CPH.LogInfo($"Root: Message from @{userName}: '{chatMessage}' does not match the expected format.");
        }
        return true;
    }

    private void SetNextUserIfAvailable(List<List<string>> priorityOrder, List<List<string>> commandOrder)
    {
        // Retrieve the current user to check if we need to set the next one
        var currentUser = CPH.GetGlobalVar<string>("current_user");

        // Combine both lists to process them as a single queue
        List<List<string>> combinedQueue = new List<List<string>>();
        combinedQueue.AddRange(priorityOrder);
        combinedQueue.AddRange(commandOrder);

        // Check for the next user only if the current user is already set
        if (!string.IsNullOrEmpty(currentUser) && combinedQueue.Count >=0 )
        {
            // The next user is the one after the current one (if available)
            var nextUser = combinedQueue[0];
            // var nextUser = combinedQueue[1];
            CPH.SetGlobalVar("next_user", nextUser[0]);
            CPH.SetGlobalVar("next_color", nextUser[1]);
            CPH.SetGlobalVar("next_mode", nextUser[2]);
//            CPH.SetGlobalVar("next_direction", nextUser[3]);
        }
        else
        {
            // If no next user is available, clear the next user info
            CPH.SetGlobalVar("next_user", null);
            CPH.SetGlobalVar("next_color", null);
            CPH.SetGlobalVar("next_mode", null);
//            CPH.SetGlobalVar("next_direction", null);
        }
    }

//    private bool TryParseModeAndColor(string message, out int mode, out string color, out string direction)
    private bool TryParseModeAndColor(string message, out int mode, out string color)
    {
        mode = 0;
        color = string.Empty;
        string modeStr = "";
//        direction = "";

        message = message.Replace(",", " ");
        string[] words = message.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        //CPH.SendMessage($"{words.Length}}");
        if (words.Length == 2){

            modeStr = words[0];
            color = words[1];
            int.TryParse(modeStr, out mode);
//            direction = "same";

            return true;
        }
        else if (words.Length == 3){

            modeStr = words[0];
            color = words[1];
            int.TryParse(modeStr, out mode);
//            direction = words[2];

            return true;
        }
        return false;

    }

//    private bool ProcessModeAndColor(int mode, string color, string direction, string userName)
    private bool ProcessModeAndColor(int mode, string color, string userName)
    {
        string[] supportedColors = { "red", "green", "blue", "yellow", "purple", "cyan", "magenta", "white" };
        int[] supportedModes = { 1, 2, 3, 4, 5, 6, -1, -2, -3, -4, -5, -6 };
//        CPH.LogInfo($"-----Adding  mode {mode}  with color {color} and direction {direction} for @{userName}-------");
        CPH.LogInfo($"-----Adding  mode {mode}  with color {color} for @{userName}-------");

        if (!Array.Exists(supportedColors, c => c.Equals(color, StringComparison.OrdinalIgnoreCase)))
        {
            CPH.SendMessage($"Sorry @{userName}, the color '{color}' is not supported.");
            return false;
        }
        if (!Array.Exists(supportedModes, m => m == mode))
        {
            CPH.SendMessage($"Sorry @{userName}, the mode '{mode}' is not supported.");
            return false;
        }

        return true;
    }
}
