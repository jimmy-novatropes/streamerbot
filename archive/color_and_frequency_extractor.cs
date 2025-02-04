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
            CPH.LogInfo("The first word is 'position'.");

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
                        CPH.SendMessage($"{userName}, You are currently at position {i + 1} out of {commandOrder.Count} in the regular list.");
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

        if (chatMessage.IndexOf("Processing", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("Now Serving", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("found in", StringComparison.OrdinalIgnoreCase) >= 0 ||
            chatMessage.IndexOf("position", StringComparison.OrdinalIgnoreCase) >= 0 ||
            eventSource != "twitch")
        {
            return true;
        }

        if (string.IsNullOrEmpty(chatMessage) || string.IsNullOrEmpty(userName))
        {
            CPH.LogWarn("Root: The required variables 'message' or 'userName' are missing.");
            return false;
        }

        if (TryParseFrequencyAndColor(chatMessage, out int frequency, out string color))
        {
            if (!ProcessFrequencyAndColor(frequency, color, userName))
            {
                return false;
            }

            CPH.LogInfo($"Root: Extracted frequency: {frequency} Hz, color: {color}");
            string stringFrequency = frequency.ToString();

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
                    targetOrder[i][2] = stringFrequency;
                    if (bits > 0)
                    {
                        targetOrder[i][3] = bits.ToString();
                    }

                    // Send an update message since the user is being updated
                    CPH.SendMessage($"Updating data for {userName}: {frequency} Hz with color {color}.");
                    
                    userFound = true;
                    break;
                }
            }

            // If the user was not found, add a new entry to the target list
            if (!userFound)
            {
                var newCommand = new List<string> { userName, color, stringFrequency };
                targetOrder.Add(newCommand);

                // Send a message for new entries
                if (bits > 0)
                {
                    CPH.SendMessage($"[Priority] Processing frequency {frequency} Hz with color {color} from {userName} (bits: {bits}).");
                }
                else
                {
                    CPH.SendMessage($"Processing frequency {frequency} Hz with color {color} from {userName}.");
                }
            }

            // Log the updated lists for debugging purposes
            CPH.LogInfo("Priority Order:");
            foreach (var command in priorityOrder)
            {
                CPH.LogInfo($"User: {command[0]}, Color: {command[1]}, Frequency: {command[2]}");
            }

            CPH.LogInfo("Regular Order:");
            foreach (var command in commandOrder)
            {
                CPH.LogInfo($"User: {command[0]}, Color: {command[1]}, Frequency: {command[2]}");
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
            
            CPH.LogInfo($"Root: Message from {userName}: '{chatMessage}' does not match the expected format.");
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
        if (!string.IsNullOrEmpty(currentUser) && combinedQueue.Count > 1)
        {
            // The next user is the one after the current one (if available)
            var nextUser = combinedQueue[0];
            // var nextUser = combinedQueue[1];
            CPH.SetGlobalVar("next_user", nextUser[0]);
            CPH.SetGlobalVar("next_color", nextUser[1]);
            CPH.SetGlobalVar("next_frequency", nextUser[2]);
        }
        else
        {
            // If no next user is available, clear the next user info
            CPH.SetGlobalVar("next_user", null);
            CPH.SetGlobalVar("next_color", null);
            CPH.SetGlobalVar("next_frequency", null);
        }
    }

    private bool TryParseFrequencyAndColor(string message, out int frequency, out string color)
    {
        frequency = 0;
        color = string.Empty;

        message = message.Replace(",", " ");
        string[] words = message.Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);

        if (words.Length >= 2)
        {
            string frequencyStr = "";
            int index = 0;

            while (index < words.Length)
            {
                string word = words[index].ToLower();

                if (word.Contains("hz"))
                {
                    word = word.Replace("hz", "").Trim();

                    if (!string.IsNullOrEmpty(word))
                    {
                        frequencyStr += word;
                    }

                    index++;
                    break;
                }
                else if (int.TryParse(word, out _))
                {
                    frequencyStr += word;
                    index++;
                }
                else
                {
                    if (word == "hz")
                    {
                        index++;
                        break;
                    }
                    else
                    {
                        CPH.LogWarn($"Parsing: Unexpected word '{word}' in frequency part.");
                        return false;
                    }
                }
            }

            if (int.TryParse(frequencyStr, out frequency))
            {
                if (index < words.Length)
                {
                    color = string.Join(" ", words, index, words.Length - index).Trim().ToLower();
                    return true;
                }
                else
                {
                    CPH.LogWarn("Parsing: No color specified.");
                    return false;
                }
            }
            else
            {
                CPH.LogWarn($"Parsing: Could not parse frequency '{frequencyStr}' as an integer.");
                return false;
            }
        }
        else
        {
            return false;
        }
    }

    private bool ProcessFrequencyAndColor(int frequency, string color, string userName)
    {
        string[] supportedColors = { "red", "green", "blue", "yellow", "purple", "cyan" };
        CPH.LogInfo($"-------------------------Processing frequency {frequency} Hz with color {color}.");

        if (!Array.Exists(supportedColors, c => c.Equals(color, StringComparison.OrdinalIgnoreCase)))
        {
            CPH.SendMessage($"Sorry {userName}, the color '{color}' is not supported.");
            return false;
        }

        return true;
    }
}
