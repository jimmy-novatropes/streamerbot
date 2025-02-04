/*
This code retrieves and compares the counts of two queues, regular_queue_count and priority_queue_count,
from global variables. If either queue has fewer than two items, it logs a message and triggers an action with a specified ID.
*/
using System;
using System.Threading; // Import the threading library for sleep functionality
using System.Collections.Generic;


public class CPHInline
{
    public bool Execute(){
		var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
		int timerActive = CPH.GetGlobalVar<int>("timer_active");

		if ((priorityOrder.Count > 0 || commandOrder.Count > 0) && timerActive > 0)
		{
			CPH.SetGlobalVar("timer_active", 55);
			return true;
			}
        else if (priorityOrder.Count > 0 || commandOrder.Count > 0){
			// Retrieve the current values from the global variables
			CPH.SetGlobalVar("timer_active", 3);
			return true;
		}
		else{
		CPH.SetGlobalVar("timer_active", 0);
		return true;
		}
    }
}
