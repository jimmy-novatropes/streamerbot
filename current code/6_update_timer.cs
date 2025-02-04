using System;
using System.Threading; // Import the threading library for sleep functionality

public class CPHInline
{
    public bool Execute()
    {
        // Set the initial timer value in seconds (e.g., 5 minutes = 300 seconds)
        int timeLeft = 300; // 5:00 in seconds

        while (timeLeft > 0)
        {
            // Convert timeLeft to minutes:seconds format
            int minutes = timeLeft / 60;
            int seconds = timeLeft % 60;

            // Format the time as "MM:SS"
            string formattedTime = $"{minutes:D2}:{seconds:D2}";

            // Update the global variable with the new time
            CPH.SetGlobalVar("sculpture_time_left", formattedTime);

            // Run an action on every 5-second decrement 7 - Update the sculpture timer display -  ec0c3cf3-c7f8-4989-9968-d95a34dfe1df
            CPH.RunActionById("ec0c3cf3-c7f8-4989-9968-d95a34dfe1df"); // Replace "YourActionName" with the action name you want to run

            // Wait for 5 seconds (5000 milliseconds)
            Thread.Sleep(900);

            // Decrement the timer by 5 seconds
            timeLeft -= 1;
        }

        // Once the timer reaches 0, you can trigger a final action
        CPH.SetGlobalVar("sculpture_time_left", "00:00");
        // Run an action on every 5-second decrement 7 - Update the sculpture timer display -  ec0c3cf3-c7f8-4989-9968-d95a34dfe1df
        CPH.RunActionById("ec0c3cf3-c7f8-4989-9968-d95a34dfe1df");

        return true;
    }
}
