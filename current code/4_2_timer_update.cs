/*
This C# script is designed for use in **Streamer.bot** to manage a countdown
timer based on the status of two command queues: `priority_order` and `order`.
It first determines the appropriate duration for the timer based on whether a 
`priority_timer` is active. If both queues are empty, it cancels the timer by 
setting it to `0`. When the timer is activated, the script enters a loop that 
updates a global `time_left` variable every 5 seconds, formats the remaining 
time as `MM:SS`, and triggers specific actions to update UI elements or widgets.
*/
using System;
using System.Threading;
using System.Collections.Generic;

public class CPHInline
{
    // Action IDs for UI updates
    private const string COMMAND_TIMER_DISPLAY_ACTION = "3269fdd1-f0f0-4141-b273-b9b84c7170d6";
    private const string TEXT_WIDGETS_ACTION = "113c947b-8a9d-44e2-892d-4a7a639fafee";
    
    // Default values in case global variables are not set
    private const int DEFAULT_PRIORITY_TIME = 20;
    private const int DEFAULT_FREE_TIME = 50;
    private const int SLEEP_INTERVAL = 4900; // 4.9 seconds to account for action delay

    public bool Execute()
    {
        try
        {
            // Get timer configuration
            int priorityTimer = CPH.GetGlobalVar<int>("priority_timer");
            string regularQueueStr = CPH.GetGlobalVar<string>("regular_queue_count");
            string prioQueueStr = CPH.GetGlobalVar<string>("priority_queue_count");
            
            // Get timer durations from global variables as strings and convert to integers
            string priorityTimeStr = CPH.GetGlobalVar<string>("time_left_priority");
            string freeTimeStr = CPH.GetGlobalVar<string>("time_left_free");
            
            int timeLeft;
            if (priorityTimer == 1)
            {
                if (string.IsNullOrEmpty(priorityTimeStr) || !int.TryParse(priorityTimeStr, out timeLeft))
                {
                    CPH.LogError($"Invalid priority timer duration: {priorityTimeStr}. Using default value.");
                    CPH.SetGlobalVar("error_message",$"Invalid priority timer duration: {priorityTimeStr}. Using default value. - timer - streamerbot");
                    CPH.RunActionById("759582b8-2849-48b5-b383-554497f1e454");
                    timeLeft = DEFAULT_PRIORITY_TIME;
                }
            }
            else
            {
                if (string.IsNullOrEmpty(freeTimeStr) || !int.TryParse(freeTimeStr, out timeLeft))
                {
                    CPH.LogError($"Invalid free timer duration: {freeTimeStr}. Using default value.");
                    CPH.SetGlobalVar("error_message",$"Invalid free timer duration: {freeTimeStr}. Using default value. - timer - streamerbot");
                    CPH.RunActionById("759582b8-2849-48b5-b383-554497f1e454");
                    timeLeft = DEFAULT_FREE_TIME;
                }
            }

            // Get queue lists
            var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
            var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
            
            // Check if timer should be active
            int timerActive = CPH.GetGlobalVar<int>("timer_active");
            int timerCurrentlyRunning = CPH.GetGlobalVar<int>("timer_currently_running");

            if (timerActive <= 0)
            {
                CPH.LogDebug("Timer is not active. Exiting.");
                CPH.SetGlobalVar("error_message",$"Timer is not active. Exiting. - timer - streamerbot");
                CPH.RunActionById("759582b8-2849-48b5-b383-554497f1e454");
                return true;
            }

            CPH.LogDebug($"Starting timer with duration: {timeLeft} seconds");

            while (timeLeft > 0)
            {
                string formattedTime = FormatTime(timeLeft);
                
                // Update the global variable with the formatted time
                CPH.SetGlobalVar("time_left", formattedTime);
                
                // Update UI elements
                UpdateUI();
                
                // Wait for the interval
                Thread.Sleep(SLEEP_INTERVAL);
                
                // Reduce the timer
                timeLeft -= 5;
                
                CPH.LogDebug($"Time remaining: {formattedTime}");
            }

            // Timer finished
            CPH.SetGlobalVar("time_left", "00:00");
            CPH.SetGlobalVar("timer_ended", 1);
            UpdateUI();
            
            CPH.LogDebug("Timer completed successfully");
            return true;
        }
        catch (Exception ex)
        {
            CPH.LogError($"Error in timer update: {ex.Message}");
            CPH.SetGlobalVar("error_message",$"Error in timer update: {ex.Message} - timer - streamerbot");
            CPH.RunActionById("759582b8-2849-48b5-b383-554497f1e454");
            return false;
        }
    }

    private string FormatTime(int seconds)
    {
        if (seconds < 60)
        {
            return $"{seconds} seconds";
        }
        
        int minutes = seconds / 60;
        int remainingSeconds = seconds % 60;
        return $"{minutes:D2}:{remainingSeconds:D2} minutes";
    }

    private void UpdateUI()
    {
        CPH.RunActionById(COMMAND_TIMER_DISPLAY_ACTION);
        CPH.RunActionById(TEXT_WIDGETS_ACTION);
    }
}
