using System;
using System.Collections.Generic;

public class CPHInline
{
    private readonly List<string> PositionCommands = new List<string>
    {
        "position",       // English
        "posición",       // Spanish
        "posição",        // Portuguese
        "positionfr"      // Custom trigger for French
    };

    private const string PRIORITY_LIST_VAR = "priority_order";
    private const string COMMAND_LIST_VAR = "order";

    public bool Execute()
    {
        CPH.TryGetArg("message", out string chatMessage);
        CPH.TryGetArg("userName", out string userName);
        CPH.TryGetArg("eventSource", out string eventSource);

        if (IsPositionCommand(chatMessage, out string lang))
        {
            var priorityList = CPH.GetGlobalVar<List<List<string>>>(PRIORITY_LIST_VAR) ?? new List<List<string>>();
            var commandList = CPH.GetGlobalVar<List<List<string>>>(COMMAND_LIST_VAR) ?? new List<List<string>>();

            CheckUserPosition(userName, priorityList, commandList, eventSource, lang);
            return true;
        }

        return true;
    }

    private bool IsPositionCommand(string message, out string lang)
    {
        lang = "en";
        if (string.IsNullOrEmpty(message)) return false;

        string keyword = message.Split(' ')[0].ToLower();
        if (keyword == "posición") lang = "es";
        else if (keyword == "posição") lang = "pt";
        else if (keyword == "positionfr") lang = "fr";
        else if (keyword == "position") lang = "en";
        else return false;

        return true;
    }

    private void CheckUserPosition(string userName, List<List<string>> priorityList, List<List<string>> commandList, string eventSource, string lang)
    {
        var messages = new Dictionary<string, (string, string, string)>
        {
            { "en", ($"{{0}}, You are currently at position {{1}} out of {{2}} in the priority list.",
                     $"{{0}}, You are currently at position {{1}} out of {{2}} in the regular list.",
                     $"User {{0}} not found in priority or regular order lists.") },
            { "es", ($"{{0}}, estás en la posición {{1}} de {{2}} en la lista prioritaria.",
                     $"{{0}}, estás en la posición {{1}} de {{2}} en la lista regular.",
                     $"Usuario {{0}} no encontrado en ninguna lista.") },
            { "pt", ($"{{0}}, você está na posição {{1}} de {{2}} na lista prioritária.",
                     $"{{0}}, você está na posição {{1}} de {{2}} na lista normal.",
                     $"Usuário {{0}} não encontrado em nenhuma lista.") },
            { "fr", ($"{{0}}, vous êtes à la position {{1}} sur {{2}} dans la liste prioritaire.",
                     $"{{0}}, vous êtes à la position {{1}} sur {{2}} dans la liste normale.",
                     $"Utilisateur {{0}} introuvable dans les listes.") }
        };

        var (priorityMsg, regularMsg, notFoundMsg) = messages.ContainsKey(lang) ? messages[lang] : messages["en"];

        int position = FindUserInList(userName, priorityList);
        string msg;
        if (position >= 0)
        {
            msg = string.Format(priorityMsg, userName, position + 1, priorityList.Count);
        }
        else
        {
            position = FindUserInList(userName, commandList);
            msg = position >= 0
                ? string.Format(regularMsg, userName, position + 1, commandList.Count)
                : string.Format(notFoundMsg, userName);
        }

        if (eventSource.Equals("twitch", StringComparison.OrdinalIgnoreCase))
            CPH.SendMessage(msg);
        else if (eventSource.Equals("youtube", StringComparison.OrdinalIgnoreCase))
            CPH.SendYouTubeMessage(msg);
    }

    private int FindUserInList(string userName, List<List<string>> list)
    {
        for (int i = 0; i < list.Count; i++)
        {
            if (list[i][0] == userName)
                return i;
        }
        return -1;
    }
}
