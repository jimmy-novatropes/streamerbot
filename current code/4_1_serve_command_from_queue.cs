using System;
using System.Collections.Generic;
using Newtonsoft.Json; // Requires Newtonsoft.Json.dll

public class CPHInline
{
    public bool Execute()
    {
        // Load color language map from JSON file
        Dictionary<string, string> colorLanguageMap;
        try
        {
            string json = System.IO.File.ReadAllText(@"A:\Desktop\Novatropes Stream\color_language_mapping.json");
            colorLanguageMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(json);
        }
        catch (Exception ex)
        {
            CPH.LogError("Failed to load color_language_mapping.json: " + ex.Message);
            colorLanguageMap = new Dictionary<string, string>();
        }

        var serveMsgs = new Dictionary<string, string>
        {
            { "en", "Now serving ~ mode {0} with color {1} for user {2}." },
            { "es", "Atendiendo ahora ~ modo {0} con color {1} para el usuario {2}." },
            { "fr", "Service en cours ~ mode {0} avec couleur {1} pour l'utilisateur {2}." },
            { "pt", "Atendendo agora ~ modo {0} com cor {1} para o usuário {2}." }
        };

        var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
        var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();

        if (priorityOrder.Count > 0)
        {
            var firstCommand = priorityOrder[0];
            CPH.LogInfo("Priority command: " + string.Join(", ", firstCommand));

            string colorNorm = firstCommand[1].Trim().ToLower();
            string lang = colorLanguageMap.ContainsKey(colorNorm) ? colorLanguageMap[colorNorm] : "en";
            string msg = string.Format(serveMsgs[lang], firstCommand[2], firstCommand[1], firstCommand[0]);

            CPH.SendMessage("[Priority] " + msg);
            CPH.SendYouTubeMessage("[Priority] " + msg);

            CPH.SetGlobalVar("current_user", firstCommand[0]);
            CPH.SetGlobalVar("current_color", firstCommand[1]);
            CPH.SetGlobalVar("current_mode", firstCommand[2]);
            CPH.SetGlobalVar("bits_donated", firstCommand[3]);
            CPH.SetGlobalVar("priority_timer", 1);

            CPH.RunActionById("3dd43bd4-961c-4ed1-96c0-06420b2eb00d");
            CPH.SetGlobalVar("timer_currently_running", 1);
            CPH.RunActionById("113c947b-8a9d-44e2-892d-4a7a639fafee");

            if (priorityOrder.Count > 1)
            {
                var nextCommand = priorityOrder[1];
                CPH.SetGlobalVar("next_user", nextCommand[0]);
                CPH.SetGlobalVar("next_color", nextCommand[1]);
                CPH.SetGlobalVar("next_mode", nextCommand[2]);
                CPH.SetGlobalVar("priority_timer", 1);
            }
            else if (commandOrder.Count > 0)
            {
                var nextCommand = commandOrder[0];
                CPH.SetGlobalVar("next_user", nextCommand[0]);
                CPH.SetGlobalVar("next_color", nextCommand[1]);
                CPH.SetGlobalVar("next_mode", nextCommand[2]);
            }
            else
            {
                CPH.SetGlobalVar("next_user", null);
                CPH.SetGlobalVar("next_color", null);
                CPH.SetGlobalVar("next_mode", null);
            }

            priorityOrder.RemoveAt(0);
            CPH.SetGlobalVar("priority_order", priorityOrder);
        }
        else if (commandOrder.Count > 0)
        {
            var firstCommand = commandOrder[0];
            CPH.LogInfo("Regular command: " + string.Join(", ", firstCommand));

            string colorNorm = firstCommand[1].Trim().ToLower();
            string lang = colorLanguageMap.ContainsKey(colorNorm) ? colorLanguageMap[colorNorm] : "en";
            string msg = string.Format(serveMsgs[lang], firstCommand[2], firstCommand[1], firstCommand[0]);

            CPH.SendMessage(msg);
            CPH.SendYouTubeMessage(msg);

            CPH.SetGlobalVar("current_user", firstCommand[0]);
            CPH.SetGlobalVar("current_color", firstCommand[1]);
            CPH.SetGlobalVar("current_mode", firstCommand[2]);
            CPH.SetGlobalVar("priority_timer", 0);

            CPH.RunActionById("3dd43bd4-961c-4ed1-96c0-06420b2eb00d");

            if (commandOrder.Count > 1)
            {
                var nextCommand = commandOrder[1];
                CPH.SetGlobalVar("next_user", nextCommand[0]);
                CPH.SetGlobalVar("next_color", nextCommand[1]);
                CPH.SetGlobalVar("next_mode", nextCommand[2]);
                CPH.SetGlobalVar("priority_timer", 0);
            }
            else
            {
                CPH.SetGlobalVar("next_user", null);
                CPH.SetGlobalVar("next_color", null);
                CPH.SetGlobalVar("next_mode", null);
                CPH.SetGlobalVar("priority_timer", 0);
            }

            commandOrder.RemoveAt(0);
            CPH.SetGlobalVar("order", commandOrder);
        }
        else
        {
            CPH.LogInfo("Both priority order and regular command order lists are empty.");
            CPH.SetGlobalVar("next_user", null);
            CPH.SetGlobalVar("next_color", null);
            CPH.SetGlobalVar("next_mode", null);
            CPH.SetGlobalVar("priority_timer", 0);
        }

        CPH.SetGlobalVar("priority_queue_count", priorityOrder.Count);
        CPH.SetGlobalVar("regular_queue_count", commandOrder.Count);

        return true;
    }
}
