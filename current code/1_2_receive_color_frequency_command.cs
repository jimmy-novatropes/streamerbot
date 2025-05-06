using System;
using System.Collections.Generic;
using Newtonsoft.Json;

public class CPHInline
{
    public bool Execute()
    {
        Dictionary<string, string> colorLanguageMap;
        try
        {
            string json = System.IO.File.ReadAllText(@"A:\\Desktop\\Novatropes Stream\\color_language_mapping.json");
            colorLanguageMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(json);
        }
        catch (Exception ex)
        {
            CPH.LogError("Failed to load color_language_mapping.json: " + ex.Message);
            colorLanguageMap = new Dictionary<string, string>();
        }

        CPH.TryGetArg("message", out string chatMessage);
        CPH.TryGetArg("userName", out string userName);
        CPH.TryGetArg("eventSource", out string eventSource);
        CPH.TryGetArg("bits", out int bits);

        if (string.IsNullOrEmpty(chatMessage) || string.IsNullOrEmpty(userName))
        {
            CPH.LogWarn("Missing chatMessage or userName");
            return false;
        }

        if (TryParseModeAndColor(chatMessage, out int mode, out string color))
        {
            if (!ProcessModeAndColor(mode, color, userName, eventSource, colorLanguageMap))
                return false;

            string stringMode = mode.ToString();
            var commandOrder = CPH.GetGlobalVar<List<List<string>>>("order") ?? new List<List<string>>();
            var priorityOrder = CPH.GetGlobalVar<List<List<string>>>("priority_order") ?? new List<List<string>>();
            var targetOrder = bits > 0 ? priorityOrder : commandOrder;

            bool userFound = false;
            string normalizedColor = color.Trim().ToLower();
            string lang = colorLanguageMap.ContainsKey(normalizedColor) ? colorLanguageMap[normalizedColor] : "en";

            var addMsgs = new Dictionary<string, string>
            {
                { "en", "Adding @{0} to queue with mode {1}, color {2}." },
                { "es", "Agregando a @{0} a la cola con modo {1}, color {2}." },
                { "fr", "Ajout de @{0} à la file avec le mode {1}, couleur {2}." },
                { "pt", "Adicionando @{0} à fila com modo {1}, cor {2}." }
            };

            var updateMsgs = new Dictionary<string, string>
            {
                { "en", "Updating data for @{0} Mode:{1}, color:{2}." },
                { "es", "Actualizando datos para @{0} Modo:{1}, color:{2}." },
                { "fr", "Mise à jour des données pour @{0} Mode:{1}, couleur:{2}." },
                { "pt", "Atualizando dados para @{0} Modo:{1}, cor:{2}." }
            };

            for (int i = 0; i < targetOrder.Count; i++)
            {
                if (targetOrder[i][0] == userName)
                {
                    targetOrder[i][1] = color;
                    targetOrder[i][2] = stringMode;
                    if (bits > 0) targetOrder[i][4] = bits.ToString();

                    string msg = string.Format(updateMsgs[lang], userName, mode, color);
                    if (eventSource == "twitch") CPH.SendMessage(msg);
                    else if (eventSource == "youtube") CPH.SendYouTubeMessage(msg);

                    userFound = true;
                    break;
                }
            }

            if (!userFound)
            {
                if (bits > 0)
                    priorityOrder.Add(new List<string> { userName, color, stringMode, bits.ToString() });
                else
                    commandOrder.Add(new List<string> { userName, color, stringMode });

                string msg = string.Format(addMsgs[lang], userName, mode, color);
                if (eventSource == "twitch") CPH.SendMessage(bits > 0 ? "[Priority] " + msg : msg);
                else if (eventSource == "youtube") CPH.SendYouTubeMessage(bits > 0 ? "[Priority] " + msg : msg);
            }

            CPH.SetGlobalVar("priority_order", priorityOrder);
            CPH.SetGlobalVar("order", commandOrder);
            SetNextUserIfAvailable(priorityOrder, commandOrder);
            CPH.SetGlobalVar("priority_queue_count", priorityOrder.Count);
            CPH.SetGlobalVar("regular_queue_count", commandOrder.Count);
        }

        return true;
    }

