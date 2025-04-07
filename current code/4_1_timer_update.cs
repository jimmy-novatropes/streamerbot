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
		{ timeLeft = 10; // 5:00 in seconds

		}
		if (regularQueueStr == "0" && prioQueueStr == "0")
        {
            timeLeft = 0;
        }


        // Set the initial timer value in seconds (e.g., 5 minutes = 300 seconds)
        // Retrieve the existing lists for both 'priority_order' and 'order'
        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
        // Retrieve the current values from the global variables
        int timerActive = CPH.GetGlobalVar<int>("timer_active");
        CPH.SetGlobalVar("timer_active", 999);
        //CPH.SendMessage($"Updating data for queue {commandOrder.Count}, {priorityOrder.Count}, {timerActive}");
        if ((priorityOrder.Count > 0 || commandOrder.Count > 0) && timerActive > 0)
        {
            // Start the countdown timer
            CPH.SetGlobalVar("timer_active", 1);
            //CPH.SendMessage($"Updating data for queue {commandOrder.Count}, {priorityOrder.Count}, {timerActive}");

            while (timeLeft > 0)
            {
                // Convert timeLeft to minutes:seconds format
                int minutes = timeLeft / 60;
                int seconds = timeLeft % 60;

                // Format the time as "MM:SS"
                string formattedTime = $"{minutes:D2}:{seconds:D2}";

                // Update the global variable with the new time
                CPH.SetGlobalVar("time_left", formattedTime);

                // Run an action on every 5-second decrement 5 - Update the command timer display - 3269fdd1-f0f0-4141-b273-b9b84c7170d6
                CPH.RunActionById("3269fdd1-f0f0-4141-b273-b9b84c7170d6");
                //CPH.SendMessage($"Updating data for {timeLeft}");
                //3 - Update Text Widgets                             113c947b-8a9d-44e2-892d-4a7a639fafee
				CPH.RunActionById("113c947b-8a9d-44e2-892d-4a7a639fafee");

                // Wait for 5 seconds (5000 milliseconds)
                Thread.Sleep(4900);

                // Decrement the timer by 5 seconds
                timeLeft -= 5;
            }

            // Once the timer reaches 0, you can trigger a final action
            CPH.SetGlobalVar("time_left", "00:00");
            // Run an action on every 5-second decrement
            CPH.RunActionById("3269fdd1-f0f0-4141-b273-b9b84c7170d6"); // Run Command 5

            return true;
        }
        else if (priorityOrder.Count == 0 || commandOrder.Count == 0)
        {
        	CPH.SetGlobalVar("timer_active", 0);
        	return true;
        	}
        else
        {
            CPH.SetGlobalVar("timer_active", 0);
            CPH.LogInfo("No users in the queue to start the countdown timer.");
            return true;
        }
    }
}
