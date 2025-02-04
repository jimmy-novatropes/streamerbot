using System;

public class CPHInline
{
    public bool Execute()
    {
        // Retrieve the current user, rpm, and color from the global variables
        string currentUser = CPH.GetGlobalVar<string>("current_user");
        string currentRPM = CPH.GetGlobalVar<string>("current_rpm");
        string currentColor = CPH.GetGlobalVar<string>("current_color");
        string currentDirection = CPH.GetGlobalVar<string>("current_direction");

        // Build the message for the current user
        string nowShowingMessage = $"Now Showing: @{currentUser}\nPattern: {currentRPM}, {currentColor}, {currentDirection}\n";

        // Retrieve the next user from the global variables
        var nextUser = CPH.GetGlobalVar<string>("next_user");
        // Retrieve the next user from the global variables
        var nextColor = CPH.GetGlobalVar<string>("next_color");
        var nextRPM = CPH.GetGlobalVar<string>("next_rpm");
        var nextDirection = CPH.GetGlobalVar<string>("next_direction");

        // If next_user exists, include the "Next Up" section
        if (!string.IsNullOrEmpty(nextUser))
        {
        	var time_left = CPH.GetGlobalVar<string>("time_left");
        	nowShowingMessage += $"Next Up: @{nextUser}\nNext Pattern: {nextRPM}, {nextColor}, {nextDirection}\n";
            string next_in_line = $"\n Next View in {time_left} minutes";


            // Store the message in a global variable
			CPH.SetGlobalVar("next_in_line", next_in_line);
        }

        // Store the message in a global variable
        CPH.SetGlobalVar("gdi_text_message", nowShowingMessage);

        return true;
    }
}