    private bool ProcessModeAndColor(int mode, string color, string userName, string eventSource, Dictionary<string, string> colorLanguageMap)
    {
        string[] supportedColors = System.IO.File.ReadAllLines(@"A:\\Desktop\\Novatropes Stream\\accepted_colors.txt");
        int[] supportedModes = { 1, 2, 3, 4, 5, 6, -1, -2, -3, -4, -5, -6 };
        string normalizedColor = color.Trim().ToLower();
        string lang = colorLanguageMap.ContainsKey(normalizedColor) ? colorLanguageMap[normalizedColor] : "en";

        var errorMessages = new Dictionary<string, string>
        {
            { "color_unsupported_en", "Sorry @{0}, the color '{1}' is not supported." },
            { "color_unsupported_es", "Lo siento @{0}, el color '{1}' no está soportado." },
            { "color_unsupported_fr", "Désolé @{0}, la couleur '{1}' n'est pas prise en charge." },
            { "color_unsupported_pt", "Desculpe @{0}, a cor '{1}' não é suportada." },
            { "mode_unsupported_en", "Sorry @{0}, the mode '{1}' is not supported." },
            { "mode_unsupported_es", "Lo siento @{0}, el modo '{1}' no está soportado." },
            { "mode_unsupported_fr", "Désolé @{0}, le mode '{1}' n'est pas pris en charge." },
            { "mode_unsupported_pt", "Desculpe @{0}, o modo '{1}' não é suportado." }
        };

        if (!Array.Exists(supportedColors, c => c.Trim().ToLower() == normalizedColor))
        {
            string msg = string.Format(errorMessages[$"color_unsupported_{lang}"], userName, color);
            SendLocalizedMessage(msg, eventSource);
            return false;
        }

        if (!Array.Exists(supportedModes, m => m == mode))
        {
            string msg = string.Format(errorMessages[$"mode_unsupported_{lang}"], userName, mode);
            SendLocalizedMessage(msg, eventSource);
            return false;
        }

        return true;
    }

    private void SendLocalizedMessage(string msg, string source)
    {
        if (source == "twitch")
            CPH.SendMessage(msg);
        else if (source == "youtube")
            CPH.SendYouTubeMessage(msg);

        CPH.SetGlobalVar("error_message", msg);
        CPH.SetGlobalVar("error_type", "user commands");
        CPH.SetGlobalVar("error_source", source);
        CPH.RunActionById("759582b8-2849-48b5-b383-554497f1e454");
    }

    private bool TryParseModeAndColor(string message, out int mode, out string color)
    {
        mode = 0;
        color = string.Empty;
        string[] words = message.Replace(",", " ").Trim().Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries);
        if (words.Length == 2 || words.Length == 3)
        {
            int.TryParse(words[0], out mode);
            color = words[1];
            return true;
        }
        return false;
    }

    private void SetNextUserIfAvailable(List<List<string>> priorityOrder, List<List<string>> commandOrder)
    {
        string currentUser = CPH.GetGlobalVar<string>("current_user");
        if (!string.IsNullOrEmpty(currentUser))
        {
            List<List<string>> combinedQueue = new List<List<string>>();
            combinedQueue.AddRange(priorityOrder);
            combinedQueue.AddRange(commandOrder);

            if (combinedQueue.Count > 0)
            {
                var nextUser = combinedQueue[0];
                CPH.SetGlobalVar("next_user", nextUser[0]);
                CPH.SetGlobalVar("next_color", nextUser[1]);
                CPH.SetGlobalVar("next_mode", nextUser[2]);
            }
            else
            {
                CPH.SetGlobalVar("next_user", null);
                CPH.SetGlobalVar("next_color", null);
                CPH.SetGlobalVar("next_mode", null);
            }
        }
    }
}
