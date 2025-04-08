/*
This C# script is designed for use in **Streamer.bot** to manage a countdown
timer based on the status of two command queues: `priority_order` and `order`.
It first determines the appropriate duration for the timer (`10`
or `20` seconds) depending on whether a `priority_timer` is active. I
f both queues are empty, it cancels the timer by setting it to `0`.
When the timer is activated, the script enters a loop that updates a global
`time_left` variable every 5 seconds, formats the remaining time as `MM:SS`,
and triggers specific actions to update UI elements or widgets. Once the
timer finishes, it resets `time_left` and can trigger a final update.
If no users are detected in the queues, the timer is not started, and a
log message is written for reference.
*/
using System;
using System.Threading; // Import the threading library for sleep functionality
using System.Collections.Generic;

public class CPHInline
{
    public bool Execute()
    {
		// CPH.SendMessage($"Updating data for queue");
		int priorityTimer = CPH.GetGlobalVar<int>("priority_timer");
		string regularQueueStr = CPH.GetGlobalVar<string>("regular_queue_count");
        string prioQueueStr = CPH.GetGlobalVar<string>("priority_queue_count");
		int timeLeft;
		if (priorityTimer == 1)
		{ timeLeft = 20; // 5:00 in seconds
		}
		else
		{ timeLeft = 50; // 5:00 in seconds
		}
        // Retrieve the existing lists for both 'priority_order' and 'order'
        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
        int timerActive = CPH.GetGlobalVar<int>("timer_active");
        int timerCurrentlyRunning = CPH.GetGlobalVar<int>("timer_currently_running");
        if (timerActive > 0)
        {
            while (timeLeft > 0)
            {
                string formattedTime;
                if (timeLeft < 60)
                {
                    // If less than a minute, display as seconds only (e.g., "45s")
                    formattedTime = $"{timeLeft} seconds";
                }
                else
                {
                    // Otherwise, display in MM:SS format (e.g., "01:30")
                    int minutes = timeLeft / 60;
                    int seconds = timeLeft % 60;
                    formattedTime = $"{minutes:D2}:{seconds:D2} minutes";
                }
                // Update the global variable with the formatted time
                CPH.SetGlobalVar("time_left", formattedTime);
                // Trigger actions to update visuals (e.g., overlays or chat updates)
                CPH.RunActionById("3269fdd1-f0f0-4141-b273-b9b84c7170d6"); // Update command timer display
                CPH.RunActionById("113c947b-8a9d-44e2-892d-4a7a639fafee"); // Update text widgets
                // Wait for 5 seconds (slightly less to offset action delay)
                Thread.Sleep(4900);
                // Reduce the timer by 5 seconds
                timeLeft -= 5;
            }

            // Once the timer reaches 0, you can trigger a final action
            CPH.SetGlobalVar("time_left", "00:00");
            CPH.SetGlobalVar("timer_ended", 1);
            // Run an action on every 5-second decrement 5 - Update the command timer display - 3269fdd1-f0f0-4141-b273-b9b84c7170d6
            CPH.RunActionById("3269fdd1-f0f0-4141-b273-b9b84c7170d6"); // Run Command 5
            //3 - Update Text Widgets                             113c947b-8a9d-44e2-892d-4a7a639fafee
			CPH.RunActionById("113c947b-8a9d-44e2-892d-4a7a639fafee");
            return true;
        }
        return true;

    }
}
