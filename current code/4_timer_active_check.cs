/*
This code retrieves and compares the counts of two queues, regular_queue_count and priority_queue_count,
from global variables. If either queue has fewer than two items, it logs a message and triggers an action with a specified ID.
*/
using System;

public class CPHInline
{
    public bool Execute()

    {

        // Retrieve the current values from the global variables
        int timerActive = CPH.GetGlobalVar<int>("timer_active");
        string regularQueueStr = CPH.GetGlobalVar<string>("regular_queue_count");
        string prioQueueStr = CPH.GetGlobalVar<string>("priority_queue_count");
        // CPH.SendMessage($"is the timer active? {timerActive}");

        // Convert the string values to integers for comparison
        int regularQueue = int.Parse(regularQueueStr);
        int prioQueue = int.Parse(prioQueueStr);

        // Check if either queue is less than 2
        if ((regularQueue > 0 || prioQueue > 0))
        {
			CPH.SetGlobalVar("timer_active", 4);
            // Perform your logic here when either variable is less than 2
            CPH.LogDebug("Either the regular queue or priority queue has less than 2.");

            // You can also trigger actions or further logic here 4 - Command Timer aed0fd9f-10b7-4f7f-83d3-eaa5775c4739
            CPH.RunActionById("aed0fd9f-10b7-4f7f-83d3-eaa5775c4739");
        }
        else{
        	CPH.SetGlobalVar("timer_active", 0);
        	}

        return true;
    }
}
