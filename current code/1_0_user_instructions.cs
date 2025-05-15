using System;
using System.Collections.Generic;
using Newtonsoft.Json;
using System.IO;

public class CPHInline
{
    public bool Execute()
    {
        CPH.TryGetArg("message", out string chatMessage);
        CPH.TryGetArg("userName", out string userName);
        CPH.TryGetArg("eventSource", out string eventSource);

        var instructionKeywords = new List<string>
        {
            "instructionsfr",
            "instrucciones",
            "instruções",
            "instructions"
        };

        if (string.IsNullOrEmpty(chatMessage)) return false;

        string command = chatMessage.Trim().Split(' ')[0].ToLower();
        if (instructionKeywords.Exists(k => k.Equals(command, StringComparison.OrdinalIgnoreCase)))
        {
            ShowLocalizedInstructions(userName, eventSource, command);
            return true;
        }

        return true;
    }

    private void ShowLocalizedInstructions(string userName, string eventSource, string command)
    {
        string lang = DetectLanguageFromCommand(command);

        Dictionary<string, string> colorMap;
        try
        {
            string colorJson = File.ReadAllText(@"A:\\Desktop\\Novatropes Stream\\color_language_mapping.json");
            colorMap = JsonConvert.DeserializeObject<Dictionary<string, string>>(colorJson);
        }
        catch (Exception ex)
        {
            CPH.LogError("Failed to load color JSON: " + ex.Message);
            colorMap = new Dictionary<string, string>();
        }

        List<string> langColors = new List<string>();
        foreach (var kvp in colorMap)
        {
            if (kvp.Value == lang)
            {
                langColors.Add(kvp.Key);
            }
        }

        string colorsExample = "a supported color";
        if (langColors.Count > 0)
        {
            List<string> quotedColors = new List<string>();
            foreach (string color in langColors)
            {
                quotedColors.Add("'" + color + "'");
            }
            colorsExample = string.Join(", ", quotedColors);
        }


        var instructions = new Dictionary<string, string>{
            { "en", "@{0}, to join the queue, type a number followed by a color. Supported colors: {1}. Supported commands: 'instructions', 'position'." },
            { "es", "@{0}, para unirte a la cola, escribe un número seguido de un color. Colores soportados: {1}. Comandos soportados: 'instrucciones', 'posición'." },
            { "fr", "@{0}, pour rejoindre la file, tapez un chiffre suivi d'une couleur. Couleurs prises en charge : {1}. Commandes prises en charge : 'instructionsfr', 'position'." },
            { "pt", "@{0}, para entrar na fila, digite um número seguido de uma cor. Cores suportadas: {1}. Comandos suportados: 'instruções', 'posição'." }
        };


        if (!instructions.ContainsKey(lang)) lang = "en";

        string msg = string.Format(instructions[lang], userName, colorsExample);

        if (eventSource.Equals("twitch", StringComparison.OrdinalIgnoreCase))
            CPH.SendMessage(msg);
        else if (eventSource.Equals("youtube", StringComparison.OrdinalIgnoreCase))
            CPH.SendYouTubeMessage(msg);
    }

    private string DetectLanguageFromCommand(string cmd)
    {
        if (cmd == "instrucciones") return "es";
        if (cmd == "instruções") return "pt";
        if (cmd == "instructionsfr") return "fr";
        if (cmd == "instructions") return "en";
        return "en";
    }
}
