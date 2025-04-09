using System;

public class CPHInline
{
    public bool Execute()
    {
        // Retrieve the next user from the global variables
		var time_left = CPH.GetGlobalVar<string>("time_left");
		string next_in_line = $"\n Next View in {time_left}";
		// Store the message in a global variable
		CPH.SetGlobalVar("next_in_line", next_in_line);

        return true;
    }
}

