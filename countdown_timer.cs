using System;
using System.Threading; // Import the threading library for sleep functionality
using System.Collections.Generic;

public class CPHInline
{
    public bool Execute()
    {
        // Set the initial timer value in seconds (e.g., 5 minutes = 300 seconds)
        int timeLeft = 90; // 5:00 in seconds
        // Retrieve the existing lists for both 'priority_order' and 'order'
        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
        if (priorityOrder.Count > 0 || commandOrder.Count > 0)
        {
            // Start the countdown timer
            // Update the global variable with the new time
            CPH.SetGlobalVar("timer_active", 1);
            while (timeLeft > 0)
            {
                // Convert timeLeft to minutes:seconds format
                int minutes = timeLeft / 60;
                int seconds = timeLeft % 60;

                // Format the time as "MM:SS"
                string formattedTime = $"{minutes:D2}:{seconds:D2}";

                // Update the global variable with the new time
                CPH.SetGlobalVar("time_left", formattedTime);

                // Run an action on every 5-second decrement
                CPH.RunActionById("3269fdd1-f0f0-4141-b273-b9b84c7170d6"); // Replace "YourActionName" with the action name you want to run

                // Wait for 5 seconds (5000 milliseconds)
                Thread.Sleep(980);

                // Decrement the timer by 5 seconds
                timeLeft -= 1;
            }

            // Once the timer reaches 0, you can trigger a final action
            CPH.SetGlobalVar("time_left", "00:00");
            // Run an action on every 5-second decrement
            CPH.RunActionById("3269fdd1-f0f0-4141-b273-b9b84c7170d6");

            return true;
        }
        else
        {
            CPH.SetGlobalVar("timer_active", 0);
            CPH.LogInfo("No users in the queue to start the countdown timer.");
            return false;
        }
    }
}
